"""
Configuração do admin para o app de usuários.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from .models import Profile

User = get_user_model()


class ProfileInline(admin.StackedInline):
    """Inline para edição de perfil junto com usuário."""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'
    fields = [
        ('document', 'phone'),
        ('address', 'city'),
        ('state', 'zip_code', 'country'),
        ('email_notifications', 'sms_notifications', 'language'),
    ]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin customizado para o modelo User."""
    
    inlines = [ProfileInline]
    list_display = [
        'email', 'username', 'full_name', 'phone', 
        'is_active', 'is_staff', 'created_at'
    ]
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 
        'created_at', 'updated_at'
    ]
    search_fields = [
        'email', 'username', 'first_name', 'last_name', 'phone'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Informações Pessoais', {
            'fields': ('first_name', 'last_name', 'phone', 'birth_date', 'avatar', 'bio')
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'date_joined', 'last_login']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    def get_queryset(self, request):
        """Retorna queryset com todos os objetos."""
        return User.all_objects.all()
    
    def has_delete_permission(self, request, obj=None):
        """Permite soft delete apenas."""
        return True
    
    def delete_model(self, request, obj):
        """Executa soft delete."""
        obj.soft_delete()
    
    def delete_queryset(self, request, queryset):
        """Executa soft delete em lote."""
        queryset.update(is_active=False)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin para o modelo Profile."""
    
    list_display = [
        'user', 'city', 'state', 'country', 
        'email_notifications', 'is_active', 'created_at'
    ]
    list_filter = [
        'is_active', 'country', 'state', 'language',
        'email_notifications', 'sms_notifications', 'created_at'
    ]
    search_fields = [
        'user__email', 'user__username', 'user__first_name', 
        'user__last_name', 'document', 'city', 'address'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Documento', {
            'fields': ('document',)
        }),
        ('Endereço', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Preferências', {
            'fields': ('email_notifications', 'sms_notifications', 'language')
        }),
        ('Metadados', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        """Retorna queryset com todos os objetos."""
        return Profile.all_objects.all()
    
    def has_delete_permission(self, request, obj=None):
        """Permite soft delete apenas."""
        return True
    
    def delete_model(self, request, obj):
        """Executa soft delete."""
        obj.soft_delete()
    
    def delete_queryset(self, request, queryset):
        """Executa soft delete em lote."""
        queryset.update(is_active=False)
    
    def get_readonly_fields(self, request, obj=None):
        """Campos readonly baseados no contexto."""
        readonly_fields = list(self.readonly_fields)
        if obj:  # Editando objeto existente
            readonly_fields.append('user')
        return readonly_fields