# 🚪 DoorGuardian API

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Supabase](https://img.shields.io/badge/Supabase-Database-orange.svg)](https://supabase.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Uma API RESTful moderna e robusta para gerenciamento de controle de acesso de portas, desenvolvida com **FastAPI** e **Supabase**. O DoorGuardian permite registrar, monitorar e gerenciar eventos de acesso com suporte a upload de imagens e funcionalidades avançadas de filtragem.

## 🌟 Características

- **API RESTful Completa**: Endpoints para criar, listar e gerenciar registros de acesso
- **Upload de Imagens**: Suporte completo para upload e armazenamento de imagens de acesso
- **Validação Robusta**: Validação de tipos de arquivo, tamanhos e conteúdo de imagens
- **Filtragem Avançada**: Filtros por data, tipo de acesso e paginação
- **Documentação Automática**: Interface Swagger/OpenAPI integrada
- **Arquitetura Limpa**: Padrões de boas práticas com separação de responsabilidades
- **Cloud-Native**: Integração completa com Supabase (Database + Storage)

## 🏗️ Arquitetura

O projeto segue as melhores práticas de desenvolvimento FastAPI com Supabase:

```
DoorGuardian_backend/
├── app/
│   ├── config/          # Configurações e extensões
│   │   ├── config.py    # Settings com Pydantic
│   │   └── extensions.py # Clients Supabase
│   ├── models/          # Modelos Pydantic
│   │   ├── access.py    # Modelos de acesso
│   │   └── image.py     # Modelos de imagem
│   ├── routes/          # Endpoints da API
│   │   └── access_routes.py
│   ├── services/        # Lógica de negócio
│   │   ├── database_service.py # Serviços de banco
│   │   └── image_service.py    # Serviços de imagem
│   ├── utils/           # Utilitários
│   │   └── file_utils.py # Manipulação de arquivos
│   └── app_factory.py   # Factory da aplicação
├── main.py              # Entry point
├── requirements.txt     # Dependências
├── .env.example        # Exemplo de configuração
└── README.md           # Este arquivo
```

## � Início Rápido

### Pré-requisitos

- Python 3.13+
- Conta no [Supabase](https://supabase.com)
- Git

### 1. Clone o Repositório

```bash
git clone https://github.com/mthonorio/DoorGuardian-Backend.git
cd DoorGuardian_backend
```

### 2. Configuração do Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configuração do Banco de Dados

#### 4.1 Configurar Supabase

1. Crie um novo projeto no [Supabase Dashboard](https://supabase.com/dashboard)
2. Vá em **Settings** → **API** e copie:
   - Project URL
   - Anon Key
   - Service Role Key

#### 4.2 Executar Schema SQL

Execute o seguinte SQL no **SQL Editor** do Supabase:

```sql
-- Criar tabela de imagens
CREATE TABLE IF NOT EXISTS images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar tabela de acessos
CREATE TABLE IF NOT EXISTS access (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    access BOOLEAN NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    image_id UUID REFERENCES images(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_access_date ON access(date DESC);
CREATE INDEX IF NOT EXISTS idx_access_access ON access(access);
CREATE INDEX IF NOT EXISTS idx_images_created_at ON images(created_at DESC);

-- Criar bucket para imagens no Storage
INSERT INTO storage.buckets (id, name, public)
VALUES ('images', 'images', true)
ON CONFLICT (id) DO NOTHING;

-- Políticas de Storage (permite upload público temporariamente)
CREATE POLICY "Allow public uploads" ON storage.objects
    FOR INSERT WITH CHECK (bucket_id = 'images');

CREATE POLICY "Allow public access" ON storage.objects
    FOR SELECT USING (bucket_id = 'images');
```

### 5. Configuração das Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar com suas credenciais
nano .env
```

Exemplo do arquivo `.env`:

```env
# FastAPI Environment
ENVIRONMENT=development
DEBUG=True

# Supabase Configuration
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-anon-key-aqui
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key-aqui

# Application Configuration
SECRET_KEY=sua-chave-secreta-super-segura
UPLOAD_FOLDER=uploads/images
MAX_FILE_SIZE=16777216

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=DoorGuardian API
VERSION=1.0.0
```

### 6. Executar a Aplicação

```bash
# Desenvolvimento
uvicorn main:app --reload

# Produção
uvicorn main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em:

- **Aplicação**: http://127.0.0.1:8000
- **Documentação**: http://127.0.0.1:8000/docs
- **OpenAPI Schema**: http://127.0.0.1:8000/openapi.json

## 📚 Documentação da API

### Endpoints Disponíveis

#### 🏠 Health Check

```
GET /health
```

Verifica o status da aplicação.

#### 📋 Listar Histórico de Acessos

```
GET /api/v1/history
```

**Parâmetros de Query:**

- `page` (int): Página (padrão: 1)
- `per_page` (int): Itens por página (padrão: 20, máx: 100)
- `sort_by` (str): Campo para ordenação (padrão: "date")
- `sort_order` (str): Ordem (asc/desc, padrão: "desc")
- `access` (bool): Filtrar por tipo de acesso
- `date_from` (datetime): Data início (ISO format)
- `date_to` (datetime): Data fim (ISO format)

**Exemplo de Resposta:**

```json
{
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "access": true,
      "date": "2023-12-07T10:30:00Z",
      "image": {
        "id": "456e7890-e89b-12d3-a456-426614174000",
        "filename": "uuid-name.jpg",
        "file_path": "access_images/uuid-name.jpg"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 1,
    "pages": 1
  }
}
```

#### ➕ Registrar Novo Acesso

```
POST /api/v1/register
```

**Parâmetros (Form Data):**

- `access` (boolean, obrigatório): Acesso concedido (true) ou negado (false)
- `date` (datetime, opcional): Data do acesso (padrão: agora)
- `image` (file, opcional): Arquivo de imagem (PNG, JPG, JPEG, GIF, WEBP)

**Exemplo de Resposta:**

```json
{
  "message": "Access record created successfully",
  "access": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "access": true,
    "date": "2023-12-07T10:30:00Z",
    "image_id": "456e7890-e89b-12d3-a456-426614174000"
  }
}
```

#### 🗑️ Deletar Registro de Acesso

```
DELETE /api/v1/history/{access_id}
```

Remove um registro de acesso e sua imagem associada.

### Tipos de Arquivo Suportados

- **Extensões**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- **MIME Types**: `image/jpeg`, `image/png`, `image/gif`, `image/webp`
- **Tamanho Máximo**: 16MB

## � Desenvolvimento

### Estrutura do Projeto

- **Models**: Definições Pydantic para validação de dados
- **Services**: Lógica de negócio e interação com banco de dados
- **Routes**: Definição dos endpoints da API
- **Utils**: Funções utilitárias (validação de arquivos, etc.)
- **Config**: Configurações da aplicação

### Executar Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio httpx

# Executar testes
pytest
```

### Linting e Formatação

```bash
# Instalar ferramentas
pip install black isort flake8

# Formatação
black .
isort .

# Linting
flake8 .
```

## 🐳 Deploy com Docker

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build
docker build -t doorguardian-api .

# Run
docker run -p 8000:8000 --env-file .env doorguardian-api
```

## 🔒 Segurança

- **Validação de Arquivos**: Múltiplas camadas de validação (extensão, MIME type, conteúdo)
- **Sanitização**: Nomes de arquivo são sanitizados e UUIDs são usados
- **Rate Limiting**: Implementar rate limiting em produção
- **CORS**: Configuração adequada para origins permitidas
- **Environment Variables**: Credenciais sensíveis em variáveis de ambiente

## 📝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Matheus Honório** - _Desenvolvedor Principal_ - [@mthonorio](https://github.com/mthonorio)

## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno e rápido
- [Supabase](https://supabase.com/) - Backend-as-a-Service
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Validação de dados
- [Pillow](https://pillow.readthedocs.io/) - Processamento de imagens

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!** ⭐
