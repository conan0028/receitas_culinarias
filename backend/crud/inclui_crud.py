from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import inclui_schema

def get_single_inclui(cod_rec_inc, titulo_liv_inc, db):
    pass

# lista todas as tuplas
def get_all_inclui(db: Session):
    return db.query(models.Inclui).all()

# obtem uma tupla
def get_inclui(cod_rec_inc: int, titulo_liv_inc: str, db: Session):
    relacao = db.query(models.Inclui).filter(
        models.Inclui.cod_rec_inc == cod_rec_inc,
        models.Inclui.titulo_liv_inc == titulo_liv_inc
    ).first()

    if not relacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relação não encontrada."
        )
    return relacao

# criar nova tupla
def create_inclui(inclui_data: inclui_schema.IncluiCreate, db: Session):
    nova_relacao = models.Inclui(**inclui_data.model_dump())
    try:
        db.add(nova_relacao)
        db.commit()
        db.refresh(nova_relacao)
        return {"message": "Relação entre receita e livro criada com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Receita ou Livro não existem."
            )
        if "duplicate key value" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta relação já foi cadastrada."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar relação receita-livro."
        )
# atualizar uma tupla
def update_inclui(
        cod_rec_inc: int,
        titulo_liv_inc: str,
        update_data: inclui_schema.IncluiUpdate,
        db: Session
):
    relacao = get_inclui(cod_rec_inc, titulo_liv_inc, db)

    try:
        # Atualiza campos se foram fornecidos
        if update_data.new_cod_rec_inc is not None:
            relacao.cod_rec_inc = update_data.new_cod_rec_inc
        if update_data.new_titulo_liv_inc is not None:
            relacao.titulo_liv_inc = update_data.new_titulo_liv_inc

        db.commit()
        return {"message": "Relação atualizada com sucesso"}

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Erro de integridade: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        )

# exclui uma tupla
def delete_inclui(cod_rec_inc: int, titulo_liv_inc: str, db: Session):
    relacao = db.query(models.Inclui).filter_by(
        cod_rec_inc=cod_rec_inc,
        titulo_liv_inc=titulo_liv_inc
    ).first()

    if not relacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relação não encontrada."
        )

    db.delete(relacao)
    db.commit()
    return {"message": "Relação excluída com sucesso."}
