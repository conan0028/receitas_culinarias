from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import ingredientes_receita_schema

def get_all_ingredientes_receita(db: Session):
    return db.query(models.IngredienteReceita).all()

def get_ingrediente_receita(cod_rec_ingrec: int, cod_ing_ingrec: int, db: Session):
    ingrediente_receita = db.query(models.IngredienteReceita).filter(
        models.IngredienteReceita.cod_rec_ingrec == cod_rec_ingrec,
        models.IngredienteReceita.cod_ing_ingrec == cod_ing_ingrec
    ).first()
    if not ingrediente_receita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de ingrediente em receita não encontrado."
        )
    return ingrediente_receita

def create_ingrediente_receita(ingrediente_receita_data: ingredientes_receita_schema.IngredienteReceitaCreate, db: Session):
    novo_ingrediente_receita = models.IngredienteReceita(**ingrediente_receita_data.model_dump())

    try:
        db.add(novo_ingrediente_receita)
        db.commit()
        db.refresh(novo_ingrediente_receita)
        return {"message": "Ingrediente associado à receita com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referência inválida: receita ou ingrediente não existem."
            )
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este ingrediente já está associado a esta receita."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao associar ingrediente à receita."
        )

def update_ingrediente_receita(
        cod_rec_ingrec: int,
        cod_ing_ingrec: int,
        ingrediente_receita_atualizado: ingredientes_receita_schema.IngredienteReceitaBase,
        db: Session
):
    ingrediente_receita = get_ingrediente_receita(cod_rec_ingrec, cod_ing_ingrec, db)

    ingrediente_receita.quant_ingrec = ingrediente_receita_atualizado.quant_ingrec
    ingrediente_receita.med_ingrec = ingrediente_receita_atualizado.med_ingrec

    try:
        db.commit()
        return {"message": "Associação de ingrediente à receita atualizada com sucesso."}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar associação de ingrediente à receita."
        )

def delete_ingrediente_receita(cod_rec_ingrec: int, cod_ing_ingrec: int, db: Session):
    ingrediente_receita = get_ingrediente_receita(cod_rec_ingrec, cod_ing_ingrec, db)

    try:
        db.delete(ingrediente_receita)
        db.commit()
        return {"message": "Associação de ingrediente à receita excluída com sucesso."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado: {str(e)}"
        )
