"""
Modelos do app de usuários.
"""

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from apps.core.models import BaseModel, ActiveManager, AllObjectsManager
from django.core.validators import RegexValidator


class User(AbstractUser, BaseModel):
    """
    Modelo de usuário customizado.
    """
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150, verbose_name='Nome')
    last_name = models.CharField(max_length=150, verbose_name='Sobrenome')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Número de telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
    )
    phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        null=True,
        verbose_name='Telefone'
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name='Data de nascimento')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Avatar')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Biografia')
    
    # Managers
    objects = UserManager()  # Manager padrão do Django para User
    all_objects = AllObjectsManager()  # Manager para todos os objetos
    active = ActiveManager()  # Manager para objetos ativos
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        """Retorna o nome completo do usuário."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Retorna o primeiro nome do usuário."""
        return self.first_name


class Profile(BaseModel):
    """
    Perfil do usuário com informações adicionais.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name='Usuário'
    )
    document = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='Documento (CPF/CNPJ)'
    )
    address = models.TextField(blank=True, verbose_name='Endereço')
    city = models.CharField(max_length=100, blank=True, verbose_name='Cidade')
    state = models.CharField(max_length=2, blank=True, verbose_name='Estado')
    zip_code = models.CharField(max_length=10, blank=True, verbose_name='CEP')
    country = models.CharField(max_length=50, default='Brasil', verbose_name='País')
    
    # Preferências
    email_notifications = models.BooleanField(default=True, verbose_name='Notificações por email')
    sms_notifications = models.BooleanField(default=False, verbose_name='Notificações por SMS')
    language = models.CharField(
        max_length=10, 
        default='pt-br',
        choices=[
            ('pt-br', 'Português (Brasil)'),
            ('en', 'English'),
            ('es', 'Español'),
        ],
        verbose_name='Idioma'
    )
    
    # Managers
    objects = models.Manager()  # Manager padrão
    all_objects = AllObjectsManager()  # Manager para todos os objetos
    active = ActiveManager()  # Manager para objetos ativos

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['-created_at']

    def __str__(self):
        return f"Perfil de {self.user.full_name}"


class UserSession(BaseModel):
    """
    Sessões de usuário para controle de login.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name='Usuário'
    )
    session_key = models.CharField(max_length=40, unique=True, verbose_name='Chave da sessão')
    ip_address = models.GenericIPAddressField(verbose_name='Endereço IP')
    user_agent = models.TextField(verbose_name='User Agent')
    last_activity = models.DateTimeField(auto_now=True, verbose_name='Última atividade')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')

    # Managers
    objects = models.Manager()  # Manager padrão
    all_objects = AllObjectsManager()  # Manager para todos os objetos
    active = ActiveManager()  # Manager para objetos ativos

    class Meta:
        verbose_name = 'Sessão do Usuário'
        verbose_name_plural = 'Sessões dos Usuários'
        ordering = ['-last_activity']

    def __str__(self):
        return f"Sessão de {self.user.full_name} - {self.ip_address}"