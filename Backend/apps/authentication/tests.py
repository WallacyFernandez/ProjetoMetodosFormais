"""
Testes para o app de autenticação.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuthentication:
    """Testes para endpoints de autenticação."""

    def test_login_success(self, api_client, user):
        """Testa login com credenciais válidas."""
        url = reverse('authentication:login')
        data = {
            'email': user.email,
            'password': 'TestPassword123!'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert 'tokens' in response.data['data']
        assert 'access' in response.data['data']['tokens']
        assert 'refresh' in response.data['data']['tokens']

    def test_login_invalid_credentials(self, api_client, user):
        """Testa login com credenciais inválidas."""
        url = reverse('authentication:login')
        data = {
            'email': user.email,
            'password': 'wrong_password'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['success'] is False

    def test_login_inactive_user(self, api_client, user):
        """Testa login com usuário inativo."""
        user.is_active = False
        user.save()
        
        url = reverse('authentication:login')
        data = {
            'email': user.email,
            'password': 'TestPassword123!'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['success'] is False

    def test_register_success(self, api_client):
        """Testa registro de novo usuário."""
        url = reverse('authentication:register')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'NewPassword123!',
            'password_confirm': 'NewPassword123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] is True
        assert User.objects.filter(email='newuser@example.com').exists()

    def test_register_duplicate_email(self, api_client, user):
        """Testa registro com email já existente."""
        url = reverse('authentication:register')
        data = {
            'email': user.email,
            'username': 'newuser',
            'password': 'NewPassword123!',
            'password_confirm': 'NewPassword123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['success'] is False

    def test_register_password_mismatch(self, api_client):
        """Testa registro com senhas diferentes."""
        url = reverse('authentication:register')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'NewPassword123!',
            'password_confirm': 'DifferentPassword123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['success'] is False

    def test_me_authenticated(self, authenticated_client, user):
        """Testa endpoint /me/ com usuário autenticado."""
        url = reverse('authentication:me')
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert response.data['data']['email'] == user.email

    def test_me_unauthenticated(self, api_client):
        """Testa endpoint /me/ sem autenticação."""
        url = reverse('authentication:me')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_password_success(self, authenticated_client, user):
        """Testa alteração de senha com sucesso."""
        url = reverse('authentication:change_password')
        data = {
            'old_password': 'TestPassword123!',
            'new_password': 'NewPassword123!',
            'new_password_confirm': 'NewPassword123!'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True

    def test_change_password_wrong_old_password(self, authenticated_client, user):
        """Testa alteração de senha com senha atual incorreta."""
        url = reverse('authentication:change_password')
        data = {
            'old_password': 'WrongPassword',
            'new_password': 'NewPassword123!',
            'new_password_confirm': 'NewPassword123!'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['success'] is False

    def test_logout_success(self, authenticated_client):
        """Testa logout com sucesso."""
        url = reverse('authentication:logout')
        
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True