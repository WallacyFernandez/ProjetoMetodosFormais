"""
Testes para o app de jogo.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from .models import GameSession, SupermarketBalance, BalanceHistory, ProductCategory

User = get_user_model()


class GameSessionModelTest(TestCase):
    """Testes para o modelo GameSession."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User'
        )

    def test_create_game_session(self):
        """Testa a criação de uma sessão de jogo."""
        game_session = GameSession.objects.create(user=self.user)
        
        self.assertEqual(game_session.user, self.user)
        self.assertEqual(game_session.game_start_date, date(2025, 1, 1))
        self.assertEqual(game_session.current_game_date, date(2025, 1, 1))
        self.assertEqual(game_session.game_end_date, date(2026, 1, 1))
        self.assertEqual(game_session.status, 'ACTIVE')
        self.assertEqual(game_session.time_acceleration, 1440)
        self.assertEqual(game_session.total_score, 0)
        self.assertEqual(game_session.days_survived, 0)

    def test_update_game_time(self):
        """Testa a atualização do tempo do jogo."""
        game_session = GameSession.objects.create(user=self.user)
        
        # Simula passagem de tempo
        game_session.last_update_time = timezone.now() - timedelta(minutes=1440)  # 1 dia
        days_passed = game_session.update_game_time()
        
        self.assertEqual(days_passed, 1)
        self.assertEqual(game_session.current_game_date, date(2025, 1, 2))
        self.assertEqual(game_session.days_survived, 1)

    def test_pause_and_resume_game(self):
        """Testa pausar e retomar o jogo."""
        game_session = GameSession.objects.create(user=self.user)
        
        game_session.pause_game()
        self.assertEqual(game_session.status, 'PAUSED')
        
        game_session.resume_game()
        self.assertEqual(game_session.status, 'ACTIVE')

    def test_reset_game(self):
        """Testa reiniciar o jogo."""
        game_session = GameSession.objects.create(user=self.user)
        game_session.current_game_date = date(2025, 6, 15)
        game_session.days_survived = 165
        game_session.total_score = 1000
        
        game_session.reset_game()
        
        self.assertEqual(game_session.current_game_date, date(2025, 1, 1))
        self.assertEqual(game_session.days_survived, 0)
        self.assertEqual(game_session.total_score, 0)
        self.assertEqual(game_session.status, 'ACTIVE')

    def test_game_progress_percentage(self):
        """Testa o cálculo do progresso do jogo."""
        game_session = GameSession.objects.create(user=self.user)
        game_session.current_game_date = date(2025, 7, 1)  # 6 meses
        
        progress = game_session.game_progress_percentage
        self.assertAlmostEqual(progress, 50.0, places=1)

    def test_days_remaining(self):
        """Testa o cálculo de dias restantes."""
        game_session = GameSession.objects.create(user=self.user)
        game_session.current_game_date = date(2025, 7, 1)  # 6 meses
        
        days_remaining = game_session.days_remaining
        self.assertEqual(days_remaining, 184)  # Aproximadamente 6 meses


class SupermarketBalanceModelTest(TestCase):
    """Testes para o modelo SupermarketBalance."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User'
        )
        self.game_session = GameSession.objects.create(user=self.user)
        self.supermarket_balance = SupermarketBalance.objects.create(
            game_session=self.game_session
        )

    def test_create_supermarket_balance(self):
        """Testa a criação do saldo do supermercado."""
        self.assertEqual(self.supermarket_balance.current_balance, Decimal('10000.00'))
        self.assertEqual(self.supermarket_balance.minimum_balance, Decimal('1000.00'))
        self.assertEqual(self.supermarket_balance.bankruptcy_threshold, Decimal('0.00'))

    def test_add_amount(self):
        """Testa adicionar valor ao saldo."""
        new_balance = self.supermarket_balance.add_amount(Decimal('500.00'), 'Teste')
        
        self.assertEqual(new_balance, Decimal('10500.00'))
        self.assertEqual(self.supermarket_balance.current_balance, Decimal('10500.00'))

    def test_subtract_amount(self):
        """Testa subtrair valor do saldo."""
        new_balance = self.supermarket_balance.subtract_amount(Decimal('500.00'), 'Teste')
        
        self.assertEqual(new_balance, Decimal('9500.00'))
        self.assertEqual(self.supermarket_balance.current_balance, Decimal('9500.00'))

    def test_set_balance(self):
        """Testa definir novo valor para o saldo."""
        new_balance = self.supermarket_balance.set_balance(Decimal('15000.00'), 'Teste')
        
        self.assertEqual(new_balance, Decimal('15000.00'))
        self.assertEqual(self.supermarket_balance.current_balance, Decimal('15000.00'))

    def test_bankruptcy_detection(self):
        """Testa detecção de falência."""
        self.supermarket_balance.subtract_amount(Decimal('10000.00'), 'Teste')
        
        self.assertTrue(self.supermarket_balance.is_bankrupt)
        self.assertEqual(self.game_session.status, 'FAILED')

    def test_low_balance_detection(self):
        """Testa detecção de saldo baixo."""
        self.supermarket_balance.subtract_amount(Decimal('9500.00'), 'Teste')
        
        self.assertTrue(self.supermarket_balance.is_low_balance)


class BalanceHistoryModelTest(TestCase):
    """Testes para o modelo BalanceHistory."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User'
        )
        self.game_session = GameSession.objects.create(user=self.user)
        self.supermarket_balance = SupermarketBalance.objects.create(
            game_session=self.game_session
        )

    def test_create_balance_history(self):
        """Testa a criação de histórico de saldo."""
        history = BalanceHistory.objects.create(
            supermarket_balance=self.supermarket_balance,
            operation='ADD',
            amount=Decimal('500.00'),
            previous_balance=Decimal('10000.00'),
            new_balance=Decimal('10500.00'),
            description='Teste'
        )
        
        self.assertEqual(history.operation, 'ADD')
        self.assertEqual(history.amount, Decimal('500.00'))
        self.assertEqual(history.description, 'Teste')


class ProductCategoryModelTest(TestCase):
    """Testes para o modelo ProductCategory."""

    def test_create_product_category(self):
        """Testa a criação de categoria de produto."""
        category = ProductCategory.objects.create(
            name='Teste',
            description='Categoria de teste',
            icon='test',
            color='#FF0000',
            profit_margin_min=Decimal('10.00'),
            profit_margin_max=Decimal('50.00'),
            shelf_life_min=1,
            shelf_life_max=30
        )
        
        self.assertEqual(category.name, 'Teste')
        self.assertEqual(category.profit_margin_min, Decimal('10.00'))
        self.assertEqual(category.shelf_life_max, 30)

    def test_get_default_categories(self):
        """Testa a obtenção de categorias padrão."""
        default_categories = ProductCategory.get_default_categories()
        
        self.assertEqual(len(default_categories), 5)
        self.assertEqual(default_categories[0]['name'], 'Alimentos')
        self.assertEqual(default_categories[1]['name'], 'Bebidas')
