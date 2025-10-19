"""
Testes para o app core.
Foca apenas nos managers customizados e funcionalidades específicas do core.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import ActiveManager, AllObjectsManager

User = get_user_model()


class TestActiveManager(TestCase):
    """Testes para o manager de objetos ativos."""

    def setUp(self):
        """Configuração inicial."""
        self.active_user = User.objects.create_user(
            username='activeuser',
            email='active@example.com',
            password='testpass123',
            first_name='Active',
            last_name='User'
        )
        
        self.inactive_user = User.objects.create_user(
            username='inactiveuser',
            email='inactive@example.com',
            password='testpass123',
            first_name='Inactive',
            last_name='User'
        )
        self.inactive_user.soft_delete()

    def test_active_manager_filters_active_objects(self):
        """Testa se o manager ativo filtra apenas objetos ativos."""
        active_users = User.active.all()
        
        self.assertEqual(active_users.count(), 1)
        self.assertIn(self.active_user, active_users)
        self.assertNotIn(self.inactive_user, active_users)

    def test_active_manager_vs_default_manager(self):
        """Testa diferença entre manager ativo e padrão."""
        all_users = User.objects.all()
        active_users = User.active.all()
        
        self.assertEqual(all_users.count(), 2)
        self.assertEqual(active_users.count(), 1)

    def test_active_manager_in_queryset(self):
        """Testa uso do manager ativo em querysets."""
        active_count = User.active.filter(first_name='Active').count()
        
        self.assertEqual(active_count, 1)


class TestAllObjectsManager(TestCase):
    """Testes para o manager de todos os objetos."""

    def setUp(self):
        """Configuração inicial."""
        self.active_user = User.objects.create_user(
            username='activeuser',
            email='active@example.com',
            password='testpass123',
            first_name='Active',
            last_name='User'
        )
        
        self.inactive_user = User.objects.create_user(
            username='inactiveuser',
            email='inactive@example.com',
            password='testpass123',
            first_name='Inactive',
            last_name='User'
        )
        self.inactive_user.soft_delete()

    def test_all_objects_manager_returns_all(self):
        """Testa se o manager all_objects retorna todos os objetos."""
        all_users = User.all_objects.all()
        
        self.assertEqual(all_users.count(), 2)
        self.assertIn(self.active_user, all_users)
        self.assertIn(self.inactive_user, all_users)

    def test_all_objects_manager_vs_default_manager(self):
        """Testa se all_objects manager é igual ao manager padrão."""
        all_users_default = User.objects.all()
        all_users_all = User.all_objects.all()
        
        self.assertEqual(all_users_default.count(), all_users_all.count())
        self.assertEqual(list(all_users_default), list(all_users_all))

    def test_all_objects_manager_with_filters(self):
        """Testa uso do manager all_objects com filtros."""
        inactive_count = User.all_objects.filter(is_active=False).count()
        
        self.assertEqual(inactive_count, 1)


class TestCoreManagerIntegration(TestCase):
    """Testes de integração dos managers do core."""

    def test_managers_work_with_user_model(self):
        """Testa se os managers do core funcionam corretamente com o modelo User."""
        # Criar usuário ativo
        active_user = User.objects.create_user(
            username='activeuser',
            email='active@example.com',
            password='testpass123',
            first_name='Active',
            last_name='User'
        )
        
        # Criar usuário inativo
        inactive_user = User.objects.create_user(
            username='inactiveuser',
            email='inactive@example.com',
            password='testpass123',
            first_name='Inactive',
            last_name='User'
        )
        inactive_user.soft_delete()
        
        # Testar ActiveManager
        active_users = User.active.all()
        self.assertEqual(active_users.count(), 1)
        self.assertIn(active_user, active_users)
        self.assertNotIn(inactive_user, active_users)
        
        # Testar AllObjectsManager
        all_users = User.all_objects.all()
        self.assertEqual(all_users.count(), 2)
        self.assertIn(active_user, all_users)
        self.assertIn(inactive_user, all_users)
