from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api_promo.models.departamento_model import DepartamentoModel
from api_promo.models.usuario_model import UsuarioModel
from api_promo.schemas.departamento_schema import DepartamentoSchema
from api_promo.core.deps import get_session, get_current_user


router = APIRouter()


# POST Departamento
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=DepartamentoSchema)
async def post_Departamento(departamento: DepartamentoSchema, db: AsyncSession = Depends(get_session)):
    novo_departamento: DepartamentoModel = DepartamentoModel(
        nome=departamento.nome)

    db.add(novo_departamento)
    await db.commit()

    return novo_departamento


# GET Departamentos
@router.get('/', response_model=List[DepartamentoSchema])
async def get_Departamentos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(DepartamentoModel)
        result = await session.execute(query)
        departamentos: List[DepartamentoModel] = result.scalars().unique().all()

        return departamentos


# GET Departamento
@router.get('/{departamento_id}', response_model=DepartamentoSchema, status_code=status.HTTP_200_OK)
async def get_Departamento(departamento_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(DepartamentoModel).filter(DepartamentoModel.id == departamento_id)
        result = await session.execute(query)
        departamento: DepartamentoModel = result.scalars().unique().one_or_none()

        if departamento:
            return departamento
        else:
            raise HTTPException(detail='Departamento não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)



# PUT Departamento
@router.patch('/{Departamento_id}', response_model=DepartamentoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_Departamento(Departamento_id: int, departamento: DepartamentoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(DepartamentoModel).filter(DepartamentoModel.id == Departamento_id)
        result = await session.execute(query)
        departamento_up: DepartamentoModel = result.scalars().unique().one_or_none()

        if departamento_up:
            patch_data = departamento.dict(exclude_unset=True)
            for key, value in patch_data.items():
                setattr(departamento_up, key, value)


            await session.commit()

            return departamento_up
        else:
            raise HTTPException(detail='Departamento não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE Departamento
@router.delete('/{departamento_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_Departamento(departamento_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(DepartamentoModel).filter(DepartamentoModel.id == departamento_id)
        result = await session.execute(query)
        departamento_del: DepartamentoModel = result.scalars().unique().one_or_none()

        if departamento_del:
            await session.delete(departamento_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Departamento não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
