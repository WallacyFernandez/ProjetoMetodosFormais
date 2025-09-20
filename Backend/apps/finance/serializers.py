"""
Serializers para o app de finanças.
"""

from rest_framework import serializers
from django.utils import timezone
from .models import UserBalance, BalanceHistory, Category, Transaction
from decimal import Decimal


class UserBalanceSerializer(serializers.ModelSerializer):
    """Serializer para o modelo UserBalance."""
    
    balance_formatted = serializers.ReadOnlyField()
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = UserBalance
        fields = [
            'id',
            'current_balance',
            'balance_formatted',
            'user_name',
            'last_updated',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'user', 'last_updated', 'created_at', 'updated_at']


class BalanceOperationSerializer(serializers.Serializer):
    """Serializer para operações de saldo (adicionar, subtrair, definir)."""
    
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0.01')
    )
    description = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True
    )
    
    def validate_amount(self, value):
        """Valida se o valor é positivo."""
        if value <= 0:
            raise serializers.ValidationError("O valor deve ser maior que zero.")
        return value


class BalanceSetSerializer(serializers.Serializer):
    """Serializer para definir um novo saldo."""
    
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0.00')
    )
    description = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True
    )


class BalanceHistorySerializer(serializers.ModelSerializer):
    """Serializer para o histórico de saldo."""
    
    user_name = serializers.CharField(source='user_balance.user.full_name', read_only=True)
    operation_display = serializers.CharField(source='get_operation_display', read_only=True)
    
    class Meta:
        model = BalanceHistory
        fields = [
            'id',
            'operation',
            'operation_display',
            'amount',
            'previous_balance',
            'new_balance',
            'description',
            'user_name',
            'created_at'
        ]
        read_only_fields = ['id', 'user_balance', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para o modelo Category."""
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'icon',
            'color',
            'category_type',
            'is_default',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'is_default', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Cria uma categoria personalizada para o usuário."""
        validated_data['user'] = self.context['request'].user
        validated_data['is_default'] = False
        return super().create(validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Transaction."""
    
    amount_formatted = serializers.ReadOnlyField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id',
            'amount',
            'amount_formatted',
            'transaction_type',
            'category',
            'category_name',
            'category_icon',
            'category_color',
            'subcategory',
            'description',
            'transaction_date',
            'receipt',
            'is_recurring',
            'recurrence_type',
            'recurrence_end_date',
            'parent_transaction',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'balance_updated']

    def create(self, validated_data):
        """Cria uma transação para o usuário autenticado."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_category(self, value):
        """Valida se a categoria pertence ao usuário ou é padrão."""
        user = self.context['request'].user
        user_categories = Category.get_user_categories(user)
        
        if value not in user_categories:
            raise serializers.ValidationError("Categoria inválida.")
        
        return value

    def validate(self, attrs):
        """Validações gerais da transação."""
        # Valida recorrência
        if attrs.get('is_recurring', False):
            if attrs.get('recurrence_type') == 'NONE':
                raise serializers.ValidationError({
                    'recurrence_type': 'Tipo de recorrência é obrigatório para transações recorrentes.'
                })
        
        # Valida data final de recorrência
        if attrs.get('recurrence_end_date'):
            if attrs.get('recurrence_end_date') <= attrs.get('transaction_date'):
                raise serializers.ValidationError({
                    'recurrence_end_date': 'Data final deve ser posterior à data da transação.'
                })

        return attrs


class TransactionCreateSerializer(TransactionSerializer):
    """Serializer específico para criação de transações com validações extras."""
    
    def validate_amount(self, value):
        """Valida o valor da transação."""
        if value <= 0:
            raise serializers.ValidationError("O valor deve ser maior que zero.")
        
        # Limite máximo para evitar erros
        if value > Decimal('999999999.99'):
            raise serializers.ValidationError("Valor muito alto.")
        
        return value


class MonthlyReportSerializer(serializers.Serializer):
    """Serializer para relatório mensal."""
    
    year = serializers.IntegerField(min_value=2020, max_value=2100)
    month = serializers.IntegerField(min_value=1, max_value=12)
    
    def validate(self, attrs):
        """Valida se a data não é futura."""
        current_date = timezone.now().date()
        report_date = timezone.datetime(attrs['year'], attrs['month'], 1).date()
        
        if report_date > current_date:
            raise serializers.ValidationError("Não é possível gerar relatório para datas futuras.")
        
        return attrs


class MonthlySummarySerializer(serializers.Serializer):
    """Serializer para resumo mensal de transações."""
    
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    income_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    expense_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    transaction_count = serializers.IntegerField()
    
    # Campos formatados
    income_total_formatted = serializers.SerializerMethodField()
    expense_total_formatted = serializers.SerializerMethodField()
    balance_formatted = serializers.SerializerMethodField()
    
    def get_income_total_formatted(self, obj):
        return f"R$ {obj['income_total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def get_expense_total_formatted(self, obj):
        return f"R$ {obj['expense_total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def get_balance_formatted(self, obj):
        balance = obj['balance']
        sign = '+' if balance >= 0 else ''
        return f"{sign}R$ {balance:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


class CategorySummarySerializer(serializers.Serializer):
    """Serializer para resumo por categoria."""
    
    category__name = serializers.CharField()
    category__icon = serializers.CharField()
    category__color = serializers.CharField()
    transaction_type = serializers.CharField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
    count = serializers.IntegerField()
    
    # Campos formatados
    total_formatted = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    
    def get_total_formatted(self, obj):
        return f"R$ {obj['total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def get_percentage(self, obj):
        """Calcula a porcentagem baseada no contexto total."""
        total_amount = self.context.get('total_amount', obj['total'])
        if total_amount > 0:
            return round((obj['total'] / total_amount) * 100, 1)
        return 0.0


class DashboardSerializer(serializers.Serializer):
    """Serializer para dados completos do dashboard."""
    
    current_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    current_balance_formatted = serializers.CharField()
    monthly_summary = MonthlySummarySerializer()
    category_summary = CategorySummarySerializer(many=True)
    recent_transactions = TransactionSerializer(many=True)
    
    # Estatísticas adicionais
    total_transactions_count = serializers.IntegerField()
    avg_monthly_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    avg_monthly_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
