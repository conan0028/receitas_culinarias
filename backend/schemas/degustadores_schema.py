from pydantic import BaseModel
from datetime import date

class DegustadorBase(BaseModel):
    nome_deg: str
    dt_contrato_deg: date
    salario_deg: int

class DegustadorCreate(DegustadorBase):
    cpf_deg: str

class Degustador(DegustadorCreate):
    class Config:
        from_attributes = True
