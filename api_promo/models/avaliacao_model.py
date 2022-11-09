from sqlalchemy import Integer, String, Column, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class AvaliacaoModel(settings.DBBaseModel):
    __tablename__ = 'avaliacao'

    usuario_id = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    promocao_id = Column(Integer, ForeignKey('promocao.id'), primary_key=True)
    descricao = Column(String(512), nullable=True)
    longitude = Column(String(256), nullable=True)
    latitude = Column(String(256), nullable=True)
    nota = Column(Integer, nullable=False)
    data_avaliacao = Column(String(256), nullable=False)
    criador = relationship("UsuarioModel", back_populates='avaliacoes', lazy='joined')
    promocao = relationship("PromocaoModel", back_populates="avaliacoes", lazy='joined')