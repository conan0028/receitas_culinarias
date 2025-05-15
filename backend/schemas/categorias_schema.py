from pydantic import BaseModel

class CategoriaBase(BaseModel):
    desc_categoria: str  # Verifique se este campo está como obrigatório

class CategoriaCreate(CategoriaBase):
    cod_categoria: int

class Categoria(CategoriaCreate):
    class Config:
        from_attributes = True