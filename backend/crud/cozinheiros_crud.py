from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from backend import models
from backend.schemas import cozinheiros_schema

def get_all_cozinheiros(db: Session):
    return db.query(models.Cozinheiro).all()

def get_cozinheiro_by_cpf(cpf_coz: str, db: Session):
    cozinheiro = db.query(models.Cozinheiro).filter(models.Cozinheiro.cpf_coz == cpf_coz).first()
    if not cozinheiro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cozinheiro não encontrado."
        )
    return cozinheiro

def create_cozinheiro(cozinheiro_data: cozinheiros_schema.CozinheiroCreate, db: Session):
    novo_cozinheiro = models.Cozinheiro(**cozinheiro_data.model_dump())

    try:
        db.add(novo_cozinheiro)
        db.commit()
        db.refresh(novo_cozinheiro)
        return {"message": "Cozinheiro criado com sucesso."}
    except IntegrityError as e:
        db.rollback()
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cozinheiro com este CPF já está cadastrado."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar cozinheiro."
        )

def update_cozinheiro(cpf_coz: str, cozinheiro_atualizado: cozinheiros_schema.CozinheiroBase, db: Session):
    cozinheiro = get_cozinheiro_by_cpf(cpf_coz, db)

    cozinheiro.nome_coz = cozinheiro_atualizado.nome_coz
    cozinheiro.nome_fantasia = cozinheiro_atualizado.nome_fantasia
    cozinheiro.dt_contrato_coz = cozinheiro_atualizado.dt_contrato_coz
    cozinheiro.salario_coz = cozinheiro_atualizado.salario_coz

    try:
        db.commit()
        return {"message": "Cozinheiro alterado com sucesso."}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao alterar cozinheiro."
        )

def delete_cozinheiro(cpf_coz: str, db: Session):
    cozinheiro = get_cozinheiro_by_cpf(cpf_coz, db)

    try:
        # Verifica dependências antes de tentar apagar
        receitas = db.query(models.Receita).filter(models.Receita.cpf_coz == cpf_coz).all()
        restaurantes = db.query(models.RestauranteCozinheiro).filter(models.RestauranteCozinheiro.cod_coz_restcoz == cpf_coz).all()

        if receitas or restaurantes:
            mensagem = "Não é possível excluir este cozinheiro pois está vinculado a:\n"
            if receitas:
                mensagem += f"- Receitas ({len(receitas)} registros):\n"
                for receita in receitas:
                    mensagem += f"  * {receita.nome_rec} (Código: {receita.cod_rec})\n"
            if restaurantes:
                mensagem += f"- Restaurantes ({len(restaurantes)} registros)\n"
            mensagem += "\nPor favor, remova estes vínculos primeiro."

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=mensagem
            )

        db.delete(cozinheiro)
        db.commit()
        return {"message": "Cozinheiro excluído com sucesso."}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado: {str(e)}"
        )
