from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.promocao_model import PromocaoModel
from models.usuario_model import UsuarioModel
from schemas.promocao_schema import PromocaoSchema
from schemas.promocao_schema import PromocaoSchemaBase
from core.deps import get_session, get_current_user


router = APIRouter()


# POST promocao
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PromocaoSchemaBase)
async def post_promocao(promocao: PromocaoSchemaBase, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    nova_promocao: PromocaoModel = PromocaoModel(
        valor_original=promocao.valor_original, valor_promocional=promocao.valor_promocional, data_validade=promocao.data_validade, usuario_id=usuario_logado.id, estabelecimento_id=promocao.estabelecimento_id, produto_id=promocao.produto_id)

    db.add(nova_promocao)
    await db.commit()

    return nova_promocao

# GET promocao
@router.get('/', response_model=List[PromocaoSchema])
async def get_promocoes(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PromocaoModel)
        result = await session.execute(query)
        promocoes: List[PromocaoModel] = result.scalars().unique().all()

        return promocoes


# GET promocao
@router.get('/{promocao_id}', response_model=PromocaoSchema, status_code=status.HTTP_200_OK)
async def get_promocao(promocao_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PromocaoModel).filter(PromocaoModel.id == promocao_id)
        result = await session.execute(query)
        promocao: PromocaoModel = result.scalars().unique().one_or_none()

        if promocao:
            return promocao
        else:
            raise HTTPException(detail='Promoção não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)



# PUT promocao
@router.patch('/{promocao_id}', response_model=PromocaoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_promocao(promocao_id: int, promocao: PromocaoSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(PromocaoModel).filter(PromocaoModel.id == promocao_id).filter(
            PromocaoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        promocao_up: PromocaoModel = result.scalars().unique().one_or_none()

        if promocao_up:
            if promocao.valor_original:
                promocao_up.valor_original = promocao.valor_original
            if promocao.valor_promocional:
                promocao_up.valor_promocional = promocao.valor_promocional
            if promocao.data_validade:
                promocao_up.data_validade = promocao.data_validade
            if usuario_logado.id != promocao_up.usuario_id:
                promocao_up.usuario_id = usuario_logado.id

            await session.commit()

            return promocao_up
        else:
            raise HTTPException(detail='Promoção não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE promocao
@router.delete('/{promocao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_promocao(promocao_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(PromocaoModel).filter(PromocaoModel.id == promocao_id).filter(
            PromocaoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        promocao_del: PromocaoModel = result.scalars().unique().one_or_none()

        if promocao_del:
            await session.delete(promocao_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Promoção não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)