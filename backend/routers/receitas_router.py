import status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from backend.crud.receitas_crud import delete_receita
from backend.database import get_db
from backend.schemas import receitas_schema
from backend.crud import receitas_crud

router = APIRouter(prefix="/receitas", tags=["Receitas"])

@router.post("/", status_code=201)
def create(receita: receitas_schema.ReceitaCreate, db: Session = Depends(get_db)):
    return receitas_crud.create_receita(receita, db)

@router.get("/", response_model=list[receitas_schema.Receita])
def read_all(db: Session = Depends(get_db)):
    return receitas_crud.get_all_receitas(db)

@router.get("/{cod_rec}", response_model=receitas_schema.Receita)
def read_one(cod_rec: int, db: Session = Depends(get_db)):
    return receitas_crud.get_receita_by_cod(cod_rec, db)

@router.put("/{cod_rec}")
def update(cod_rec: int, receita: receitas_schema.ReceitaBase, db: Session = Depends(get_db)):
    return receitas_crud.update_receita(cod_rec, receita, db)

# @router.delete("/{cod_rec}", status_code=200)
# def delete(cod_rec: int, db: Session = Depends(get_db)):
#     return receitas_crud.delete_receita(cod_rec, db)
@router.delete("/{cod_rec}", status_code=status.HTTP_200_OK)
def excluir_receita(cod_rec: int, db: Session = Depends(get_db)):
    return delete_receita(cod_rec, db)
