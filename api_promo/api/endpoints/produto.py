from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.produto_model import ProdutoModel
from schemas.produto_schema import ProdutoSchema
from core.deps import get_session
from scrapers.produto_scrap import buscar_produto


router = APIRouter()


# POST produto
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProdutoSchema)
async def post_produto(produto: ProdutoSchema, db: AsyncSession = Depends(get_session)):
    novo_produto: ProdutoModel = ProdutoModel(
        id=produto.id, nome=produto.nome, tipo=produto.tipo, marca=produto.marca, departamento=produto.departamento, urlImagem=produto.urlImagem)

    db.add(novo_produto)
    await db.commit()

    return novo_produto

# POST produto
@router.post('/ean/{ean}', status_code=status.HTTP_201_CREATED)
async def post_produto_ean(ean: int, db: AsyncSession = Depends(get_session)):
    produtoEan = buscar_produto(ean)
    novo_produto: ProdutoModel = ProdutoModel(
        nome=produtoEan.nome, marca=produtoEan.marca, urlImagem=produtoEan.urlImagem, id=produtoEan.id)
    db.add(novo_produto)
    await db.commit()
    return novo_produto

# GET produtos
@router.get('/', response_model=List[ProdutoSchema])
async def get_produtos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProdutoModel)
        result = await session.execute(query)
        produtos: List[ProdutoModel] = result.scalars().unique().all()

        return produtos


# GET produto
@router.get('/{produto_id}', response_model=List[ProdutoSchema], status_code=status.HTTP_200_OK)
async def get_produto(produto_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProdutoModel).filter(ProdutoModel.id == produto_id)
        result = await session.execute(query)
        produto: List[ProdutoModel] = result.scalars().unique().all()

        if produto:
            return produto
        else:
            raise HTTPException(detail='Produto não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT produto
@router.patch('/{produto_id}', response_model=ProdutoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_produto(produto_id: int, produto: ProdutoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProdutoModel).filter(ProdutoModel.id == produto_id)
        result = await session.execute(query)
        produto_up: ProdutoModel = result.scalars().unique().one_or_none()

        if produto_up:
            if produto.nome:
                produto_up.nome = produto.nome
            if produto.tipo:
                produto_up.tipo = produto.tipo
            if produto.marca:
                produto_up.marca = produto.marca
            if produto.departamento:
                produto_up.departamento = produto.departamento
            if produto.urlImagem:
                produto_up.urlImagem = produto.urlImagem

            await session.commit()

            return produto_up
        else:
            raise HTTPException(detail='Produto não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE produto
@router.delete('/{produto_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(produto_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProdutoModel).filter(ProdutoModel.id == produto_id)
        result = await session.execute(query)
        produto_del: ProdutoModel = result.scalars().unique().one_or_none()

        if produto_del:
            await session.delete(produto_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Produto não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
