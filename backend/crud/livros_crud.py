from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import livros_schema


def get_all_livros(db: Session):
    return db.query(models.Livro).all()


def get_livro_by_titulo(titulo_livro: str, db: Session):
    livro = db.query(models.Livro).filter(models.Livro.titulo_livro == titulo_livro).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )
    return livro


def create_livro(livro_data: livros_schema.LivroCreate, db: Session):
    novo_livro = models.Livro(**livro_data.model_dump())

    try:
        db.add(novo_livro)
        db.commit()
        return {"message": "Livro incluído com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "duplicate key value violates unique constraint" in str(e.orig):
            if "livros_pkey" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Livro com este título já está cadastrado."
                )
            elif "livros_isbn_key" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Livro com este ISBN já está cadastrado."
                )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao incluir livro."
        )


def update_livro(titulo_livro: str, livro_atualizado: livros_schema.LivroBase, db: Session):
    livro = get_livro_by_titulo(titulo_livro, db)

    livro.isbn = livro_atualizado.isbn

    try:
        db.commit()
        return {"message": "Livro alterado com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um livro com este ISBN."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao alterar livro."
        )

# def delete_livro(titulo_livro: str, db: Session):
#     livro = get_livro_by_titulo(titulo_livro, db)
#
#     try:
#         db.delete(livro)
#         db.commit()
#         return {"message": "Livro excluído com sucesso."}
#     except IntegrityError as e:
#         db.rollback()
#         if "violates foreign key constraint" in str(e.orig):
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Não é possível excluir este livro: ele está vinculado a outras tabelas."
#             )
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Erro ao excluir livro."
#         )
def delete_livro(titulo_livro: str, db: Session):
    # Verifica dependências na tabela inclui
    qtd_inclui = db.query(models.Inclui).filter_by(titulo_liv_inc=titulo_livro).count()

    if qtd_inclui > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não é possível excluir este livro pois ele está vinculado a {qtd_inclui} receitas.\n"
                   "Por favor, remova primeiro estas relações através do endpoint:\n"
                   "- DELETE /inclui/livro/{titulo_livro}\n"
                   "Ou para relações específicas:\n"
                   "- DELETE /inclui/{cod_rec}/{titulo_livro}"
        )

    # Se não houver dependências, apaga
    livro = db.query(models.Livro).get(titulo_livro)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    db.delete(livro)
    db.commit()
    return {"message": "Livro excluído com sucesso"}