from typing import Optional

from pydantic import BaseModel


class ConquistaSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    valor: int
    urlimagem: Optional[str]

    class Config:
        orm_mode = True

class ConquistaSchemaAlter(BaseModel):
    id: Optional[int] = None
    nome: Optional[str]
    valor: Optional[int]
    urlimagem: Optional[str]


    class Config:
        orm_mode = True