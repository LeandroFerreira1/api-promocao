from typing import Optional

from pydantic import BaseModel
from typing import Optional
from typing import List


class ProdutoSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    tipo: Optional[str]
    marca: Optional[str]
    departamento: str
    urlImagem: str
    ean: str


    class Config:
        orm_mode = True