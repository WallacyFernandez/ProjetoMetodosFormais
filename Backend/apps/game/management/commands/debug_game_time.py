from django.core.management.base import BaseCommand
from apps.game.models import GameSession
from apps.users.models import User
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Debug do sistema de tempo do jogo.'

    def handle(self, *args, **options):
        # Busca o primeiro usuário
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('Nenhum usuário encontrado.'))
            return
        
        # Busca a sessão de jogo
        session = GameSession.objects.filter(user=user).first()
        if not session:
            self.stdout.write(self.style.ERROR('Nenhuma sessão de jogo encontrada.'))
            return
        
        self.stdout.write(f'Sessão: {session}')
        self.stdout.write(f'Status: {session.status}')
        self.stdout.write(f'Data atual: {session.current_game_date}')
        self.stdout.write(f'Última atualização: {session.last_update_time}')
        self.stdout.write(f'Aceleração: {session.time_acceleration} minutos por dia')
        
        # Simula tempo decorrido
        now = timezone.now()
        time_diff = now - session.last_update_time
        minutes_passed = time_diff.total_seconds() / 60
        game_days_passed = int(minutes_passed / session.time_acceleration)
        
        self.stdout.write(f'Tempo atual: {now}')
        self.stdout.write(f'Diferença de tempo: {time_diff}')
        self.stdout.write(f'Minutos passados: {minutes_passed}')
        self.stdout.write(f'Dias do jogo que passaram: {game_days_passed}')
        
        # Força tempo decorrido para teste
        if game_days_passed == 0:
            self.stdout.write('Forçando tempo decorrido para teste...')
            session.last_update_time = now - timedelta(minutes=5)  # 5 minutos atrás
            session.save()
            
            # Recalcula
            time_diff = now - session.last_update_time
            minutes_passed = time_diff.total_seconds() / 60
            game_days_passed = int(minutes_passed / session.time_acceleration)
            
            self.stdout.write(f'Nova diferença: {time_diff}')
            self.stdout.write(f'Novos minutos: {minutes_passed}')
            self.stdout.write(f'Novos dias: {game_days_passed}')
            
            # Testa update_game_time
            days_passed = session.update_game_time()
            self.stdout.write(f'Dias passados pelo método: {days_passed}')
            self.stdout.write(f'Nova data: {session.current_game_date}')
