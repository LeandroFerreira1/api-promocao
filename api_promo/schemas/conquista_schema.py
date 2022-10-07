from typing import Optional

from pydantic import BaseModel


class ConquistaSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    valor: int

class ConquistaSchemaAlter(BaseModel):
    id: Optional[int] = None
    nome: Optional[str]
    valor: Optional[int]


    class Config:
        orm_mode = True