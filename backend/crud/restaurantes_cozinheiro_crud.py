from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import restaurantes_cozinheiro_schema

def get_all_restaurantes_cozinheiro(db: Session):
    return db.query(models.RestauranteCozinheiro).all()

def get_restaurante_cozinheiro(cod_coz_restcoz: str, nome_rest_restcoz: str, db: Session):
    restaurante_cozinheiro = db.query(models.RestauranteCozinheiro).filter(
        models.RestauranteCozinheiro.cod_coz_restcoz == cod_coz_restcoz,
        models.RestauranteCozinheiro.nome_rest_restcoz == nome_rest_restcoz
    ).first()
    if not restaurante_cozinheiro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de cozinheiro em restaurante não encontrado."
        )
    return restaurante_cozinheiro

def create_restaurante_cozinheiro(restaurante_cozinheiro_data: restaurantes_cozinheiro_schema.RestauranteCozinheiroCreate, db: Session):
    novo_restaurante_cozinheiro = models.RestauranteCozinheiro(**restaurante_cozinheiro_data.model_dump())

    try:
        db.add(novo_restaurante_cozinheiro)
        db.commit()
        db.refresh(novo_restaurante_cozinheiro)
        return {"message": "Cozinheiro associado ao restaurante com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referência inválida: cozinheiro ou restaurante não existem."
            )
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este cozinheiro já está associado a este restaurante."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao associar cozinheiro ao restaurante."
        )

def update_restaurante_cozinheiro(
        cod_coz_restcoz: str,
        nome_rest_restcoz: str,
        restaurante_cozinheiro_atualizado: restaurantes_cozinheiro_schema.RestauranteCozinheiroBase,
        db: Session
):
    restaurante_cozinheiro = get_restaurante_cozinheiro(cod_coz_restcoz, nome_rest_restcoz, db)

    restaurante_cozinheiro.dt_contratacao = restaurante_cozinheiro_atualizado.dt_contratacao

    try:
        db.commit()
        return {"message": "Associação de cozinheiro ao restaurante atualizada com sucesso."}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar associação de cozinheiro ao restaurante."
        )

def delete_restaurante_cozinheiro(cod_coz_restcoz: str, nome_rest_restcoz: str, db: Session):
    restaurante_cozinheiro = get_restaurante_cozinheiro(cod_coz_restcoz, nome_rest_restcoz, db)

    try:
        db.delete(restaurante_cozinheiro)
        db.commit()
        return {"message": "Associação de cozinheiro ao restaurante excluída com sucesso."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado: {str(e)}"
        )
