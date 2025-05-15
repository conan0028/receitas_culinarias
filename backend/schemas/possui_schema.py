from pydantic import BaseModel

class PossuiBase(BaseModel):
    cod_rec_pos: int
    cpf_edit_pos: str

class PossuiCreate(PossuiBase):
    pass

class Possui(PossuiBase):
    class Config:
        from_attributes = True
