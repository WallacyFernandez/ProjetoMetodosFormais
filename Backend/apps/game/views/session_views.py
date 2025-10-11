"""
Views para gerenciamento de sessões de jogo.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import GameSession
from ..serializers import GameSessionSerializer


class GameSessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar sessões de jogo.
    """
    serializer_class = GameSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GameSession.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(
            GameSession,
            user=self.request.user
        )

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Retorna a sessão atual do usuário."""
        game_session = self.get_object()
        serializer = self.get_serializer(game_session)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def update_time(self, request):
        """Atualiza o tempo do jogo."""
        game_session = self.get_object()
        days_passed = game_session.update_game_time()
        serializer = self.get_serializer(game_session)
        return Response({
            'game_session': serializer.data,
            'days_passed': days_passed
        })

    @action(detail=False, methods=['post'])
    def pause(self, request):
        """Pausa o jogo."""
        game_session = self.get_object()
        game_session.pause_game()
        serializer = self.get_serializer(game_session)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def resume(self, request):
        """Retoma o jogo."""
        game_session = self.get_object()
        game_session.resume_game()
        serializer = self.get_serializer(game_session)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def start(self, request):
        """Inicia o jogo."""
        game_session = self.get_object()
        game_session.start_game()
        serializer = self.get_serializer(game_session)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def reset(self, request):
        """Reinicia o jogo completamente."""
        game_session = self.get_object()
        game_session.reset_game()
        serializer = self.get_serializer(game_session)
        return Response(serializer.data)


