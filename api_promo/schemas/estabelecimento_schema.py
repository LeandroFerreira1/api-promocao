from typing import Optional

from typing import List

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

class Promocao(BaseModel):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class EstabelecimentoSchemaPromocao(BaseModel):
    id: Optional[int] = None
    nome: str
    promocoes: List[Promocao]

    class Config:
        orm_mode = True




