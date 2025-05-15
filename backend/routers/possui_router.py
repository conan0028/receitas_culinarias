from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from backend.database import get_db
from backend.schemas import possui_schema
from backend.crud import possui_crud

router = APIRouter(prefix="/possui", tags=["Possui"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(possui: possui_schema.PossuiCreate, db: Session = Depends(get_db)):
    return possui_crud.create_possui(possui, db)

@router.delete("/{cod_rec_pos}/{cpf_edit_pos}", status_code=status.HTTP_200_OK)
def delete(cod_rec_pos: int, cpf_edit_pos: str, db: Session = Depends(get_db)):
    return possui_crud.delete_possui(cod_rec_pos, cpf_edit_pos, db)
