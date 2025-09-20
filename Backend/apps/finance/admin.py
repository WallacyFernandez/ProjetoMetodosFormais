from django.contrib import admin
from .models import UserBalance, BalanceHistory


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
