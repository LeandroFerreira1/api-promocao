import imp
from fastapi import APIRouter

from api.endpoints import promocao
from api.endpoints import usuario
from api.endpoints import produto
from api.endpoints import estabelecimento
from api.endpoints import usuario_estabelecimento
from api.endpoints import usuario_conquista
from api.endpoints import conquista
from api.endpoints import avaliacao
from api.endpoints import upload_image
from api.endpoints import departamento

api_router = APIRouter()

api_router.include_router(
    promocao.router, prefix='/promocoes', tags=['promocoes'])
api_router.include_router(
    avaliacao.router, prefix='/avaliacoes', tags=['avaliacoes'])
api_router.include_router(
    estabelecimento.router, prefix='/estabelecimentos', tags=['estabelecimentos'])
api_router.include_router(
    produto.router, prefix='/produtos', tags=['produtos'])
api_router.include_router(
    departamento.router, prefix='/departamentos', tags=['departamentos'])
api_router.include_router(
    conquista.router, prefix='/conquistas', tags=['conquistas'])
api_router.include_router(
    usuario_conquista.router, prefix='/usuario-conquistas', tags=['usuario-conquistas'])
api_router.include_router(
    usuario.router, prefix='/usuarios', tags=['usuarios'])
api_router.include_router(
    upload_image.router, prefix='/upload-images', tags=['upload-images'])
api_router.include_router(
    usuario_estabelecimento.router, prefix='/usuarios-estabelecimentos', tags=['usuarios-estabelecimentos'])