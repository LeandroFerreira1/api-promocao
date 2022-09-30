from typing import Optional

from pydantic import BaseModel
from typing import Optional
from typing import List
from sqlalchemy import BigInteger


class ProdutoSchema(BaseModel):
    id: int
    nome: str
    tipo: Optional[str]
    marca: Optional[str]
    departamento: Optional[str]
    urlImagem: str

    class Config:
        orm_mode = True
