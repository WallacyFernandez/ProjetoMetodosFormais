"""
Testes para o app de usuários.
"""

import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
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