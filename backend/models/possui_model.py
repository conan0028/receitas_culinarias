from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Possui(Base):
    __tablename__ = "possui"

    cod_rec_pos = Column(Integer, ForeignKey('receitas.cod_rec'), primary_key=True)
    cpf_edit_pos = Column(String(11), ForeignKey('editores.cpf_edit'), primary_key=True)

    # Relacionamentos
    editor = relationship("Editor", back_populates="possui")
    receita = relationship("Receita", back_populates="editores")
