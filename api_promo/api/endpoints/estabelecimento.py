from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.estabelecimento_model import EstabelecimentoModel
from models.usuario_model import UsuarioModel
from schemas.estabelecimento_schema import EstabelecimentoSchema, EstabelecimentoSchemaPromocao
from core.deps import get_session, get_current_user


router = APIRouter()


# POST estabelecimento
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=EstabelecimentoSchema)
async def post_estabelecimento(estabelecimento: EstabelecimentoSchema, db: AsyncSession = Depends(get_session)):
    novo_estabelecimento: EstabelecimentoModel = EstabelecimentoModel(
        nome=estabelecimento.nome, telefone=estabelecimento.telefone, endereco=estabelecimento.endereco, latitude=estabelecimento.latitude, longitude=estabelecimento.longitude)

    db.add(novo_estabelecimento)
    await db.commit()

    return novo_estabelecimento


# GET estabelecimentos
@router.get('/', response_model=List[EstabelecimentoSchema])
async def get_estabelecimentos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EstabelecimentoModel)
        result = await session.execute(query)
        estabelecimentos: List[EstabelecimentoModel] = result.scalars().unique().all()

        return estabelecimentos

# GET estabelecimentos que tem promocao
@router.get('/promocoes/', response_model=List[EstabelecimentoSchemaPromocao])
async def get_estabelecimentos_promocao(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EstabelecimentoModel).where(EstabelecimentoModel.promocoes != None)
        result = await session.execute(query)
        estabelecimentos: List[EstabelecimentoModel] = result.scalars().unique().all()

        return estabelecimentos


# GET estabelecimento
@router.get('/{estabelecimento_id}', response_model=EstabelecimentoSchema, status_code=status.HTTP_200_OK)
async def get_estabelecimento(estabelecimento_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EstabelecimentoModel).filter(EstabelecimentoModel.id == estabelecimento_id)
        result = await session.execute(query)
        estabelecimento: EstabelecimentoModel = result.scalars().unique().one_or_none()

        if estabelecimento:
            return estabelecimento
        else:
            raise HTTPException(detail='Estabelecimento não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)

# GET estabelecimento
@router.get('/promocao/{estabelecimento_id}', response_model=EstabelecimentoSchemaPromocao, status_code=status.HTTP_200_OK)
async def get_estabelecimento(estabelecimento_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EstabelecimentoModel).filter(EstabelecimentoModel.id == estabelecimento_id)
        result = await session.execute(query)
        estabelecimento: EstabelecimentoModel = result.scalars().unique().one_or_none()

        if estabelecimento:
            return estabelecimento
        else:
            raise HTTPException(detail='Estabelecimento não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT estabelecimento
@router.patch('/{estabelecimento_id}', response_model=EstabelecimentoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_estabelecimento(estabelecimento_id: int, estabelecimento: EstabelecimentoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EstabelecimentoModel).filter(EstabelecimentoModel.id == estabelecimento_id)
        result = await session.execute(query)
        estabelecimento_up: EstabelecimentoModel = result.scalars().unique().one_or_none()

        if estabelecimento_up:
            patch_data = estabelecimento.dict(exclude_unset=True)
            for key, value in patch_data.items():
                setattr(estabelecimento_up, key, value)


            await session.commit()

            return estabelecimento_up
        else:
            raise HTTPException(detail='Estabelecimento não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE estabelecimento
@router.delete('/{estabelecimento_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_estabelecimento(estabelecimento_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EstabelecimentoModel).filter(EstabelecimentoModel.id == estabelecimento_id)
        result = await session.execute(query)
        estabelecimento_del: EstabelecimentoModel = result.scalars().unique().one_or_none()

        if estabelecimento_del:
            await session.delete(estabelecimento_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Estabelecimento não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
