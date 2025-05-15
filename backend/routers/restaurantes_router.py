# ~/PycharmProjects/receitas_culinarias/routers/restaurantes_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import restaurantes_schema
from backend.crud import restaurantes_crud

router = APIRouter(prefix="/restaurantes", tags=["Restaurantes"])


@router.post("/", status_code=201)
def create(restaurante: restaurantes_schema.RestauranteCreate, db: Session = Depends(get_db)):
    return restaurantes_crud.create_restaurante(restaurante, db)


@router.get("/", response_model=list[restaurantes_schema.Restaurante])
def read_all(db: Session = Depends(get_db)):
    return restaurantes_crud.get_all_restaurantes(db)


@router.get("/{nome_rest}", response_model=restaurantes_schema.Restaurante)
def read_one(nome_rest: str, db: Session = Depends(get_db)):
    return restaurantes_crud.get_restaurante_by_nome(nome_rest, db)


@router.put("/{nome_rest}")
def update(nome_rest: str, restaurante: restaurantes_schema.RestauranteBase, db: Session = Depends(get_db)):
    return restaurantes_crud.update_restaurante(nome_rest, restaurante, db)


@router.delete("/{nome_rest}", status_code=200)
def delete(nome_rest: str, db: Session = Depends(get_db)):
    return restaurantes_crud.delete_restaurante(nome_rest, db)
