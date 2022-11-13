from typing import Optional
from typing import List

from pydantic import BaseModel, EmailStr

from schemas.promocao_schema import PromocaoSchemaBase
from schemas.conquista_schema import ConquistaSchema


class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: Optional[str]
    email: EmailStr
    urlImagem: Optional[str]
    pontuacao: Optional[int]

    class Config:
        orm_mode = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str


class UsuarioSchemaPromocoes(UsuarioSchemaBase):
    promocoes: Optional[List[PromocaoSchemaBase]]

class UsuarioSchemaPonto (BaseModel):
    pontuacao: Optional[int]

    class Config:
        orm_mode = True

class UsuarioSchemaUp(UsuarioSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]