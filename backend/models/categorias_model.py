from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    cod_categoria = Column(Integer, primary_key=True, index=True)
    desc_categoria = Column(String, nullable=False)

    receitas = relationship("Receita", back_populates="categoria")
