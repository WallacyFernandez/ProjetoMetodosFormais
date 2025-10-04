"""
Serializers do app de funcionários.
"""

from rest_framework import serializers
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date
from .models import EmployeePosition, Employee, Payroll, PayrollHistory


class EmployeePositionSerializer(serializers.ModelSerializer):
    """
    Serializer para cargos de funcionários.
    """
    department_display = serializers.CharField(source='get_department_display', read_only=True)
    
    class Meta:
        model = EmployeePosition
        fields = [
            'id', 'name', 'description', 'base_salary', 'min_salary', 
            'max_salary', 'department', 'department_display', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_base_salary(self, value):
        """Valida o salário base."""
        if value <= 0:
            raise serializers.ValidationError("Salário base deve ser maior que zero.")
        return value

    def validate(self, attrs):
        """Validação geral."""
        min_salary = attrs.get('min_salary')
        max_salary = attrs.get('max_salary')
        base_salary = attrs.get('base_salary')
        
        if min_salary and max_salary and min_salary > max_salary:
            raise serializers.ValidationError(
                "Salário mínimo não pode ser maior que o máximo."
            )
        
        if base_salary and min_salary and base_salary < min_salary:
            raise serializers.ValidationError(
                "Salário base não pode ser menor que o mínimo."
            )
        
        if base_salary and max_salary and base_salary > max_salary:
            raise serializers.ValidationError(
                "Salário base não pode ser maior que o máximo."
            )
        
        return attrs


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer para funcionários.
    """
    position_name = serializers.CharField(source='position.name', read_only=True)
    position_department = serializers.CharField(source='position.department', read_only=True)
    employment_status_display = serializers.CharField(source='get_employment_status_display', read_only=True)
    salary_formatted = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id', 'name', 'cpf', 'email', 'phone', 'position', 'position_name',
            'position_department', 'salary', 'salary_formatted', 'hire_date',
            'employment_status', 'employment_status_display', 'is_active',
            'termination_date', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_cpf(self, value):
        """Valida o CPF."""
        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, value))
        
        if len(cpf) != 11:
            raise serializers.ValidationError("CPF deve ter 11 dígitos.")
        
        # Validação básica de CPF
        if cpf == cpf[0] * 11:
            raise serializers.ValidationError("CPF inválido.")
        
        return value

    def validate_salary(self, value):
        """Valida o salário."""
        if value <= 0:
            raise serializers.ValidationError("Salário deve ser maior que zero.")
        return value

    def validate(self, attrs):
        """Validação geral."""
        position = attrs.get('position')
        salary = attrs.get('salary')
        
        if position and salary:
            if salary < position.min_salary:
                raise serializers.ValidationError(
                    f"Salário não pode ser menor que o mínimo do cargo: R$ {position.min_salary}"
                )
            if salary > position.max_salary:
                raise serializers.ValidationError(
                    f"Salário não pode ser maior que o máximo do cargo: R$ {position.max_salary}"
                )
        
        return attrs


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de funcionários.
    """
    class Meta:
        model = Employee
        fields = [
            'name', 'cpf', 'email', 'phone', 'position', 'salary',
            'hire_date', 'notes'
        ]

    def validate_cpf(self, value):
        """Valida o CPF."""
        cpf = ''.join(filter(str.isdigit, value))
        
        if len(cpf) != 11:
            raise serializers.ValidationError("CPF deve ter 11 dígitos.")
        
        if cpf == cpf[0] * 11:
            raise serializers.ValidationError("CPF inválido.")
        
        return value


class EmployeeTerminateSerializer(serializers.Serializer):
    """
    Serializer para demissão de funcionários.
    """
    termination_date = serializers.DateField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_termination_date(self, value):
        """Valida a data de demissão."""
        if value and value > date.today():
            raise serializers.ValidationError("Data de demissão não pode ser futura.")
        return value


class PayrollSerializer(serializers.ModelSerializer):
    """
    Serializer para folha de pagamento.
    """
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_position = serializers.CharField(source='employee.position.name', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    total_formatted = serializers.CharField(read_only=True)
    
    class Meta:
        model = Payroll
        fields = [
            'id', 'employee', 'employee_name', 'employee_position',
            'payment_month', 'base_salary', 'overtime_hours', 'overtime_value',
            'bonus', 'deductions', 'total_amount', 'total_formatted',
            'payment_date', 'payment_status', 'payment_status_display',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_overtime_hours(self, value):
        """Valida horas extras."""
        if value < 0:
            raise serializers.ValidationError("Horas extras não podem ser negativas.")
        return value

    def validate_overtime_value(self, value):
        """Valida valor das horas extras."""
        if value < 0:
            raise serializers.ValidationError("Valor das horas extras não pode ser negativo.")
        return value

    def validate_bonus(self, value):
        """Valida bônus."""
        if value < 0:
            raise serializers.ValidationError("Bônus não pode ser negativo.")
        return value

    def validate_deductions(self, value):
        """Valida descontos."""
        if value < 0:
            raise serializers.ValidationError("Descontos não podem ser negativos.")
        return value


class PayrollCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de folha de pagamento.
    """
    class Meta:
        model = Payroll
        fields = [
            'employee', 'payment_month', 'base_salary', 'overtime_hours',
            'overtime_value', 'bonus', 'deductions', 'notes'
        ]

    def validate_payment_month(self, value):
        """Valida o mês de pagamento."""
        if value > date.today():
            raise serializers.ValidationError("Mês de pagamento não pode ser futuro.")
        return value


class PayrollProcessSerializer(serializers.Serializer):
    """
    Serializer para processamento de pagamentos mensais.
    """
    payment_month = serializers.DateField()
    include_inactive = serializers.BooleanField(default=False)

    def validate_payment_month(self, value):
        """Valida o mês de pagamento."""
        if value > date.today():
            raise serializers.ValidationError("Mês de pagamento não pode ser futuro.")
        return value


class PayrollHistorySerializer(serializers.ModelSerializer):
    """
    Serializer para histórico de pagamentos.
    """
    payment_month_display = serializers.CharField(source='payment_month.strftime', read_only=True)
    total_amount_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = PayrollHistory
        fields = [
            'id', 'payment_month', 'payment_month_display', 'total_employees',
            'total_amount', 'total_amount_formatted', 'processed_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_total_amount_formatted(self, obj):
        """Retorna o valor total formatado."""
        return f"R$ {obj.total_amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


class EmployeeSummarySerializer(serializers.Serializer):
    """
    Serializer para resumo de funcionários.
    """
    total_employees = serializers.IntegerField()
    active_employees = serializers.IntegerField()
    inactive_employees = serializers.IntegerField()
    total_monthly_payroll = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_monthly_payroll_formatted = serializers.CharField()
    employees_by_department = serializers.DictField()
    employees_by_position = serializers.DictField()


class PayrollSummarySerializer(serializers.Serializer):
    """
    Serializer para resumo de folha de pagamento.
    """
    month = serializers.DateField()
    total_employees = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_amount_formatted = serializers.CharField()
    average_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    average_salary_formatted = serializers.CharField()
    payrolls = PayrollSerializer(many=True)
