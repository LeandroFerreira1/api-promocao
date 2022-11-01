from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr
from schemas.estabelecimento_schema import EstabelecimentoSchema
from schemas.produto_schema import ProdutoSchema


class PromocaoSchemaBase(BaseModel):
    id: Optional[int] = None
    valor_original: Optional[str]
    valor_promocional: str
    data_validade: Optional[str]
    usuario_id: int
    estabelecimento_id: int
    produto_id: int

    class Config:
        orm_mode = True

class PromocaoSchemaAlter(BaseModel):
    id: Optional[int] = None
    valor_original: Optional[str]
    valor_promocional: Optional[str]
    data_validade: Optional[str]
    usuario_id: Optional[int]
    estabelecimento_id: Optional[int]
    produto_id: Optional[int]

    class Config:
        orm_mode = True

class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: Optional[str]
    email: EmailStr
    urlImagem: Optional[str]

    class Config:
        orm_mode = True

class PromocaoSchema(BaseModel):
    id: Optional[int] = None
    valor_original: str
    valor_promocional: Optional[str]
    data_validade: Optional[str]
    estabelecimento: Optional[EstabelecimentoSchema]
    produto: Optional[ProdutoSchema]
    criador: Optional[UsuarioSchemaBase]

    class Config:
        orm_mode = True