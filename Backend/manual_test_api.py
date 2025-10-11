#!/usr/bin/env python
"""
Script de teste para verificar se a API está funcionando corretamente.
"""

import requests
import json

# Configurações
BASE_URL = "http://127.0.0.1:8000/api/v1"
AUTH_URL = f"{BASE_URL}/auth"

def test_api_endpoints():
    """Testa os principais endpoints da API."""
    print("🚀 Testando API Django REST Framework...")
    print("=" * 50)
    
    # 1. Testar documentação
    try:
        response = requests.get("http://127.0.0.1:8000/api/docs/")
        if response.status_code == 200:
            print("✅ Documentação Swagger acessível")
        else:
            print(f"❌ Erro na documentação: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar documentação: {e}")
    
    # 2. Testar registro de usuário
    print("\n📝 Testando registro de usuário...")
    register_data = {
        "email": "teste@exemplo.com",
        "username": "teste123",
        "password": "MinhaSenh@123",
        "password_confirm": "MinhaSenh@123",
        "first_name": "Teste",
        "last_name": "Usuario"
    }
    
    try:
        response = requests.post(f"{AUTH_URL}/register/", json=register_data)
        if response.status_code == 201:
            print("✅ Registro de usuário funcionando")
            user_data = response.json()
            access_token = user_data['data']['tokens']['access']
            print(f"   Token recebido: {access_token[:20]}...")
        else:
            print(f"❌ Erro no registro: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro ao registrar usuário: {e}")
        return None
    
    # 3. Testar login
    print("\n🔐 Testando login...")
    login_data = {
        "email": "teste@exemplo.com",
        "password": "MinhaSenh@123"
    }
    
    try:
        response = requests.post(f"{AUTH_URL}/login/", json=login_data)
        if response.status_code == 200:
            print("✅ Login funcionando")
            login_response = response.json()
            access_token = login_response['data']['tokens']['access']
        else:
            print(f"❌ Erro no login: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Erro ao fazer login: {e}")
        return None
    
    # 4. Testar endpoint /me/ autenticado
    print("\n👤 Testando endpoint /me/...")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{AUTH_URL}/me/", headers=headers)
        if response.status_code == 200:
            print("✅ Endpoint /me/ funcionando")
            user_info = response.json()
            print(f"   Usuário: {user_info['data']['full_name']}")
        else:
            print(f"❌ Erro no endpoint /me/: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar /me/: {e}")
    
    # 5. Testar admin
    print("\n⚙️ Testando acesso ao admin...")
    try:
        response = requests.get("http://127.0.0.1:8000/admin/")
        if response.status_code == 200:
            print("✅ Admin Django acessível")
        else:
            print(f"❌ Erro no admin: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar admin: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Teste concluído!")
    print("\n📋 URLs importantes:")
    print(f"   API Base: {BASE_URL}")
    print(f"   Documentação: http://127.0.0.1:8000/api/docs/")
    print(f"   Admin: http://127.0.0.1:8000/admin/")
    print(f"   ReDoc: http://127.0.0.1:8000/api/redoc/")

if __name__ == "__main__":
    test_api_endpoints()
