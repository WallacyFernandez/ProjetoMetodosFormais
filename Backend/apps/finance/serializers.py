"""
Serializers para o app de finanças.
"""

from rest_framework import serializers
from .models import UserBalance, BalanceHistory
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
