from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class RestauranteCozinheiro(Base):
    __tablename__ = "restaurantes_cozinheiro"

    cod_coz_restcoz = Column(String(11), ForeignKey("cozinheiros.cpf_coz"), primary_key=True)
    nome_rest_restcoz = Column(String(80), ForeignKey("restaurantes.nome_rest"), primary_key=True)
    dt_contratacao = Column(Date, nullable=False)

    cozinheiro = relationship("Cozinheiro", back_populates="restaurantes")
    restaurante = relationship("Restaurante", back_populates="cozinheiros")
