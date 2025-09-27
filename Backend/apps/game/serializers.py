"""
Serializers para o app de jogo.
"""

from rest_framework import serializers
from .models import (
    GameSession, ProductCategory, Supplier, Product, ProductStockHistory, RealtimeSale
)


class GameSessionSerializer(serializers.ModelSerializer):
    """Serializer para sessões de jogo."""
    
    game_progress_percentage = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    current_game_time = serializers.SerializerMethodField()
    is_market_open = serializers.SerializerMethodField()
    
    class Meta:
        model = GameSession
        fields = [
            'id', 'user_name', 'game_start_date', 'current_game_date', 
            'game_end_date', 'status', 'time_acceleration', 'total_score',
            'days_survived', 'game_progress_percentage', 'days_remaining',
            'current_day_sales_count', 'last_update_time', 'current_game_time',
            'is_market_open', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_current_game_time(self, obj):
        """Retorna a hora atual do jogo."""
        from apps.game.models import RealtimeSale
        from django.utils import timezone
        
        now = timezone.now()
        game_time = RealtimeSale().get_game_time_from_real_time(now, obj)
        return game_time.strftime('%H:%M:%S')
    
    def get_is_market_open(self, obj):
        """Verifica se o mercado está aberto."""
        from apps.game.models import RealtimeSale
        from django.utils import timezone
        
        now = timezone.now()
        game_time = RealtimeSale().get_game_time_from_real_time(now, obj)
        return RealtimeSale().is_market_open(game_time)


# Removido: SupermarketBalanceSerializer e BalanceOperationSerializer
# Agora usamos o sistema financeiro existente


# Removido: BalanceHistorySerializer
# Agora usamos o sistema financeiro existente


class ProductCategorySerializer(serializers.ModelSerializer):
    """Serializer para categorias de produtos."""
    
    class Meta:
        model = ProductCategory
        fields = [
            'id', 'name', 'description', 'icon', 'color', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RealtimeSaleSerializer(serializers.ModelSerializer):
    """Serializer para vendas em tempo real."""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_icon = serializers.CharField(source='product.category.icon', read_only=True)
    sale_time_formatted = serializers.SerializerMethodField()
    game_date_formatted = serializers.SerializerMethodField()
    game_time_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = RealtimeSale
        fields = [
            'id', 'product_name', 'product_icon', 'quantity', 
            'unit_price', 'total_value', 'sale_time_formatted',
            'game_date', 'game_date_formatted', 'game_time', 'game_time_formatted'
        ]
    
    def get_sale_time_formatted(self, obj):
        """Formata o horário real da venda."""
        return obj.sale_time.strftime('%H:%M:%S')
    
    def get_game_date_formatted(self, obj):
        """Formata a data do jogo."""
        return obj.game_date.strftime('%d/%m/%Y')
    
    def get_game_time_formatted(self, obj):
        """Formata a hora do jogo."""
        return obj.game_time.strftime('%H:%M:%S')


class GameDashboardSerializer(serializers.Serializer):
    """Serializer para dados do dashboard do jogo."""
    
    game_session = GameSessionSerializer()
    balance = serializers.DictField()
    products = serializers.DictField()
    sales = serializers.DictField()
    stock_alerts = serializers.DictField()
    realtime_sales = RealtimeSaleSerializer(many=True)


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer para fornecedores."""
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'contact_person', 'email', 'phone', 'address',
            'delivery_time_days', 'minimum_order_value', 'reliability_score',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer para produtos."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    profit_margin = serializers.ReadOnlyField()
    profit_margin_formatted = serializers.ReadOnlyField()
    current_price = serializers.ReadOnlyField()
    is_low_stock = serializers.ReadOnlyField()
    is_out_of_stock = serializers.ReadOnlyField()
    stock_status = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'category_name',
            'category_icon', 'category_color', 'supplier', 'supplier_name',
            'purchase_price', 'sale_price', 'current_price', 'profit_margin',
            'profit_margin_formatted', 'current_stock', 'min_stock', 'max_stock',
            'shelf_life_days', 'is_active', 'is_promotional', 'promotional_price',
            'promotional_start_date', 'promotional_end_date', 'is_low_stock',
            'is_out_of_stock', 'stock_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductStockHistorySerializer(serializers.ModelSerializer):
    """Serializer para histórico de estoque."""
    
    operation_display = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    unit_price_formatted = serializers.SerializerMethodField()
    total_value_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductStockHistory
        fields = [
            'id', 'product', 'product_name', 'operation', 'operation_display',
            'quantity', 'previous_stock', 'new_stock', 'unit_price',
            'unit_price_formatted', 'total_value', 'total_value_formatted',
            'description', 'game_date', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_operation_display(self, obj):
        """Retorna o display da operação."""
        operation_displays = {
            'PURCHASE': 'Compra',
            'SALE': 'Venda',
            'ADJUSTMENT': 'Ajuste',
            'LOSS': 'Perda',
            'RETURN': 'Devolução',
        }
        return operation_displays.get(obj.operation, obj.operation)
    
    def get_unit_price_formatted(self, obj):
        """Retorna o preço unitário formatado."""
        if obj.unit_price:
            return f"R$ {obj.unit_price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return None
    
    def get_total_value_formatted(self, obj):
        """Retorna o valor total formatado."""
        if obj.total_value:
            return f"R$ {obj.total_value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return None


class ProductStockOperationSerializer(serializers.Serializer):
    """Serializer para operações de estoque."""
    
    quantity = serializers.IntegerField(min_value=1)
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)


class ProductPurchaseSerializer(serializers.Serializer):
    """Serializer para compra de produtos."""
    
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, min_value=0.01)
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)
