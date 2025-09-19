## 🚀 Pull Request

<!-- Descreva brevemente o objetivo desta mudança -->

### 🎯 Objetivo da Mudança

<!-- Explique qual problema esta mudança resolve ou qual funcionalidade adiciona -->

### 📋 Checklist

<!-- Marque com X os itens que foram completados -->

#### Pré-submissão:
- [ ] Código segue os padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada (se necessário)
- [ ] Lint passou sem erros
- [ ] Build está funcionando

#### Atomic Design:
- [ ] Componentes seguem a hierarquia Atomic Design
- [ ] Novos componentes estão na pasta correta (atoms/molecules/organisms)
- [ ] Componentes são reutilizáveis
- [ ] Props estão bem definidas

#### Styled Components:
- [ ] Estilos usam styled-components
- [ ] Tema é utilizado corretamente
- [ ] Componentes são responsivos
- [ ] Acessibilidade foi considerada

#### Git Flow:
- [ ] Branch segue convenção de nomenclatura
- [ ] Commits são atômicos e descritivos
- [ ] Branch está atualizada com a main

### 🔄 Tipo de Mudança

<!-- Marque com X o tipo de mudança -->

- [ ] **Bug fix** - Correção de bug
- [ ] **New feature** - Nova funcionalidade
- [ ] **Breaking change** - Mudança que quebra compatibilidade
- [ ] **Documentation** - Atualização de documentação
- [ ] **Refactoring** - Refatoração de código
- [ ] **Performance** - Melhoria de performance
- [ ] **Styling** - Mudança de estilo/UI

### 🎨 Design System Impact

<!-- Marque com X se a mudança afeta o design system -->

- [ ] **Atom** - Componente básico modificado/criado
- [ ] **Molecule** - Combinação de átomos modificada/criada
- [ ] **Organism** - Componente complexo modificado/criado
- [ ] **Theme** - Variáveis do tema modificadas
- [ ] **Styled Components** - Estilos modificados

### 📱 Screenshots/Imagens

<!-- Adicione screenshots das mudanças visuais -->
<!-- Você pode arrastar e soltar imagens diretamente nesta área -->

#### Antes:
<!-- Screenshot do estado anterior -->

#### Depois:
<!-- Screenshot do novo estado -->

### 🧪 Como Testar Manualmente

<!-- Liste os passos para testar as mudanças -->

1. **Setup:**
   ```bash
   # Comandos para configurar o ambiente
   yarn install
   yarn dev
   ```

2. **Teste 1:** [Descrição do teste]
   - Vá para `http://localhost:3000/rota`
   - Clique em [elemento]
   - Verifique se [comportamento esperado]

3. **Teste 2:** [Descrição do teste]
   - [Passos específicos]
   - [Resultado esperado]

4. **Teste 3:** [Descrição do teste]
   - [Passos específicos]
   - [Resultado esperado]

### 📁 Arquivos Modificados

<!-- Liste os principais arquivos que foram modificados -->

#### Novos Arquivos:
- `src/components/atoms/NovoComponente/index.tsx`
- `src/components/molecules/NovoComponente/index.tsx`

#### Arquivos Modificados:
- `src/components/atoms/ComponenteExistente/index.tsx`
- `src/styles/theme.ts`

#### Arquivos Removidos:
- `src/components/obsoleto/index.tsx`

### 🔧 Mudanças Técnicas

<!-- Descreva mudanças técnicas importantes -->

#### Dependências:
- [ ] Novas dependências adicionadas
- [ ] Dependências removidas
- [ ] Dependências atualizadas

#### APIs:
- [ ] Novas APIs criadas
- [ ] APIs modificadas
- [ ] APIs removidas

#### Performance:
- [ ] Otimizações de performance implementadas
- [ ] Bundle size impactado
- [ ] Tempo de carregamento melhorado

### 🧪 Testes

<!-- Descreva os testes implementados -->

#### Testes Unitários:
- [ ] Testes para novos componentes
- [ ] Testes para funcionalidades modificadas
- [ ] Cobertura de testes adequada

#### Testes de Integração:
- [ ] Testes de fluxo completo
- [ ] Testes de API
- [ ] Testes de UI

#### Testes Manuais:
- [ ] Testado em diferentes navegadores
- [ ] Testado em diferentes dispositivos
- [ ] Testado em diferentes resoluções

### 📚 Documentação

<!-- Descreva mudanças na documentação -->

- [ ] README atualizado
- [ ] Documentação de componentes atualizada
- [ ] Storybook atualizado
- [ ] Comentários de código adicionados

### 🏷️ Labels Sugeridas

<!-- Labels que devem ser aplicadas a este PR -->

- `feature` / `bugfix` / `documentation`
- `atomic-design` (se relacionado a componentes)
- `styled-components` (se relacionado a estilos)
- `breaking-change` (se quebra compatibilidade)

### 📞 Informações Adicionais

<!-- Qualquer informação adicional relevante -->

**Issue Relacionada:** #[número da issue]
**Dependências:** #[número do PR dependente]
**Rollback:** [Instruções para reverter as mudanças se necessário]

### 🔍 Checklist do Reviewer

<!-- Para o reviewer marcar -->

- [ ] Código foi revisado
- [ ] Funcionalidade foi testada
- [ ] Documentação está adequada
- [ ] Testes estão adequados
- [ ] Performance foi considerada
- [ ] Segurança foi considerada
- [ ] Acessibilidade foi considerada

---

<!-- Template baseado no Atomic Design, Git Flow e Styled Components --> 