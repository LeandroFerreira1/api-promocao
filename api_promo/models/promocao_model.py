from sqlalchemy import Integer, String, Column, Date, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class PromocaoModel(settings.DBBaseModel):
    __tablename__ = 'promocao'

    id = Column(Integer, primary_key=True, autoincrement=True)
    valor_original = Column(String(256), nullable=True)
    valor_promocional = Column(String(256), nullable=True)
    data_validade = Column(String(256), nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    estabelecimento_id = Column(Integer, ForeignKey('estabelecimento.id'))
    produto_id = Column(Integer, ForeignKey('produto.id'))
    criador = relationship("UsuarioModel", back_populates='promocoes', lazy='joined')
    produto = relationship("ProdutoModel", back_populates="promocoes", lazy='joined')
    estabelecimento = relationship("EstabelecimentoModel", back_populates="promocoes", lazy='joined')
    avaliacoes = relationship("AvaliacaoModel", back_populates="promocao")

