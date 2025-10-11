#!/usr/bin/env python3
"""
Script para testar a API de transações e verificar a estrutura da resposta
"""

import requests
import json
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
BASE_URL = "http://localhost:8000"
USERNAME = "wallacyfernandez"
PASSWORD = "123456"

def get_auth_token():
    """Obter token de autenticação"""
    login_url = f"{BASE_URL}/api/v1/auth/login/"
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        response.raise_for_status()
        
        data = response.json()
        return data.get("access")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer login: {e}")
        return None

def test_transactions_api():
    """Testar API de transações"""
    token = get_auth_token()
    if not token:
        print("❌ Não foi possível obter token de autenticação")
        return
    
    print(f"✅ Token obtido: {token[:20]}...")
    
    # Headers com autenticação
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Testar endpoint de transações
    transactions_url = f"{BASE_URL}/api/v1/finance/transactions/"
    
    try:
        print(f"\n🔍 Testando: {transactions_url}")
        response = requests.get(transactions_url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Tipo de resposta: {type(data)}")
        print(f"📊 É lista: {isinstance(data, list)}")
        print(f"📊 É dicionário: {isinstance(data, dict)}")
        
        if isinstance(data, dict):
            print(f"📊 Chaves do dicionário: {list(data.keys())}")
            if "results" in data:
                print(f"📊 Quantidade de resultados: {len(data['results'])}")
                print(f"📊 Primeiro resultado: {data['results'][0] if data['results'] else 'Nenhum'}")
            else:
                print(f"📊 Conteúdo: {data}")
        elif isinstance(data, list):
            print(f"📊 Quantidade de transações: {len(data)}")
            print(f"📊 Primeira transação: {data[0] if data else 'Nenhuma'}")
        
        print(f"\n📋 Resposta completa:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"📊 Status: {e.response.status_code}")
            print(f"📊 Resposta: {e.response.text}")

if __name__ == "__main__":
    print("🚀 Testando API de Transações")
    print("=" * 50)
    test_transactions_api()