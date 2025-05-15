from sqlalchemy import Column, Integer, String, Date, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Testa(Base):
    __tablename__ = "testa"

    cod_rec_test = Column(Integer, ForeignKey("receitas.cod_rec"), primary_key=True)
    cpf_deg_test = Column(String(11), ForeignKey("degustadores.cpf_deg"), primary_key=True)
    dt_test = Column(Date, nullable=False)
    nota_test = Column(BigInteger, nullable=False)

    receita = relationship("Receita", back_populates="testadas")
    degustador = relationship("Degustador", back_populates="testes")
