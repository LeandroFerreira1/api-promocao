from typing import Optional

from pydantic import BaseModel
from typing import Optional
from typing import List
from sqlalchemy import BigInteger
from schemas.departamento_schema import DepartamentoSchema


class ProdutoSchema(BaseModel):
    id: int
    nome: str
    marca: Optional[str]
    departamento_id: Optional[int] = None
    urlImagem: str

    class Config:
        orm_mode = True

class ProdutoSchemaCompleto(BaseModel):
    id: int
    nome: str
    marca: Optional[str]
    urlImagem: str
    departamento: Optional[DepartamentoSchema]

    class Config:
        orm_mode = True
