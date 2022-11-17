from sqlalchemy import Integer, String, Column, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from api_promo.core.configs import settings


class CurtidaModel(settings.DBBaseModel):
    __tablename__ = 'curtida'

    usuario_id = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    promocao_id = Column(Integer, ForeignKey('promocao.id'), primary_key=True)
    criador = relationship("UsuarioModel", back_populates='curtidas', lazy='joined')
    promocao = relationship("PromocaoModel", back_populates="curtidas", lazy='joined')