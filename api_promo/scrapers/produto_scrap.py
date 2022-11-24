import os

import requests
from bs4 import BeautifulSoup

from api_promo.models.produto_model import ProdutoModel

dirname = os.path.dirname(__file__)

IMAGE_FOLDER_PRODUTO = os.path.join(dirname, '../data/images/')


cabecalho = {'user-agent' : 'Mozzila/5.0'}
base_url = 'https://cosmos.bluesoft.com.br/products/'
image_url = 'https://cdn-cosmos.bluesoft.com.br/products/'


def buscar_produto(ean: str) -> ProdutoModel:
    try:
        url = base_url + ean
        url_image = image_url + ean

        resposta = requests.get(url, headers=cabecalho)
        sopa = resposta.text
        sopa_bonita = BeautifulSoup(sopa, 'html.parser')

        ean2 = sopa_bonita.find(id='product_gtin')
        ean_produto = ean2.text.strip()

        description = sopa_bonita.find(id='product_description')
        description_produto = description.text.strip()

        #ncm = sopa_bonita.find_all('span', {'class':'ncm-name'})
        #ncm_produto = ncm[0].contents[1].text

        marca = sopa_bonita.find('span', {'class':'brand-name'})
        marca_produto = marca.text.strip()

        filename = f'{IMAGE_FOLDER_PRODUTO}{ean_produto}.jpg'
        caminhoApi = '/api/v1/upload-images/'
        caminhoAbsoluto = caminhoApi + ean_produto
        
        r = requests.get(url_image, headers=cabecalho)
        if (r.status_code == requests.codes.ok):
            with open(f'{filename}', 'wb') as f:
             f.write(r.content)
        else:
            return None
        
        produto = ProdutoModel

        produto.ean = ean_produto
        produto.nome = description_produto
        produto.marca = marca_produto
        produto.tipo = ""
        produto.departamento = ""
        produto.urlImagem = caminhoAbsoluto
   

        return (produto)
    except:
        return None

