# Database Migrations

Esta pasta contém as migrações do banco de dados para o projeto DoorGuardian.

## 📋 Migrações Disponíveis

### 001_add_image_url_column.sql

**Data**: 2025-09-28  
**Descrição**: Adiciona coluna `image_url` na tabela `access` para armazenar a URL pública das imagens.

**Alterações**:

- ✅ Adiciona coluna `image_url` do tipo `TEXT`
- ✅ Cria índice para performance em consultas por `image_url`
- ✅ Atualiza registros existentes com URLs das imagens
- ✅ Cria função e trigger automático para popular `image_url`
- ✅ Adiciona comentários de documentação

## 🚀 Como Executar Migrações

### Método 1: Script Automático

```bash
cd database
python migrate.py
```

### Método 2: Manual (Recomendado)

1. Acesse o [Supabase Dashboard](https://supabase.com/dashboard)
2. Selecione seu projeto DoorGuardian
3. Vá para **SQL Editor**
4. Copie o conteúdo do arquivo de migração desejado
5. Cole no editor e execute

### Método 3: Via Terminal

```bash
# Execute a migração usando o terminal
cd database
cat migrations/001_add_image_url_column.sql
```

## 📊 Estrutura da Tabela Após Migração

### Tabela `access`

```sql
CREATE TABLE access (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    access BOOLEAN NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    image_id UUID REFERENCES images(id) ON DELETE SET NULL,
    image_url TEXT,  -- 🆕 Nova coluna
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Como Funciona o Trigger

Quando um registro é criado ou o `image_id` é atualizado:

1. O trigger `trigger_update_access_image_url` é acionado
2. A função `update_access_image_url()` busca o `file_path` na tabela `images`
3. Constrói a URL completa: `https://seu-projeto.supabase.co/storage/v1/object/public/images/{file_path}`
4. Popula automaticamente o campo `image_url`

## 🔍 Exemplo de Uso

### Antes da Migração

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "access": true,
  "date": "2023-12-07T10:30:00Z",
  "image_id": "789e0123-e89b-12d3-a456-426614174001",
  "created_at": "2023-12-07T10:30:00Z"
}
```

### Após a Migração

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "access": true,
  "date": "2023-12-07T10:30:00Z",
  "image_id": "789e0123-e89b-12d3-a456-426614174001",
  "image_url": "https://hqglopazdwoeqdagmtom.supabase.co/storage/v1/object/public/images/access_images/uuid-name.jpg",
  "created_at": "2023-12-07T10:30:00Z"
}
```

## ⚠️ Importante

- ✅ **Backup**: Sempre faça backup antes de executar migrações
- ✅ **Teste**: Execute primeiro em ambiente de desenvolvimento
- ✅ **Ordem**: Execute as migrações na ordem numérica
- ✅ **Verificação**: Confirme se os triggers foram criados corretamente

## 📱 Benefícios para o Frontend

Com a nova coluna `image_url`, o frontend pode:

- 🖼️ Acessar imagens diretamente via URL
- 🚀 Carregar imagens mais rapidamente
- 🔄 Não precisar fazer requests extras para obter URLs
- 📱 Implementar cache de imagens facilmente

## 🛠️ Reverter Migração (Se necessário)

Para reverter a migração `001_add_image_url_column.sql`:

```sql
-- Remove trigger and function
DROP TRIGGER IF EXISTS trigger_update_access_image_url ON access;
DROP FUNCTION IF EXISTS update_access_image_url();

-- Remove index
DROP INDEX IF EXISTS idx_access_image_url;

-- Remove column
ALTER TABLE access DROP COLUMN IF EXISTS image_url;
```
