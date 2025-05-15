from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import restaurantes_schema


def get_all_restaurantes(db: Session):
    return db.query(models.Restaurante).all()


def get_restaurante_by_nome(nome_rest: str, db: Session):
    restaurante = db.query(models.Restaurante).filter(models.Restaurante.nome_rest == nome_rest).first()
    if not restaurante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurante não encontrado."
        )
    return restaurante


def create_restaurante(restaurante_data: restaurantes_schema.RestauranteCreate, db: Session):
    novo_restaurante = models.Restaurante(**restaurante_data.model_dump())

    try:
        db.add(novo_restaurante)
        db.commit()
        return {"message": "Restaurante cadastrado com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurante com este nome já está cadastrado."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao cadastrar restaurante."
        )


def update_restaurante(nome_rest: str, restaurante_atualizado: restaurantes_schema.RestauranteBase, db: Session):
    restaurante = get_restaurante_by_nome(nome_rest, db)

    restaurante.endereco = restaurante_atualizado.endereco

    try:
        db.commit()
        return {"message": "Restaurante atualizado com sucesso."}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar restaurante."
        )


def delete_restaurante(nome_rest: str, db: Session):
    restaurante = get_restaurante_by_nome(nome_rest, db)

    try:
        db.delete(restaurante)
        db.commit()
        return {"message": "Restaurante removido com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "violates foreign key constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível remover este restaurante: ele está vinculado a outras tabelas."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao remover restaurante."
        )
