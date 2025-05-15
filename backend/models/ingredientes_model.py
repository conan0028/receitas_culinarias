from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database import Base

class Ingrediente(Base):
    __tablename__ = "ingredientes"

    cod_ingred = Column(Integer, primary_key=True, index=True)
    nome_ingred = Column(String(40), nullable=False, unique=True)

    # Relacionamento corrigido (nome consistente)
    receitas = relationship("IngredienteReceita", back_populates="ingrediente", cascade="all, delete-orphan")
