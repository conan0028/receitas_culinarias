from fastapi import APIRouter, Depends, status  # Adicionei o status aqui
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import empregados_schema
from backend.crud import empregados_crud

router = APIRouter(prefix="/empregados", tags=["Empregados"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_empregado(empregado: empregados_schema.EmpregadoCreate, db: Session = Depends(get_db)):
    return empregados_crud.create_empregado(empregado, db)

@router.get("/", response_model=list[empregados_schema.Empregado])
def read_all_empregados(db: Session = Depends(get_db)):
    return empregados_crud.get_all_empregados(db)

@router.get("/{rg}", response_model=empregados_schema.Empregado)
def read_empregado(rg: str, db: Session = Depends(get_db)):
    return empregados_crud.get_empregado_by_rg(rg, db)

@router.put("/{rg}")
def update_empregado(
        rg: str,
        empregado: empregados_schema.EmpregadoBase,
        db: Session = Depends(get_db)
):
    return empregados_crud.update_empregado(rg, empregado, db)

@router.delete("/{rg}", status_code=status.HTTP_200_OK)
def delete_empregado(rg: str, db: Session = Depends(get_db)):
    return empregados_crud.delete_empregado(rg, db)
