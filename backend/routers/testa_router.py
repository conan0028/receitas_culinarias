from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from backend.crud import testa_crud
from backend.database import get_db
from backend.schemas import testa_schema

router = APIRouter(prefix="/testa", tags=["Testa"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(testa: testa_schema.TestaCreate, db: Session = Depends(get_db)):
    return testa_crud.create_testa(testa, db)

@router.get("/", response_model=list[testa_schema.Testa])
def read_all(db: Session = Depends(get_db)):
    return testa_crud.get_all_testas(db)

@router.get("/{cod_rec_test}/{cpf_deg_test}", response_model=testa_schema.Testa)
def read_one(cod_rec_test: int, cpf_deg_test: str, db: Session = Depends(get_db)):
    return testa_crud.get_testa(cod_rec_test, cpf_deg_test, db)

@router.put("/{cod_rec_test}/{cpf_deg_test}")
def update(
        cod_rec_test: int,
        cpf_deg_test: str,
        testa: testa_schema.TestaBase,
        db: Session = Depends(get_db)
):
    return testa_crud.update_testa(cod_rec_test, cpf_deg_test, testa, db)

@router.delete("/{cod_rec_test}/{cpf_deg_test}", status_code=status.HTTP_200_OK)
def delete(cod_rec_test: int, cpf_deg_test: str, db: Session = Depends(get_db)):
    return testa_crud.delete_testa(cod_rec_test, cpf_deg_test, db)
