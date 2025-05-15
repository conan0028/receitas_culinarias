from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import editores_schema

def get_all_editores(db: Session):
    return db.query(models.Editor).all()

def get_editor_by_cpf(cpf_edit: str, db: Session):
    editor = db.query(models.Editor).filter(models.Editor.cpf_edit == cpf_edit).first()
    if not editor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Editor não encontrado."
        )
    return editor

def create_editor(editor_data: editores_schema.EditorCreate, db: Session):
    novo_editor = models.Editor(**editor_data.model_dump())

    try:
        db.add(novo_editor)
        db.commit()
        db.refresh(novo_editor)
        return {"message": "Editor criado com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Editor com este CPF já está cadastrado."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar editor."
        )

def update_editor(cpf_edit: str, editor_atualizado: editores_schema.EditorBase, db: Session):
    editor = get_editor_by_cpf(cpf_edit, db)

    editor.nome_edit = editor_atualizado.nome_edit
    editor.dt_contrato_edit = editor_atualizado.dt_contrato_edit
    editor.salario_edit = editor_atualizado.salario_edit

    try:
        db.commit()
        return {"message": "Editor alterado com sucesso."}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao alterar editor."
        )

def delete_editor(cpf_edit: str, db: Session):
    editor = get_editor_by_cpf(cpf_edit, db)

    try:
        # Verifica dependências antes de tentar apagar
        receitas = db.query(models.Possui).filter(models.Possui.cpf_edit_pos == cpf_edit).all()

        if receitas:
            mensagem = "Não é possível excluir este editor pois está vinculado a:\n"
            mensagem += f"- Receitas ({len(receitas)} registros):\n"
            for possui in receitas:
                receita = db.query(models.Receita).filter(models.Receita.cod_rec == possui.cod_rec_pos).first()
                mensagem += f"  * Receita {receita.nome_rec if receita else 'Desconhecida'}\n"

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=mensagem
            )

        db.delete(editor)
        db.commit()
        return {"message": "Editor excluído com sucesso."}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado: {str(e)}"
        )
