"""
Testes para o app de finanças.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from django.http import HttpRequest
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal

from apps.finance.models import UserBalance, BalanceHistory
from apps.finance.admin import UserBalanceAdmin, BalanceHistoryAdmin

User = get_user_model()


class TestUserBalanceModel(TestCase):
    """Testes para o modelo UserBalance."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        # Usar get_or_create para evitar conflitos com signals
        self.balance, created = UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('100.00')}
        )
        # Se já existia, definir o saldo para o valor de teste
        if not created:
            self.balance.current_balance = Decimal('100.00')
            self.balance.save()
    
    def test_user_balance_creation(self):
        """Testa a criação de um saldo de usuário."""
        self.assertEqual(self.balance.user, self.user)
        self.assertEqual(self.balance.current_balance, Decimal('100.00'))
        self.assertTrue(self.balance.created_at)
        self.assertTrue(self.balance.last_updated)
    
    def test_add_amount(self):
        """Testa a adição de valor ao saldo."""
        initial_balance = self.balance.current_balance
        amount_to_add = Decimal('50.00')
        
        new_balance = self.balance.add_amount(amount_to_add)
        
        self.assertEqual(new_balance, initial_balance + amount_to_add)
        self.assertEqual(self.balance.current_balance, Decimal('150.00'))
    
    def test_subtract_amount(self):
        """Testa a subtração de valor do saldo."""
        initial_balance = self.balance.current_balance
        amount_to_subtract = Decimal('30.00')
        
        new_balance = self.balance.subtract_amount(amount_to_subtract)
        
        self.assertEqual(new_balance, initial_balance - amount_to_subtract)
        self.assertEqual(self.balance.current_balance, Decimal('70.00'))
    
    def test_set_balance(self):
        """Testa a definição de um novo saldo."""
        new_amount = Decimal('200.00')
        
        new_balance = self.balance.set_balance(new_amount)
        
        self.assertEqual(new_balance, new_amount)
        self.assertEqual(self.balance.current_balance, new_amount)
    
    def test_add_negative_amount_raises_error(self):
        """Testa que adicionar valor negativo gera erro."""
        with self.assertRaises(ValueError):
            self.balance.add_amount(-50)
    
    def test_subtract_negative_amount_raises_error(self):
        """Testa que subtrair valor negativo gera erro."""
        with self.assertRaises(ValueError):
            self.balance.subtract_amount(-30)
    
    def test_balance_formatted(self):
        """Testa a formatação do saldo."""
        self.balance.current_balance = Decimal('1234.56')
        self.balance.save()
        
        formatted = self.balance.balance_formatted
        self.assertEqual(formatted, 'R$ 1.234,56')
    
    def test_str_method(self):
        """Testa o método __str__ do modelo."""
        expected = f"Saldo de {self.user.full_name}: R$ {self.balance.current_balance}"
        self.assertEqual(str(self.balance), expected)


class TestBalanceHistoryModel(TestCase):
    """Testes para o modelo BalanceHistory."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        # Usar get_or_create para evitar conflitos com signals
        self.balance, created = UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('100.00')}
        )
        if not created:
            self.balance.current_balance = Decimal('100.00')
            self.balance.save()
    
    def test_balance_history_creation(self):
        """Testa a criação de um histórico de saldo."""
        history = BalanceHistory.objects.create(
            user_balance=self.balance,
            operation='ADD',
            amount=Decimal('50.00'),
            previous_balance=Decimal('100.00'),
            new_balance=Decimal('150.00'),
            description='Teste de adição'
        )
        
        self.assertEqual(history.user_balance, self.balance)
        self.assertEqual(history.operation, 'ADD')
        self.assertEqual(history.amount, Decimal('50.00'))
        self.assertEqual(history.previous_balance, Decimal('100.00'))
        self.assertEqual(history.new_balance, Decimal('150.00'))
        self.assertEqual(history.description, 'Teste de adição')


class TestUserBalanceAPI(APITestCase):
    """Testes para a API de saldo do usuário."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Autentica o usuário
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        self.balance_url = reverse('finance:balance-list')
    
    def test_get_balance_creates_if_not_exists(self):
        """Testa que GET cria saldo se não existir."""
        response = self.client.get(self.balance_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Com signals, o saldo pode já existir com valor padrão
        self.assertIn('current_balance', response.data)
        
        # Verifica se foi criado no banco
        self.assertTrue(UserBalance.objects.filter(user=self.user).exists())
    
    def test_add_amount_success(self):
        """Testa adição de valor com sucesso."""
        # Garantir que temos um saldo inicial conhecido
        balance, created = UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('0.00')}
        )
        if not created:
            balance.current_balance = Decimal('0.00')
            balance.save()
        
        url = reverse('finance:balance-add-amount')
        data = {
            'amount': '100.50',
            'description': 'Teste de adição'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['balance']['current_balance'], '100.50')
        
        # Verifica histórico
        balance.refresh_from_db()
        history = BalanceHistory.objects.filter(user_balance=balance).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.operation, 'ADD')
        self.assertEqual(history.amount, Decimal('100.50'))
    
    def test_add_amount_invalid_data(self):
        """Testa adição com dados inválidos."""
        url = reverse('finance:balance-add-amount')
        data = {
            'amount': '-50.00'  # Valor negativo
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)
    
    def test_subtract_amount_success(self):
        """Testa subtração de valor com sucesso."""
        # Primeiro adiciona saldo
        balance, created = UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('200.00')}
        )
        if not created:
            balance.current_balance = Decimal('200.00')
            balance.save()
        
        url = reverse('finance:balance-subtract-amount')
        data = {
            'amount': '50.25',
            'description': 'Teste de subtração'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance']['current_balance'], '149.75')
    
    def test_subtract_amount_insufficient_balance(self):
        """Testa subtração com saldo insuficiente."""
        balance, created = UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('30.00')}
        )
        if not created:
            balance.current_balance = Decimal('30.00')
            balance.save()
        
        url = reverse('finance:balance-subtract-amount')
        data = {
            'amount': '50.00'  # Maior que o saldo disponível
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('Saldo insuficiente', response.data['error'])
    
    def test_set_balance_success(self):
        """Testa definição de saldo com sucesso."""
        url = reverse('finance:balance-set-balance')
        data = {
            'amount': '500.00',
            'description': 'Saldo inicial'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance']['current_balance'], '500.00')
    
    def test_set_balance_success(self):
        """Testa definição de saldo com sucesso."""
        url = reverse('finance:balance-set-balance')
        data = {
            'amount': '500.00',
            'description': 'Saldo inicial'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance']['current_balance'], '500.00')
        
        # Verifica histórico
        balance = UserBalance.objects.get(user=self.user)
        history = BalanceHistory.objects.filter(user_balance=balance).first()
        self.assertEqual(history.operation, 'SET')
    
    def test_reset_balance_success(self):
        """Testa reset do saldo com sucesso."""
        balance, created = UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('300.00')}
        )
        if not created:
            balance.current_balance = Decimal('300.00')
            balance.save()
        
        url = reverse('finance:balance-reset-balance')
        
        response = self.client.post(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance']['current_balance'], '0.00')
        
        # Verifica histórico
        balance.refresh_from_db()
        history = BalanceHistory.objects.filter(user_balance=balance).first()
        self.assertEqual(history.operation, 'RESET')
    
    def test_get_balance_history(self):
        """Testa obtenção do histórico de saldo."""
        balance, created = UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('100.00')}
        )
        if not created:
            balance.current_balance = Decimal('100.00')
            balance.save()
        
        # Cria alguns registros de histórico
        BalanceHistory.objects.create(
            user_balance=balance,
            operation='ADD',
            amount=Decimal('100.00'),
            previous_balance=Decimal('0.00'),
            new_balance=Decimal('100.00'),
            description='Saldo inicial'
        )
        
        url = reverse('finance:balance-history')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se a resposta tem a estrutura de paginação ou lista direta
        if 'results' in response.data:
            # Resposta paginada
            results = response.data['results']
            self.assertGreaterEqual(len(results), 1)
            add_operations = [item for item in results if item['operation'] == 'ADD']
            self.assertGreater(len(add_operations), 0)
        else:
            # Resposta direta (lista)
            self.assertGreaterEqual(len(response.data), 1)
            add_operations = [item for item in response.data if item['operation'] == 'ADD']
            self.assertGreater(len(add_operations), 0)
    
    def test_unauthorized_access(self):
        """Testa acesso não autorizado."""
        self.client.credentials()  # Remove autenticação
        
        response = self.client.get(self.balance_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_can_only_access_own_balance(self):
        """Testa que usuário só pode acessar seu próprio saldo."""
        # Cria outro usuário
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123',
            first_name='Other',
            last_name='User'
        )
        balance, created = UserBalance.objects.get_or_create(
            user=other_user,
            defaults={'current_balance': Decimal('999.99')}
        )
        if not created:
            balance.current_balance = Decimal('999.99')
            balance.save()
        
        # Faz requisição como primeiro usuário
        response = self.client.get(self.balance_url)
        
        # Deve retornar o saldo do primeiro usuário, não do outro
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # O saldo pode ser diferente devido aos signals, mas deve ser do usuário correto
        user_balance = UserBalance.objects.get(user=self.user)
        self.assertEqual(response.data['current_balance'], str(user_balance.current_balance))


class TestUserBalanceAdmin(TestCase):
    """Testes para o admin de UserBalance."""
    
    def setUp(self):
        self.site = AdminSite()
        self.admin = UserBalanceAdmin(UserBalance, self.site)
        
        # Cria usuário admin
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        
        # Cria usuário comum
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Usar get_or_create para evitar conflitos
        self.balance, created = UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('100.00')}
        )
        if not created:
            self.balance.current_balance = Decimal('100.00')
            self.balance.save()
        
        # Cria request mock
        self.request = HttpRequest()
        self.request.user = self.admin_user
    
    def test_list_display(self):
        """Testa se os campos corretos são exibidos na lista."""
        expected_fields = ['user', 'current_balance', 'balance_formatted', 'last_updated', 'created_at']
        self.assertEqual(list(self.admin.list_display), expected_fields)
    
    def test_list_filter(self):
        """Testa se os filtros corretos estão configurados."""
        expected_filters = ['created_at', 'last_updated']
        self.assertEqual(list(self.admin.list_filter), expected_filters)
    
    def test_search_fields(self):
        """Testa se os campos de busca estão corretos."""
        expected_fields = ['user__email', 'user__first_name', 'user__last_name']
        self.assertEqual(list(self.admin.search_fields), expected_fields)
    
    def test_readonly_fields(self):
        """Testa se os campos readonly estão configurados."""
        expected_fields = ['created_at', 'updated_at', 'last_updated']
        self.assertEqual(list(self.admin.readonly_fields), expected_fields)
    
    def test_ordering(self):
        """Testa se a ordenação está correta."""
        expected_ordering = ['-last_updated']
        self.assertEqual(list(self.admin.ordering), expected_ordering)
    
    def test_has_add_permission_false(self):
        """Testa se não é permitido adicionar saldos pelo admin."""
        self.assertFalse(self.admin.has_add_permission(self.request))
    
    def test_has_change_permission_true(self):
        """Testa se é permitido editar saldos pelo admin."""
        self.assertTrue(self.admin.has_change_permission(self.request))
        self.assertTrue(self.admin.has_change_permission(self.request, self.balance))
    
    def test_has_delete_permission_true(self):
        """Testa se é permitido deletar saldos pelo admin."""
        self.assertTrue(self.admin.has_delete_permission(self.request))
        self.assertTrue(self.admin.has_delete_permission(self.request, self.balance))


class TestBalanceHistoryAdmin(TestCase):
    """Testes para o admin de BalanceHistory."""
    
    def setUp(self):
        self.site = AdminSite()
        self.admin = BalanceHistoryAdmin(BalanceHistory, self.site)
        
        # Cria usuário admin
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        
        # Cria usuário comum
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Usar get_or_create para evitar conflitos
        self.balance, created = UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('100.00')}
        )
        if not created:
            self.balance.current_balance = Decimal('100.00')
            self.balance.save()
        
        self.history = BalanceHistory.objects.create(
            user_balance=self.balance,
            operation='ADD',
            amount=Decimal('50.00'),
            previous_balance=Decimal('50.00'),
            new_balance=Decimal('100.00'),
            description='Teste'
        )
        
        # Cria request mock
        self.request = HttpRequest()
        self.request.user = self.admin_user
    
    def test_list_display(self):
        """Testa se os campos corretos são exibidos na lista."""
        expected_fields = ['user_balance', 'operation', 'amount', 'previous_balance', 'new_balance', 'created_at']
        self.assertEqual(list(self.admin.list_display), expected_fields)
    
    def test_list_filter(self):
        """Testa se os filtros corretos estão configurados."""
        expected_filters = ['operation', 'created_at']
        self.assertEqual(list(self.admin.list_filter), expected_filters)
    
    def test_search_fields(self):
        """Testa se os campos de busca estão corretos."""
        expected_fields = ['user_balance__user__email', 'user_balance__user__first_name', 'description']
        self.assertEqual(list(self.admin.search_fields), expected_fields)
    
    def test_readonly_fields(self):
        """Testa se os campos readonly estão configurados."""
        expected_fields = ['created_at', 'updated_at']
        self.assertEqual(list(self.admin.readonly_fields), expected_fields)
    
    def test_ordering(self):
        """Testa se a ordenação está correta."""
        expected_ordering = ['-created_at']
        self.assertEqual(list(self.admin.ordering), expected_ordering)
    
    def test_has_add_permission_false(self):
        """Testa se não é permitido adicionar histórico pelo admin."""
        self.assertFalse(self.admin.has_add_permission(self.request))
    
    def test_has_change_permission_false(self):
        """Testa se não é permitido editar histórico pelo admin."""
        self.assertFalse(self.admin.has_change_permission(self.request))
        self.assertFalse(self.admin.has_change_permission(self.request, self.history))
    
    def test_has_delete_permission_false(self):
        """Testa se não é permitido deletar histórico pelo admin."""
        self.assertFalse(self.admin.has_delete_permission(self.request))
        self.assertFalse(self.admin.has_delete_permission(self.request, self.history))


class TestAdminIntegration(TestCase):
    """Testes de integração do admin com o Django."""
    
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Usar get_or_create para evitar conflitos
        self.balance, created = UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('250.75')}
        )
        if not created:
            self.balance.current_balance = Decimal('250.75')
            self.balance.save()
        
        self.history = BalanceHistory.objects.create(
            user_balance=self.balance,
            operation='SET',
            amount=Decimal('250.75'),
            previous_balance=Decimal('0.00'),
            new_balance=Decimal('250.75'),
            description='Saldo inicial'
        )
    
    def test_admin_user_balance_changelist_view(self):
        """Testa se a view de lista de saldos funciona no admin."""
        self.client.force_login(self.admin_user)
        url = reverse('admin:finance_userbalance_changelist')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.full_name)
        self.assertContains(response, 'R$ 250,75')
    
    def test_admin_user_balance_change_view(self):
        """Testa se a view de edição de saldo funciona no admin."""
        self.client.force_login(self.admin_user)
        url = reverse('admin:finance_userbalance_change', args=[self.balance.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.full_name)
        self.assertContains(response, '250.75')
    
    def test_admin_balance_history_changelist_view(self):
        """Testa se a view de lista de histórico funciona no admin."""
        self.client.force_login(self.admin_user)
        url = reverse('admin:finance_balancehistory_changelist')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SET')
        self.assertContains(response, '250.75')
        # Verifica se o nome do usuário aparece (através do user_balance)
        self.assertContains(response, self.user.full_name)
    
    def test_admin_balance_history_change_view(self):
        """Testa se a view de visualização de histórico funciona no admin."""
        self.client.force_login(self.admin_user)
        url = reverse('admin:finance_balancehistory_change', args=[self.history.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SET')
        self.assertContains(response, '250.75')
    
    def test_admin_search_functionality(self):
        """Testa se a funcionalidade de busca funciona no admin."""
        self.client.force_login(self.admin_user)
        
        # Busca por email do usuário
        url = reverse('admin:finance_userbalance_changelist')
        response = self.client.get(url, {'q': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.full_name)
        
        # Busca por nome do usuário
        response = self.client.get(url, {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.full_name)
    
    def test_admin_filter_functionality(self):
        """Testa se os filtros funcionam no admin."""
        self.client.force_login(self.admin_user)
        
        # Testa filtro por data de criação
        url = reverse('admin:finance_userbalance_changelist')
        today = self.balance.created_at.date()
        response = self.client.get(url, {'created_at__date': today.strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, 200)
        
        # Testa filtro por operação no histórico
        url = reverse('admin:finance_balancehistory_changelist')
        response = self.client.get(url, {'operation': 'SET'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SET')
    
    def test_admin_permissions_non_staff(self):
        """Testa se usuários não-staff não conseguem acessar o admin."""
        regular_user = User.objects.create_user(
            username='regular',
            email='regular@test.com',
            password='regular123'
        )
        
        self.client.force_login(regular_user)
        url = reverse('admin:finance_userbalance_changelist')
        response = self.client.get(url)
        
        # Deve redirecionar para login do admin
        self.assertEqual(response.status_code, 302)