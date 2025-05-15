import status
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend.crud.inclui_crud import get_single_inclui
from backend.database import get_db
from backend.crud import inclui_crud
from backend.schemas import inclui_schema
from backend.schemas.inclui_schema import IncluiCreate, IncluiRead
from typing import Optional
router = APIRouter(prefix="/inclui", tags=["Inclui"])

@router.get("/", response_model=list[IncluiRead])
def listar_todas_relacoes(db: Session = Depends(get_db)):
    return inclui_crud.get_all_inclui(db)

@router.post("/", status_code=201)
def criar_relacao(inclui_data: IncluiCreate, db: Session = Depends(get_db)):
    return inclui_crud.create_inclui(inclui_data, db)

@router.delete("/")
def excluir_relacao(cod_rec_inc: int, titulo_liv_inc: str, db: Session = Depends(get_db)):
    return inclui_crud.delete_inclui(cod_rec_inc, titulo_liv_inc, db)

# No router (inclui_router.py)
@router.put("/{cod_rec_inc}/{titulo_liv_inc}")
def update_relation(
        cod_rec_inc: int,
        titulo_liv_inc: str,
        update_data: inclui_schema.IncluiUpdate,
        db: Session = Depends(get_db)
):
    return inclui_crud.update_inclui(cod_rec_inc, titulo_liv_inc, update_data, db)

@router.put("/{cod_rec_inc}/{titulo_liv_inc}")
def update_relation(
        cod_rec_inc: int,
        titulo_liv_inc: str,
        update_data: inclui_schema.IncluiUpdate,
        db: Session = Depends(get_db)
):
    return inclui_crud.update_inclui(cod_rec_inc, titulo_liv_inc, update_data, db)
