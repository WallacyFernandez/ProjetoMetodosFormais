"""
Sinais para o app de funcionários.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from datetime import date, datetime
from decimal import Decimal

from apps.employees.models import Employee, Payroll, PayrollHistory
from apps.finance.models import UserBalance, Transaction, Category
from apps.game.models import GameSession


@receiver(post_save, sender=GameSession)
def process_monthly_payroll_on_time_update(sender, instance, created, **kwargs):
    """
    Processa pagamentos mensais quando o tempo do jogo avança.
    """
    if created:
        return  # Não processar para novas sessões
    
    # Verificar se o jogo está ativo
    if instance.status != 'ACTIVE':
        return
    
    # Verificar se passou um mês no jogo
    current_month = instance.current_game_date.replace(day=1)
    
    # Buscar último pagamento processado
    last_payroll = PayrollHistory.objects.filter(
        user=instance.user
    ).order_by('-payment_month').first()
    
    if last_payroll:
        last_payment_month = last_payroll.payment_month.replace(day=1)
        
        # Se já processou para este mês, não processar novamente
        if last_payment_month >= current_month:
            return
    
    # Processar pagamentos para o mês atual
    try:
        with transaction.atomic():
            # Buscar funcionários ativos
            employees = Employee.objects.filter(
                user=instance.user,
                employment_status='ACTIVE'
            )
            
            if not employees.exists():
                return  # Não há funcionários para pagar
            
            # Verificar saldo disponível
            user_balance = UserBalance.objects.get(user=instance.user)
            total_payroll = sum(emp.salary for emp in employees)
            
            if user_balance.current_balance < total_payroll:
                # Saldo insuficiente - não processar pagamentos
                return
            
            # Criar folhas de pagamento
            created_payrolls = []
            for employee in employees:
                payroll = Payroll.objects.create(
                    employee=employee,
                    payment_month=current_month,
                    base_salary=employee.salary,
                    overtime_hours=Decimal('0.00'),
                    overtime_value=Decimal('0.00'),
                    bonus=Decimal('0.00'),
                    deductions=Decimal('0.00'),
                    notes=f'Pagamento automático do jogo - {current_month.strftime("%m/%Y")}'
                )
                created_payrolls.append(payroll)
            
            # Debitar do saldo
            user_balance.subtract_amount(total_payroll)
            
            # Criar transação financeira
            payroll_category, _ = Category.objects.get_or_create(
                name='Folha de Pagamento',
                defaults={
                    'description': 'Pagamento de salários dos funcionários',
                    'category_type': 'EXPENSE'
                }
            )
            
            Transaction.objects.create(
                user=instance.user,
                category=payroll_category,
                amount=total_payroll,
                description=f'Folha de pagamento automática - {current_month.strftime("%m/%Y")}',
                transaction_type='EXPENSE',
                transaction_date=instance.current_game_date
            )
            
            # Marcar como pago
            for payroll in created_payrolls:
                payroll.mark_as_paid()
            
            # Criar histórico
            PayrollHistory.objects.create(
                user=instance.user,
                payment_month=current_month,
                total_employees=len(created_payrolls),
                total_amount=total_payroll
            )
            
    except Exception as e:
        # Log do erro (em produção, usar logging adequado)
        print(f"Erro ao processar pagamentos automáticos: {str(e)}")
