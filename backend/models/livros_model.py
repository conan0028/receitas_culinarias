from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from backend.models.inclui_model import Inclui
from backend.models.receitas_model import Receita

from backend.database import Base


class Livro(Base):
    __tablename__ = "livros"

    titulo_livro = Column(String(200), primary_key=True, index=True)
    isbn = Column(Integer, unique=True, nullable=False)

    receitas = relationship(Receita, back_populates="livro")
    receitas_incluidas = relationship(Inclui, back_populates="livro")
