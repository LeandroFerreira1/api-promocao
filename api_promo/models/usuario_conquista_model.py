from sqlalchemy import Integer, String, Column, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class UsuarioConquistaModel(settings.DBBaseModel):
    __tablename__ = 'usuario_conquista'

    usuario_id = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    conquista_id = Column(Integer, ForeignKey('conquista.id'), primary_key=True)
    data_canquista = Column(Date, nullable=False)
    criador = relationship("UsuarioModel", back_populates='conquistas', lazy='joined')
    conquistas = relationship("ConquistaModel", back_populates="usuarios", lazy='joined')
    
