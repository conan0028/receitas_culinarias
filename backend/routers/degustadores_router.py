from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from backend.database import get_db
from backend.schemas import degustadores_schema
from backend.crud import degustadores_crud

router = APIRouter(prefix="/degustadores", tags=["Degustadores"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(degustador: degustadores_schema.DegustadorCreate, db: Session = Depends(get_db)):
    return degustadores_crud.create_degustador(degustador, db)

@router.get("/", response_model=list[degustadores_schema.Degustador])
def read_all(db: Session = Depends(get_db)):
    return degustadores_crud.get_all_degustadores(db)

@router.get("/{cpf_deg}", response_model=degustadores_schema.Degustador)
def read_one(cpf_deg: str, db: Session = Depends(get_db)):
    return degustadores_crud.get_degustador_by_cpf(cpf_deg, db)

@router.put("/{cpf_deg}")
def update(cpf_deg: str, degustador: degustadores_schema.DegustadorBase, db: Session = Depends(get_db)):
    return degustadores_crud.update_degustador(cpf_deg, degustador, db)

@router.delete("/{cpf_deg}", status_code=status.HTTP_200_OK)
def delete(cpf_deg: str, db: Session = Depends(get_db)):
    return degustadores_crud.delete_degustador(cpf_deg, db)
