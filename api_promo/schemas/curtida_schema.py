from typing import Optional
from datetime import date

from pydantic import BaseModel
from schemas.promocao_schema import PromocaoSchemaBase
from schemas.usuario_schema import UsuarioSchemaBase

class CurtidaSchemaBase(BaseModel):
    usuario_id: int
    promocao_id: int
    
    class Config:
        orm_mode = True

class CurtidaSchema(CurtidaSchemaBase):
    criador: Optional[UsuarioSchemaBase]
    promocao: Optional[PromocaoSchemaBase]

    class Config:
        orm_mode = True

class CurtidaPromocaoSchema(CurtidaSchemaBase):
    criador: Optional[UsuarioSchemaBase]

    class Config:
        orm_mode = True