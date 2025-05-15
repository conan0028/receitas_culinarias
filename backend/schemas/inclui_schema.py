from typing import Optional

from pydantic import BaseModel, Field


class IncluiBase(BaseModel):
    cod_rec_inc: int
    titulo_liv_inc: str

class IncluiCreate(IncluiBase):
    pass

class IncluiRead(IncluiBase):
    class Config:
        orm_mode = True

class IncluiUpdate(BaseModel):
    new_cod_rec_inc: Optional[int] = None
    new_titulo_liv_inc: Optional[str] = None
