# 🛍️ API Promoção - Sistema Colaborativo de Promoções

Uma API REST completa desenvolvida em Python com FastAPI para um sistema colaborativo de divulgação de promoções. O projeto permite que usuários compartilhem promoções de produtos em estabelecimentos, avaliem ofertas e interajam através de um sistema de pontuação e conquistas.

## 🚀 Funcionalidades Principais

### 👥 Gestão de Usuários
- Cadastro e autenticação de usuários
- Sistema de pontuação baseado em atividades
- Perfis com imagens personalizadas
- Sistema de conquistas e gamificação

### 🏪 Estabelecimentos
- Cadastro de estabelecimentos com localização (latitude/longitude)
- Gestão de informações (nome, telefone, endereço)
- Associação com usuários responsáveis
- Upload de imagens dos estabelecimentos

### 📦 Produtos
- Busca automática de produtos por código EAN
- Web scraping para obter informações detalhadas
- Organização por departamentos
- Gestão de marcas e categorias

### 🎯 Promoções
- Criação colaborativa de promoções
- Comparação de preços (valor original vs promocional)
- Data de validade das ofertas
- Associação produto-estabelecimento-usuário

### 💬 Interações Sociais
- Sistema de avaliações das promoções
- Curtidas em promoções
- Comentários e feedback da comunidade

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Banco de dados relacional
- **Pydantic** - Validação de dados
- **JWT** - Autenticação e autorização

### Infraestrutura
- **Docker & Docker Compose** - Containerização
- **Poetry** - Gerenciamento de dependências
- **Uvicorn** - Servidor ASGI

### Ferramentas Adicionais
- **BeautifulSoup4** - Web scraping de produtos
- **Requests** - Cliente HTTP
- **Passlib & Bcrypt** - Criptografia de senhas
- **Python-Jose** - Manipulação de tokens JWT

## 📋 Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Poetry (opcional, mas recomendado)

## 🔧 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone
cd api-promocao
```

### 2. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
PG_USER=postgres
PG_PASS=sua_senha
PG_DB=promocao
JWT_SECRET=seu_jwt_secret_aqui
```

### 3. Inicie os serviços com Docker
```bash
docker-compose up -d
```

### 4. Instale as dependências (desenvolvimento local)
```bash
# Com Poetry
poetry install

# Ou com pip
pip install -r requirements.txt
```

### 5. Execute as migrações do banco
```bash
python api_promo/criar_tabelas.py
```

### 6. Inicie a aplicação
```bash
# Desenvolvimento
uvicorn api_promo.main:app --reload

# Produção com Docker
docker build -t api-promo .
docker run -p 8000:8000 api-promo
```

## 📚 Documentação da API

Após iniciar a aplicação, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Principais Endpoints

#### Usuários
- `POST /api/v1/usuarios` - Cadastro de usuário
- `GET /api/v1/usuarios` - Listar usuários
- `PUT /api/v1/usuarios/{id}` - Atualizar usuário

#### Promoções
- `POST /api/v1/promocoes` - Criar promoção
- `GET /api/v1/promocoes` - Listar promoções
- `GET /api/v1/promocoes/{id}` - Detalhes da promoção

#### Estabelecimentos
- `POST /api/v1/estabelecimentos` - Cadastrar estabelecimento
- `GET /api/v1/estabelecimentos` - Listar estabelecimentos

#### Produtos
- `POST /api/v1/produtos` - Cadastrar produto
- `GET /api/v1/produtos` - Buscar produtos

## 🗄️ Estrutura do Banco de Dados

O sistema utiliza as seguintes entidades principais:

- **Usuario** - Dados dos usuários e pontuação
- **Estabelecimento** - Lojas e pontos de venda
- **Produto** - Catálogo de produtos com EAN
- **Promocao** - Ofertas criadas pelos usuários
- **Avaliacao** - Avaliações das promoções
- **Curtida** - Sistema de likes
- **Conquista** - Sistema de gamificação

## 🧪 Testes

Execute os testes com:
```bash
pytest tests/
```

## 📁 Estrutura do Projeto

```
api_promo/
├── api/                 # Rotas e endpoints
├── core/               # Configurações e autenticação
├── models/             # Modelos SQLAlchemy
├── schemas/            # Schemas Pydantic
├── scrapers/           # Web scraping de produtos
└── data/               # Armazenamento de arquivos
```

## 🚀 Deploy

### Docker
```bash
docker build -t api-promo .
docker run -p 8000:8000 api-promo
```

### Variáveis de Ambiente para Produção
- `DB_URL` - URL de conexão com PostgreSQL
- `JWT_SECRET` - Chave secreta para JWT
- `API_V1_STR` - Prefixo da API (padrão: /api/v1)

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!
