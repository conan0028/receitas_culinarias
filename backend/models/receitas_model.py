from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.models.inclui_model import Inclui
from backend.database import Base

class Receita(Base):
    __tablename__ = "receitas"

    cod_rec = Column(Integer, primary_key=True, index=True)
    nome_rec = Column(String(80), nullable=False)
    dt_criacao_rec = Column(Date, nullable=False)
    cod_categoria_rec = Column(Integer, ForeignKey("categorias.cod_categoria"), nullable=False)
    cpf_coz = Column(String(11), ForeignKey("cozinheiros.cpf_coz"), nullable=False)
    isbn_rec = Column(Integer, ForeignKey("livros.isbn"), nullable=False)

    categoria = relationship("Categoria", back_populates="receitas")
    cozinheiro = relationship("Cozinheiro", back_populates="receitas")
    livro = relationship("Livro", back_populates="receitas")
    testadas = relationship("Testa", back_populates="receita")
    editores = relationship("Possui", back_populates="receita")
    ingredientes_receitas = relationship("IngredienteReceita", back_populates="receita")
    ingredientes = relationship("IngredienteReceita", back_populates="receita", cascade="all, delete-orphan")

Receita.livros_incluidos = relationship(Inclui, back_populates="receita")
# Adicione este relacionamento à classe Receita
