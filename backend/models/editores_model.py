from sqlalchemy import Column, String, Date, BigInteger
from sqlalchemy.orm import relationship
from backend.database import Base

class Editor(Base):
    __tablename__ = "editores"

    cpf_edit = Column(String(11), primary_key=True, index=True)
    nome_edit = Column(String(80), nullable=False)
    dt_contrato_edit = Column(Date, nullable=False)
    salario_edit = Column(BigInteger, nullable=False)

    receitas = relationship("Possui", back_populates="editor")
    possui = relationship("Possui", back_populates="editor")
