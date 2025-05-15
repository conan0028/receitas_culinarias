from sqlalchemy import Column, String, Date, BigInteger
from sqlalchemy.orm import relationship
from backend.database import Base

class Degustador(Base):
    __tablename__ = "degustadores"

    cpf_deg = Column(String(11), primary_key=True, index=True)
    nome_deg = Column(String(80), nullable=False)
    dt_contrato_deg = Column(Date, nullable=False)
    salario_deg = Column(BigInteger, nullable=False)

    testes = relationship("Testa", back_populates="degustador")
