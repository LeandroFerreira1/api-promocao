from typing import Optional
from typing import List

from pydantic import BaseModel, EmailStr

from schemas.promocao_schema import PromocaoSchema


class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr

    class Config:
        orm_mode = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str


class UsuarioSchemaPromocoes(UsuarioSchemaBase):
    promocoes: Optional[List[PromocaoSchema]]


class UsuarioSchemaUp(UsuarioSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]