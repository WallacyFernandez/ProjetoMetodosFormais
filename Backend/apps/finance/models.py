"""
Modelos do app de finanças.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.core.models import BaseModel, ActiveManager, AllObjectsManager

User = get_user_model()


class UserBalance(BaseModel):
    """
    Modelo para gerenciar o saldo atual de cada usuário.
    Este modelo mantém o saldo consolidado do usuário.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='balance',
        verbose_name='Usuário'
    )
    current_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Saldo Atual'
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Atualização'
    )

    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Saldo do Usuário'
        verbose_name_plural = 'Saldos dos Usuários'
        ordering = ['-last_updated']

    def __str__(self):
        return f"Saldo de {self.user.full_name}: R$ {self.current_balance}"

    def add_amount(self, amount):
        """Adiciona um valor ao saldo atual."""
        if amount < 0:
            raise ValueError("Use subtract_amount() para valores negativos")
        self.current_balance += Decimal(str(amount))
        self.save()
        return self.current_balance

    def subtract_amount(self, amount):
        """Subtrai um valor do saldo atual."""
        if amount < 0:
            raise ValueError("Use add_amount() para valores positivos")
        self.current_balance -= Decimal(str(amount))
        self.save()
        return self.current_balance

    def set_balance(self, amount):
        """Define um novo valor para o saldo."""
        self.current_balance = Decimal(str(amount))
        self.save()
        return self.current_balance

    @property
    def balance_formatted(self):
        """Retorna o saldo formatado em reais."""
        return f"R$ {self.current_balance:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


class BalanceHistory(BaseModel):
    """
    Histórico de alterações no saldo do usuário.
    Registra todas as modificações para auditoria.
    """
    OPERATION_CHOICES = [
        ('ADD', 'Adição'),
        ('SUBTRACT', 'Subtração'),
        ('SET', 'Definição'),
        ('RESET', 'Reset'),
    ]

    user_balance = models.ForeignKey(
        UserBalance,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name='Saldo do Usuário'
    )
    operation = models.CharField(
        max_length=10,
        choices=OPERATION_CHOICES,
        verbose_name='Operação'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Valor'
    )
    previous_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Saldo Anterior'
    )
    new_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Novo Saldo'
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Descrição'
    )

    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Histórico de Saldo'
        verbose_name_plural = 'Históricos de Saldo'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.operation} - {self.user_balance.user.full_name} - R$ {self.amount}"
