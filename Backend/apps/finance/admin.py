from django.contrib import admin
from .models import UserBalance, BalanceHistory, Category, Transaction


@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    """Configuração do admin para UserBalance."""
    list_display = ['user', 'current_balance', 'balance_formatted', 'last_updated', 'created_at']
    list_filter = ['created_at', 'last_updated']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at', 'last_updated']
    ordering = ['-last_updated']

    def has_add_permission(self, request):
        """Não permite adicionar saldos manualmente pelo admin."""
        return False


@admin.register(BalanceHistory)
class BalanceHistoryAdmin(admin.ModelAdmin):
    """Configuração do admin para BalanceHistory."""
    list_display = ['user_balance', 'operation', 'amount', 'previous_balance', 'new_balance', 'created_at']
    list_filter = ['operation', 'created_at']
    search_fields = ['user_balance__user__email', 'user_balance__user__first_name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        """Não permite adicionar histórico manualmente pelo admin."""
        return False

    def has_change_permission(self, request, obj=None):
        """Não permite editar histórico."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Não permite deletar histórico."""
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Configuração do admin para Category."""
    list_display = ['name', 'icon', 'category_type', 'is_default', 'user', 'created_at']
    list_filter = ['category_type', 'is_default', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['is_default', 'category_type', 'name']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description', 'icon', 'color')
        }),
        ('Configurações', {
            'fields': ('category_type', 'is_default', 'user')
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Customiza a queryset para mostrar todas as categorias."""
        return Category.all_objects.all()


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Configuração do admin para Transaction."""
    list_display = [
        'user', 'amount_formatted', 'transaction_type', 'category', 
        'description', 'transaction_date', 'balance_updated', 'created_at'
    ]
    list_filter = [
        'transaction_type', 'category', 'is_recurring', 'balance_updated', 
        'transaction_date', 'created_at'
    ]
    search_fields = ['description', 'subcategory', 'user__email', 'user__first_name']
    readonly_fields = ['balance_updated', 'created_at', 'updated_at']
    ordering = ['-transaction_date', '-created_at']
    date_hierarchy = 'transaction_date'
    
    fieldsets = (
        ('Informações da Transação', {
            'fields': ('user', 'amount', 'transaction_type', 'description')
        }),
        ('Categorização', {
            'fields': ('category', 'subcategory')
        }),
        ('Data e Comprovante', {
            'fields': ('transaction_date', 'receipt')
        }),
        ('Recorrência', {
            'fields': ('is_recurring', 'recurrence_type', 'recurrence_end_date', 'parent_transaction'),
            'classes': ('collapse',)
        }),
        ('Sistema', {
            'fields': ('balance_updated', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Otimiza a queryset com select_related."""
        return Transaction.objects.select_related('user', 'category').all()

    def amount_formatted(self, obj):
        """Mostra o valor formatado."""
        return obj.amount_formatted
    amount_formatted.short_description = 'Valor'
    amount_formatted.admin_order_field = 'amount'
