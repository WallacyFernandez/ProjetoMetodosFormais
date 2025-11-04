"""
Comando para criar transações de teste.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from apps.finance.models import Transaction, Category, UserBalance
from apps.game.models import GameSession

User = get_user_model()


class Command(BaseCommand):
    help = 'Cria transações de teste para o usuário'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            help='Email do usuário para criar transações',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Número de transações a criar (padrão: 10)',
        )
        parser.add_argument(
            '--use-game-date',
            action='store_true',
            help='Usar a data do jogo ao invés da data real',
        )

    def handle(self, *args, **options):
        user_email = options.get('user_email')
        count = options.get('count', 10)
        use_game_date = options.get('use_game_date', False)
        
        self.stdout.write('=' * 60)
        self.stdout.write('Criação de Transações de Teste')
        self.stdout.write('=' * 60)
        
        # Buscar usuário
        try:
            if user_email:
                user = User.objects.get(email=user_email)
            else:
                user = User.objects.first()
            
            if not user:
                self.stdout.write(self.style.ERROR('Nenhum usuário encontrado'))
                return
            
            self.stdout.write(f'\nUsuário: {user.full_name} ({user.email})')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao buscar usuário: {e}'))
            return
        
        # Buscar ou criar categoria padrão
        try:
            category, created = Category.objects.get_or_create(
                name='Vendas',
                defaults={
                    'description': 'Receitas de vendas de produtos',
                    'color': '#10B981',
                    'icon': '💰',
                    'category_type': 'INCOME',
                    'is_default': True,
                    'user': None
                }
            )
            
            expense_category, created = Category.objects.get_or_create(
                name='Despesas',
                defaults={
                    'description': 'Despesas operacionais',
                    'color': '#EF4444',
                    'icon': '💸',
                    'category_type': 'EXPENSE',
                    'is_default': True,
                    'user': None
                }
            )
            
            self.stdout.write(f'\nCategoria de receitas: {category.name}')
            self.stdout.write(f'Categoria de despesas: {expense_category.name}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao buscar/criar categorias: {e}'))
            return
        
        # Determinar data a usar
        transaction_date = None
        if use_game_date:
            try:
                game_session = GameSession.objects.filter(user=user).first()
                if game_session:
                    transaction_date = game_session.current_game_date
                    self.stdout.write(f'\nUsando data do jogo: {transaction_date}')
                else:
                    self.stdout.write(self.style.WARNING('GameSession não encontrada, usando data real'))
                    transaction_date = date.today()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Erro ao buscar GameSession: {e}, usando data real'))
                transaction_date = date.today()
        else:
            transaction_date = date.today()
            self.stdout.write(f'\nUsando data real: {transaction_date}')
        
        # Criar transações
        created_count = 0
        current_date = timezone.now()
        
        for i in range(count):
            # Alternar entre receitas e despesas
            if i % 2 == 0:
                transaction_type = 'INCOME'
                trans_category = category
                amount = Decimal(str(100 + (i * 10)))
                description = f'Venda de teste {i+1}'
            else:
                transaction_type = 'EXPENSE'
                trans_category = expense_category
                amount = Decimal(str(50 + (i * 5)))
                description = f'Despesa de teste {i+1}'
            
            # Variar a data para alguns casos
            if i < count // 2:
                trans_date = transaction_date
            else:
                # Usar mês anterior para alguns
                if transaction_date.month == 1:
                    trans_date = date(transaction_date.year - 1, 12, transaction_date.day)
                else:
                    trans_date = date(transaction_date.year, transaction_date.month - 1, transaction_date.day)
            
            try:
                transaction = Transaction.objects.create(
                    user=user,
                    amount=amount,
                    transaction_type=transaction_type,
                    category=trans_category,
                    description=description,
                    transaction_date=trans_date,
                    is_active=True
                )
                created_count += 1
                self.stdout.write(
                    f'  ✓ Criada: {trans_date} | {transaction_type:8s} | '
                    f'R$ {amount:10.2f} | {description}'
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Erro ao criar transação {i+1}: {e}')
                )
        
        # Verificar resumo mensal
        self.stdout.write(f'\n--- Resumo Mensal Atual ---')
        monthly_summary = Transaction.get_monthly_summary(
            user,
            current_date.year,
            current_date.month
        )
        self.stdout.write(f'Receitas: R$ {monthly_summary["income_total"]}')
        self.stdout.write(f'Despesas: R$ {monthly_summary["expense_total"]}')
        self.stdout.write(f'Saldo: R$ {monthly_summary["balance"]}')
        self.stdout.write(f'Total de transações: {monthly_summary["transaction_count"]}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(
            self.style.SUCCESS(
                f'Transações criadas com sucesso! ({created_count}/{count})'
            )
        )
        self.stdout.write(
            '\nExecute: python manage.py test_monthly_summary para verificar'
        )

