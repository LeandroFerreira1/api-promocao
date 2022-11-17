from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api_promo.models.curtida_model import CurtidaModel
from api_promo.schemas.curtida_schema import CurtidaSchemaBase, CurtidaPromocaoSchema
from api_promo.core.deps import get_session
from api_promo.models.usuario_model import UsuarioModel
from api_promo.core.deps import get_session, get_current_user


router = APIRouter()

# POST curtida
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CurtidaSchemaBase)
async def post_curtida(curtida: CurtidaSchemaBase, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    nova_curtida: CurtidaModel = CurtidaModel(usuario_id=usuario_logado.id, promocao_id=curtida.promocao_id)

    db.add(nova_curtida)
    await db.commit()

    return nova_curtida

# GET curtida por promocao
@router.get('/curtidas_promocao/{promocao_id}', response_model=List[CurtidaPromocaoSchema], status_code=status.HTTP_200_OK)
async def get_curtidas_promocao(promocao_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CurtidaModel).filter(
            CurtidaModel.promocao_id == promocao_id)
        result = await session.execute(query)
        curtidas: List[CurtidaModel] = result.scalars().unique().all()
        return curtidas

# GET curtida
@router.get('/curtida_usuario/{promocao_id}', response_model=CurtidaPromocaoSchema, status_code=status.HTTP_200_OK)
async def get_curtida_usuario(promocao_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(CurtidaModel).filter(CurtidaModel.promocao_id == promocao_id).filter(
            CurtidaModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        curtida: CurtidaModel = result.scalars().first()

        if curtida:
            return curtida
        else:
            raise HTTPException(detail='Curtida não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE curtida
@router.delete('/{promocao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curtida(promocao_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(CurtidaModel).filter(CurtidaModel.promocao_id == promocao_id).filter(
            CurtidaModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        curtida_del: CurtidaModel = result.scalars().unique().one_or_none()

        if curtida_del:
            await session.delete(curtida_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Promoção não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)