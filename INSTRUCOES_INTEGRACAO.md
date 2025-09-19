# Instruções para Integração Frontend-Backend

## ✅ O que foi implementado

### 1. Serviços de Autenticação Atualizados
- **Login**: Agora usa endpoint `/api/v1/auth/login/` com email e senha
- **Registro**: Novo serviço usando endpoint `/api/v1/auth/register/`
- **GetUserData**: Atualizado para endpoint `/api/v1/auth/me/`

### 2. Formulário de Login Atualizado
- Campo "Usuário" alterado para "Email" (type="email")
- Integração com a API Django REST Framework
- Tratamento de erros melhorado

### 3. Formulário de Cadastro Atualizado
- Simplificado para 2 steps (removido SIAPE)
- Campos: Nome, Sobrenome, Nome de usuário, Email, Senha, Confirmar Senha
- **Login automático após cadastro bem-sucedido** ✅
- Validações de senha (mínimo 8 caracteres, confirmação)
- Tratamento de erros específicos (email/username já em uso)

### 4. Tipos TypeScript Atualizados
- Novos tipos: `RegisterData` e `RegisterResponse`
- `UserProfile` atualizado com campos do Django

## 🚀 Como usar

### 1. Configurar Variável de Ambiente
Você precisa criar um arquivo `.env.local` na raiz do projeto com:

```env
NEXT_PUBLIC_URL_API=http://127.0.0.1:8000
```

### 2. Garantir que o Backend está rodando
O backend Django deve estar rodando em `http://127.0.0.1:8000`

### 3. Testar o fluxo completo

#### Cadastro:
1. Acesse `/cadastro`
2. Preencha Nome e Sobrenome, Nome de usuário
3. Clique em "Continuar"
4. Preencha Email, Senha e Confirmar Senha
5. Clique em "Finalizar Cadastro"
6. **O usuário será automaticamente logado e redirecionado para o dashboard**

#### Login:
1. Acesse `/login`
2. Digite email e senha
3. Clique em "Entrar"
4. Será redirecionado para o dashboard

## 🔄 Formato dos dados da API

### Registro (POST /api/v1/auth/register/)
```json
{
  "email": "usuario@exemplo.com",
  "username": "usuario123",
  "password": "MinhaSenh@123",
  "password_confirm": "MinhaSenh@123",
  "first_name": "João",
  "last_name": "Silva"
}
```

### Login (POST /api/v1/auth/login/)
```json
{
  "email": "usuario@exemplo.com",
  "password": "MinhaSenh@123"
}
```

### Resposta esperada (Registro e Login)
```json
{
  "data": {
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    },
    "user": {
      "id": 1,
      "username": "usuario123",
      "email": "usuario@exemplo.com",
      "first_name": "João",
      "last_name": "Silva",
      "full_name": "João Silva"
    }
  }
}
```

## 🔧 Melhorias implementadas

1. **Validações no frontend**: Senha mínima, confirmação de senha
2. **Feedback visual**: Loading states e toasts informativos
3. **Tratamento de erros**: Mensagens específicas para diferentes tipos de erro
4. **UX melhorada**: Login automático após cadastro
5. **Consistência**: Uso de email em vez de username para login

## ⚠️ Importante

- Certifique-se de que a API Django está configurada com CORS para aceitar requisições do frontend
- O token JWT é armazenado automaticamente no localStorage e cookies
- O contexto do usuário é atualizado automaticamente após login/cadastro

## 🧪 Testando a integração

Para testar se tudo está funcionando, você pode usar o script `Backend/test_api.py` para verificar se a API está respondendo corretamente, e então testar o frontend.
