from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import testa_schema

def get_all_testas(db: Session):
    return db.query(models.Testa).all()

def get_testa(cod_rec_test: int, cpf_deg_test: str, db: Session):
    testa = db.query(models.Testa).filter(
        models.Testa.cod_rec_test == cod_rec_test,
        models.Testa.cpf_deg_test == cpf_deg_test
    ).first()
    if not testa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de degustação não encontrado."
        )
    return testa

def create_testa(testa_data: testa_schema.TestaCreate, db: Session):
    if not (0 <= testa_data.nota_test <= 10):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A nota deve estar entre 0 e 10."
        )

    nova_testa = models.Testa(**testa_data.model_dump())

    try:
        db.add(nova_testa)
        db.commit()
        db.refresh(nova_testa)
        return {"message": "Degustação registrada com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referência inválida: receita ou degustador não existem."
            )
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta degustação já está registrada."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao registrar degustação."
        )

def update_testa(
        cod_rec_test: int,
        cpf_deg_test: str,
        testa_atualizado: testa_schema.TestaBase,
        db: Session
):
    testa = get_testa(cod_rec_test, cpf_deg_test, db)

    if not (0 <= testa_atualizado.nota_test <= 10):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A nota deve estar entre 0 e 10."
        )

    testa.dt_test = testa_atualizado.dt_test
    testa.nota_test = testa_atualizado.nota_test

    try:
        db.commit()
        return {"message": "Degustação atualizada com sucesso."}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar degustação."
        )

def delete_testa(cod_rec_test: int, cpf_deg_test: str, db: Session):
    testa = get_testa(cod_rec_test, cpf_deg_test, db)

    try:
        db.delete(testa)
        db.commit()
        return {"message": "Degustação excluída com sucesso."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado: {str(e)}"
        )
