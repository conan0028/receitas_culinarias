from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from backend.database import get_db
from backend.schemas import editores_schema
from backend.crud import editores_crud

router = APIRouter(prefix="/editores", tags=["Editores"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(editor: editores_schema.EditorCreate, db: Session = Depends(get_db)):
    return editores_crud.create_editor(editor, db)

@router.get("/", response_model=list[editores_schema.Editor])
def read_all(db: Session = Depends(get_db)):
    return editores_crud.get_all_editores(db)

@router.get("/{cpf_edit}", response_model=editores_schema.Editor)
def read_one(cpf_edit: str, db: Session = Depends(get_db)):
    return editores_crud.get_editor_by_cpf(cpf_edit, db)

@router.put("/{cpf_edit}")
def update(cpf_edit: str, editor: editores_schema.EditorBase, db: Session = Depends(get_db)):
    return editores_crud.update_editor(cpf_edit, editor, db)

@router.delete("/{cpf_edit}", status_code=status.HTTP_200_OK)
def delete(cpf_edit: str, db: Session = Depends(get_db)):
    return editores_crud.delete_editor(cpf_edit, db)
