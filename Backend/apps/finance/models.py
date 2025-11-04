"""
Modelos do app de finanças.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from datetime import date
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


class Category(BaseModel):
    """
    Modelo para categorias de transações.
    """
    CATEGORY_TYPES = [
        ('INCOME', 'Receita'),
        ('EXPENSE', 'Despesa'),
        ('BOTH', 'Ambos'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name='Nome'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )
    icon = models.CharField(
        max_length=50,
        default='💰',
        verbose_name='Ícone'
    )
    color = models.CharField(
        max_length=7,
        default='#3B82F6',
        help_text='Cor em hexadecimal (#RRGGBB)',
        verbose_name='Cor'
    )
    category_type = models.CharField(
        max_length=10,
        choices=CATEGORY_TYPES,
        default='BOTH',
        verbose_name='Tipo de Categoria'
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='Categoria Padrão',
        help_text='Categorias padrão do sistema'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='custom_categories',
        null=True,
        blank=True,
        verbose_name='Usuário',
        help_text='Se vazio, é uma categoria padrão do sistema'
    )

    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']
        unique_together = [['name', 'user']]  # Nome único por usuário

    def __str__(self):
        return f"{self.icon} {self.name}"

    @classmethod
    def get_default_categories(cls):
        """Retorna as categorias padrão do sistema."""
        return cls.objects.filter(is_default=True)

    @classmethod
    def get_user_categories(cls, user):
        """Retorna todas as categorias disponíveis para um usuário."""
        return cls.objects.filter(
            models.Q(is_default=True) | models.Q(user=user)
        )


class Transaction(BaseModel):
    """
    Modelo para transações financeiras (receitas e despesas).
    """
    TRANSACTION_TYPES = [
        ('INCOME', 'Receita'),
        ('EXPENSE', 'Despesa'),
    ]

    RECURRENCE_TYPES = [
        ('NONE', 'Não recorrente'),
        ('DAILY', 'Diário'),
        ('WEEKLY', 'Semanal'),
        ('MONTHLY', 'Mensal'),
        ('YEARLY', 'Anual'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Usuário'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor'
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES,
        verbose_name='Tipo'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='Categoria'
    )
    subcategory = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Subcategoria'
    )
    description = models.CharField(
        max_length=255,
        verbose_name='Descrição'
    )
    transaction_date = models.DateField(
        default=date.today,
        verbose_name='Data da Transação'
    )
    receipt = models.ImageField(
        upload_to='receipts/%Y/%m/',
        null=True,
        blank=True,
        verbose_name='Comprovante'
    )
    
    # Campos para transações recorrentes
    is_recurring = models.BooleanField(
        default=False,
        verbose_name='É Recorrente'
    )
    recurrence_type = models.CharField(
        max_length=10,
        choices=RECURRENCE_TYPES,
        default='NONE',
        verbose_name='Tipo de Recorrência'
    )
    recurrence_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data Final da Recorrência'
    )
    parent_transaction = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='recurring_transactions',
        verbose_name='Transação Pai'
    )

    # Campo para controlar se já afetou o saldo
    balance_updated = models.BooleanField(
        default=False,
        verbose_name='Saldo Atualizado'
    )

    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-transaction_date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'transaction_date']),
            models.Index(fields=['user', 'transaction_type']),
            models.Index(fields=['user', 'category']),
        ]

    def __str__(self):
        sign = '+' if self.transaction_type == 'INCOME' else '-'
        return f"{sign}R$ {self.amount} - {self.description} ({self.transaction_date})"

    @property
    def amount_formatted(self):
        """Retorna o valor formatado em reais."""
        sign = '+' if self.transaction_type == 'INCOME' else '-'
        return f"{sign}R$ {self.amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    def save(self, *args, **kwargs):
        """Override do save para atualizar o saldo automaticamente."""
        is_new = self.pk is None
        old_transaction = None
        
        if not is_new:
            try:
                old_transaction = Transaction.objects.get(pk=self.pk)
            except Transaction.DoesNotExist:
                # Se a transação não existe mais, trata como nova
                is_new = True

        super().save(*args, **kwargs)

        # Atualiza o saldo se necessário
        if is_new and not self.balance_updated:
            self.update_user_balance()
        elif old_transaction and (
            old_transaction.amount != self.amount or 
            old_transaction.transaction_type != self.transaction_type
        ):
            # Se mudou valor ou tipo, reverte o valor antigo e aplica o novo
            self.revert_balance_update(old_transaction)
            self.update_user_balance()

    def update_user_balance(self):
        """Atualiza o saldo do usuário baseado nesta transação."""
        from django.db import transaction
        
        with transaction.atomic():
            balance, created = UserBalance.objects.get_or_create(
                user=self.user,
                defaults={'current_balance': Decimal('0.00')}
            )
            
            previous_balance = balance.current_balance
            
            if self.transaction_type == 'INCOME':
                balance.current_balance += self.amount
                operation = 'ADD'
            else:  # EXPENSE
                balance.current_balance -= self.amount
                operation = 'SUBTRACT'
            
            balance.save()
            
            # Registra no histórico
            BalanceHistory.objects.create(
                user_balance=balance,
                operation=operation,
                amount=self.amount,
                previous_balance=previous_balance,
                new_balance=balance.current_balance,
                description=f"Transação: {self.description}"
            )
            
            # Marca como atualizado
            self.balance_updated = True
            Transaction.objects.filter(pk=self.pk).update(balance_updated=True)

    def revert_balance_update(self, old_transaction):
        """Reverte a atualização de saldo de uma transação antiga."""
        from django.db import transaction as db_transaction
        
        with db_transaction.atomic():
            balance = UserBalance.objects.get(user=self.user)
            previous_balance = balance.current_balance
            
            # Reverte o valor antigo
            if old_transaction.transaction_type == 'INCOME':
                balance.current_balance -= old_transaction.amount
                operation = 'SUBTRACT'
            else:  # EXPENSE
                balance.current_balance += old_transaction.amount
                operation = 'ADD'
            
            balance.save()
            
            # Registra no histórico
            BalanceHistory.objects.create(
                user_balance=balance,
                operation=operation,
                amount=old_transaction.amount,
                previous_balance=previous_balance,
                new_balance=balance.current_balance,
                description=f"Reversão: {old_transaction.description}"
            )

    def delete(self, *args, **kwargs):
        """Override do delete para reverter o saldo."""
        if self.balance_updated:
            self.revert_balance_update(self)
        super().delete(*args, **kwargs)

    @classmethod
    def get_monthly_summary(cls, user, year=None, month=None):
        """Retorna resumo mensal de transações."""
        if not year:
            year = timezone.now().year
        if not month:
            month = timezone.now().month

        transactions = cls.objects.filter(
            user=user,
            is_active=True
        ).filter(
            transaction_date__year=year,
            transaction_date__month=month
        )

        income_total = transactions.filter(
            transaction_type='INCOME'
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')

        expense_total = transactions.filter(
            transaction_type='EXPENSE'
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')

        balance = income_total - expense_total

        return {
            'year': year,
            'month': month,
            'income_total': income_total,
            'expense_total': expense_total,
            'balance': balance,
            'transaction_count': transactions.count(),
        }

    @classmethod
    def get_category_summary(cls, user, year=None, month=None):
        """Retorna resumo por categoria."""
        if not year:
            year = timezone.now().year
        if not month:
            month = timezone.now().month

        return cls.objects.filter(
            user=user,
            transaction_date__year=year,
            transaction_date__month=month,
            is_active=True
        ).values(
            'category__name',
            'category__icon',
            'category__color',
            'transaction_type'
        ).annotate(
            total=models.Sum('amount'),
            count=models.Count('id')
        ).order_by('-total')
