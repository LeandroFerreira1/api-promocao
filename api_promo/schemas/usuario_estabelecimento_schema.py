from typing import Optional
from typing import List

from pydantic import BaseModel, EmailStr

from schemas.estabelecimento_schema import EstabelecimentoSchema


class UsuarioEstabelecimentoSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr

    class Config:
        orm_mode = True


class UsuarioEstabelecimentoSchemaCreate(UsuarioEstabelecimentoSchemaBase):
    senha: str


class UsuarioEstabelecimentoSchemaEstabelecimentos(UsuarioEstabelecimentoSchemaBase):
    Estabelecimentos: Optional[List[EstabelecimentoSchema]]


class UsuarioEstabelecimentoSchemaUp(UsuarioEstabelecimentoSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
