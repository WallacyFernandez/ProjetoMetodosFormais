from django.core.management.base import BaseCommand
from apps.game.models import GameSession
from apps.users.models import User
from apps.game.views import GameSessionViewSet
from django.test import RequestFactory
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Testa a view update_time como o frontend faria.'

    def handle(self, *args, **options):
        # Busca o primeiro usuário
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('Nenhum usuário encontrado.'))
            return
        
        # Simula uma requisição POST
        factory = RequestFactory()
        request = factory.post('/api/v1/game/sessions/update_time/')
        request.user = user
        
        # Cria a view
        view = GameSessionViewSet()
        view.request = request
        
        # Testa get_object
        try:
            game_session = view.get_object()
            self.stdout.write(f'Sessão encontrada: {game_session}')
            self.stdout.write(f'Status: {game_session.status}')
            self.stdout.write(f'Data atual: {game_session.current_game_date}')
            self.stdout.write(f'Última atualização: {game_session.last_update_time}')
            
            # Testa update_time
            days_passed = game_session.update_game_time()
            self.stdout.write(f'Dias passados: {days_passed}')
            self.stdout.write(f'Nova data: {game_session.current_game_date}')
            
            # Testa serializer
            serializer = view.get_serializer(game_session)
            self.stdout.write(f'Dados serializados: {serializer.data}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro: {e}'))
