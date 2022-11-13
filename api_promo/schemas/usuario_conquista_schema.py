from typing import Optional
from datetime import date
from typing import List

from pydantic import BaseModel
from schemas.conquista_schema import ConquistaSchema
from schemas.usuario_schema import UsuarioSchemaBase


class UsuarioConquistaSchemaBase(BaseModel):
    usuario_id: int
    conquista_id: int
    
    class Config:
        orm_mode = True

class UsuarioConquistaSchema(UsuarioConquistaSchemaBase):
    criador: Optional[UsuarioSchemaBase]
    conquita: Optional[ConquistaSchema]

    class Config:
        orm_mode = True