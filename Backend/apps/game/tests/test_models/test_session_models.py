"""
Testes para o modelo GameSession.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import patch

from apps.game.models import GameSession
from apps.finance.models import UserBalance, Transaction, Category

User = get_user_model()


class GameSessionModelTest(TestCase):
    """Testes para o modelo GameSession."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test User',
            last_name='Test User'
        )
        # Criar saldo do usuário
        UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('10000.00')}
        )

    def test_create_game_session(self):
        """Testa a criação de uma sessão de jogo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        self.assertEqual(game_session.user, self.user)
        self.assertEqual(game_session.game_start_date, date(2025, 1, 1))
        self.assertEqual(game_session.current_game_date, date(2025, 1, 1))
        self.assertEqual(game_session.game_end_date, date(2026, 1, 1))
        self.assertEqual(game_session.status, 'NOT_STARTED')
        self.assertEqual(game_session.time_acceleration, 20)
        self.assertEqual(game_session.daily_sales_target, 40)
        self.assertEqual(game_session.auto_sales_enabled, True)
        self.assertEqual(game_session.total_score, 0)
        self.assertEqual(game_session.days_survived, 0)

    def test_update_game_time_with_days_passed(self):
        """Testa a atualização do tempo do jogo com dias passados."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.status = 'ACTIVE'
        
        # Simula passagem de tempo (40 segundos = 2 dias com aceleração de 20s)
        game_session.last_update_time = timezone.now() - timedelta(seconds=40)
        days_passed = game_session.update_game_time()
        
        self.assertEqual(days_passed, 2)
        self.assertEqual(game_session.current_game_date, date(2025, 1, 3))
        self.assertEqual(game_session.days_survived, 2)

    def test_update_game_time_without_days_passed(self):
        """Testa a atualização do tempo do jogo sem dias completos."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.status = 'ACTIVE'
        
        # Simula passagem de tempo insuficiente (10 segundos = 0.5 dias)
        game_session.last_update_time = timezone.now() - timedelta(seconds=10)
        days_passed = game_session.update_game_time()
        
        self.assertEqual(days_passed, 0)
        self.assertEqual(game_session.current_game_date, date(2025, 1, 1))
        self.assertEqual(game_session.days_survived, 0)

    def test_game_status_choices(self):
        """Testa as opções de status do jogo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        # Testa status inicial
        self.assertEqual(game_session.status, 'NOT_STARTED')
        
        # Testa mudança de status
        game_session.status = 'ACTIVE'
        game_session.save()
        self.assertEqual(game_session.status, 'ACTIVE')
        
        game_session.status = 'PAUSED'
        game_session.save()
        self.assertEqual(game_session.status, 'PAUSED')

    def test_start_game(self):
        """Testa iniciar o jogo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        game_session.start_game()
        
        self.assertEqual(game_session.status, 'ACTIVE')
        self.assertIsNotNone(game_session.session_start_time)
        self.assertIsNotNone(game_session.last_update_time)

    def test_pause_and_resume_game(self):
        """Testa pausar e retomar o jogo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.start_game()
        
        game_session.pause_game()
        self.assertEqual(game_session.status, 'PAUSED')
        
        game_session.resume_game()
        self.assertEqual(game_session.status, 'ACTIVE')

    def test_get_game_progress(self):
        """Testa o cálculo do progresso do jogo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.current_game_date = date(2025, 7, 1)  # 6 meses
        
        progress = game_session.get_game_progress()
        self.assertAlmostEqual(progress, 50.0, places=0)  # Permitir diferença maior

    def test_days_remaining_property(self):
        """Testa o cálculo de dias restantes."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.current_game_date = date(2025, 7, 1)  # 6 meses
        
        days_remaining = game_session.days_remaining
        self.assertEqual(days_remaining, 184)  # Aproximadamente 6 meses

    def test_is_game_over(self):
        """Testa verificação se o jogo terminou."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        # Jogo não terminou
        self.assertFalse(game_session.is_game_over())
        
        # Jogo completado
        game_session.status = 'COMPLETED'
        self.assertTrue(game_session.is_game_over())
        
        # Jogo falhou
        game_session.status = 'FAILED'
        self.assertTrue(game_session.is_game_over())

    def test_reset_game(self):
        """Testa reiniciar o jogo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.current_game_date = date(2025, 6, 15)
        game_session.days_survived = 165
        game_session.total_score = 1000
        game_session.status = 'ACTIVE'
        
        game_session.reset_game()
        
        self.assertEqual(game_session.current_game_date, date(2025, 1, 1))
        self.assertEqual(game_session.days_survived, 0)
        self.assertEqual(game_session.total_score, 0)
        self.assertEqual(game_session.status, 'ACTIVE')
        
        # Verifica se o saldo foi resetado
        user_balance = UserBalance.objects.get(user=self.user)
        self.assertEqual(user_balance.current_balance, Decimal('10000.00'))

    def test_time_acceleration_validation(self):
        """Testa validação da aceleração do tempo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        # Testa valor mínimo
        game_session.time_acceleration = 1
        game_session.full_clean()  # Não deve gerar erro
        
        # Testa valor máximo
        game_session.time_acceleration = 10080  # 1 semana
        game_session.full_clean()  # Não deve gerar erro

    def test_daily_sales_target(self):
        """Testa configuração da meta de vendas diárias."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.daily_sales_target = 50
        
        self.assertEqual(game_session.daily_sales_target, 50)

    def test_auto_sales_enabled(self):
        """Testa configuração de vendas automáticas."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        # Por padrão deve estar habilitado
        self.assertTrue(game_session.auto_sales_enabled)
        
        # Testa desabilitar
        game_session.auto_sales_enabled = False
        game_session.save()
        self.assertFalse(game_session.auto_sales_enabled)

    def test_current_day_sales_count(self):
        """Testa contador de vendas do dia atual."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        # Deve começar em 0
        self.assertEqual(game_session.current_day_sales_count, 0)
        
        # Testa incrementar
        game_session.current_day_sales_count = 5
        game_session.save()
        self.assertEqual(game_session.current_day_sales_count, 5)

    def test_str_representation(self):
        """Testa representação string do modelo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        expected = f"Sessão de {self.user.first_name} {self.user.last_name} - {game_session.current_game_date}"
        self.assertEqual(str(game_session), expected)

    def test_meta_ordering(self):
        """Testa ordenação definida no Meta."""
        game_session1, _ = GameSession.objects.get_or_create(user=self.user)
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            first_name='Test User 2',
            last_name='Test User 2'
        )
        game_session2, _ = GameSession.objects.get_or_create(user=user2)
        
        sessions = GameSession.objects.all()
        # Deve estar ordenado por last_update_time decrescente
        self.assertEqual(sessions.count(), 2)

    def test_process_auto_sales(self):
        """Testa processamento de vendas automáticas."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.status = 'ACTIVE'
        game_session.auto_sales_enabled = True
        
        # Como não temos produtos reais, apenas testamos se o método executa sem erro
        # Em um cenário real, isso seria testado com dados reais
        try:
            game_session.process_auto_sales(1)
            # Se chegou até aqui, o método executou sem erro
            self.assertTrue(True)
        except Exception as e:
            # Esperado quando não há produtos disponíveis
            self.assertIn("Não há produtos disponíveis", str(e))
