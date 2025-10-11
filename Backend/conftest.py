"""
Configurações globais para testes com pytest.
"""

import os
import sys
import django
from django.conf import settings

# Configurar o Django antes de qualquer import
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

import pytest


@pytest.fixture
def api_client():
    """Fixture que retorna um cliente da API."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user_data():
    """Fixture com dados básicos de usuário para testes."""
    return {
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'TestPassword123!',
        'first_name': 'Test',
        'last_name': 'User',
        'phone': '+5511999999999'
    }


@pytest.fixture
def user(db, user_data):
    """Fixture que cria um usuário para testes."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(**user_data)


@pytest.fixture
def superuser(db):
    """Fixture que cria um superusuário para testes."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='AdminPassword123!',
        first_name='Admin',
        last_name='User'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Fixture que retorna um cliente autenticado."""
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def admin_client(api_client, superuser):
    """Fixture que retorna um cliente autenticado como admin."""
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(superuser)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client
