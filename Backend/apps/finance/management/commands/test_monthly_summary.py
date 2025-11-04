"""
Comando para testar o resumo mensal de transações.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Sum
from datetime import date
from decimal import Decimal
from apps.finance.models import Transaction, Category, UserBalance
from apps.game.models import GameSession

User = get_user_model()


class Command(BaseCommand):
    help = 'Testa o resumo mensal de transações financeiras'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('Teste de Resumo Mensal de Transações')
        self.stdout.write('=' * 60)
        
        # Buscar usuário (pode ser o primeiro ou especificar)
        try:
            user = User.objects.first()
            if not user:
                self.stdout.write(self.style.ERROR('Nenhum usuário encontrado'))
                return
            
            self.stdout.write(f'\nUsuário: {user.full_name} ({user.email})')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao buscar usuário: {e}'))
            return
        
        # Verificar saldo
        try:
            balance, created = UserBalance.objects.get_or_create(
                user=user,
                defaults={'current_balance': Decimal('0.00')}
            )
            self.stdout.write(f'\nSaldo atual: R$ {balance.current_balance}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao buscar saldo: {e}'))
            return
        
        # Verificar transações
        current_date = timezone.now()
        all_transactions = Transaction.objects.filter(user=user)
        active_transactions = all_transactions.filter(is_active=True)
        inactive_transactions = all_transactions.filter(is_active=False)
        
        self.stdout.write(f'\n--- Estatísticas de Transações ---')
        self.stdout.write(f'Total de transações: {all_transactions.count()}')
        self.stdout.write(f'Transações ativas: {active_transactions.count()}')
        self.stdout.write(f'Transações inativas: {inactive_transactions.count()}')
        
        # Verificar transações do mês atual
        current_month_transactions = active_transactions.filter(
            transaction_date__year=current_date.year,
            transaction_date__month=current_date.month
        )
        self.stdout.write(f'\nTransações do mês atual ({current_date.year}-{current_date.month:02d}): {current_month_transactions.count()}')
        
        # Mostrar primeiras transações ativas
        if active_transactions.exists():
            self.stdout.write(f'\n--- Primeiras 10 Transações Ativas ---')
            for i, t in enumerate(active_transactions[:10], 1):
                self.stdout.write(
                    f'{i}. {t.transaction_date} | {t.transaction_type:8s} | '
                    f'R$ {t.amount:10.2f} | {t.description[:50]:50s} | '
                    f'is_active={t.is_active}'
                )
        else:
            self.stdout.write(self.style.WARNING('\nNenhuma transação ativa encontrada'))
        
        # Verificar GameSession para ver a data do jogo
        try:
            game_session = GameSession.objects.filter(user=user).first()
            if game_session:
                self.stdout.write(f'\n--- Informações do Jogo ---')
                self.stdout.write(f'Data atual do jogo: {game_session.current_game_date}')
                self.stdout.write(f'Data inicial do jogo: {game_session.game_start_date}')
                self.stdout.write(f'Data final do jogo: {game_session.game_end_date}')
                
                # Verificar transações com data do jogo
                game_date_transactions = active_transactions.filter(
                    transaction_date=game_session.current_game_date
                )
                self.stdout.write(f'\nTransações com data do jogo ({game_session.current_game_date}): {game_date_transactions.count()}')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'\nErro ao buscar GameSession: {e}'))
        
        # Testar get_monthly_summary
        self.stdout.write(f'\n--- Teste get_monthly_summary ---')
        monthly_summary = Transaction.get_monthly_summary(
            user,
            current_date.year,
            current_date.month
        )
        self.stdout.write(f'Ano: {monthly_summary["year"]}')
        self.stdout.write(f'Mês: {monthly_summary["month"]}')
        self.stdout.write(f'Receitas: R$ {monthly_summary["income_total"]}')
        self.stdout.write(f'Despesas: R$ {monthly_summary["expense_total"]}')
        self.stdout.write(f'Saldo: R$ {monthly_summary["balance"]}')
        self.stdout.write(f'Total de transações: {monthly_summary["transaction_count"]}')
        
        # Verificar se há transações em outros meses
        self.stdout.write(f'\n--- Transações por Mês/Ano ---')
        months_with_transactions = active_transactions.values_list(
            'transaction_date__year',
            'transaction_date__month'
        ).distinct().order_by('-transaction_date__year', '-transaction_date__month')
        
        for year, month in months_with_transactions[:12]:
            month_transactions = active_transactions.filter(
                transaction_date__year=year,
                transaction_date__month=month
            )
            income = month_transactions.filter(transaction_type='INCOME').aggregate(
                total=Sum('amount')
            )['total'] or Decimal('0.00')
            expense = month_transactions.filter(transaction_type='EXPENSE').aggregate(
                total=Sum('amount')
            )['total'] or Decimal('0.00')
            
            self.stdout.write(
                f'{year}-{month:02d}: {month_transactions.count()} transações | '
                f'Receitas: R$ {income} | Despesas: R$ {expense}'
            )
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('Teste concluído!'))

