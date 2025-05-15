from pydantic import BaseModel
from datetime import date

class TestaBase(BaseModel):
    dt_test: date
    nota_test: int

class TestaCreate(TestaBase):
    cod_rec_test: int
    cpf_deg_test: str

class Testa(TestaCreate):
    class Config:
        orm_mode = True
