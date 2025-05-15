from pydantic import BaseModel
from datetime import date

class RestauranteCozinheiroBase(BaseModel):
    dt_contratacao: date

class RestauranteCozinheiroCreate(RestauranteCozinheiroBase):
    cod_coz_restcoz: str
    nome_rest_restcoz: str

class RestauranteCozinheiro(RestauranteCozinheiroCreate):
    class Config:
        orm_mode = True
