"""
Comando para corrigir datas das vendas existentes.
"""
from django.core.management.base import BaseCommand
from apps.game.models import RealtimeSale, GameSession
from django.utils import timezone


class Command(BaseCommand):
    help = 'Corrige as datas das vendas existentes para corresponder à data atual do jogo'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando correção das datas das vendas...')
        
        # Busca todas as sessões de jogo
        game_sessions = GameSession.objects.all()
        
        for session in game_sessions:
            self.stdout.write(f'Processando sessão do usuário: {session.user.full_name}')
            
            # Busca vendas desta sessão
            sales = RealtimeSale.objects.filter(game_session=session)
            
            if sales.exists():
                self.stdout.write(f'  Encontradas {sales.count()} vendas')
                
                # Atualiza todas as vendas para usar a data atual do jogo
                updated_count = sales.update(game_date=session.current_game_date)
                
                self.stdout.write(f'  Atualizadas {updated_count} vendas para data {session.current_game_date}')
            else:
                self.stdout.write('  Nenhuma venda encontrada')
        
        self.stdout.write(
            self.style.SUCCESS('Correção das datas das vendas concluída!')
        )

