from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import ingredientes_schema
from backend.crud import ingredientes_crud

router = APIRouter(
    prefix="/ingredientes",
    tags=["ingredientes"]
)

@router.post("/", response_model=ingredientes_schema.Ingrediente, status_code=status.HTTP_201_CREATED)
def criar_ingrediente(
        ingrediente: ingredientes_schema.IngredienteCreate,
        db: Session = Depends(get_db)
):
    return ingredientes_crud.create_ingrediente(db, ingrediente)

@router.get("/", response_model=list[ingredientes_schema.Ingrediente])
def listar_ingredientes(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=200),
        db: Session = Depends(get_db)
):
    return ingredientes_crud.get_ingredientes(db, skip=skip, limit=limit)

@router.get("/{cod_ingred}", response_model=ingredientes_schema.Ingrediente)
def obter_ingrediente(cod_ingred: int, db: Session = Depends(get_db)):
    db_ingrediente = ingredientes_crud.get_ingrediente(db, cod_ingred)
    if not db_ingrediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não encontrado"
        )
    return db_ingrediente

@router.put("/{cod_ingred}", response_model=ingredientes_schema.Ingrediente)
def atualizar_ingrediente(
        cod_ingred: int,
        ingrediente: ingredientes_schema.IngredienteUpdate,
        db: Session = Depends(get_db)
):
    return ingredientes_crud.update_ingrediente(db, cod_ingred, ingrediente)

@router.delete("/{cod_ingred}", status_code=status.HTTP_200_OK)
def remover_ingrediente(cod_ingred: int, db: Session = Depends(get_db)):
    return ingredientes_crud.delete_ingrediente(db, cod_ingred)
