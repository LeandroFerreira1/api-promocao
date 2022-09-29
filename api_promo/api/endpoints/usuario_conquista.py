from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_conquista_model import UsuarioConquistaModel
from models.usuario_model import UsuarioModel
from schemas.usuario_conquista_schema import UsuarioConquistaSchema
from schemas.usuario_conquista_schema import UsuarioConquistaSchemaBase
from core.deps import get_session, get_current_user


router = APIRouter()

# POST usuario_conquista
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UsuarioConquistaSchemaBase)
async def post_usuario_conquista(usuario_conquista: UsuarioConquistaSchemaBase, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    nova_usuario_conquista: UsuarioConquistaModel = UsuarioConquistaModel(
        data_conquista=usuario_conquista.data_canquista, usuario_id=usuario_logado.id, conquista_id=usuario_conquista.conquista_id)

    db.add(nova_usuario_conquista)
    await db.commit()

    return nova_usuario_conquista

# GET usuario_conquista
@router.get('/usuario_conquistas/', response_model=List[UsuarioConquistaSchema])
async def get_usuario_conquistas_usuario(usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioConquistaModel).filter(
            UsuarioConquistaModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        usuario_conquistas: List[UsuarioConquistaModel] = result.scalars().unique().all()

        return usuario_conquistas


# GET usuario_conquista
@router.get('/{promocao_id}', response_model=UsuarioConquistaSchema, status_code=status.HTTP_200_OK)
async def get_usuario_conquista_usuario(promocao_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioConquistaModel).filter(UsuarioConquistaModel.promocao_id == promocao_id).filter(
            UsuarioConquistaModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        usuario_conquista: UsuarioConquistaModel = result.scalars().unique().one_or_none()

        if usuario_conquista:
            return usuario_conquista
        else:
            raise HTTPException(detail='Promoção não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT usuario_conquista
@router.patch('/{promocao_id}', response_model=UsuarioConquistaSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def patch_usuario_conquista(promocao_id: int, usuario_conquista: UsuarioConquistaSchemaBase, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioConquistaModel).filter(UsuarioConquistaModel.promocao_id == promocao_id).filter(
            UsuarioConquistaModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        usuario_conquista_up: UsuarioConquistaModel = result.scalars().unique().one_or_none()

        if usuario_conquista_up:
            patch_data = usuario_conquista.dict(exclude_unset=True)
            for key, value in patch_data.items():
                setattr(usuario_conquista_up, key, value)
            await session.commit()

            return usuario_conquista_up
        else:
            raise HTTPException(detail='Promoção não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE usuario_conquista
@router.delete('/{promocao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario_conquista(promocao_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioConquistaModel).filter(UsuarioConquistaModel.promocao_id == promocao_id).filter(
            UsuarioConquistaModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        usuario_conquista_del: UsuarioConquistaModel = result.scalars().unique().one_or_none()

        if usuario_conquista_del:
            await session.delete(usuario_conquista_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Promoção não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)