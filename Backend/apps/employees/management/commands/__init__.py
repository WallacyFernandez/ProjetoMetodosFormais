"""
Comando para processar pagamentos mensais automaticamente.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth import get_user_model
from datetime import date, datetime
from decimal import Decimal

from apps.employees.models import Employee, Payroll, PayrollHistory, EmployeePosition
from apps.finance.models import UserBalance, Transaction, Category

User = get_user_model()


class Command(BaseCommand):
    help = 'Processa pagamentos mensais de todos os usuários'

    def add_arguments(self, parser):
        parser.add_argument(
            '--month',
            type=str,
            help='Mês para processar no formato YYYY-MM (padrão: mês anterior)',
        )
        parser.add_argument(
            '--user-id',
            type=int,
            help='ID do usuário específico para processar (padrão: todos)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula o processamento sem executar',
        )

    def handle(self, *args, **options):
        # Determinar o mês de pagamento
        if options['month']:
            try:
                payment_month = datetime.strptime(options['month'], '%Y-%m').date()
            except ValueError:
                raise CommandError('Formato de mês inválido. Use YYYY-MM')
        else:
            # Mês anterior por padrão
            today = date.today()
            if today.month == 1:
                payment_month = date(today.year - 1, 12, 1)
            else:
                payment_month = date(today.year, today.month - 1, 1)

        # Determinar usuários para processar
        if options['user_id']:
            try:
                users = [User.objects.get(id=options['user_id'])]
            except User.DoesNotExist:
                raise CommandError(f'Usuário com ID {options["user_id"]} não encontrado')
        else:
            users = User.objects.filter(is_active=True)

        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'Modo DRY-RUN: Simulando processamento para {payment_month.strftime("%m/%Y")}')
            )

        total_processed = 0
        total_amount = Decimal('0.00')

        for user in users:
            try:
                result = self.process_user_payments(user, payment_month, dry_run)
                if result['processed']:
                    total_processed += result['employees_count']
                    total_amount += result['total_amount']
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ {user.full_name}: {result["employees_count"]} funcionários, '
                            f'R$ {result["total_amount"]:,.2f}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ {user.full_name}: {result["message"]}')
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ {user.full_name}: Erro - {str(e)}')
                )

        # Resumo final
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'Mês processado: {payment_month.strftime("%m/%Y")}')
        self.stdout.write(f'Usuários processados: {len(users)}')
        self.stdout.write(f'Funcionários pagos: {total_processed}')
        self.stdout.write(f'Valor total: R$ {total_amount:,.2f}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('Modo DRY-RUN: Nenhum pagamento foi processado'))

    def process_user_payments(self, user, payment_month, dry_run=False):
        """Processa pagamentos para um usuário específico."""
        
        # Buscar funcionários ativos
        employees = Employee.objects.filter(
            user=user,
            employment_status='ACTIVE'
        )
        
        if not employees.exists():
            return {
                'processed': False,
                'message': 'Nenhum funcionário ativo encontrado',
                'employees_count': 0,
                'total_amount': Decimal('0.00')
            }

        # Verificar se já existe folha para este mês
        existing_payrolls = Payroll.objects.filter(
            employee__user=user,
            payment_month=payment_month
        )
        
        if existing_payrolls.exists():
            return {
                'processed': False,
                'message': f'Folha para {payment_month.strftime("%m/%Y")} já existe',
                'employees_count': 0,
                'total_amount': Decimal('0.00')
            }

        if dry_run:
            # Simular processamento
            total_amount = sum(emp.salary for emp in employees)
            return {
                'processed': True,
                'message': 'Simulação concluída',
                'employees_count': employees.count(),
                'total_amount': total_amount
            }

        # Processar pagamentos reais
        try:
            with transaction.atomic():
                # Verificar saldo
                user_balance = UserBalance.objects.get(user=user)
                total_amount = sum(emp.salary for emp in employees)
                
                if user_balance.current_balance < total_amount:
                    return {
                        'processed': False,
                        'message': f'Saldo insuficiente (R$ {user_balance.current_balance:,.2f} < R$ {total_amount:,.2f})',
                        'employees_count': 0,
                        'total_amount': Decimal('0.00')
                    }

                # Criar folhas de pagamento
                created_payrolls = []
                for employee in employees:
                    payroll = Payroll.objects.create(
                        employee=employee,
                        payment_month=payment_month,
                        base_salary=employee.salary,
                        overtime_hours=Decimal('0.00'),
                        overtime_value=Decimal('0.00'),
                        bonus=Decimal('0.00'),
                        deductions=Decimal('0.00'),
                        notes=f'Pagamento mensal automático - {payment_month.strftime("%m/%Y")}'
                    )
                    created_payrolls.append(payroll)

                # Debitar do saldo
                user_balance.subtract_amount(total_amount)

                # Criar transação financeira
                payroll_category, _ = Category.objects.get_or_create(
                    name='Folha de Pagamento',
                    defaults={
                        'description': 'Pagamento de salários dos funcionários',
                        'category_type': 'EXPENSE'
                    }
                )

                Transaction.objects.create(
                    user=user,
                    category=payroll_category,
                    amount=total_amount,
                    description=f'Folha de pagamento - {payment_month.strftime("%m/%Y")}',
                    transaction_type='EXPENSE'
                )

                # Marcar como pago
                for payroll in created_payrolls:
                    payroll.mark_as_paid()

                # Criar histórico
                PayrollHistory.objects.create(
                    user=user,
                    payment_month=payment_month,
                    total_employees=len(created_payrolls),
                    total_amount=total_amount
                )

                return {
                    'processed': True,
                    'message': 'Pagamentos processados com sucesso',
                    'employees_count': len(created_payrolls),
                    'total_amount': total_amount
                }

        except Exception as e:
            raise Exception(f'Erro ao processar pagamentos: {str(e)}')
