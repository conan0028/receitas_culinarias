from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import possui_schema

def create_possui(possui_data: possui_schema.PossuiCreate, db: Session):
    novo_possui = models.Possui(**possui_data.model_dump())

    try:
        db.add(novo_possui)
        db.commit()
        db.refresh(novo_possui)
        return {"message": "Relação criada com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta relação já existe."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar relação."
        )

def delete_possui(cod_rec_pos: int, cpf_edit_pos: str, db: Session):
    possui = db.query(models.Possui).filter(
        models.Possui.cod_rec_pos == cod_rec_pos,
        models.Possui.cpf_edit_pos == cpf_edit_pos
    ).first()

    if not possui:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relação não encontrada."
        )

    try:
        db.delete(possui)
        db.commit()
        return {"message": "Relação removida com sucesso."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover relação: {str(e)}"
        )
