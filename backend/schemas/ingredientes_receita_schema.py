from pydantic import BaseModel

class IngredienteReceitaBase(BaseModel):
    quant_ingrec: float
    med_ingrec: str

class IngredienteReceitaCreate(IngredienteReceitaBase):
    cod_rec_ingrec: int
    cod_ing_ingrec: int

class IngredienteReceita(IngredienteReceitaCreate):
    class Config:
        orm_mode = True
