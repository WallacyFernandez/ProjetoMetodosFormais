from django.core.management.base import BaseCommand
from apps.game.models import GameSession, Product
from apps.users.models import User
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Testa o sistema de vendas automáticas do jogo.'

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
        
        self.stdout.write(f'Sessão encontrada: {session}')
        self.stdout.write(f'Status: {session.status}')
        self.stdout.write(f'Data atual: {session.current_game_date}')
        self.stdout.write(f'Última atualização: {session.last_update_time}')
        self.stdout.write(f'Aceleração: {session.time_acceleration} minutos por dia')
        
        # Verifica produtos
        products = Product.objects.filter(is_active=True, current_stock__gt=0)
        self.stdout.write(f'Produtos disponíveis: {products.count()}')
        
        # Simula passagem de tempo
        if session.status == 'ACTIVE':
            self.stdout.write('Simulando passagem de tempo...')
            old_date = session.current_game_date
            old_stock = sum(p.current_stock for p in products)
            
            # Força atualização de tempo
            session.last_update_time = timezone.now() - timedelta(minutes=5)  # 5 minutos atrás
            session.save()
            
            days_passed = session.update_game_time()
            self.stdout.write(f'Dias que passaram: {days_passed}')
            self.stdout.write(f'Data anterior: {old_date}')
            self.stdout.write(f'Data atual: {session.current_game_date}')
            
            # Verifica estoque
            products = Product.objects.filter(is_active=True, current_stock__gt=0)
            new_stock = sum(p.current_stock for p in products)
            self.stdout.write(f'Estoque anterior: {old_stock}')
            self.stdout.write(f'Estoque atual: {new_stock}')
            self.stdout.write(f'Produtos vendidos: {old_stock - new_stock}')
        else:
            self.stdout.write(f'Jogo não está ativo. Status: {session.status}')
            self.stdout.write('Iniciando o jogo para teste...')
            session.start_game()
            self.stdout.write(f'Status após iniciar: {session.status}')
            
            # Simula passagem de tempo após iniciar
            old_date = session.current_game_date
            old_stock = sum(p.current_stock for p in products)
            
            # Força atualização de tempo
            session.last_update_time = timezone.now() - timedelta(minutes=5)  # 5 minutos atrás
            session.save()
            
            days_passed = session.update_game_time()
            self.stdout.write(f'Dias que passaram: {days_passed}')
            self.stdout.write(f'Data anterior: {old_date}')
            self.stdout.write(f'Data atual: {session.current_game_date}')
            
            # Verifica estoque
            products = Product.objects.filter(is_active=True, current_stock__gt=0)
            new_stock = sum(p.current_stock for p in products)
            self.stdout.write(f'Estoque anterior: {old_stock}')
            self.stdout.write(f'Estoque atual: {new_stock}')
            self.stdout.write(f'Produtos vendidos: {old_stock - new_stock}')
