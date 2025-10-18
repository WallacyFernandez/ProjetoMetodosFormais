"""
Views do app de funcionários.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Sum, Count, Q
from decimal import Decimal
from datetime import date, datetime
from collections import defaultdict

from apps.finance.models import UserBalance, Transaction, Category
from .models import EmployeePosition, Employee, Payroll, PayrollHistory
from .serializers import (
    EmployeePositionSerializer, EmployeeSerializer, EmployeeCreateSerializer,
    EmployeeTerminateSerializer, PayrollSerializer, PayrollCreateSerializer,
    PayrollHistorySerializer, EmployeeSummarySerializer,
    PayrollSummarySerializer
)


class EmployeePositionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar cargos de funcionários.
    """
    serializer_class = EmployeePositionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EmployeePosition.objects.filter(is_active=True)

    @action(detail=False, methods=['post'])
    def create_default_positions(self, request):
        """Cria cargos padrão."""
        try:
            created_positions = []
            for position_data in EmployeePosition.get_default_positions():
                position, created = EmployeePosition.objects.get_or_create(
                    name=position_data['name'],
                    defaults=position_data
                )
                if created:
                    created_positions.append(position)
            
            serializer = self.get_serializer(created_positions, many=True)
            return Response({
                'message': f'{len(created_positions)} cargos criados com sucesso',
                'positions': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Erro ao criar cargos: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar funcionários.
    """
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return EmployeeCreateSerializer
        return EmployeeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def terminate(self, request, pk=None):
        """Demite um funcionário."""
        employee = self.get_object()
        
        if employee.employment_status == 'TERMINATED':
            return Response(
                {'error': 'Funcionário já foi demitido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = EmployeeTerminateSerializer(data=request.data)
        if serializer.is_valid():
            termination_date = serializer.validated_data.get('termination_date')
            notes = serializer.validated_data.get('notes', '')
            
            employee.terminate(termination_date)
            if notes:
                employee.notes = notes
                employee.save()
            
            return Response({
                'message': 'Funcionário demitido com sucesso',
                'employee': EmployeeSerializer(employee).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reactivate(self, request, pk=None):
        """Reativa um funcionário."""
        employee = self.get_object()
        
        if employee.employment_status != 'TERMINATED':
            return Response(
                {'error': 'Funcionário não está demitido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        employee.reactivate()
        
        return Response({
            'message': 'Funcionário reativado com sucesso',
            'employee': EmployeeSerializer(employee).data
        })

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Retorna resumo dos funcionários."""
        employees = self.get_queryset()
        
        # Estatísticas básicas
        total_employees = employees.count()
        active_employees = employees.filter(employment_status='ACTIVE').count()
        inactive_employees = total_employees - active_employees
        
        # Salário total mensal
        total_monthly_payroll = employees.filter(
            employment_status='ACTIVE'
        ).aggregate(total=Sum('salary'))['total'] or Decimal('0.00')
        
        # Funcionários por departamento
        employees_by_department = defaultdict(int)
        employees_by_position = defaultdict(int)
        
        for employee in employees.filter(employment_status='ACTIVE'):
            employees_by_department[employee.position.get_department_display()] += 1
            employees_by_position[employee.position.name] += 1
        
        serializer = EmployeeSummarySerializer({
            'total_employees': total_employees,
            'active_employees': active_employees,
            'inactive_employees': inactive_employees,
            'total_monthly_payroll': total_monthly_payroll,
            'total_monthly_payroll_formatted': f"R$ {total_monthly_payroll:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            'employees_by_department': dict(employees_by_department),
            'employees_by_position': dict(employees_by_position),
        })
        
        return Response(serializer.data)


class PayrollViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar folha de pagamento.
    """
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payroll.objects.filter(employee__user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return PayrollCreateSerializer
        return PayrollSerializer


    @action(detail=False, methods=['get'])
    def by_month(self, request):
        """Retorna folhas de pagamento por mês."""
        month = request.query_params.get('month')
        
        if not month:
            return Response(
                {'error': 'Parâmetro month é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            payment_month = datetime.strptime(month, '%Y-%m').date()
        except ValueError:
            return Response(
                {'error': 'Formato de mês inválido. Use YYYY-MM'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payrolls = self.get_queryset().filter(payment_month=payment_month)
        
        if not payrolls.exists():
            return Response(
                {'error': f'Nenhuma folha encontrada para {payment_month.strftime("%m/%Y")}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calcular estatísticas
        total_amount = payrolls.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
        average_salary = total_amount / payrolls.count() if payrolls.count() > 0 else Decimal('0.00')
        
        serializer = PayrollSummarySerializer({
            'month': payment_month,
            'total_employees': payrolls.count(),
            'total_amount': total_amount,
            'total_amount_formatted': f"R$ {total_amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            'average_salary': average_salary,
            'average_salary_formatted': f"R$ {average_salary:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            'payrolls': payrolls
        })
        
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        """Marca uma folha como paga."""
        payroll = self.get_object()
        
        if payroll.payment_status == 'PAID':
            return Response(
                {'error': 'Folha já foi paga'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payroll.mark_as_paid()
        
        return Response({
            'message': 'Folha marcada como paga',
            'payroll': PayrollSerializer(payroll).data
        })


class PayrollHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para histórico de pagamentos.
    """
    serializer_class = PayrollHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PayrollHistory.objects.filter(user=self.request.user)