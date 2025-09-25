"""
Comando para debugar e corrigir a data do jogo.
"""
from django.core.management.base import BaseCommand
from apps.game.models import GameSession
from django.utils import timezone
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Debuga e corrige a data atual do jogo'

    def handle(self, *args, **options):
        self.stdout.write('Investigando datas do jogo...')
        
        # Busca todas as sessões (ativas e pausadas)
        sessions = GameSession.objects.all()
        
        if not sessions.exists():
            self.stdout.write('Nenhuma sessão ativa encontrada')
            return
        
        # Processa cada sessão
        for session in sessions:
            self.stdout.write(f'\n--- Sessão do usuário: {session.user.full_name} ---')
            
            self.stdout.write(f'Usuário: {session.user.full_name}')
            self.stdout.write(f'Data de início do jogo: {session.game_start_date}')
            self.stdout.write(f'Data atual do jogo: {session.current_game_date}')
            self.stdout.write(f'Data de fim do jogo: {session.game_end_date}')
            self.stdout.write(f'Dias sobrevividos: {session.days_survived}')
            self.stdout.write(f'Última atualização: {session.last_update_time}')
            
            # Calcula qual deveria ser a data atual
            expected_date = session.game_start_date + timedelta(days=session.days_survived)
            self.stdout.write(f'Data esperada (início + dias sobrevividos): {expected_date}')
            
            # Verifica se há diferença
            if session.current_game_date != expected_date:
                self.stdout.write(
                    self.style.WARNING(f'DIFERENÇA ENCONTRADA! Data atual ({session.current_game_date}) != Data esperada ({expected_date})')
                )
                
                # Pergunta se deve corrigir
                response = input('Deseja corrigir a data atual para a data esperada? (s/n): ')
                if response.lower() == 's':
                    session.current_game_date = expected_date
                    session.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Data corrigida para: {session.current_game_date}')
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Data atual está correta!')
                )
