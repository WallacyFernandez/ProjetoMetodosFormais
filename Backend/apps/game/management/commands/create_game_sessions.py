"""
Comando de management para criar sessões de jogo para usuários existentes.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.game.models import GameSession, SupermarketBalance, ProductCategory

User = get_user_model()


class Command(BaseCommand):
    help = 'Cria sessões de jogo para usuários existentes que não possuem uma'

    def handle(self, *args, **options):
        """Executa o comando."""
        users_without_session = User.objects.filter(game_session__isnull=True)
        
        if not users_without_session.exists():
            self.stdout.write(
                self.style.SUCCESS('Todos os usuários já possuem sessões de jogo.')
            )
            return
        
        # Cria categorias padrão se não existirem
        if not ProductCategory.objects.exists():
            self.stdout.write('Criando categorias padrão...')
            for category_data in ProductCategory.get_default_categories():
                ProductCategory.objects.create(**category_data)
            self.stdout.write(
                self.style.SUCCESS('Categorias padrão criadas com sucesso.')
            )
        
        # Cria sessões de jogo para usuários sem sessão
        created_count = 0
        for user in users_without_session:
            try:
                game_session = GameSession.objects.create(user=user)
                SupermarketBalance.objects.create(game_session=game_session)
                created_count += 1
                self.stdout.write(f'Sessão criada para usuário: {user.email}')
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Erro ao criar sessão para {user.email}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'{created_count} sessões de jogo criadas com sucesso.')
        )
