from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import livros_schema
from backend.crud import livros_crud

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.post("/", status_code=201)
def create(livro: livros_schema.LivroCreate, db: Session = Depends(get_db)):
    return livros_crud.create_livro(livro, db)


@router.get("/", response_model=list[livros_schema.Livro])
def read_all(db: Session = Depends(get_db)):
    return livros_crud.get_all_livros(db)


@router.get("/{titulo_livro}", response_model=livros_schema.Livro)
def read_one(titulo_livro: str, db: Session = Depends(get_db)):
    return livros_crud.get_livro_by_titulo(titulo_livro, db)


@router.put("/{titulo_livro}")
def update(titulo_livro: str, livro: livros_schema.LivroBase, db: Session = Depends(get_db)):
    return livros_crud.update_livro(titulo_livro, livro, db)


@router.delete("/{titulo_livro}", status_code=200)
def delete(titulo_livro: str, db: Session = Depends(get_db)):
    return livros_crud.delete_livro(titulo_livro, db)
