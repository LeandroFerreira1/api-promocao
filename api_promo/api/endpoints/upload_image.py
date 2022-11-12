import shutil, os, time 
from turtle import width 
from typing import List 
 
from fastapi import APIRouter, status,File, UploadFile, Depends, HTTPException, Response
from fastapi.responses import FileResponse
 
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select 
from models.usuario_model import UsuarioModel 
from models.produto_model import ProdutoModel 
from core.configs import settings 
from core.deps import get_session 
IMAGE_FOLDER_PRODUTO = os.path.join('./data/images/')
IMAGE_FOLDER_ESTABELECIMENTO = os.path.join('./data/estabelecimentos/')
IMAGE_FOLDER_USER = os.path.join('./data/users/')
IMAGE_FOLDER_TAGS = os.path.join('./data/tags/')
 
 
router = APIRouter() 
 
 
# POST Imagem Usuario 
@router.post('/user/{id}', status_code=status.HTTP_201_CREATED) 
async def post_img(id: int,file: UploadFile = File(...), db: AsyncSession = Depends(get_session)): 
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == id)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().first()
        caminhoApi = '/api/v1/upload-images/user/'
        caminhoAbsoluto = caminhoApi + str(usuario.id)
        usuario.urlImagem = caminhoAbsoluto
        await session.commit()
    ext = file.filename.rsplit('.', 1)[1].lower() 
    filename = f'{IMAGE_FOLDER_USER}{usuario.id}.{ext}'
    with open(f'{filename}', "wb") as buffer: 
        shutil.copyfileobj(file.file, buffer)

    return{"file_name": filename}

# POST Imagem produto 
@router.post('/{ean}', status_code=status.HTTP_201_CREATED) 
async def post_img(ean: int,file: UploadFile = File(...), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProdutoModel).filter(ProdutoModel.id == ean)
        result = await session.execute(query)
        produto: ProdutoModel = result.scalars().first()
        caminhoApi = '/api/v1/upload-images/'
        caminhoAbsoluto = caminhoApi + str(produto.id)
        produto.urlImagem = caminhoAbsoluto
        await session.commit()
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f'{IMAGE_FOLDER_PRODUTO}{ean}.{ext}'
    with open(f'{filename}', "wb") as buffer: 
        shutil.copyfileobj(file.file, buffer)
    return{"file_name": filename}

# GET imagem Produto
@router.get('/{ean}', status_code=status.HTTP_200_OK)
async def get_image_ean(ean: int):
    filename = f'{ean}.jpg'
    file_path = os.path.join(IMAGE_FOLDER_PRODUTO, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/jpg")
    else:
        raise HTTPException(detail='imagem não encontrada',
                            status_code=status.HTTP_404_NOT_FOUND)


# GET imagem Estabelecimento
@router.get('/estabelecimento/{id}', status_code=status.HTTP_200_OK)
async def get_image_ean(id: int):
    filename = f'{id}.png'
    file_path = os.path.join(IMAGE_FOLDER_ESTABELECIMENTO, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png")
    else:
        raise HTTPException(detail='imagem não encontrada',
                            status_code=status.HTTP_404_NOT_FOUND)

# GET imagem USER
@router.get('/user/{id}', status_code=status.HTTP_200_OK)
async def get_image_user(id: int):

    filename = f'{id}.jpg'
    file_path = os.path.join(IMAGE_FOLDER_USER, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/jpg")
    else:
        raise HTTPException(detail='imagem não encontrada',
                            status_code=status.HTTP_404_NOT_FOUND)


# GET imagem TAG
@router.get('/tags/{id}', status_code=status.HTTP_200_OK)
async def get_image_tag(id: int):

    filename = f'{id}.png'
    file_path = os.path.join(IMAGE_FOLDER_TAGS, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png")
    else:
        raise HTTPException(detail='imagem não encontrada',
                            status_code=status.HTTP_404_NOT_FOUND)