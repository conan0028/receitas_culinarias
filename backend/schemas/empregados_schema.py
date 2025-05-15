from pydantic import BaseModel, Field

class EmpregadoBase(BaseModel):
    salario: int = Field(..., gt=0, description="O salário deve ser maior que zero")

class EmpregadoCreate(EmpregadoBase):
    rg: str = Field(..., max_length=20, description="RG do empregado")

class Empregado(EmpregadoCreate):
    class Config:
        from_attributes = True
