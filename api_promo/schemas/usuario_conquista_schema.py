from typing import Optional
from datetime import date
from typing import List

from pydantic import BaseModel
from schemas.conquista_schema import ConquistaSchema
from schemas.usuario_schema import UsuarioSchemaBase

from datetime import datetime
now = datetime.now()


class UsuarioConquistaSchemaBase(BaseModel):
    usuario_id: int
    conquista_id: int
    data_canquista: date = now
    
    class Config:
        orm_mode = True

class UsuarioConquistaSchema(UsuarioConquistaSchemaBase):
    criador: Optional[UsuarioSchemaBase]
    conquitas: Optional[List[ConquistaSchema]]

    class Config:
        orm_mode = True