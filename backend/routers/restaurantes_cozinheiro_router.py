from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from backend.crud import restaurantes_cozinheiro_crud
from backend.database import get_db
from backend.schemas import restaurantes_cozinheiro_schema

router = APIRouter(prefix="/restaurantes_cozinheiro", tags=["Restaurantes_Cozinheiro"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(restaurante_cozinheiro: restaurantes_cozinheiro_schema.RestauranteCozinheiroCreate, db: Session = Depends(get_db)):
    return restaurantes_cozinheiro_crud.create_restaurante_cozinheiro(restaurante_cozinheiro, db)

@router.get("/", response_model=list[restaurantes_cozinheiro_schema.RestauranteCozinheiro])
def read_all(db: Session = Depends(get_db)):
    return restaurantes_cozinheiro_crud.get_all_restaurantes_cozinheiro(db)

@router.get("/{cod_coz_restcoz}/{nome_rest_restcoz}", response_model=restaurantes_cozinheiro_schema.RestauranteCozinheiro)
def read_one(cod_coz_restcoz: str, nome_rest_restcoz: str, db: Session = Depends(get_db)):
    return restaurantes_cozinheiro_crud.get_restaurante_cozinheiro(cod_coz_restcoz, nome_rest_restcoz, db)

@router.put("/{cod_coz_restcoz}/{nome_rest_restcoz}")
def update(
        cod_coz_restcoz: str,
        nome_rest_restcoz: str,
        restaurante_cozinheiro: restaurantes_cozinheiro_schema.RestauranteCozinheiroBase,
        db: Session = Depends(get_db)
):
    return restaurantes_cozinheiro_crud.update_restaurante_cozinheiro(cod_coz_restcoz, nome_rest_restcoz, restaurante_cozinheiro, db)

@router.delete("/{cod_coz_restcoz}/{nome_rest_restcoz}", status_code=status.HTTP_200_OK)
def delete(cod_coz_restcoz: str, nome_rest_restcoz: str, db: Session = Depends(get_db)):
    return restaurantes_cozinheiro_crud.delete_restaurante_cozinheiro(cod_coz_restcoz, nome_rest_restcoz, db)
