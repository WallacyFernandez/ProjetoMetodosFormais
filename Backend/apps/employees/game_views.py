"""
Views adicionais para integração com o jogo.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from decimal import Decimal

from apps.employees.models import Employee, Payroll, PayrollHistory
from apps.employees.serializers import EmployeeSummarySerializer


class EmployeeGameIntegrationViewSet(viewsets.ViewSet):
    """
    ViewSet para integração de funcionários com o jogo.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def game_dashboard_summary(self, request):
        """Retorna resumo de funcionários para o dashboard do jogo."""
        employees = Employee.objects.filter(user=request.user)
        
        # Estatísticas básicas
        total_employees = employees.count()
        active_employees = employees.filter(employment_status='ACTIVE').count()
        inactive_employees = total_employees - active_employees
        
        # Salário total mensal
        total_monthly_payroll = employees.filter(
            employment_status='ACTIVE'
        ).aggregate(total=Sum('salary'))['total'] or Decimal('0.00')
        
        # Funcionários por departamento
        employees_by_department = {}
        employees_by_position = {}
        
        for employee in employees.filter(employment_status='ACTIVE'):
            dept = employee.position.get_department_display()
            pos = employee.position.name
            
            employees_by_department[dept] = employees_by_department.get(dept, 0) + 1
            employees_by_position[pos] = employees_by_position.get(pos, 0) + 1
        
        # Próximo pagamento (último mês processado + 1)
        last_payroll = PayrollHistory.objects.filter(
            user=request.user
        ).order_by('-payment_month').first()
        
        next_payment_month = None
        if last_payroll:
            # Calcular próximo mês
            year = last_payroll.payment_month.year
            month = last_payroll.payment_month.month
            if month == 12:
                next_payment_month = f"{year + 1}-01"
            else:
                next_payment_month = f"{year}-{month + 1:02d}"
        
        serializer = EmployeeSummarySerializer({
            'total_employees': total_employees,
            'active_employees': active_employees,
            'inactive_employees': inactive_employees,
            'total_monthly_payroll': total_monthly_payroll,
            'total_monthly_payroll_formatted': f"R$ {total_monthly_payroll:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            'employees_by_department': employees_by_department,
            'employees_by_position': employees_by_position,
        })
        
        return Response({
            'employees': serializer.data,
            'next_payment_month': next_payment_month,
            'has_employees': active_employees > 0,
            'can_afford_payroll': request.user.balance.current_balance >= total_monthly_payroll if hasattr(request.user, 'balance') else False
        })

    @action(detail=False, methods=['post'])
    def hire_employee(self, request):
        """Contrata um funcionário rapidamente."""
        from apps.employees.serializers import EmployeeCreateSerializer
        
        serializer = EmployeeCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                employee = serializer.save(user=request.user)
                
                return Response({
                    'message': 'Funcionário contratado com sucesso',
                    'employee': {
                        'id': employee.id,
                        'name': employee.name,
                        'position': employee.position.name,
                        'salary': employee.salary,
                        'salary_formatted': employee.salary_formatted
                    }
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response(
                    {'error': f'Erro ao contratar funcionário: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def payroll_forecast(self, request):
        """Retorna previsão de custos de folha de pagamento."""
        employees = Employee.objects.filter(
            user=request.user,
            employment_status='ACTIVE'
        )
        
        if not employees.exists():
            return Response({
                'message': 'Nenhum funcionário ativo',
                'forecast': {
                    'monthly_cost': 0,
                    'monthly_cost_formatted': 'R$ 0,00',
                    'employees_count': 0
                }
            })
        
        monthly_cost = sum(emp.salary for emp in employees)
        
        return Response({
            'forecast': {
                'monthly_cost': monthly_cost,
                'monthly_cost_formatted': f"R$ {monthly_cost:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                'employees_count': employees.count(),
                'average_salary': monthly_cost / employees.count(),
                'average_salary_formatted': f"R$ {monthly_cost / employees.count():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            }
        })
