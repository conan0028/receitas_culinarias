from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import degustadores_schema

def get_all_degustadores(db: Session):
    return db.query(models.Degustador).all()

def get_degustador_by_cpf(cpf_deg: str, db: Session):
    degustador = db.query(models.Degustador).filter(models.Degustador.cpf_deg == cpf_deg).first()
    if not degustador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Degustador não encontrado."
        )
    return degustador

def create_degustador(degustador_data: degustadores_schema.DegustadorCreate, db: Session):
    novo_degustador = models.Degustador(**degustador_data.model_dump())

    try:
        db.add(novo_degustador)
        db.commit()
        db.refresh(novo_degustador)
        return {"message": "Degustador criado com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Degustador com este CPF já está cadastrado."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar degustador."
        )

def update_degustador(cpf_deg: str, degustador_atualizado: degustadores_schema.DegustadorBase, db: Session):
    degustador = get_degustador_by_cpf(cpf_deg, db)

    degustador.nome_deg = degustador_atualizado.nome_deg
    degustador.dt_contrato_deg = degustador_atualizado.dt_contrato_deg
    degustador.salario_deg = degustador_atualizado.salario_deg

    try:
        db.commit()
        return {"message": "Degustador alterado com sucesso."}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao alterar degustador."
        )

def delete_degustador(cpf_deg: str, db: Session):
    degustador = get_degustador_by_cpf(cpf_deg, db)

    try:
        # Verifica dependências antes de tentar apagar
        testes = db.query(models.Testa).filter(models.Testa.cpf_deg_test == cpf_deg).all()

        if testes:
            mensagem = "Não é possível excluir este degustador pois está vinculado a:\n"
            mensagem += f"- Testes de receitas ({len(testes)} registros):\n"
            for teste in testes:
                receita = db.query(models.Receita).filter(models.Receita.cod_rec == teste.cod_rec_test).first()
                mensagem += f"  * Receita {receita.nome_rec if receita else 'Desconhecida'} (Data: {teste.dt_test})\n"

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=mensagem
            )

        db.delete(degustador)
        db.commit()
        return {"message": "Degustador excluído com sucesso."}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado: {str(e)}"
        )
