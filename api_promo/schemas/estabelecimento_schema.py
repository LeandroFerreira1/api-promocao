from typing import Optional

from pydantic import BaseModel

    
class EstabelecimentoSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    telefone: Optional[str]
    endereco: str
    latitude: str
    longitude: str
    usuario_estabelecimento_id: Optional[int] = None

    class Config:
        orm_mode = True
