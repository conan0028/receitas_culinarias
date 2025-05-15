from pydantic import BaseModel
from datetime import date

class CozinheiroBase(BaseModel):
    nome_coz: str
    nome_fantasia: str
    dt_contrato_coz: date
    salario_coz: int

class CozinheiroCreate(CozinheiroBase):
    cpf_coz: str

class Cozinheiro(CozinheiroCreate):
    class Config:
        from_attributes = True
