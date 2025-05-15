from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from backend.database import Base

class Restaurante(Base):
    __tablename__ = "restaurantes"

    nome_rest = Column(String(80), primary_key=True, index=True)
    endereco = Column(String(200), nullable=False)

    cozinheiros = relationship("RestauranteCozinheiro", back_populates="restaurante")