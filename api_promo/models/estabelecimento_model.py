from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class EstabelecimentoModel(settings.DBBaseModel):
    __tablename__ = 'estabelecimento'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256), nullable=False)
    telefone = Column(String(256), nullable=True)
    endereco = Column(String(256), nullable=True)
    latitude = Column(String(256), nullable=False)
    longitude = Column(String(256), nullable=False)
    urlImagem = Column(String(256), nullable=True)
    usuario_estabelecimento_id = Column(Integer, ForeignKey('usuario_estabelecimento.id'), nullable=True)
    promocoes = relationship("PromocaoModel", back_populates="estabelecimento", lazy='subquery')