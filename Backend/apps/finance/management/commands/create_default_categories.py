"""
Comando Django para criar as categorias padrão do sistema.
"""

from django.core.management.base import BaseCommand
from apps.finance.models import Category


class Command(BaseCommand):
    help = 'Cria as categorias padrão do sistema FinanceTracker'

    def handle(self, *args, **options):
        """Executa o comando."""
        
        # Lista de categorias padrão
        default_categories = [
            # Receitas
            {
                'name': 'Salário',
                'description': 'Salário mensal e benefícios trabalhistas',
                'icon': '💰',
                'color': '#10B981',
                'category_type': 'INCOME',
                'is_default': True,
            },
            {
                'name': 'Freelance',
                'description': 'Trabalhos freelancer e projetos extras',
                'icon': '💻',
                'color': '#3B82F6',
                'category_type': 'INCOME',
                'is_default': True,
            },
            {
                'name': 'Investimentos',
                'description': 'Dividendos, juros e rendimentos',
                'icon': '📈',
                'color': '#8B5CF6',
                'category_type': 'INCOME',
                'is_default': True,
            },
            {
                'name': 'Vendas',
                'description': 'Vendas de produtos ou serviços',
                'icon': '🛒',
                'color': '#F59E0B',
                'category_type': 'INCOME',
                'is_default': True,
            },
            {
                'name': 'Outros Ganhos',
                'description': 'Outras fontes de renda',
                'icon': '💸',
                'color': '#06B6D4',
                'category_type': 'INCOME',
                'is_default': True,
            },
            
            # Despesas
            {
                'name': 'Alimentação',
                'description': 'Supermercado, restaurantes e delivery',
                'icon': '🍽️',
                'color': '#EF4444',
                'category_type': 'EXPENSE',
                'is_default': True,
            },
            {
                'name': 'Transporte',
                'description': 'Combustível, transporte público e manutenção',
                'icon': '🚗',
                'color': '#F97316',
                'category_type': 'EXPENSE',
                'is_default': True,
            },
            {
                'name': 'Moradia',
                'description': 'Aluguel, financiamento e contas da casa',
                'icon': '🏠',
                'color': '#84CC16',
                'category_type': 'EXPENSE',
                'is_default': True,
            },
            {
                'name': 'Lazer',
                'description': 'Entretenimento, viagens e diversão',
                'icon': '🎉',
                'color': '#EC4899',
                'category_type': 'EXPENSE',
                'is_default': True,
            },
            {
                'name': 'Saúde',
                'description': 'Médicos, medicamentos e planos de saúde',
                'icon': '🏥',
                'color': '#14B8A6',
                'category_type': 'EXPENSE',
                'is_default': True,
            },
            {
                'name': 'Educação',
                'description': 'Cursos, livros e material educativo',
                'icon': '📚',
                'color': '#6366F1',
                'category_type': 'EXPENSE',
                'is_default': True,
            },
            {
                'name': 'Vestuário',
                'description': 'Roupas, calçados e acessórios',
                'icon': '👕',
                'color': '#A855F7',
                'category_type': 'EXPENSE',
                'is_default': True,
            },
            {
                'name': 'Tecnologia',
                'description': 'Eletrônicos, software e assinaturas digitais',
                'icon': '💻',
                'color': '#0EA5E9',
                'category_type': 'EXPENSE',
                'is_default': True,
            },
            {
                'name': 'Serviços',
                'description': 'Serviços profissionais e manutenções',
                'icon': '🔧',
                'color': '#64748B',
                'category_type': 'EXPENSE',
                'is_default': True,
            },
            {
                'name': 'Impostos',
                'description': 'Impostos, taxas e contribuições',
                'icon': '🏛️',
                'color': '#DC2626',
                'category_type': 'EXPENSE',
                'is_default': True,
            },
            {
                'name': 'Pets',
                'description': 'Gastos com animais de estimação',
                'icon': '🐕',
                'color': '#D97706',
                'category_type': 'EXPENSE',
                'is_default': True,
            },
            {
                'name': 'Doações',
                'description': 'Caridade e doações',
                'icon': '❤️',
                'color': '#F43F5E',
                'category_type': 'EXPENSE',
                'is_default': True,
            },
            {
                'name': 'Outros Gastos',
                'description': 'Outras despesas não categorizadas',
                'icon': '📋',
                'color': '#6B7280',
                'category_type': 'EXPENSE',
                'is_default': True,
            },
        ]

        created_count = 0
        updated_count = 0

        for category_data in default_categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                is_default=True,
                defaults=category_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Categoria criada: {category.icon} {category.name}')
                )
            else:
                # Atualiza campos se necessário
                updated = False
                for field, value in category_data.items():
                    if field != 'name' and getattr(category, field) != value:
                        setattr(category, field, value)
                        updated = True
                
                if updated:
                    category.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'🔄 Categoria atualizada: {category.icon} {category.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.HTTP_INFO(f'ℹ️ Categoria já existe: {category.icon} {category.name}')
                    )

        # Resumo
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'📊 RESUMO:'))
        self.stdout.write(self.style.SUCCESS(f'   • {created_count} categorias criadas'))
        self.stdout.write(self.style.SUCCESS(f'   • {updated_count} categorias atualizadas'))
        self.stdout.write(self.style.SUCCESS(f'   • {len(default_categories)} categorias padrão no total'))
        self.stdout.write('='*50)
        
        # Verifica se todas foram criadas
        total_categories = Category.objects.filter(is_default=True).count()
        if total_categories == len(default_categories):
            self.stdout.write(
                self.style.SUCCESS('🎉 Todas as categorias padrão foram configuradas com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'⚠️ Esperado: {len(default_categories)}, Encontrado: {total_categories}')
            )
