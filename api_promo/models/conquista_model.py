from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings


class ConquistaModel(settings.DBBaseModel):
    __tablename__ = 'conquista'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256), nullable=False)
    valor = Column(Integer, nullable=False)
    urlimagem = Column(String(256), nullable=True)
    usuarios = relationship(
        "UsuarioConquistaModel",
        cascade="all,delete-orphan",
        back_populates="conquistas",
        uselist=True,
        lazy="joined"
    )