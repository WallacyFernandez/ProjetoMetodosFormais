"""
Modelos do app de funcionários.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
from datetime import date, datetime
from apps.core.models import BaseModel, ActiveManager, AllObjectsManager

User = get_user_model()


class EmployeePosition(BaseModel):
    """
    Modelo para cargos/funções dos funcionários no supermercado.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nome do Cargo'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    base_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Salário Base'
    )
    min_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Salário Mínimo'
    )
    max_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Salário Máximo'
    )
    department = models.CharField(
        max_length=50,
        choices=[
            ('VENDAS', 'Vendas'),
            ('ESTOQUE', 'Estoque'),
            ('CAIXA', 'Caixa'),
            ('GERENCIA', 'Gerência'),
            ('LIMPEZA', 'Limpeza'),
            ('SEGURANCA', 'Segurança'),
            ('RH', 'Recursos Humanos'),
        ],
        verbose_name='Departamento'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )

    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.get_department_display()}"

    @classmethod
    def get_default_positions(cls):
        """Retorna cargos padrão para o supermercado."""
        return [
            {
                'name': 'Caixa',
                'description': 'Responsável pelo atendimento ao cliente e operação do caixa',
                'base_salary': Decimal('1500.00'),
                'min_salary': Decimal('1200.00'),
                'max_salary': Decimal('2000.00'),
                'department': 'CAIXA',
            },
            {
                'name': 'Vendedor',
                'description': 'Atendimento ao cliente e reposição de produtos',
                'base_salary': Decimal('1400.00'),
                'min_salary': Decimal('1100.00'),
                'max_salary': Decimal('1800.00'),
                'department': 'VENDAS',
            },
            {
                'name': 'Repositor',
                'description': 'Responsável pela reposição e organização do estoque',
                'base_salary': Decimal('1300.00'),
                'min_salary': Decimal('1000.00'),
                'max_salary': Decimal('1700.00'),
                'department': 'ESTOQUE',
            },
            {
                'name': 'Gerente',
                'description': 'Supervisão geral das operações do supermercado',
                'base_salary': Decimal('3000.00'),
                'min_salary': Decimal('2500.00'),
                'max_salary': Decimal('4000.00'),
                'department': 'GERENCIA',
            },
            {
                'name': 'Auxiliar de Limpeza',
                'description': 'Limpeza e manutenção do ambiente',
                'base_salary': Decimal('1000.00'),
                'min_salary': Decimal('800.00'),
                'max_salary': Decimal('1300.00'),
                'department': 'LIMPEZA',
            },
            {
                'name': 'Segurança',
                'description': 'Vigilância e segurança do estabelecimento',
                'base_salary': Decimal('1600.00'),
                'min_salary': Decimal('1300.00'),
                'max_salary': Decimal('2100.00'),
                'department': 'SEGURANCA',
            },
        ]


class Employee(BaseModel):
    """
    Modelo para funcionários da empresa.
    """
    EMPLOYMENT_STATUS_CHOICES = [
        ('ACTIVE', 'Ativo'),
        ('INACTIVE', 'Inativo'),
        ('ON_LEAVE', 'Afastado'),
        ('TERMINATED', 'Demitido'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name='Empregador'
    )
    name = models.CharField(
        max_length=150,
        verbose_name='Nome Completo'
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        verbose_name='CPF'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email'
    )
    phone = models.CharField(
        max_length=17,
        blank=True,
        null=True,
        verbose_name='Telefone'
    )
    position = models.ForeignKey(
        EmployeePosition,
        on_delete=models.PROTECT,
        related_name='employees',
        verbose_name='Cargo'
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Salário'
    )
    hire_date = models.DateField(
        default=date.today,
        verbose_name='Data de Contratação'
    )
    employment_status = models.CharField(
        max_length=12,
        choices=EMPLOYMENT_STATUS_CHOICES,
        default='ACTIVE',
        verbose_name='Status'
    )
    termination_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Data de Demissão'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações'
    )

    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['name']
        unique_together = ['user', 'cpf']

    def __str__(self):
        return f"{self.name} - {self.position.name}"

    def clean(self):
        """Validação personalizada."""
        from django.core.exceptions import ValidationError
        
        # Validar se o salário está dentro dos limites do cargo
        if self.salary < self.position.min_salary:
            raise ValidationError(
                f"Salário não pode ser menor que o mínimo do cargo: R$ {self.position.min_salary}"
            )
        if self.salary > self.position.max_salary:
            raise ValidationError(
                f"Salário não pode ser maior que o máximo do cargo: R$ {self.position.max_salary}"
            )

    def terminate(self, termination_date=None):
        """Demite o funcionário."""
        self.employment_status = 'TERMINATED'
        self.termination_date = termination_date or date.today()
        self.save()

    def reactivate(self):
        """Reativa o funcionário."""
        self.employment_status = 'ACTIVE'
        self.termination_date = None
        self.save()

    @property
    def is_active(self):
        """Verifica se o funcionário está ativo."""
        return self.employment_status == 'ACTIVE'

    @property
    def salary_formatted(self):
        """Retorna o salário formatado."""
        return f"R$ {self.salary:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


class Payroll(BaseModel):
    """
    Modelo para controle de folha de pagamento.
    """
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('PAID', 'Pago'),
        ('CANCELLED', 'Cancelado'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='payrolls',
        verbose_name='Funcionário'
    )
    payment_month = models.DateField(
        verbose_name='Mês de Pagamento'
    )
    base_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Salário Base'
    )
    overtime_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Horas Extras'
    )
    overtime_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Valor Horas Extras'
    )
    bonus = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Bônus'
    )
    deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Descontos'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor Total'
    )
    payment_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Data de Pagamento'
    )
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING',
        verbose_name='Status do Pagamento'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações'
    )

    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Folha de Pagamento'
        verbose_name_plural = 'Folhas de Pagamento'
        ordering = ['-payment_month', 'employee__name']
        unique_together = ['employee', 'payment_month']

    def __str__(self):
        return f"{self.employee.name} - {self.payment_month.strftime('%m/%Y')}"

    def calculate_total(self):
        """Calcula o valor total da folha."""
        self.total_amount = (
            self.base_salary + 
            self.overtime_value + 
            self.bonus - 
            self.deductions
        )
        return self.total_amount

    def save(self, *args, **kwargs):
        """Salva calculando o total automaticamente."""
        self.calculate_total()
        super().save(*args, **kwargs)

    def mark_as_paid(self, payment_date=None):
        """Marca como pago."""
        self.payment_status = 'PAID'
        self.payment_date = payment_date or date.today()
        self.save()

    @property
    def total_formatted(self):
        """Retorna o valor total formatado."""
        return f"R$ {self.total_amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


class PayrollHistory(BaseModel):
    """
    Histórico de pagamentos processados.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payroll_histories',
        verbose_name='Empregador'
    )
    payment_month = models.DateField(
        verbose_name='Mês de Pagamento'
    )
    total_employees = models.IntegerField(
        verbose_name='Total de Funcionários'
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Valor Total Pago'
    )
    processed_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Processado em'
    )

    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Histórico de Pagamentos'
        verbose_name_plural = 'Históricos de Pagamentos'
        ordering = ['-payment_month']

    def __str__(self):
        return f"Pagamentos {self.payment_month.strftime('%m/%Y')} - {self.user.full_name}"