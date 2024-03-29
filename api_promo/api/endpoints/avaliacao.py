from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api_promo.models.avaliacao_model import AvaliacaoModel
from api_promo.models.usuario_model import UsuarioModel
from api_promo.schemas.avaliacao_schema import AvaliacaoSchema
from api_promo.schemas.avaliacao_schema import AvaliacaoSchemaBase, AvaliacaoPromocaoSchema, AvaliacaoSchemaAlter
from api_promo.core.deps import get_session, get_current_user

from datetime import date, datetime

router = APIRouter()

# POST avaliacao
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AvaliacaoSchemaBase)
async def post_avaliacao(avaliacao: AvaliacaoSchemaBase, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    nova_avaliacao: AvaliacaoModel = AvaliacaoModel(
        descricao=avaliacao.descricao, longitude=avaliacao.longitude, latitude=avaliacao.latitude, data_avaliacao=date.today().strftime('%d/%m/%Y'), nota=avaliacao.nota, usuario_id=usuario_logado.id, promocao_id=avaliacao.promocao_id)

    db.add(nova_avaliacao)
    await db.commit()

    return nova_avaliacao

# GET avaliacao
@router.get('/avaliacoes_usuario/', response_model=List[AvaliacaoSchema])
async def get_avaliacoes_usuario(usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AvaliacaoModel).filter(
            AvaliacaoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        avaliacoes: List[AvaliacaoModel] = result.scalars().unique().all()

        return avaliacoes

# GET avaliacao
@router.get('/avaliacoes_promocao/{promocao_id}', response_model=List[AvaliacaoPromocaoSchema], status_code=status.HTTP_200_OK)
async def get_avaliacoes_promocao(promocao_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AvaliacaoModel).filter(
            AvaliacaoModel.promocao_id == promocao_id)
        result = await session.execute(query)
        avaliacoes: List[AvaliacaoModel] = result.scalars().unique().all()
        return avaliacoes


# GET avaliacao
@router.get('/{promocao_id}', response_model=AvaliacaoSchema, status_code=status.HTTP_200_OK)
async def get_avaliacao_usuario(promocao_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(AvaliacaoModel).filter(AvaliacaoModel.promocao_id == promocao_id).filter(
            AvaliacaoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        avaliacao: AvaliacaoModel = result.scalars().unique().one_or_none()

        if avaliacao:
            return avaliacao
        else:
            raise HTTPException(detail='avaliação não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT avaliacao
@router.patch('/{promocao_id}', response_model=AvaliacaoSchemaAlter, status_code=status.HTTP_202_ACCEPTED)
async def patch_avaliacao(promocao_id: int, avaliacao: AvaliacaoSchemaAlter, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(AvaliacaoModel).filter(AvaliacaoModel.promocao_id == promocao_id).filter(
            AvaliacaoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        avaliacao_up: AvaliacaoModel = result.scalars().unique().one_or_none()

        if avaliacao_up:
            patch_data = avaliacao.dict(exclude_unset=True)
            for key, value in patch_data.items():
                setattr(avaliacao_up, key, value)
            await session.commit()

            return avaliacao_up
        else:
            raise HTTPException(detail='Promoção não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE avaliacao
@router.delete('/{promocao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_avaliacao(promocao_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(AvaliacaoModel).filter(AvaliacaoModel.promocao_id == promocao_id).filter(
            AvaliacaoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        avaliacao_del: AvaliacaoModel = result.scalars().unique().one_or_none()

        if avaliacao_del:
            await session.delete(avaliacao_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Promoção não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)
