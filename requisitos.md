[1 tool called]

Perfeito! Com **Next.js + Django**, podemos criar algo muito mais robusto. Aqui está o projeto detalhado:

## **"FinanceTracker" - Sistema de Controle Financeiro Pessoal**

### **Stack Tecnológica:**
- **Frontend:** Next.js 14 + TypeScript + Tailwind CSS
- **Backend:** Django REST Framework + PostgreSQL
- **Autenticação:** JWT (django-rest-auth)
- **Deploy:** Vercel (frontend) + Railway/Heroku (backend)

### **Requisitos Funcionais Específicos:**

#### **1. Autenticação e Perfil**
- Registro com email e senha (validação de email)
- Login/logout com JWT
- Perfil básico: nome, foto, moeda preferida (BRL, USD, EUR)
- Recuperação de senha via email

#### **2. Dashboard Inteligente**
- Saldo atual em tempo real
- Resumo mensal: receitas, despesas, economia
- Gráfico de pizza: gastos por categoria (últimos 30 dias)
- Gráfico de linha: evolução do saldo (últimos 6 meses)
- Top 5 maiores gastos do mês
- Previsão de saldo para final do mês baseado na média

#### **3. Gestão de Transações**
- CRUD completo de transações
- Campos: valor, categoria, subcategoria, descrição, data, tipo (receita/despesa)
- Upload de comprovante (imagem - opcional)
- Transações recorrentes (salário, aluguel, etc.)
- Busca e filtros: por período, categoria, valor mínimo/máximo
- Paginação das transações

#### **4. Sistema de Categorias Inteligente**
- Categorias pré-definidas: Alimentação, Transporte, Moradia, Lazer, Saúde, Educação, Trabalho, Investimentos
- Subcategorias: ex: Alimentação → Restaurante, Mercado, Delivery
- Criação de categorias personalizadas
- Ícones e cores para cada categoria
- Sugestão automática de categoria baseada na descrição

#### **5. Orçamento e Metas**
- Definir orçamento mensal por categoria
- Alertas visuais: verde (ok), amarelo (80% do limite), vermelho (excedeu)
- Meta de economia mensal
- Progresso visual das metas (barra de progresso)
- Histórico de cumprimento de metas

#### **6. Relatórios e Análises**
- Relatório mensal detalhado (PDF exportável)
- Comparativo entre meses
- Análise de tendências: "Você gastou 20% menos em alimentação este mês"
- Identificação de gastos desnecessários
- Sugestões de economia baseadas nos dados

#### **7. Funcionalidades Extras**
- Calculadora de juros compostos
- Simulador de economia: "Se economizar R$ X por mês, em Y meses terá Z"
- Lembretes: pagar conta, registrar gasto
- Modo escuro/claro
- Exportar dados (CSV, JSON)

#### **8. Responsividade e UX**
- Interface totalmente responsiva
- PWA (Progressive Web App) - funciona offline básico
- Loading states e feedback visual
- Validações em tempo real nos formulários
- Confirmações para ações destrutivas

### **Requisitos Técnicos:**

#### **Backend (Django)**
- API RESTful com DRF
- Autenticação JWT
- Validações robustas
- Paginação automática
- Filtros e ordenação
- Middleware de CORS
- Logs de auditoria
- Backup automático do banco

#### **Frontend (Next.js)**
- SSR para SEO
- TypeScript para type safety
- Tailwind para styling consistente
- React Hook Form para formulários
- React Query para cache de dados
- Zustand para estado global
- Componentes reutilizáveis
- Lazy loading de imagens

### **Estrutura de Dados Principal:**

```typescript
// Usuário
User {
  id, email, nome, foto, moeda_preferida, created_at
}

// Transação
Transaction {
  id, user, valor, categoria, subcategoria, 
  descricao, data, tipo, comprovante, 
  is_recorrente, created_at, updated_at
}

// Categoria
Category {
  id, nome, icone, cor, is_custom, user
}

// Orçamento
Budget {
  id, user, categoria, valor_limite, mes_ano
}

// Meta
Goal {
  id, user, nome, valor_meta, valor_atual, 
  prazo, status, created_at
}
```

### **MVP (Versão Inicial):**
1. Autenticação básica
2. CRUD de transações
3. Dashboard com gráficos básicos
4. Categorias pré-definidas
5. Orçamento simples por categoria

### **Roadmap Futuro:**
- Integração com bancos (Open Banking)
- App mobile com React Native
- Relatórios mais avançados
- Compartilhamento familiar
- IA para categorização automática

Este projeto é realista, útil e pode ser desenvolvido gradualmente. Tem potencial para crescer e realmente ajudar pessoas com suas finanças pessoais, contribuindo para o **ODS 1 - Erradicação da pobreza** através da educação financeira.

Quer que eu comece a implementar alguma parte específica?

[1 tool called]