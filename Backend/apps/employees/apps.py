"""
Configuração do app de funcionários.
"""

from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.employees'
    verbose_name = 'Funcionários'
    
    def ready(self):
        """Registra os sinais quando o app está pronto."""
        import apps.employees.signals