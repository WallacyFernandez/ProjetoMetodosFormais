# SigContas - Sistema de Gestão de Contas

## 📋 Sobre o Projeto

O **SigContas** é um sistema desenvolvido com Next.js 15, React 19 e TypeScript. O projeto utiliza uma arquitetura baseada em componentes atômicos (Atomic Design) e styled-components para uma interface moderna e responsiva.

### 🎯 Funcionalidades Principais

- **Sistema de Autenticação**: Login e cadastro de usuários
- **Interface Moderna**: Design responsivo com tema personalizado
- **Arquitetura Escalável**: Baseada em Atomic Design (atoms, molecules, organisms)
- **TypeScript**: Tipagem estática para maior segurança e produtividade

### 🏗️ Arquitetura do Projeto

```
src/
├── app/                    # App Router do Next.js 15
│   ├── cadastro/          # Página de cadastro
│   ├── login/             # Página de login
│   ├── styles/            # Configurações de tema e estilos globais
│   └── layout.tsx         # Layout principal da aplicação
├── components/            # Componentes organizados por Atomic Design
│   ├── atoms/            # Componentes básicos (Button, Input, Logo)
│   ├── molecules/        # Componentes compostos (LoginForm, RegisterForm)
│   └── organisms/        # Componentes complexos (LoginContainer, RegisterForm)
├── contexts/             # Contextos React (se necessário)
├── hooks/                # Custom hooks
└── services/             # Serviços e APIs
```

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Node.js 18+ 
- Yarn
- Git Flow

### Instalação

1. **Clone o repositório**
   ```bash
   git clone [URL_DO_REPOSITORIO]
   cd sigcontas_front
   ```

2. **Instale as dependências**
   ```bash
   yarn install
   ```

3. **Execute o projeto em modo de desenvolvimento**
   ```bash
   yarn dev
   ```

4. **Acesse a aplicação**
   Abra [http://localhost:3000](http://localhost:3000) no seu navegador

### Scripts Disponíveis

```bash
# Desenvolvimento com Turbopack (mais rápido)
yarn dev

# Build para produção
yarn build

# Executar build de produção
yarn start

# Verificar linting
yarn lint
```

## 🎨 Design System

O projeto utiliza um design system consistente com:

### Cores Principais
- **Azul Primário**: `#1E3A8A` - Cor principal da marca
- **Azul Secundário**: `#0052CC` - Elementos de destaque
- **Azul Claro**: `#3B82F6` - Elementos interativos
- **Branco**: `#FFFFFF` - Fundo principal
- **Cinza**: `#6B7280` - Textos secundários

### Componentes Base
- **Button**: Botões com variantes primário e secundário
- **Input**: Campos de entrada com validação
- **Logo**: Logo da marca em versões azul e branca
- **TextLink**: Links de navegação

## 🔧 Tecnologias Utilizadas

- **Next.js 15**: Framework React com App Router
- **React 19**: Biblioteca para interfaces de usuário
- **TypeScript**: Tipagem estática
- **Styled Components**: CSS-in-JS para estilização
- **React Icons**: Biblioteca de ícones
- **Turbopack**: Bundler rápido para desenvolvimento
