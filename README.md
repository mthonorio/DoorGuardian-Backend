# DoorGuardian Backend API

Uma API RESTful moderna desenvolvida em **FastAPI** para gerenciamento de acessos de portaria inteligente, com **Supabase** como backend de banco de dados e armazenamento.

## 📋 Funcionalidades

- **Registro de Acessos**: Registrar novos acessos com data, status e imagem opcional
- **Histórico de Acessos**: Consultar histórico com paginação e filtros avançados
- **Gerenciamento de Imagens**: Upload e armazenamento na nuvem via Supabase Storage
- **Exclusão de Registros**: Remover registros específicos do histórico
- **Documentação Interativa**: Swagger UI e ReDoc automaticamente gerados
- **Validação de Dados**: Validação robusta com Pydantic
- **Performance**: API assíncrona de alta performance com FastAPI

## 🏗️ Arquitetura

O projeto segue as melhores práticas de desenvolvimento FastAPI com Supabase:

```
DoorGuardian_backend/
├── app/
│   ├── __init__.py
│   ├── app_factory.py          # Factory pattern para criação da app FastAPI
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config.py           # Configurações com Pydantic Settings
│   │   └── extensions.py       # Cliente Supabase
│   ├── models/
│   │   ├── __init__.py
│   │   ├── access.py          # Modelos Pydantic para acesso
│   │   └── image.py           # Modelos Pydantic para imagem
│   ├── routes/
│   │   ├── __init__.py
│   │   └── access_routes.py   # Rotas FastAPI
│   ├── services/
│   │   ├── __init__.py
│   │   └── database_service.py # Serviços de banco Supabase
│   └── utils/
│       ├── __init__.py
│       └── file_utils.py      # Utilitários para upload
├── database/
│   └── schema.sql             # Schema SQL para Supabase
├── app.py                     # Ponto de entrada da aplicação
├── requirements.txt           # Dependências Python
├── .env.example              # Exemplo de variáveis de ambiente
├── .gitignore               # Arquivos ignorados pelo Git
└── README.md                # Este arquivo
```

## 🔧 Stack Tecnológica

- **FastAPI**: Framework web moderno e de alta performance
- **Supabase**: Backend-as-a-Service com PostgreSQL
- **Pydantic**: Validação de dados e serialização
- **Uvicorn**: Servidor ASGI para aplicações assíncronas
- **Pillow**: Processamento de imagens
- **PostgreSQL**: Banco de dados relacional (via Supabase)

## 🚀 Instalação

### Pré-requisitos

- Python 3.8+
- Conta no Supabase (gratuita disponível)
- pip (gerenciador de pacotes Python)

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd DoorGuardian_backend
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Supabase

1. Acesse [supabase.com](https://supabase.com) e crie uma conta
2. Crie um novo projeto
3. Anote a **URL** e **anon key** do seu projeto
4. Acesse o **SQL Editor** no painel do Supabase
5. Execute o script `database/schema.sql` para criar as tabelas
6. No **Storage**, crie um bucket chamado `images` e configure como público

### 5. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e configure suas variáveis:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
# FastAPI Environment
ENVIRONMENT=development
DEBUG=True

# Supabase Configuration
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your-anon-public-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# Application Configuration
SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=uploads/images
MAX_FILE_SIZE=16777216

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=DoorGuardian API
VERSION=1.0.0
```

### 6. Execute a aplicação

```bash
# Desenvolvimento
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Ou use os scripts de conveniência
./run_dev.sh       # Linux/Mac
run_dev.bat        # Windows
```

A API estará disponível em:

- **API**: `http://localhost:8000`
- **Documentação Swagger**: `http://localhost:8000/docs`
- **Documentação ReDoc**: `http://localhost:8000/redoc`

## 📚 API Endpoints

### Base URL

```
http://localhost:8000/api/v1
```

### Documentação Interativa

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 1. Obter Histórico de Acessos

**GET** `/history`

Recupera o histórico de acessos com suporte a paginação e filtros.

#### Parâmetros Query (opcionais):

- `page` (int): Número da página (padrão: 1)
- `per_page` (int): Itens por página (padrão: 20, máx: 100)
- `sort_by` (string): Campo para ordenação ('date' ou 'created_at', padrão: 'date')
- `sort_order` (string): Ordem ('asc' ou 'desc', padrão: 'desc')
- `access` (boolean): Filtrar por status de acesso (true/false)
- `date_from` (ISO datetime): Filtrar a partir desta data
- `date_to` (ISO datetime): Filtrar até esta data

#### Exemplo de Resposta:

```json
{
  "access_records": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "date": "2023-12-07T10:30:00Z",
      "access": true,
      "created_at": "2023-12-07T10:30:00Z",
      "updated_at": "2023-12-07T10:30:00Z",
      "image": {
        "id": "789e0123-e89b-12d3-a456-426614174001",
        "filename": "uuid-generated-name.jpg",
        "original_filename": "person.jpg",
        "file_size": 1024567,
        "mime_type": "image/jpeg"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

### 2. Registrar Acesso

**POST** `/register`

Registra um novo acesso no sistema.

#### Content-Type:

- `application/json` (sem imagem)
- `multipart/form-data` (com imagem)

#### Campos:

- `access` (boolean, obrigatório): Status do acesso (true/false)
- `date` (ISO datetime, opcional): Data do acesso (padrão: agora)
- `image` (file, opcional): Arquivo de imagem (PNG, JPG, JPEG, GIF, WEBP)

#### Exemplo JSON (sem imagem):

```json
{
  "access": true,
  "date": "2023-12-07T10:30:00Z"
}
```

#### Exemplo com imagem (multipart/form-data):

```
POST /api/v1/register
Content-Type: multipart/form-data

access: true
date: 2023-12-07T10:30:00Z
image: [arquivo de imagem]
```

#### Resposta de Sucesso:

```json
{
  "message": "Access record created successfully",
  "access_record": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "date": "2023-12-07T10:30:00Z",
    "access": true,
    "created_at": "2023-12-07T10:30:00Z",
    "updated_at": "2023-12-07T10:30:00Z",
    "image": {
      "id": "789e0123-e89b-12d3-a456-426614174001",
      "filename": "uuid-generated-name.jpg",
      "original_filename": "person.jpg"
    }
  }
}
```

### 3. Deletar Acesso

**DELETE** `/history/{id}`

Remove um registro de acesso específico.

#### Parâmetros:

- `id` (string): ID do registro de acesso

#### Resposta de Sucesso:

```json
{
  "message": "Access record deleted successfully",
  "deleted_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

## 🔧 Endpoints Adicionais

### Health Check

**GET** `/health`

Verifica se a API está funcionando.

### Informações da API

**GET** `/api/v1`

Retorna informações sobre a API e endpoints disponíveis.

## 📊 Modelos de Dados

### Access (Acesso)

- `id`: String UUID (Chave primária)
- `date`: DateTime (Data/hora do acesso)
- `access`: Boolean (Status do acesso - permitido/negado)
- `image_id`: String UUID (Chave estrangeira para Image)
- `created_at`: DateTime (Data de criação)
- `updated_at`: DateTime (Data de atualização)

### Image (Imagem)

- `id`: String UUID (Chave primária)
- `filename`: String (Nome do arquivo único)
- `original_filename`: String (Nome original do arquivo)
- `file_path`: String (Caminho do arquivo)
- `file_size`: Integer (Tamanho em bytes)
- `mime_type`: String (Tipo MIME)
- `created_at`: DateTime (Data de criação)
- `updated_at`: DateTime (Data de atualização)

## ⚙️ Configuração

### Variáveis de Ambiente

| Variável                    | Descrição                         | Padrão             |
| --------------------------- | --------------------------------- | ------------------ |
| `ENVIRONMENT`               | Ambiente (development/production) | `development`      |
| `DEBUG`                     | Modo debug                        | `True`             |
| `SUPABASE_URL`              | URL do projeto Supabase           | -                  |
| `SUPABASE_KEY`              | Chave anônima pública do Supabase | -                  |
| `SUPABASE_SERVICE_ROLE_KEY` | Chave de service role do Supabase | -                  |
| `SECRET_KEY`                | Chave secreta da aplicação        | -                  |
| `UPLOAD_FOLDER`             | Pasta para upload de imagens      | `uploads/images`   |
| `MAX_FILE_SIZE`             | Tamanho máximo de upload (bytes)  | `16777216` (16MB)  |
| `PROJECT_NAME`              | Nome do projeto                   | `DoorGuardian API` |

### Configurações de Imagem

- **Formatos suportados**: PNG, JPG, JPEG, GIF, WEBP
- **Tamanho máximo**: 16MB (configurável)
- **Validação**: Verificação de tipo MIME e integridade da imagem
- **Armazenamento**: Supabase Storage com nomes únicos (UUID)

## 🛡️ Segurança

- Validação de tipos de arquivo
- Verificação de integridade de imagens
- Sanitização de nomes de arquivos
- Limitação de tamanho de upload
- Tratamento seguro de erros
- UUID para IDs únicos

## 🚀 Deploy em Produção

### 1. Configure as variáveis de ambiente para produção:

```env
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your-production-secret-key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-production-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-production-service-role-key
```

### 2. Use uvicorn em produção:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Configure um proxy reverso (Nginx) e HTTPS

### 4. O Supabase já fornece um banco PostgreSQL gerenciado na nuvem

## 🧪 Desenvolvimento

### Executar em modo desenvolvimento:

```bash
# Com uvicorn diretamente
uvicorn app:app --host 0.0.0.0 --port 8000 --reload --log-level debug

# Ou com os scripts de conveniência
./run_dev.sh       # Linux/Mac
run_dev.bat        # Windows
```

### Gerenciamento do Banco:

O Supabase gerencia automaticamente o banco PostgreSQL. Para mudanças no schema:

1. Edite o arquivo `database/schema.sql`
2. Execute o SQL no painel do Supabase
3. Ou use migrações via API do Supabase

## 📝 Logs

A aplicação registra logs importantes incluindo:

- Erros de validação
- Falhas de upload de imagem
- Erros de banco de dados
- Tentativas de acesso inválidas

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório do projeto.
