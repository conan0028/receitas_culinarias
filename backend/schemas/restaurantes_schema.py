from pydantic import BaseModel

class RestauranteBase(BaseModel):
    endereco: str

class RestauranteCreate(RestauranteBase):
    nome_rest: str

class Restaurante(RestauranteCreate):
    class Config:
        orm_mode = True
