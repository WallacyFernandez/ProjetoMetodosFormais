"""
Comando para criar categorias financeiras necessárias para o jogo.
"""

from django.core.management.base import BaseCommand
from apps.finance.models import Category


class Command(BaseCommand):
    help = 'Cria categorias financeiras necessárias para o jogo'

    def handle(self, *args, **options):
        """Executa o comando."""
        
        # Categorias necessárias para o jogo
        categories_data = [
            {
                'name': 'Vendas',
                'description': 'Receitas de vendas de produtos',
                'color': '#10B981',  # Verde
                'icon': '💰'
            },
            {
                'name': 'Compras',
                'description': 'Compras de produtos dos fornecedores',
                'color': '#EF4444',  # Vermelho
                'icon': '🛒'
            },
            {
                'name': 'Operacionais',
                'description': 'Despesas operacionais do supermercado',
                'color': '#F59E0B',  # Amarelo
                'icon': '⚙️'
            }
        ]
        
        created_count = 0
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults=category_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Categoria criada: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Categoria já existe: {category.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'{created_count} categorias criadas com sucesso.')
        )
