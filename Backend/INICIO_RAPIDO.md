# 🚀 Início Rápido - API Django REST Framework

## ✅ Configuração Concluída!

Seu ambiente Django REST Framework foi configurado com sucesso! Aqui estão os próximos passos:

## 🔧 Para Começar a Usar

### 1. Ativar o Ambiente Virtual
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Configurar Variáveis de Ambiente
- Copie `env_example.txt` para `.env`
- Ajuste as configurações se necessário

### 3. Criar um Superusuário
```bash
python manage.py createsuperuser
```

### 4. Executar o Servidor
```bash
python manage.py runserver
```

## 🌐 URLs Importantes

- **API Base**: http://127.0.0.1:8000/api/v1/
- **Admin Django**: http://127.0.0.1:8000/admin/
- **Documentação Swagger**: http://127.0.0.1:8000/api/docs/
- **Documentação ReDoc**: http://127.0.0.1:8000/api/redoc/

## 🔐 Endpoints de Autenticação

### Registro de Usuário
```bash
POST http://127.0.0.1:8000/api/v1/auth/register/
Content-Type: application/json

{
    "email": "usuario@exemplo.com",
    "username": "usuario123",
    "password": "MinhaSenh@123",
    "password_confirm": "MinhaSenh@123",
    "first_name": "João",
    "last_name": "Silva"
}
```

### Login
```bash
POST http://127.0.0.1:8000/api/v1/auth/login/
Content-Type: application/json

{
    "email": "usuario@exemplo.com",
    "password": "MinhaSenh@123"
}
```

### Acessar Informações do Usuário
```bash
GET http://127.0.0.1:8000/api/v1/auth/me/
Authorization: Bearer SEU_ACCESS_TOKEN
```

## 🧪 Executar Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=apps

# Testes específicos
pytest apps/authentication/tests.py -v
```

## 📁 Estrutura Criada

```
Backend/
├── apps/
│   ├── authentication/     # ✅ Autenticação JWT
│   ├── core/              # ✅ Modelos base e utilitários
│   └── users/             # ✅ Gestão de usuários
├── config/                # ✅ Configurações Django
├── logs/                  # ✅ Arquivos de log
├── media/                 # ✅ Upload de arquivos
├── static/                # ✅ Arquivos estáticos
├── venv/                  # ✅ Ambiente virtual
├── db.sqlite3             # ✅ Banco de dados
├── manage.py              # ✅ Gerenciador Django
├── requirements.txt       # ✅ Dependências
├── pytest.ini            # ✅ Configuração de testes
├── .gitignore             # ✅ Controle de versão
└── README.md              # ✅ Documentação completa
```

## 🎯 Recursos Implementados

- ✅ **Django REST Framework** configurado
- ✅ **Autenticação JWT** com refresh tokens
- ✅ **Modelos de usuário customizados**
- ✅ **Testes automatizados** com pytest
- ✅ **Documentação automática** (Swagger/OpenAPI)
- ✅ **Estrutura modular** organizada
- ✅ **CORS** configurado para frontend
- ✅ **Soft delete** implementado
- ✅ **Cache** configurado (Redis)
- ✅ **Logs** estruturados
- ✅ **Validações** robustas
- ✅ **Managers customizados**

## 🔄 Próximos Passos Sugeridos

1. **Testar a API** usando a documentação Swagger
2. **Criar novos endpoints** seguindo a estrutura dos apps
3. **Configurar Redis** para cache (opcional)
4. **Configurar PostgreSQL** para produção
5. **Implementar deploy** em serviços como Heroku, AWS, etc.

## 🆘 Comandos Úteis

```bash
# Executar servidor
python manage.py runserver

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Shell Django
python manage.py shell

# Executar testes
pytest

# Verificar código
python manage.py check
```

## 📞 Suporte

Se precisar de ajuda:
1. Consulte o `README.md` para documentação completa
2. Verifique os logs em `logs/django.log`
3. Execute `python manage.py check` para verificar problemas

---

**Parabéns! Seu ambiente Django REST Framework está pronto para desenvolvimento! 🎉**
