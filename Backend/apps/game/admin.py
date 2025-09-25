"""
Admin para o app de jogo.
"""

from django.contrib import admin
from .models import (
    GameSession, ProductCategory, Supplier, Product, ProductStockHistory
)


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_game_date', 'status', 'days_survived', 'total_score']
    list_filter = ['status', 'game_start_date']
    search_fields = ['user__email', 'user__full_name']
    readonly_fields = ['session_start_time', 'last_update_time']


# Removido: SupermarketBalanceAdmin e BalanceHistoryAdmin
# Agora usamos o sistema financeiro existente


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'icon', 'color', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'delivery_time_days', 'reliability_score', 'is_active']
    list_filter = ['is_active', 'delivery_time_days']
    search_fields = ['name', 'contact_person', 'email']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'supplier', 'current_stock', 'sale_price', 'is_active']
    list_filter = ['category', 'supplier', 'is_active', 'is_promotional']
    search_fields = ['name', 'description']
    readonly_fields = ['profit_margin', 'profit_margin_formatted', 'current_price', 'stock_status']


@admin.register(ProductStockHistory)
class ProductStockHistoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'operation', 'quantity', 'game_date', 'description']
    list_filter = ['operation', 'game_date']
    search_fields = ['product__name', 'description']
