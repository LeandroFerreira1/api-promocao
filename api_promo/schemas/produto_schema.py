from typing import Optional

from pydantic import BaseModel
from typing import Optional
from typing import List


class ProdutoSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    tipo: Optional[str]
    marca: Optional[str]
    departamento: Optional[str]
    urlImagem: str
    ean: Optional[str]


    class Config:
        orm_mode = True

class EanSchema(BaseModel):
    ean: Optional[str]
    class Config:
        orm_mode = True