from pydantic import BaseModel
from datetime import date

class ReceitaBase(BaseModel):
    nome_rec: str
    dt_criacao_rec: date
    cod_categoria_rec: int
    cpf_coz: str
    isbn_rec: int

class ReceitaCreate(ReceitaBase):
    cod_rec: int

class Receita(ReceitaCreate):
    class Config:
        orm_mode = True
