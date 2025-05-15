from sqlalchemy import Column, String, Date, BigInteger
from sqlalchemy.orm import relationship
from backend.database import Base

class Cozinheiro(Base):
    __tablename__ = "cozinheiros"

    cpf_coz = Column(String(11), primary_key=True, index=True)
    nome_coz = Column(String(80), nullable=False)
    nome_fantasia = Column(String(80), nullable=False)
    dt_contrato_coz = Column(Date, nullable=False)
    salario_coz = Column(BigInteger, nullable=False)

    receitas = relationship("Receita", back_populates="cozinheiro")
    restaurantes = relationship("RestauranteCozinheiro", back_populates="cozinheiro")
