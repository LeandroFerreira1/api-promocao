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
IMAGE_FOLDER = os.path.join('./data/images/')
UPLOAD_FOLDER = os.path.join('./data/')
 
 
router = APIRouter() 
 
 
# POST Imagem produto 
@router.post('/', status_code=status.HTTP_201_CREATED) 
async def post_img(file: UploadFile = File(...)): 
 
    ext = file.filename.rsplit('.', 1)[1].lower() 
    os.mkdir("./uploads/img/4") 
    filename = f'{UPLOAD_FOLDER}/4/Produto{1}-{int(time.time())}.{ext}' 
    print(filename) 
    with open(f'{filename}', "wb") as buffer: 
        shutil.copyfileobj(file.file, buffer) 
    return{"file_name": filename}

# POST Imagem produto 
@router.post('/{ean}', status_code=status.HTTP_201_CREATED) 
async def post_img(ean: str,file: UploadFile = File(...), db: AsyncSession = Depends(get_session)):
 
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f'{IMAGE_FOLDER}{ean}.{ext}'
    with open(f'{filename}', "wb") as buffer: 
        shutil.copyfileobj(file.file, buffer)
    novo_produto: ProdutoModel = ProdutoModel(
        urlImagem=filename, id=int(ean), nome ="")
    db.add(novo_produto)
    await db.commit()
    
    return{"file_name": filename}

# GET imagem Produto
@router.get('/{ean}', status_code=status.HTTP_200_OK)
async def get_image_ean(ean: int):
    filename = f'{ean}.jpg'
    file_path = os.path.join(IMAGE_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/jpg")
    else:
        raise HTTPException(detail='imagem não encontrada',
                            status_code=status.HTTP_404_NOT_FOUND)