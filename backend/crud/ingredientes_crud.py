from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import ingredientes_schema

def get_ingrediente(db: Session, cod_ingred: int):
    return db.query(models.Ingrediente).filter(models.Ingrediente.cod_ingred == cod_ingred).first()

def get_ingrediente_by_nome(db: Session, nome_ingred: str):
    return db.query(models.Ingrediente).filter(models.Ingrediente.nome_ingred == nome_ingred).first()

def get_ingredientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ingrediente).offset(skip).limit(limit).all()

def create_ingrediente(db: Session, ingrediente: ingredientes_schema.IngredienteCreate):
    db_ingrediente = models.Ingrediente(**ingrediente.model_dump())

    try:
        db.add(db_ingrediente)
        db.commit()
        db.refresh(db_ingrediente)
        return db_ingrediente
    except IntegrityError as e:
        db.rollback()
        if "unique constraint" in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ingrediente com este nome já existe"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar ingrediente"
        )

def update_ingrediente(db: Session, cod_ingred: int, ingrediente: ingredientes_schema.IngredienteUpdate):
    db_ingrediente = get_ingrediente(db, cod_ingred)
    if not db_ingrediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não encontrado"
        )

    update_data = ingrediente.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_ingrediente, key, value)

    try:
        db.commit()
        db.refresh(db_ingrediente)
        return db_ingrediente
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ingrediente com este nome já existe"
        )

def delete_ingrediente(db: Session, cod_ingred: int):
    db_ingrediente = get_ingrediente(db, cod_ingred)
    if not db_ingrediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não encontrado"
        )

    # Verificação corrigida para usar o nome do relacionamento atualizado
    if db_ingrediente.receitas:
        # Opção 1: Impede a exclusão se houver receitas associadas
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível excluir ingrediente vinculado a receitas"
        )

        # Opção 2: Ou exclui em cascata (se cascade estiver configurado)
        # db.delete(db_ingrediente)

    try:
        db.delete(db_ingrediente)
        db.commit()
        return {"message": "Ingrediente removido com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover ingrediente: {str(e)}"
        )
