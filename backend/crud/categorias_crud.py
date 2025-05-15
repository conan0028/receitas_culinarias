from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import categorias_schema


def get_all_categorias(db: Session):
    return db.query(models.Categoria).all()


def get_categoria_by_cod(cod_categoria: int, db: Session):
    categoria = db.query(models.Categoria).filter(models.Categoria.cod_categoria == cod_categoria).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada."
        )
    return categoria


def create_categoria(categoria_data: categorias_schema.CategoriaCreate, db: Session):
    nova_categoria = models.Categoria(**categoria_data.model_dump())

    try:
        db.add(nova_categoria)
        db.commit()
        return {"message": "Categoria cadastrada com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Categoria com este código já está cadastrada."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao cadastrar categoria."
        )


def update_categoria(cod_categoria: int, categoria_atualizada: categorias_schema.CategoriaBase, db: Session):
    categoria = get_categoria_by_cod(cod_categoria, db)

    categoria.desc_categoria = categoria_atualizada.desc_categoria

    try:
        db.commit()
        return {"message": "Categoria atualizada com sucesso."}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar categoria."
        )


def delete_categoria(cod_categoria: int, db: Session):
    categoria = get_categoria_by_cod(cod_categoria, db)

    try:
        db.delete(categoria)
        db.commit()
        return {"message": "Categoria removida com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "violates foreign key constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível remover esta categoria: ela está vinculada a receitas."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao remover categoria."
        )
