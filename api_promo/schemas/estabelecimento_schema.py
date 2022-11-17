from typing import Optional

from typing import List
from datetime import date

from pydantic import BaseModel

from api_promo.schemas.produto_schema import ProdutoSchema

    
class EstabelecimentoSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    telefone: Optional[str]
    endereco: str
    latitude: str
    longitude: str
    urlImagem: Optional[str]
    usuario_estabelecimento_id: Optional[int] = None

    class Config:
        orm_mode = True

class EstabelecimentoSchemaAlter(BaseModel):
    id: Optional[int] = None
    nome: Optional[str]
    telefone: Optional[str]
    endereco: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    urlImagem: Optional[str]
    usuario_estabelecimento_id: Optional[int] = None

    class Config:
        orm_mode = True

class Promocao(BaseModel):
    id: Optional[int] = None
    valor_original: str
    valor_promocional: Optional[str]
    data_validade: Optional[str]
    produto: Optional[ProdutoSchema]

    class Config:
        orm_mode = True

class EstabelecimentoSchemaPromocao(EstabelecimentoSchema):
    promocoes: List[Promocao]

    class Config:
        orm_mode = True




