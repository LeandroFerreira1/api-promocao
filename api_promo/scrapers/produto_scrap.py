import requests
from bs4 import BeautifulSoup
from models.produto_model import ProdutoModel

cabecalho = {'user-agent' : 'Mozzila/5.0'}
base_url = 'https://cosmos.bluesoft.com.br/products/'
image_url = 'https://cdn-cosmos.bluesoft.com.br/products/'


def buscar_produto(ean: str) -> ProdutoModel:

    url = base_url + ean
    url_image = image_url + ean

    resposta = requests.get(url, headers=cabecalho)
    sopa = resposta.text
    sopa_bonita = BeautifulSoup(sopa, 'html.parser')

    ean = sopa_bonita.find_all(id='product_gtin')
    ean_produto = ean[0].contents[0].text

    description = sopa_bonita.find_all(id='product_description')
    description_produto = description[0].contents[0].text

    #ncm = sopa_bonita.find_all('span', {'class':'ncm-name'})
    #ncm_produto = ncm[0].contents[1].text

    marca = sopa_bonita.find_all('span', {'class':'brand-name'})
    marca_produto = marca[0].contents[1].text

    caminho = './data/images/'
    imagename = caminho + ean_produto + '.jpg'

    caminhoApi = '/api/v1/upload-images/'
    caminhoAbsoluto = caminhoApi + ean_produto

    with open(imagename, 'wb') as f:
        f.write(requests.get(url_image, headers=cabecalho).content)
    
    produto = ProdutoModel

    produto.nome = description_produto
    produto.marca = marca_produto
    produto.tipo = ""
    produto.departamento = ""
    produto.urlImagem = caminhoAbsoluto
    produto.ean = ean_produto

    return (produto)