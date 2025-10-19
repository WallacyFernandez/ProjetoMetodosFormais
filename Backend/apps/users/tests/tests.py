"""
Testes para o app de usuários.
"""

import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import Profile, UserSession

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Testes para o modelo User."""

    def test_create_user_success(self, user_data):
        """Testa criação de usuário com sucesso."""
        user = User.objects.create_user(**user_data)
        
        assert user.email == user_data['email']
        assert user.username == user_data['username']
        assert user.first_name == user_data['first_name']
        assert user.last_name == user_data['last_name']
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser_success(self):
        """Testa criação de superusuário."""
        user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='AdminPassword123!',
            first_name='Admin',
            last_name='User'
        )
        
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.is_active is True

    def test_user_full_name_property(self, user):
        """Testa a propriedade full_name do usuário."""
        expected_name = f"{user.first_name} {user.last_name}"
        assert user.full_name == expected_name

    def test_user_get_short_name(self, user):
        """Testa o método get_short_name."""
        assert user.get_short_name() == user.first_name

    def test_user_str_representation(self, user):
        """Testa a representação string do usuário."""
        expected_str = f"{user.first_name} {user.last_name} ({user.email})"
        assert str(user) == expected_str

    def test_email_uniqueness(self, user_data):
        """Testa a unicidade do email."""
        User.objects.create_user(**user_data)
        
        with pytest.raises(Exception):  # IntegrityError or ValidationError
            User.objects.create_user(**user_data)

    def test_user_soft_delete(self, user):
        """Testa o soft delete do usuário."""
        assert user.is_active is True
        
        user.soft_delete()
        
        assert user.is_active is False

    def test_user_restore(self, user):
        """Testa a restauração do usuário."""
        user.soft_delete()
        assert user.is_active is False
        
        user.restore()
        assert user.is_active is True

    def test_active_manager(self, user_data):
        """Testa o manager de usuários ativos."""
        # Cria usuário ativo
        active_user = User.objects.create_user(**user_data)
        
        # Cria usuário inativo
        inactive_data = user_data.copy()
        inactive_data['email'] = 'inactive@example.com'
        inactive_data['username'] = 'inactive'
        inactive_user = User.objects.create_user(**inactive_data)
        inactive_user.soft_delete()
        
        # Testa o manager active
        active_users = User.active.all()
        all_users = User.objects.all()
        
        assert active_users.count() == 1
        assert all_users.count() == 2
        assert active_user in active_users
        assert inactive_user not in active_users


@pytest.mark.django_db
class TestProfileModel:
    """Testes para o modelo Profile."""

    def test_create_profile(self, user):
        """Testa criação de perfil de usuário."""
        profile = Profile.objects.create(
            user=user,
            document='12345678901',
            address='Rua Teste, 123',
            city='São Paulo',
            state='SP',
            zip_code='01234-567',
            country='Brasil'
        )
        
        assert profile.user == user
        assert profile.document == '12345678901'
        assert profile.city == 'São Paulo'
        assert profile.is_active is True

    def test_profile_str_representation(self, user):
        """Testa a representação string do perfil."""
        profile = Profile.objects.create(user=user)
        expected_str = f"Perfil de {user.full_name}"
        assert str(profile) == expected_str

    def test_profile_default_values(self, user):
        """Testa os valores padrão do perfil."""
        profile = Profile.objects.create(user=user)
        
        assert profile.email_notifications is True
        assert profile.sms_notifications is False
        assert profile.language == 'pt-br'
        assert profile.country == 'Brasil'


@pytest.mark.django_db
class TestUserSessionModel:
    """Testes para o modelo UserSession."""

    def test_create_user_session(self, user):
        """Testa criação de sessão de usuário."""
        session = UserSession.objects.create(
            user=user,
            session_key='test_session_key_123',
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0 Test Browser',
            is_active=True
        )
        
        assert session.user == user
        assert session.session_key == 'test_session_key_123'
        assert session.ip_address == '192.168.1.1'
        assert session.is_active is True

    def test_user_session_str_representation(self, user):
        """Testa a representação string da sessão."""
        session = UserSession.objects.create(
            user=user,
            session_key='test_session_key_123',
            ip_address='192.168.1.1',
            user_agent='Test Browser'
        )
        
        expected_str = f"Sessão de {user.full_name} - 192.168.1.1"
        assert str(session) == expected_str


# Testes de API
@pytest.mark.django_db
class TestUserAPI:
    """Testes para a API de usuários."""
    
    @pytest.fixture
    def user_data(self):
        """Dados básicos de usuário para testes de API."""
        return {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'TestPassword123!',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '+5511999999999',
            'bio': 'Test bio'
        }
        
    @pytest.fixture
    def profile_data(self):
        """Dados de perfil para testes de API."""
        return {
            'document': '12345678901',
            'address': 'Rua Teste, 123',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '01234567',
            'country': 'Brasil',
            'email_notifications': True,
            'sms_notifications': False,
            'language': 'pt-br'
        }
    
    @pytest.fixture
    def api_client(self):
        """Cliente de API para testes."""
        return APIClient()
    
    def test_create_user_success(self, api_client, user_data):
        """Testa criação de usuário via API."""
        url = reverse('users:user-list')
        data = {**user_data, 'password_confirm': user_data['password']}
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        
        user = User.objects.get(email=user_data['email'])
        assert user.username == user_data['username']
        assert user.first_name == user_data['first_name']
        assert user.last_name == user_data['last_name']
    
    def test_create_user_with_profile(self, api_client, user_data, profile_data):
        """Testa criação de usuário com perfil via API."""
        url = reverse('users:user-list')
        data = {
            **user_data, 
            'password_confirm': user_data['password'],
            'profile': profile_data
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert Profile.objects.count() == 1
        
        user = User.objects.get(email=user_data['email'])
        profile = user.profile
        assert profile.city == profile_data['city']
        assert profile.state == profile_data['state']
    
    def test_create_user_invalid_email(self, api_client, user_data):
        """Testa criação de usuário com email duplicado."""
        User.objects.create_user(**user_data)
        
        url = reverse('users:user-list')
        data = {
            'email': user_data['email'],  # Email duplicado
            'username': 'otheruser',
            'password': 'TestPassword123!',
            'password_confirm': 'TestPassword123!',
            'first_name': 'Other',
            'last_name': 'User'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
    
    def test_create_user_password_mismatch(self, api_client, user_data):
        """Testa criação de usuário com senhas diferentes."""
        url = reverse('users:user-list')
        data = {
            **user_data,
            'password_confirm': 'DifferentPassword123!'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password_confirm' in response.data
    
    def test_get_current_user_authenticated(self, api_client, user_data):
        """Testa obtenção do usuário logado."""
        user = User.objects.create_user(**user_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:user-current-user')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['username'] == user.username
    
    def test_get_current_user_unauthenticated(self, api_client):
        """Testa obtenção do usuário logado sem autenticação."""
        url = reverse('users:user-current-user')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_current_user(self, api_client, user_data):
        """Testa atualização do usuário logado."""
        user = User.objects.create_user(**user_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:user-current-user')
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'Updated bio'
        }
        
        response = api_client.patch(url, update_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.first_name == 'Updated'
        assert user.last_name == 'Name'
        assert user.bio == 'Updated bio'
    
    def test_change_password_success(self, api_client, user_data):
        """Testa mudança de senha com sucesso."""
        user = User.objects.create_user(**user_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:user-change-password')
        password_data = {
            'old_password': user_data['password'],
            'new_password': 'NewPassword123!',
            'new_password_confirm': 'NewPassword123!'
        }
        
        response = api_client.post(url, password_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'Senha alterada com sucesso' in response.data['detail']
    
    def test_change_password_wrong_old_password(self, api_client, user_data):
        """Testa mudança de senha com senha atual incorreta."""
        user = User.objects.create_user(**user_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:user-change-password')
        password_data = {
            'old_password': 'WrongPassword123!',
            'new_password': 'NewPassword123!',
            'new_password_confirm': 'NewPassword123!'
        }
        
        response = api_client.post(url, password_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'old_password' in response.data
    
    def test_soft_delete_user(self, api_client, user_data):
        """Testa soft delete do usuário."""
        user = User.objects.create_user(**user_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:user-detail', kwargs={'pk': user.pk})
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        user.refresh_from_db()
        assert user.is_active is False


@pytest.mark.django_db
class TestProfileAPI:
    """Testes para a API de perfis."""
    
    @pytest.fixture
    def user_data(self):
        """Dados básicos de usuário para testes de API."""
        return {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'TestPassword123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
    @pytest.fixture
    def profile_data(self):
        """Dados de perfil para testes de API."""
        return {
            'document': '12345678901',
            'address': 'Rua Teste, 123',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '01234567',
            'country': 'Brasil',
            'email_notifications': True,
            'sms_notifications': False,
            'language': 'pt-br'
        }
    
    @pytest.fixture
    def api_client(self):
        """Cliente de API para testes."""
        return APIClient()
    
    def test_create_profile_success(self, api_client, user_data, profile_data):
        """Testa criação de perfil via API."""
        user = User.objects.create_user(**user_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:profile-list')
        response = api_client.post(url, profile_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Profile.objects.count() == 1
        
        profile = Profile.objects.get(user=user)
        assert profile.city == profile_data['city']
        assert profile.state == profile_data['state']
    
    def test_create_profile_already_exists(self, api_client, user_data, profile_data):
        """Testa criação de perfil quando já existe."""
        user = User.objects.create_user(**user_data)
        Profile.objects.create(user=user, **profile_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:profile-list')
        response = api_client.post(url, profile_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Você já possui um perfil' in response.data['detail']
    
    def test_get_current_profile(self, api_client, user_data, profile_data):
        """Testa obtenção do perfil atual."""
        user = User.objects.create_user(**user_data)
        profile = Profile.objects.create(user=user, **profile_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:profile-current-profile')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['city'] == profile.city
        assert response.data['state'] == profile.state
    
    def test_get_current_profile_auto_create(self, api_client, user_data):
        """Testa obtenção do perfil atual com criação automática."""
        user = User.objects.create_user(**user_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:profile-current-profile')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert Profile.objects.count() == 1
        assert response.data['country'] == 'Brasil'  # Valor padrão
    
    def test_update_current_profile(self, api_client, user_data, profile_data):
        """Testa atualização do perfil atual."""
        user = User.objects.create_user(**user_data)
        profile = Profile.objects.create(user=user, **profile_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:profile-current-profile')
        update_data = {
            'city': 'Rio de Janeiro',
            'state': 'RJ',
            'language': 'en'
        }
        
        response = api_client.patch(url, update_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        profile.refresh_from_db()
        assert profile.city == 'Rio de Janeiro'
        assert profile.state == 'RJ'
        assert profile.language == 'en'
    
    def test_update_current_profile_auto_create(self, api_client, user_data):
        """Testa atualização do perfil atual com criação automática."""
        user = User.objects.create_user(**user_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:profile-current-profile')
        update_data = {
            'city': 'Belo Horizonte',
            'state': 'MG'
        }
        
        response = api_client.patch(url, update_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert Profile.objects.count() == 1
        
        profile = Profile.objects.get(user=user)
        assert profile.city == 'Belo Horizonte'
        assert profile.state == 'MG'
    
    def test_soft_delete_profile(self, api_client, user_data, profile_data):
        """Testa soft delete do perfil."""
        user = User.objects.create_user(**user_data)
        profile = Profile.objects.create(user=user, **profile_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:profile-detail', kwargs={'pk': profile.pk})
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        profile.refresh_from_db()
        assert profile.is_active is False
    
    def test_profile_validation_document(self, api_client, user_data, profile_data):
        """Testa validação de documento."""
        user = User.objects.create_user(**user_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:profile-list')
        data = {**profile_data, 'document': '123'}  # Documento inválido
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'document' in response.data
    
    def test_profile_validation_state(self, api_client, user_data, profile_data):
        """Testa validação de estado."""
        user = User.objects.create_user(**user_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:profile-list')
        data = {**profile_data, 'state': 'XX'}  # Estado inválido
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'state' in response.data
    
    def test_profile_validation_zip_code(self, api_client, user_data, profile_data):
        """Testa validação de CEP."""
        user = User.objects.create_user(**user_data)
        api_client.force_authenticate(user=user)
        
        url = reverse('users:profile-list')
        data = {**profile_data, 'zip_code': '123'}  # CEP inválido
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'zip_code' in response.data
    
    def test_profile_access_other_user_forbidden(self, api_client, user_data, profile_data):
        """Testa acesso ao perfil de outro usuário."""
        user = User.objects.create_user(**user_data)
        other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='TestPassword123!',
            first_name='Other',
            last_name='User'
        )
        other_profile = Profile.objects.create(user=other_user, **profile_data)
        
        api_client.force_authenticate(user=user)
        
        url = reverse('users:profile-detail', kwargs={'pk': other_profile.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND