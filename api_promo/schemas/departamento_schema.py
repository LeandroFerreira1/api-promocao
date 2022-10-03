from typing import Optional

from pydantic import BaseModel

class DepartamentoSchema(BaseModel):
    id: Optional[int] = None
    nome: str

    class Config:
        orm_mode = True
