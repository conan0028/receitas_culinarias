from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import categorias_schema
from backend.crud import categorias_crud

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post("/", status_code=201)
def create(categoria: categorias_schema.CategoriaCreate, db: Session = Depends(get_db)):
    return categorias_crud.create_categoria(categoria, db)


@router.get("/", response_model=list[categorias_schema.Categoria])
def read_all(db: Session = Depends(get_db)):
    return categorias_crud.get_all_categorias(db)


@router.get("/{cod_categoria}", response_model=categorias_schema.Categoria)
def read_one(cod_categoria: int, db: Session = Depends(get_db)):
    return categorias_crud.get_categoria_by_cod(cod_categoria, db)


@router.put("/{cod_categoria}")
def update(cod_categoria: int, categoria: categorias_schema.CategoriaBase, db: Session = Depends(get_db)):
    return categorias_crud.update_categoria(cod_categoria, categoria, db)


@router.delete("/{cod_categoria}", status_code=200)
def delete(cod_categoria: int, db: Session = Depends(get_db)):
    return categorias_crud.delete_categoria(cod_categoria, db)
