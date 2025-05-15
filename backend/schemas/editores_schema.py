from pydantic import BaseModel
from datetime import date

class EditorBase(BaseModel):
    nome_edit: str
    dt_contrato_edit: date
    salario_edit: int

class EditorCreate(EditorBase):
    cpf_edit: str

class Editor(EditorCreate):
    class Config:
        from_attributes = True
