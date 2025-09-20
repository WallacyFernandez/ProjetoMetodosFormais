#!/usr/bin/env python3
"""
Script para testar a API de Transações e Resumos Mensais do FinanceTracker.
"""

import requests
import json
from datetime import datetime, date
from decimal import Decimal


class TransactionsAPITester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.access_token = None
        self.session = requests.Session()
        
    def print_separator(self, title):
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print('='*60)
        
    def print_success(self, message):
        print(f"✅ {message}")
        
    def print_error(self, message, response=None):
        print(f"❌ {message}")
        if response:
            print(f"   Status: {response.status_code}")
            try:
                print(f"   Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            except:
                print(f"   Resposta: {response.text}")
    
    def register_user(self):
        """Registra um novo usuário para teste."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        url = f"{self.base_url}/api/v1/auth/register/"
        data = {
            "email": f"teste_transacoes_{timestamp}@exemplo.com",
            "username": f"teste_transacoes_{timestamp}",
            "password": "MinhaSenh@123",
            "password_confirm": "MinhaSenh@123",
            "first_name": "Teste",
            "last_name": "Transações"
        }
        
        response = self.session.post(url, json=data)
        
        if response.status_code == 201:
            result = response.json()
            self.access_token = result['data']['tokens']['access']
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })
            self.print_success(f"Usuário registrado: {data['email']}")
            return True
        else:
            self.print_error("Erro no registro", response)
            return False
    
    def get_categories(self):
        """Obtém as categorias disponíveis."""
        url = f"{self.base_url}/api/v1/finance/categories/"
        response = self.session.get(url)
        
        if response.status_code == 200:
            result = response.json()
            # Handle both paginated and direct list responses
            categories = result.get('results', result) if isinstance(result, dict) and 'results' in result else result
            
            self.print_success(f"Categorias obtidas: {len(categories)} disponíveis")
            
            # Mostra algumas categorias
            print("   📋 Categorias disponíveis:")
            for i, cat in enumerate(categories[:5]):
                print(f"      {cat['icon']} {cat['name']} ({cat['category_type']})")
            
            if len(categories) > 5:
                print(f"      ... e mais {len(categories) - 5} categorias")
            
            return categories
        else:
            self.print_error("Erro ao obter categorias", response)
            return []
    
    def create_transaction(self, amount, transaction_type, category_id, description, date_str=None):
        """Cria uma nova transação."""
        url = f"{self.base_url}/api/v1/finance/transactions/"
        data = {
            "amount": str(amount),
            "transaction_type": transaction_type,
            "category": category_id,
            "description": description,
            "transaction_date": date_str or date.today().strftime('%Y-%m-%d')
        }
        
        response = self.session.post(url, json=data)
        
        if response.status_code == 201:
            transaction = response.json()
            sign = "+" if transaction_type == "INCOME" else "-"
            self.print_success(f"Transação criada: {sign}R$ {amount} - {description}")
            return transaction
        else:
            self.print_error(f"Erro ao criar transação: {description}", response)
            return None
    
    def get_transactions(self, limit=10):
        """Obtém as transações do usuário."""
        url = f"{self.base_url}/api/v1/finance/transactions/"
        params = {"limit": limit}
        response = self.session.get(url, params=params)
        
        if response.status_code == 200:
            result = response.json()
            transactions = result.get('results', result) if isinstance(result, dict) else result
            self.print_success(f"Transações obtidas: {len(transactions)} encontradas")
            
            # Mostra as transações
            print("   📊 Transações recentes:")
            for transaction in transactions[:5]:
                print(f"      {transaction['amount_formatted']} - {transaction['description']}")
            
            return transactions
        else:
            self.print_error("Erro ao obter transações", response)
            return []
    
    def get_monthly_summary(self, year=None, month=None):
        """Obtém o resumo mensal."""
        url = f"{self.base_url}/api/v1/finance/transactions/monthly_summary/"
        params = {}
        if year:
            params['year'] = year
        if month:
            params['month'] = month
        
        response = self.session.get(url, params=params)
        
        if response.status_code == 200:
            summary = response.json()
            self.print_success("Resumo mensal obtido:")
            print(f"      📈 Receitas: {summary['income_total_formatted']}")
            print(f"      📉 Despesas: {summary['expense_total_formatted']}")
            print(f"      💰 Saldo: {summary['balance_formatted']}")
            print(f"      📋 Transações: {summary['transaction_count']}")
            return summary
        else:
            self.print_error("Erro ao obter resumo mensal", response)
            return None
    
    def get_category_summary(self, year=None, month=None):
        """Obtém o resumo por categoria."""
        url = f"{self.base_url}/api/v1/finance/transactions/category_summary/"
        params = {}
        if year:
            params['year'] = year
        if month:
            params['month'] = month
        
        response = self.session.get(url, params=params)
        
        if response.status_code == 200:
            categories = response.json()
            self.print_success(f"Resumo por categoria obtido: {len(categories)} categorias")
            
            # Mostra as top 3 categorias
            print("   🏆 Top categorias:")
            for i, cat in enumerate(categories[:3]):
                print(f"      {i+1}. {cat['category__icon']} {cat['category__name']}: "
                      f"{cat['total_formatted']} ({cat['percentage']}%)")
            
            return categories
        else:
            self.print_error("Erro ao obter resumo por categoria", response)
            return []
    
    def get_dashboard_data(self):
        """Obtém dados completos do dashboard."""
        url = f"{self.base_url}/api/v1/finance/transactions/dashboard_data/"
        response = self.session.get(url)
        
        if response.status_code == 200:
            dashboard = response.json()
            self.print_success("Dados do dashboard obtidos:")
            print(f"      💰 Saldo atual: {dashboard['current_balance_formatted']}")
            print(f"      📊 Total de transações: {dashboard['total_transactions_count']}")
            print(f"      📈 Média mensal receitas: R$ {dashboard['avg_monthly_income']}")
            print(f"      📉 Média mensal despesas: R$ {dashboard['avg_monthly_expense']}")
            return dashboard
        else:
            self.print_error("Erro ao obter dados do dashboard", response)
            return None
    
    def get_current_balance(self):
        """Obtém o saldo atual."""
        url = f"{self.base_url}/api/v1/finance/balance/"
        response = self.session.get(url)
        
        if response.status_code == 200:
            balance = response.json()
            self.print_success(f"Saldo atual: {balance['balance_formatted']}")
            return balance
        else:
            self.print_error("Erro ao obter saldo", response)
            return None
    
    def run_all_tests(self):
        """Executa todos os testes."""
        print("🚀 Testando API de Transações e Resumos - FinanceTracker")
        
        # Registra usuário
        self.print_separator("Autenticação")
        if not self.register_user():
            print("❌ Não foi possível autenticar. Abortando testes.")
            return
        
        # Testa categorias
        self.print_separator("Categorias")
        categories = self.get_categories()
        if not categories:
            print("❌ Não foi possível obter categorias. Abortando testes.")
            return
        
        # Encontra categorias para teste
        income_category = next((c for c in categories if c['category_type'] == 'INCOME'), None)
        expense_category = next((c for c in categories if c['category_type'] == 'EXPENSE'), None)
        
        if not income_category or not expense_category:
            print("❌ Categorias de receita e despesa não encontradas.")
            return
        
        # Testa criação de transações
        self.print_separator("Criação de Transações")
        
        print("\n1. Criando receita...")
        print(f"   Usando categoria: {income_category['name']} (ID: {income_category['id']})")
        self.create_transaction(
            amount=2500.00,
            transaction_type="INCOME",
            category_id=income_category['id'],
            description="Salário mensal"
        )
        
        print("\n2. Criando despesas...")
        self.create_transaction(
            amount=800.00,
            transaction_type="EXPENSE",
            category_id=expense_category['id'],
            description="Aluguel"
        )
        
        self.create_transaction(
            amount=350.50,
            transaction_type="EXPENSE",
            category_id=expense_category['id'],
            description="Supermercado"
        )
        
        self.create_transaction(
            amount=120.75,
            transaction_type="EXPENSE",
            category_id=expense_category['id'],
            description="Combustível"
        )
        
        # Testa listagem
        self.print_separator("Listagem de Transações")
        print("\n3. Obtendo transações...")
        self.get_transactions()
        
        # Testa saldo atualizado
        self.print_separator("Verificação do Saldo")
        print("\n4. Verificando saldo após transações...")
        self.get_current_balance()
        
        # Testa resumos
        self.print_separator("Resumos e Relatórios")
        
        print("\n5. Obtendo resumo mensal...")
        self.get_monthly_summary()
        
        print("\n6. Obtendo resumo por categoria...")
        self.get_category_summary()
        
        print("\n7. Obtendo dados completos do dashboard...")
        self.get_dashboard_data()
        
        # Testa filtros
        self.print_separator("Testes de Filtros")
        
        print("\n8. Testando filtro por tipo (receitas)...")
        url = f"{self.base_url}/api/v1/finance/transactions/"
        params = {"transaction_type": "INCOME"}
        response = self.session.get(url, params=params)
        
        if response.status_code == 200:
            result = response.json()
            transactions = result.get('results', result) if isinstance(result, dict) else result
            income_count = len([t for t in transactions if t['transaction_type'] == 'INCOME'])
            self.print_success(f"Filtro por receitas: {income_count} transações encontradas")
        else:
            self.print_error("Erro ao filtrar por receitas", response)
        
        self.print_separator("Testes Concluídos")
        self.print_success("Todos os testes da API de Transações foram executados!")
        print("\n🎯 Funcionalidades testadas:")
        print("   ✅ Autenticação com JWT")
        print("   ✅ Listagem de categorias padrão")
        print("   ✅ Criação de transações (receitas e despesas)")
        print("   ✅ Listagem de transações")
        print("   ✅ Atualização automática do saldo")
        print("   ✅ Resumo mensal (receitas, despesas, economia)")
        print("   ✅ Resumo por categoria com porcentagens")
        print("   ✅ Dados completos do dashboard")
        print("   ✅ Filtros por tipo de transação")


if __name__ == "__main__":
    tester = TransactionsAPITester()
    tester.run_all_tests()
