from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import empregados_schema

def get_all_empregados(db: Session):
    return db.query(models.Empregado).all()

def get_empregado_by_rg(rg: str, db: Session):
    empregado = db.query(models.Empregado).filter(models.Empregado.rg == rg).first()
    if not empregado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empregado não encontrado."
        )
    return empregado

def create_empregado(empregado_data: empregados_schema.EmpregadoCreate, db: Session):
    novo_empregado = models.Empregado(**empregado_data.model_dump())

    try:
        db.add(novo_empregado)
        db.commit()
        return {"message": "Empregado cadastrado com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empregado com este RG já está cadastrado."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao cadastrar empregado."
        )

def update_empregado(rg: str, empregado_atualizado: empregados_schema.EmpregadoBase, db: Session):
    empregado = get_empregado_by_rg(rg, db)

    empregado.salario = empregado_atualizado.salario

    try:
        db.commit()
        return {"message": "Empregado atualizado com sucesso."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar empregado: {str(e)}"
        )

def delete_empregado(rg: str, db: Session):
    empregado = get_empregado_by_rg(rg, db)

    try:
        db.delete(empregado)
        db.commit()
        return {"message": "Empregado removido com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "violates foreign key constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível remover este empregado: registro vinculado a outras tabelas."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao remover empregado."
        )
