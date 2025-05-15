from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from backend.database import Base

class Inclui(Base):
    __tablename__ = "inclui"

    cod_rec_inc = Column(Integer, ForeignKey("receitas.cod_rec"), primary_key=True)
    titulo_liv_inc = Column(String(200), ForeignKey("livros.titulo_livro"), primary_key=True)

    receita = relationship("Receita", back_populates="livros_incluidos")
    livro = relationship("Livro", back_populates="receitas_incluidas")
