from typing import Optional
from datetime import date

from pydantic import BaseModel
from schemas.promocao_schema import PromocaoSchemaBase
from schemas.usuario_schema import UsuarioSchemaBase




class AvaliacaoSchemaBase(BaseModel):
    usuario_id: int
    promocao_id: int
    descricao: Optional[str]
    longitude: Optional[str]
    latitude: Optional[str]
    nota: int
    
    class Config:
        orm_mode = True

class AvaliacaoSchema(AvaliacaoSchemaBase):
    criador: Optional[UsuarioSchemaBase]
    promocao: Optional[PromocaoSchemaBase]

    class Config:
        orm_mode = True

class AvaliacaoPromocaoSchema(AvaliacaoSchemaBase):
    criador: Optional[UsuarioSchemaBase]

    class Config:
        orm_mode = True