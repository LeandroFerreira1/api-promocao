from sqlalchemy import Integer, String, Column, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from core.configs import settings


class ProdutoModel(settings.DBBaseModel):
    __tablename__ = 'produto'

    id = Column(BigInteger, primary_key=True)
    nome = Column(String(256), nullable=False)
    tipo = Column(String(512), nullable=True)
    marca = Column(String(256), nullable=True)
    departamento = Column(String(256), nullable=True)
    urlImagem = Column(String(256), nullable=True)
    promocoes = relationship("PromocaoModel", back_populates="produto")
    