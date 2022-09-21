from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.usuario_estabelecimento_model import UsuarioEstabelecimentoModel
from schemas.usuario_estabelecimento_schema import UsuarioEstabelecimentoSchemaBase, UsuarioEstabelecimentoSchemaCreate, UsuarioEstabelecimentoSchemaUp, UsuarioEstabelecimentoSchemaEstabelecimentos
from core.deps import get_session, get_current_user_estabelecimento
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso


router = APIRouter()


# GET Logado
@router.get('/logado', response_model=UsuarioEstabelecimentoSchemaBase)
def get_logado(usuario_estabelecimento_logado: UsuarioEstabelecimentoModel = Depends(get_current_user_estabelecimento)):
    return usuario_estabelecimento_logado


# POST / Signup
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioEstabelecimentoSchemaBase)
async def post_usuario_estabelecimento(usuario_estabelecimento: UsuarioEstabelecimentoSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario_estabelecimento: UsuarioEstabelecimentoModel = UsuarioEstabelecimentoModel(nome=usuario_estabelecimento.nome, sobrenome=usuario_estabelecimento.sobrenome,
                                              email=usuario_estabelecimento.email, senha=gerar_hash_senha(usuario_estabelecimento.senha))
    async with db as session:
        try:
            session.add(novo_usuario_estabelecimento)
            await session.commit()

            return novo_usuario_estabelecimento
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe um usuário com este email cadastrado.')


# GET UsuarioEstabelecimentos
@router.get('/', response_model=List[UsuarioEstabelecimentoSchemaBase])
async def get_usuario_estabelecimentos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioEstabelecimentoModel)
        result = await session.execute(query)
        usuario_estabelecimentos: List[UsuarioEstabelecimentoSchemaBase] = result.scalars().unique().all()

        return usuario_estabelecimentos


# GET UsuarioEstabelecimento
@router.get('/{usuario_estabelecimento_id}', response_model=UsuarioEstabelecimentoSchemaEstabelecimentos, status_code=status.HTTP_200_OK)
async def get_usuario_estabelecimento(usuario_estabelecimento_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioEstabelecimentoModel).filter(UsuarioEstabelecimentoModel.id == usuario_estabelecimento_id)
        result = await session.execute(query)
        usuario_estabelecimento: UsuarioEstabelecimentoSchemaEstabelecimentos = result.scalars().unique().one_or_none()

        if usuario_estabelecimento:
            return usuario_estabelecimento
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT UsuarioEstabelecimento
@router.patch('/{usuario_estabelecimento_id}', response_model=UsuarioEstabelecimentoSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario_estabelecimento(usuario_estabelecimento_id: int, usuario_estabelecimento: UsuarioEstabelecimentoSchemaUp, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioEstabelecimentoModel).filter(UsuarioEstabelecimentoModel.id == usuario_estabelecimento_id)
        result = await session.execute(query)
        usuario_estabelecimento_up: UsuarioEstabelecimentoSchemaBase = result.scalars().unique().one_or_none()

        if usuario_estabelecimento_up:
            if usuario_estabelecimento.nome:
                usuario_estabelecimento_up.nome = usuario_estabelecimento.nome
            if usuario_estabelecimento.sobrenome:
                usuario_estabelecimento_up.sobrenome = usuario_estabelecimento.sobrenome
            if usuario_estabelecimento.email:
                usuario_estabelecimento_up.email = usuario_estabelecimento.email
            if usuario_estabelecimento.senha:
                usuario_estabelecimento_up.senha = gerar_hash_senha(usuario_estabelecimento.senha)

            await session.commit()

            return usuario_estabelecimento_up
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE usuario_estabelecimento
@router.delete('/{usuario_estabelecimento_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario_estabelecimento(usuario_estabelecimento_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioEstabelecimentoModel).filter(UsuarioEstabelecimentoModel.id == usuario_estabelecimento_id)
        result = await session.execute(query)
        usuario_estabelecimento_del: UsuarioEstabelecimentoSchemaEstabelecimentos = result.scalars().unique().one_or_none()

        if usuario_estabelecimento_del:
            await session.delete(usuario_estabelecimento_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario_estabelecimento = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario_estabelecimento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos.')

    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario_estabelecimento.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)
