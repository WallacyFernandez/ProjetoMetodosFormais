# API Django REST Framework

Uma API completa desenvolvida com Django REST Framework, seguindo as melhores práticas de desenvolvimento.

## 🚀 Características

- **Django REST Framework** para criação de APIs robustas
- **Autenticação JWT** com Simple JWT
- **Documentação automática** com Swagger/OpenAPI
- **Testes automatizados** com pytest
- **Estrutura modular** organizada em apps
- **Modelos base** com timestamp e UUID
- **Cache** com Redis
- **Soft delete** implementado
- **CORS** configurado para frontend
- **Logs** estruturados

## 📁 Estrutura do Projeto

```
Backend/
├── apps/
│   ├── authentication/     # Autenticação JWT
│   ├── core/              # Modelos e utilitários base
│   └── users/             # Gestão de usuários
├── config/                # Configurações Django
├── logs/                  # Arquivos de log
├── media/                 # Arquivos de mídia
├── static/                # Arquivos estáticos
├── venv/                  # Ambiente virtual
├── manage.py
├── requirements.txt
└── pytest.ini
```

## 🛠️ Configuração do Ambiente

### Pré-requisitos

- Python 3.10+
- pip
- Git

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd Backend
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   - Copie o arquivo `env_example.txt` para `.env`
   - Ajuste as configurações conforme necessário

5. **Execute as migrações:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crie um superusuário:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Execute o servidor:**
   ```bash
   python manage.py runserver
   ```

## 📝 Endpoints da API

### Autenticação
- `POST /api/v1/auth/login/` - Login do usuário
- `POST /api/v1/auth/register/` - Registro de novo usuário
- `POST /api/v1/auth/logout/` - Logout do usuário
- `POST /api/v1/auth/refresh/` - Renovar token de acesso
- `POST /api/v1/auth/change-password/` - Alterar senha
- `GET /api/v1/auth/me/` - Informações do usuário logado

### Documentação
- `/api/docs/` - Documentação Swagger
- `/api/redoc/` - Documentação ReDoc
- `/api/schema/` - Schema OpenAPI

## 🧪 Testes

Execute os testes com pytest:

```bash
# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=apps

# Executar testes específicos
pytest apps/authentication/tests.py

# Executar com verbose
pytest -v
```

### Marcadores de Teste

- `@pytest.mark.unit` - Testes unitários
- `@pytest.mark.integration` - Testes de integração
- `@pytest.mark.api` - Testes de API
- `@pytest.mark.slow` - Testes lentos

## 🔧 Configurações

### Banco de Dados

Por padrão, o projeto usa SQLite para desenvolvimento. Para produção, configure PostgreSQL:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

### Cache (Redis)

Configure o Redis para cache:

```env
REDIS_URL=redis://127.0.0.1:6379/1
```

### Email

Configure o email para produção:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha
```

## 🔐 Autenticação

A API usa autenticação JWT com os seguintes tokens:

- **Access Token**: Válido por 60 minutos
- **Refresh Token**: Válido por 7 dias (rotativo)

### Exemplo de Uso

```javascript
// Login
const response = await fetch('/api/v1/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password'
  })
});

const { data } = await response.json();
const { tokens } = data;

// Usar o token nas requisições
fetch('/api/v1/auth/me/', {
  headers: {
    'Authorization': `Bearer ${tokens.access}`
  }
});
```

## 📊 Modelos Base

### BaseModel

Todos os modelos herdam características comuns:

- `id` - UUID como chave primária
- `created_at` - Data de criação
- `updated_at` - Data de atualização
- `is_active` - Para soft delete

### Managers

- `objects` - Todos os objetos (incluindo inativos)
- `active` - Apenas objetos ativos

## 🌍 Ambientes

### Desenvolvimento
```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Produção
```env
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com
SECRET_KEY=sua-chave-secreta-segura
```

## 📈 Logs

Os logs são configurados para diferentes níveis:

- **INFO**: Operações normais
- **WARNING**: Situações que requerem atenção
- **ERROR**: Erros que não interrompem a aplicação
- **CRITICAL**: Erros críticos

Logs são salvos em `logs/django.log` e exibidos no console em desenvolvimento.

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆘 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique a documentação
2. Procure por issues similares
3. Abra uma nova issue com detalhes do problema

## 🔧 Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver

# Shell Django
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar testes
pytest

# Verificar código com flake8
flake8 apps/

# Formatar código com black
black apps/

# Ordenar imports
isort apps/
```
