#!/usr/bin/env python3
"""
Script simples para testar criação de transação.
"""

import requests
import json
from datetime import datetime, date

# Configurações
BASE_URL = "http://127.0.0.1:8000"
session = requests.Session()

def register_and_login():
    """Registra e faz login de um usuário."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Registro
    url = f"{BASE_URL}/api/v1/auth/register/"
    data = {
        "email": f"teste_simples_{timestamp}@exemplo.com",
        "username": f"teste_simples_{timestamp}",
        "password": "MinhaSenh@123",
        "password_confirm": "MinhaSenh@123",
        "first_name": "Teste",
        "last_name": "Simples"
    }
    
    response = session.post(url, json=data)
    print(f"Registro: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        token = result['data']['tokens']['access']
        session.headers.update({'Authorization': f'Bearer {token}'})
        print("✅ Usuário autenticado")
        return True
    else:
        print(f"❌ Erro no registro: {response.text}")
        return False

def get_categories():
    """Obtém categorias."""
    url = f"{BASE_URL}/api/v1/finance/categories/"
    response = session.get(url)
    
    print(f"Categorias: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        categories = result.get('results', result) if isinstance(result, dict) and 'results' in result else result
        print(f"✅ {len(categories)} categorias encontradas")
        
        # Mostra primeira categoria de cada tipo
        income_cat = next((c for c in categories if c['category_type'] == 'INCOME'), None)
        expense_cat = next((c for c in categories if c['category_type'] == 'EXPENSE'), None)
        
        if income_cat:
            print(f"   Receita: {income_cat['name']} (ID: {income_cat['id']})")
        if expense_cat:
            print(f"   Despesa: {expense_cat['name']} (ID: {expense_cat['id']})")
            
        return categories
    else:
        print(f"❌ Erro ao obter categorias: {response.text}")
        return []

def create_transaction(category_id, amount, transaction_type, description):
    """Cria uma transação."""
    url = f"{BASE_URL}/api/v1/finance/transactions/"
    data = {
        "amount": str(amount),
        "transaction_type": transaction_type,
        "category": category_id,
        "description": description,
        "transaction_date": date.today().strftime('%Y-%m-%d')
    }
    
    print(f"\nCriando transação:")
    print(f"  Dados: {json.dumps(data, indent=2)}")
    
    response = session.post(url, json=data)
    print(f"  Status: {response.status_code}")
    
    if response.status_code == 201:
        transaction = response.json()
        print(f"✅ Transação criada: {transaction['amount_formatted']} - {transaction['description']}")
        return transaction
    else:
        print(f"❌ Erro ao criar transação:")
        try:
            error_data = response.json()
            print(f"   {json.dumps(error_data, indent=2, ensure_ascii=False)}")
        except:
            print(f"   {response.text}")
        return None

def main():
    print("🧪 Teste Simples de Transação")
    print("="*40)
    
    # Autentica
    if not register_and_login():
        return
    
    # Obtém categorias
    categories = get_categories()
    if not categories:
        return
    
    # Encontra categorias para teste
    income_category = next((c for c in categories if c['category_type'] == 'INCOME'), None)
    expense_category = next((c for c in categories if c['category_type'] == 'EXPENSE'), None)
    
    if not income_category:
        print("❌ Categoria de receita não encontrada")
        return
    
    if not expense_category:
        print("❌ Categoria de despesa não encontrada")
        return
    
    # Testa criação
    print("\n" + "="*40)
    print("Testando criação de transações:")
    
    # Receita
    create_transaction(
        category_id=income_category['id'],
        amount=1000.00,
        transaction_type="INCOME",
        description="Teste de receita"
    )
    
    # Despesa
    create_transaction(
        category_id=expense_category['id'],
        amount=500.00,
        transaction_type="EXPENSE",
        description="Teste de despesa"
    )

if __name__ == "__main__":
    main()
