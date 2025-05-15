from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from backend.crud import ingredientes_receita_crud
from backend.database import get_db
from backend.schemas import ingredientes_receita_schema

router = APIRouter(prefix="/ingredientes_receita", tags=["Ingredientes_Receita"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(ingrediente_receita: ingredientes_receita_schema.IngredienteReceitaCreate, db: Session = Depends(get_db)):
    return ingredientes_receita_crud.create_ingrediente_receita(ingrediente_receita, db)

@router.get("/", response_model=list[ingredientes_receita_schema.IngredienteReceita])
def read_all(db: Session = Depends(get_db)):
    return ingredientes_receita_crud.get_all_ingredientes_receita(db)

@router.get("/{cod_rec_ingrec}/{cod_ing_ingrec}", response_model=ingredientes_receita_schema.IngredienteReceita)
def read_one(cod_rec_ingrec: int, cod_ing_ingrec: int, db: Session = Depends(get_db)):
    return ingredientes_receita_crud.get_ingrediente_receita(cod_rec_ingrec, cod_ing_ingrec, db)

@router.put("/{cod_rec_ingrec}/{cod_ing_ingrec}")
def update(
        cod_rec_ingrec: int,
        cod_ing_ingrec: int,
        ingrediente_receita: ingredientes_receita_schema.IngredienteReceitaBase,
        db: Session = Depends(get_db)
):
    return ingredientes_receita_crud.update_ingrediente_receita(cod_rec_ingrec, cod_ing_ingrec, ingrediente_receita, db)

@router.delete("/{cod_rec_ingrec}/{cod_ing_ingrec}", status_code=status.HTTP_200_OK)
def delete(cod_rec_ingrec: int, cod_ing_ingrec: int, db: Session = Depends(get_db)):
    return ingredientes_receita_crud.delete_ingrediente_receita(cod_rec_ingrec, cod_ing_ingrec, db)
