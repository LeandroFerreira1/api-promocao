from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api_promo.models.conquista_model import ConquistaModel
from api_promo.schemas.conquista_schema import ConquistaSchema, ConquistaSchemaAlter
from api_promo.core.deps import get_session


router = APIRouter()


# POST conquista
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ConquistaSchema)
async def post_conquista(conquista: ConquistaSchema, db: AsyncSession = Depends(get_session)):
    novo_conquista: ConquistaModel = ConquistaModel(nome=conquista.nome, valor=conquista.valor, urlimagem=conquista.urlimagem)
    db.add(novo_conquista)
    await db.commit()

    return novo_conquista


# GET conquistas
@router.get('/', response_model=List[ConquistaSchema])
async def get_conquistas(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ConquistaModel)
        result = await session.execute(query)
        conquistas: List[ConquistaModel] = result.scalars().unique().all()

        return conquistas


# GET conquista
@router.get('/{conquista_id}', response_model=ConquistaSchema, status_code=status.HTTP_200_OK)
async def get_conquista(conquista_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ConquistaModel).filter(ConquistaModel.id == conquista_id)
        result = await session.execute(query)
        conquista: ConquistaModel = result.scalars().unique().one_or_none()

        if conquista:
            return conquista
        else:
            raise HTTPException(detail='Conquista não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT conquista
@router.patch('/{conquista_id}', response_model=ConquistaSchemaAlter, status_code=status.HTTP_202_ACCEPTED)
async def put_conquista(conquista_id: int, conquista: ConquistaSchemaAlter, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ConquistaModel).filter(ConquistaModel.id == conquista_id)
        result = await session.execute(query)
        conquista_up: ConquistaModel = result.scalars().unique().one_or_none()

        if conquista_up:
            patch_data = conquista.dict(exclude_unset=True)
            for key, value in patch_data.items():
                setattr(conquista_up, key, value)
                
            await session.commit()

            return conquista_up
        else:
            raise HTTPException(detail='Conquista não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE conquista
@router.delete('/{conquista_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_conquista(conquista_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ConquistaModel).filter(ConquistaModel.id == conquista_id)
        result = await session.execute(query)
        conquista_del: ConquistaModel = result.scalars().unique().one_or_none()

        if conquista_del:
            await session.delete(conquista_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Conquista não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
