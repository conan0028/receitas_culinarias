from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class IngredienteReceita(Base):
    __tablename__ = "ingredientes_receita"

    cod_rec_ingrec = Column(Integer, ForeignKey('receitas.cod_rec'), primary_key=True)
    cod_ing_ingrec = Column(Integer, ForeignKey('ingredientes.cod_ingred'), primary_key=True)
    quant_ingrec = Column(DECIMAL(6, 2), nullable=False)
    med_ingrec = Column(String(10), nullable=False)

    # Relacionamentos corrigidos
    receita = relationship("Receita", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente", back_populates="receitas")
