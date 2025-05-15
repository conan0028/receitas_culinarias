from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import receitas_schema

def get_all_receitas(db: Session):
    return db.query(models.Receita).all()

def get_receita_by_cod(cod_rec: int, db: Session):
    receita = db.query(models.Receita).filter(models.Receita.cod_rec == cod_rec).first()
    if not receita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receita não encontrada."
        )
    return receita

def create_receita(receita_data: receitas_schema.ReceitaCreate, db: Session):
    nova_receita = models.Receita(**receita_data.model_dump())

    try:
        db.add(nova_receita)
        db.commit()
        db.refresh(nova_receita)
        return {"message": "Receita criada com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referência inválida: categoria, cozinheiro ou livro não existem."
            )
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Receita com este código já está cadastrada."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar receita."
        )

def update_receita(cod_rec: int, receita_atualizada: receitas_schema.ReceitaBase, db: Session):
    receita = get_receita_by_cod(cod_rec, db)

    receita.nome_rec = receita_atualizada.nome_rec
    receita.dt_criacao_rec = receita_atualizada.dt_criacao_rec
    receita.cod_categoria_rec = receita_atualizada.cod_categoria_rec
    receita.cpf_coz = receita_atualizada.cpf_coz
    receita.isbn_rec = receita_atualizada.isbn_rec

    try:
        db.commit()
        return {"message": "Receita alterada com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referência inválida: categoria, cozinheiro ou livro não existem."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao alterar receita."
        )

def delete_receita(cod_rec: int, db: Session):
    # Verifica todas as dependências primeiro
    dependencias = {
        "Ingredientes": db.query(models.IngredienteReceita)
        .filter_by(cod_rec_ingrec=cod_rec).count(),
        "Degustações": db.query(models.Testa)
        .filter_by(cod_rec_test=cod_rec).count(),
        "Editores": db.query(models.Possui)
        .filter_by(cod_rec_pos=cod_rec).count(),
        "Livros": db.query(models.Inclui)
        .filter_by(cod_rec_inc=cod_rec).count()
    }

    if any(dependencias.values()):
        # Monta uma mensagem estruturada para o frontend
        mensagem = {
            "mensagem": "Não é possível excluir esta receita pois ela está vinculada a outras entidades.",
            "vinculos": {k: v for k, v in dependencias.items() if v > 0},
            "endpoints_para_remocao": []
        }

        if dependencias["Ingredientes"] > 0:
            mensagem["endpoints_para_remocao"].append("/ingredientes-receita/{cod_rec}")
        if dependencias["Degustações"] > 0:
            mensagem["endpoints_para_remocao"].append("/testa/receita/{cod_rec}")
        if dependencias["Editores"] > 0:
            mensagem["endpoints_para_remocao"].append("/possui/receita/{cod_rec}")
        if dependencias["Livros"] > 0:
            mensagem["endpoints_para_remocao"].append("/inclui/receita/{cod_rec}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )

    # Se não houver dependências, tenta localizar e apagar
    receita = db.query(models.Receita).filter_by(cod_rec=cod_rec).first()
    if not receita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receita não encontrada"
        )

    db.delete(receita)
    db.commit()

    return {"message": "Receita excluída com sucesso"}
