"""
Comando para corrigir a data do jogo para 31/03/2025.
"""
from django.core.management.base import BaseCommand
from apps.game.models import GameSession, RealtimeSale
from datetime import date


class Command(BaseCommand):
    help = 'Corrige a data do jogo para 31/03/2025'

    def handle(self, *args, **options):
        self.stdout.write('Corrigindo data do jogo para 31/03/2025...')
        
        # Busca todas as sessões e encontra a do wallacy
        sessions = GameSession.objects.all()
        session = None
        
        for s in sessions:
            if 'wallacy' in s.user.full_name.lower():
                session = s
                break
        
        if not session:
            self.stdout.write('Sessão do usuário wallacy não encontrada')
            return
        
        # Define a data correta
        correct_date = date(2025, 3, 31)  # 31/03/2025
        
        self.stdout.write(f'Data atual: {session.current_game_date}')
        self.stdout.write(f'Corrigindo para: {correct_date}')
        
        # Atualiza a sessão
        session.current_game_date = correct_date
        session.save()
        
        # Atualiza todas as vendas desta sessão
        sales_count = RealtimeSale.objects.filter(game_session=session).update(game_date=correct_date)
        
        self.stdout.write(f'Sessão atualizada para: {session.current_game_date}')
        self.stdout.write(f'{sales_count} vendas atualizadas para: {correct_date}')
        
        self.stdout.write(
            self.style.SUCCESS('Correção concluída!')
        )
