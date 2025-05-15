from pydantic import BaseModel, Field
from typing import Optional

class IngredienteBase(BaseModel):
    nome_ingred: str = Field(..., max_length=40, example="Farinha de Trigo")

class IngredienteCreate(IngredienteBase):
    cod_ingred: int

class IngredienteUpdate(BaseModel):
    nome_ingred: Optional[str] = Field(None, max_length=40, example="Farinha Integral")

class Ingrediente(IngredienteBase):
    cod_ingred: int

    class Config:
        from_attributes = True
