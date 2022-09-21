from typing import Optional
from datetime import date

from pydantic import BaseModel
from schemas.estabelecimento_schema import EstabelecimentoSchema
from schemas.produto_schema import ProdutoSchema


class PromocaoSchemaBase(BaseModel):
    id: Optional[int] = None
    valor_original: Optional[str]
    valor_promocional: str
    data_validade: Optional[date]
    usuario_id: int
    estabelecimento_id: int
    produto_id: int

    class Config:
        orm_mode = True

class PromocaoSchema(BaseModel):
    id: Optional[int] = None
    valor_original: Optional[str]
    valor_promocional: str
    data_validade: Optional[date]
    estabelecimento: Optional[EstabelecimentoSchema]
    produto: Optional[ProdutoSchema]

    class Config:
        orm_mode = True