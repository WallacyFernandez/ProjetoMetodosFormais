"""
Testes para as views de sessão de jogo.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from apps.game.models import GameSession
from apps.finance.models import UserBalance

User = get_user_model()


class TestGameSessionViewSet(TestCase):
    """Testes para GameSessionViewSet."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test User',
            last_name='Test User'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Criar saldo do usuário
        UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('10000.00')}
        )

    def test_get_current_session(self):
        """Testa obter sessão atual do usuário."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        url = reverse('game-session-current')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_name'], f'{self.user.first_name} {self.user.last_name}')
        self.assertEqual(response.data['current_game_date'], '2025-01-01')

    def test_get_current_session_not_found(self):
        """Testa obter sessão atual quando não existe."""
        # Criar um usuário sem sessão
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@test.com',
            first_name='Other',
            last_name='User'
        )
        self.client.force_authenticate(user=other_user)
        
        url = reverse('game-session-current')
        response = self.client.get(url)
        
        # Com o sinal, sempre cria uma sessão automaticamente
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_time(self):
        """Testa atualização do tempo do jogo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.status = 'ACTIVE'
        game_session.last_update_time = timezone.now() - timedelta(seconds=40)
        game_session.save()
        
        url = reverse('game-session-update-time')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('game_session', response.data)
        self.assertIn('days_passed', response.data)
        self.assertEqual(response.data['days_passed'], 2)

    def test_pause_game(self):
        """Testa pausar o jogo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.start_game()
        
        url = reverse('game-session-pause')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        game_session.refresh_from_db()
        self.assertEqual(game_session.status, 'PAUSED')

    def test_resume_game(self):
        """Testa retomar o jogo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.start_game()
        game_session.pause_game()
        
        url = reverse('game-session-resume')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        game_session.refresh_from_db()
        self.assertEqual(game_session.status, 'ACTIVE')

    def test_start_game(self):
        """Testa iniciar o jogo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        url = reverse('game-session-start')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        game_session.refresh_from_db()
        self.assertEqual(game_session.status, 'ACTIVE')

    def test_reset_game(self):
        """Testa reiniciar o jogo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.start_game()
        game_session.current_game_date = date(2025, 6, 15)
        game_session.days_survived = 165
        game_session.total_score = 1000
        game_session.save()
        
        url = reverse('game-session-reset')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        game_session.refresh_from_db()
        self.assertEqual(game_session.current_game_date, date(2025, 1, 1))
        self.assertEqual(game_session.days_survived, 0)
        self.assertEqual(game_session.total_score, 0)
        self.assertEqual(game_session.status, 'ACTIVE')

    def test_unauthenticated_access(self):
        """Testa acesso não autenticado."""
        self.client.logout()
        
        url = reverse('game-session-current')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_queryset_filters_by_user(self):
        """Testa se o queryset filtra por usuário."""
        # Criar outro usuário
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123',
            first_name='Other User',
            last_name='Other User'
        )
        
        # Criar sessões para ambos os usuários
        user_session, _ = GameSession.objects.get_or_create(user=self.user)
        other_session, _ = GameSession.objects.get_or_create(user=other_user)
        
        # Autenticar como primeiro usuário
        self.client.force_authenticate(user=self.user)
        
        url = reverse('game-session-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(str(response.data['results'][0]['id']), str(user_session.id))

    def test_get_object_returns_user_session(self):
        """Testa se get_object retorna a sessão do usuário."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        url = reverse('game-session-current')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['id']), str(game_session.id))

    def test_update_time_with_no_days_passed(self):
        """Testa atualização do tempo sem dias passados."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.status = 'ACTIVE'
        game_session.last_update_time = timezone.now() - timedelta(seconds=5)
        game_session.save()
        
        url = reverse('game-session-update-time')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['days_passed'], 0)

    def test_pause_already_paused_game(self):
        """Testa pausar jogo já pausado."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.start_game()
        game_session.pause_game()
        
        url = reverse('game-session-pause')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        game_session.refresh_from_db()
        self.assertEqual(game_session.status, 'PAUSED')

    def test_resume_not_paused_game(self):
        """Testa retomar jogo não pausado."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.start_game()
        
        url = reverse('game-session-resume')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        game_session.refresh_from_db()
        self.assertEqual(game_session.status, 'ACTIVE')

    def test_start_already_started_game(self):
        """Testa iniciar jogo já iniciado."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.start_game()
        
        url = reverse('game-session-start')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        game_session.refresh_from_db()
        self.assertEqual(game_session.status, 'ACTIVE')

    def test_reset_game_resets_user_balance(self):
        """Testa se reset do jogo reseta o saldo do usuário."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        # Alterar saldo
        user_balance = UserBalance.objects.get(user=self.user)
        user_balance.current_balance = Decimal('5000.00')
        user_balance.save()
        
        url = reverse('game-session-reset')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_balance.refresh_from_db()
        self.assertEqual(user_balance.current_balance, Decimal('10000.00'))

    def test_game_session_serializer_fields(self):
        """Testa se o serializer retorna todos os campos necessários."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        url = reverse('game-session-current')
        response = self.client.get(url)
        
        expected_fields = [
            'id', 'user_name', 'game_start_date', 'current_game_date', 'game_end_date',
            'status', 'time_acceleration',
            'total_score', 'days_survived', 'current_day_sales_count', 'created_at'
        ]
        
        for field in expected_fields:
            self.assertIn(field, response.data)

    def test_update_time_updates_game_progress(self):
        """Testa se atualização do tempo atualiza o progresso do jogo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        game_session.status = 'ACTIVE'
        game_session.last_update_time = timezone.now() - timedelta(seconds=20)
        game_session.save()
        
        initial_date = game_session.current_game_date
        initial_days = game_session.days_survived
        
        url = reverse('game-session-update-time')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        game_session.refresh_from_db()
        
        self.assertGreater(game_session.current_game_date, initial_date)
        self.assertGreater(game_session.days_survived, initial_days)
