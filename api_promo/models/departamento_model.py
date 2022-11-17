from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from api_promo.core.configs import settings


class DepartamentoModel(settings.DBBaseModel):
    __tablename__ = 'departamento'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(512), nullable=False)
    produtos = relationship("ProdutoModel", back_populates="departamentos", lazy='subquery')