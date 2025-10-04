"""
Admin do app de funcionários.
"""

from django.contrib import admin
from .models import EmployeePosition, Employee, Payroll, PayrollHistory


@admin.register(EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'base_salary', 'min_salary', 'max_salary', 'is_active']
    list_filter = ['department', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'salary', 'employment_status', 'hire_date', 'user']
    list_filter = ['employment_status', 'position__department', 'hire_date', 'user']
    search_fields = ['name', 'cpf', 'email']
    ordering = ['name']
    raw_id_fields = ['user', 'position']


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ['employee', 'payment_month', 'total_amount', 'payment_status', 'payment_date']
    list_filter = ['payment_status', 'payment_month', 'employee__user']
    search_fields = ['employee__name', 'notes']
    ordering = ['-payment_month', 'employee__name']
    raw_id_fields = ['employee']


@admin.register(PayrollHistory)
class PayrollHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_month', 'total_employees', 'total_amount', 'processed_at']
    list_filter = ['payment_month', 'processed_at', 'user']
    ordering = ['-payment_month']
    raw_id_fields = ['user']