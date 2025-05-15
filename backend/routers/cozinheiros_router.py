from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from backend.database import get_db
from backend.schemas import cozinheiros_schema
from backend.crud import cozinheiros_crud

router = APIRouter(prefix="/cozinheiros", tags=["Cozinheiros"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(cozinheiro: cozinheiros_schema.CozinheiroCreate, db: Session = Depends(get_db)):
    return cozinheiros_crud.create_cozinheiro(cozinheiro, db)

@router.get("/", response_model=list[cozinheiros_schema.Cozinheiro])
def read_all(db: Session = Depends(get_db)):
    return cozinheiros_crud.get_all_cozinheiros(db)

@router.get("/{cpf_coz}", response_model=cozinheiros_schema.Cozinheiro)
def read_one(cpf_coz: str, db: Session = Depends(get_db)):
    return cozinheiros_crud.get_cozinheiro_by_cpf(cpf_coz, db)

@router.put("/{cpf_coz}")
def update(cpf_coz: str, cozinheiro: cozinheiros_schema.CozinheiroBase, db: Session = Depends(get_db)):
    return cozinheiros_crud.update_cozinheiro(cpf_coz, cozinheiro, db)

@router.delete("/{cpf_coz}", status_code=status.HTTP_200_OK)
def delete(cpf_coz: str, db: Session = Depends(get_db)):
    return cozinheiros_crud.delete_cozinheiro(cpf_coz, db)
