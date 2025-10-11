#!/usr/bin/env python3
"""
Script para testar a API de Saldo do FinanceTracker.
"""

import requests
import json
from datetime import datetime


class FinanceAPITester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.access_token = None
        self.session = requests.Session()
        
    def print_separator(self, title):
        print(f"\n{'='*50}")
        print(f"🧪 {title}")
        print('='*50)
        
    def print_success(self, message):
        print(f"✅ {message}")
        
    def print_error(self, message, response=None):
        print(f"❌ {message}")
        if response:
            print(f"   Status: {response.status_code}")
            try:
                print(f"   Resposta: {response.json()}")
            except:
                print(f"   Resposta: {response.text}")
    
    def register_user(self):
        """Registra um novo usuário para teste."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        url = f"{self.base_url}/api/v1/auth/register/"
        data = {
            "email": f"teste_saldo_{timestamp}@exemplo.com",
            "username": f"teste_saldo_{timestamp}",
            "password": "MinhaSenh@123",
            "password_confirm": "MinhaSenh@123",
            "first_name": "Teste",
            "last_name": "Saldo"
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
    
    def login_existing_user(self):
        """Faz login com usuário existente."""
        url = f"{self.base_url}/api/v1/auth/login/"
        data = {
            "email": "admin@admin.com",  # Usuário padrão
            "password": "admin123"
        }
        
        response = self.session.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            self.access_token = result['data']['tokens']['access']
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })
            self.print_success("Login realizado com sucesso")
            return True
        else:
            self.print_error("Erro no login", response)
            return False
    
    def get_balance(self):
        """Obtém o saldo atual do usuário."""
        url = f"{self.base_url}/api/v1/finance/balance/"
        response = self.session.get(url)
        
        if response.status_code == 200:
            result = response.json()
            balance = result['current_balance']
            formatted = result['balance_formatted']
            self.print_success(f"Saldo atual: {formatted}")
            return float(balance)
        else:
            self.print_error("Erro ao obter saldo", response)
            return None
    
    def add_amount(self, amount, description=""):
        """Adiciona valor ao saldo."""
        url = f"{self.base_url}/api/v1/finance/balance/add_amount/"
        data = {
            "amount": str(amount),
            "description": description or f"Adição de R$ {amount}"
        }
        
        response = self.session.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            new_balance = result['balance']['balance_formatted']
            self.print_success(f"Valor adicionado! Novo saldo: {new_balance}")
            return True
        else:
            self.print_error(f"Erro ao adicionar R$ {amount}", response)
            return False
    
    def subtract_amount(self, amount, description=""):
        """Subtrai valor do saldo."""
        url = f"{self.base_url}/api/v1/finance/balance/subtract_amount/"
        data = {
            "amount": str(amount),
            "description": description or f"Subtração de R$ {amount}"
        }
        
        response = self.session.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            new_balance = result['balance']['balance_formatted']
            self.print_success(f"Valor subtraído! Novo saldo: {new_balance}")
            return True
        else:
            self.print_error(f"Erro ao subtrair R$ {amount}", response)
            return False
    
    def set_balance(self, amount, description=""):
        """Define um novo saldo."""
        url = f"{self.base_url}/api/v1/finance/balance/set_balance/"
        data = {
            "amount": str(amount),
            "description": description or f"Saldo definido para R$ {amount}"
        }
        
        response = self.session.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            new_balance = result['balance']['balance_formatted']
            self.print_success(f"Saldo definido! Novo saldo: {new_balance}")
            return True
        else:
            self.print_error(f"Erro ao definir saldo para R$ {amount}", response)
            return False
    
    def reset_balance(self):
        """Reseta o saldo para zero."""
        url = f"{self.base_url}/api/v1/finance/balance/reset_balance/"
        
        response = self.session.post(url, json={})
        
        if response.status_code == 200:
            result = response.json()
            new_balance = result['balance']['balance_formatted']
            self.print_success(f"Saldo resetado! Novo saldo: {new_balance}")
            return True
        else:
            self.print_error("Erro ao resetar saldo", response)
            return False
    
    def get_history(self):
        """Obtém o histórico de saldo."""
        url = f"{self.base_url}/api/v1/finance/balance/history/"
        response = self.session.get(url)
        
        if response.status_code == 200:
            result = response.json()
            history_count = len(result) if isinstance(result, list) else len(result.get('results', []))
            self.print_success(f"Histórico obtido: {history_count} registros")
            
            # Mostra os últimos 3 registros
            history_items = result if isinstance(result, list) else result.get('results', [])
            for i, item in enumerate(history_items[:3]):
                operation = item['operation_display']
                amount = item['amount']
                date = item['created_at'][:19]  # Remove timezone info
                print(f"   {i+1}. {operation} - R$ {amount} em {date}")
                
            return True
        else:
            self.print_error("Erro ao obter histórico", response)
            return False
    
    def test_insufficient_balance(self):
        """Testa subtração com saldo insuficiente."""
        current_balance = self.get_balance()
        if current_balance is not None:
            # Tenta subtrair mais do que tem
            amount_to_subtract = current_balance + 100
            url = f"{self.base_url}/api/v1/finance/balance/subtract_amount/"
            data = {"amount": str(amount_to_subtract)}
            
            response = self.session.post(url, json=data)
            
            if response.status_code == 400:
                self.print_success("Validação de saldo insuficiente funcionando corretamente")
                return True
            else:
                self.print_error("Validação de saldo insuficiente não funcionou", response)
                return False
        return False
    
    def run_all_tests(self):
        """Executa todos os testes."""
        print("🚀 Testando API de Saldo - FinanceTracker")
        
        # Tenta fazer login primeiro, se falhar tenta registrar
        self.print_separator("Autenticação")
        if not self.login_existing_user():
            if not self.register_user():
                print("❌ Não foi possível autenticar. Abortando testes.")
                return
        
        # Testa operações básicas
        self.print_separator("Operações de Saldo")
        
        print("\n1. Obtendo saldo inicial...")
        self.get_balance()
        
        print("\n2. Definindo saldo inicial...")
        self.set_balance(500.00, "Saldo inicial para testes")
        
        print("\n3. Adicionando valor...")
        self.add_amount(150.50, "Teste de adição")
        
        print("\n4. Subtraindo valor...")
        self.subtract_amount(75.25, "Teste de subtração")
        
        print("\n5. Verificando saldo após operações...")
        final_balance = self.get_balance()
        
        # Testa validações
        self.print_separator("Testes de Validação")
        
        print("\n6. Testando saldo insuficiente...")
        self.test_insufficient_balance()
        
        # Testa histórico
        self.print_separator("Histórico de Operações")
        
        print("\n7. Obtendo histórico...")
        self.get_history()
        
        print("\n8. Resetando saldo...")
        self.reset_balance()
        
        print("\n9. Verificando saldo após reset...")
        self.get_balance()
        
        self.print_separator("Testes Concluídos")
        self.print_success("Todos os testes da API de Saldo foram executados!")


if __name__ == "__main__":
    tester = FinanceAPITester()
    tester.run_all_tests()
