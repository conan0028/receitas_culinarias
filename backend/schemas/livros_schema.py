from pydantic import BaseModel

class LivroBase(BaseModel):
    isbn: int

class LivroCreate(LivroBase):
    titulo_livro: str

class Livro(LivroCreate):
    class Config:
        orm_mode = True
