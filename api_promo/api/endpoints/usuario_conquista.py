from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api_promo.models.usuario_conquista_model import UsuarioConquistaModel
from api_promo.models.usuario_model import UsuarioModel
from api_promo.schemas.usuario_conquista_schema import UsuarioConquistaSchema
from api_promo.schemas.usuario_conquista_schema import UsuarioConquistaSchemaBase
from api_promo.core.deps import get_session, get_current_user


router = APIRouter()

# POST usuario_conquista
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UsuarioConquistaSchemaBase)
async def post_usuario_conquista(usuario_conquista: UsuarioConquistaSchemaBase, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
<<<<<<< Updated upstream
    nova_usuario_conquista: UsuarioConquistaModel = UsuarioConquistaModel(
        usuario_id=usuario_logado.id, conquista_id=usuario_conquista.conquista_id)
=======
    nova_usuario_conquista: UsuarioConquistaModel = UsuarioConquistaModel(usuario_id=usuario_logado.id, conquista_id=usuario_conquista.conquista_id)
>>>>>>> Stashed changes

    db.add(nova_usuario_conquista)
    await db.commit()

    return nova_usuario_conquista

# GET usuario_conquista
@router.get('/', response_model=List[UsuarioConquistaSchema])
async def get_usuario_conquistas_usuario(usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioConquistaModel).filter(
            UsuarioConquistaModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        usuario_conquistas: List[UsuarioConquistaModel] = result.scalars().unique().all()

        return usuario_conquistas


# GET usuario_conquista
@router.get('/{usuario_id}', response_model=List[UsuarioConquistaSchema])
async def get_usuario_conquista_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioConquistaModel).filter(UsuarioConquistaModel.usuario_id == usuario_id)
        result = await session.execute(query)
        usuario_conquistas: List[UsuarioConquistaModel] = result.scalars().unique().all()

        return usuario_conquistas



# DELETE usuario_conquista
@router.delete('/{conquista_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario_conquista(conquista_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioConquistaModel).filter(UsuarioConquistaModel.conquista_id == conquista_id).filter(
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
