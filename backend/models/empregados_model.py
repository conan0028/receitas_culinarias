from sqlalchemy import Column, String, BigInteger
from backend.database import Base

class Empregado(Base):
    __tablename__ = "empregados_rg"

    rg = Column(String(20), primary_key=True, index=True)
    salario = Column(BigInteger, nullable=False)
