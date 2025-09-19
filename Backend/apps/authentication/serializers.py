"""
Serializers de autenticação.
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from apps.users.models import User
from apps.core.utils import validate_email_address


class LoginSerializer(serializers.Serializer):
    """
    Serializer para login de usuário.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate_email(self, value):
        """Valida o formato do email."""
        if not validate_email_address(value):
            raise serializers.ValidationError("Email inválido.")
        return value.lower()

    def validate(self, attrs):
        """Validação adicional."""
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email e senha são obrigatórios.")

        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de novo usuário.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone'
        )
        extra_kwargs = {
            'username': {'required': True},
            'phone': {'required': False},
        }

    def validate_email(self, value):
        """Valida se o email já está em uso."""
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value.lower()

    def validate_username(self, value):
        """Valida se o username já está em uso."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value

    def validate(self, attrs):
        """Valida se as senhas coincidem."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs

    def create(self, validated_data):
        """Cria um novo usuário."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer para alteração de senha.
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        """Valida se a senha atual está correta."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Senha atual incorreta.")
        return value

    def validate(self, attrs):
        """Valida se as novas senhas coincidem."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("As novas senhas não coincidem.")
        return attrs


class TokenRefreshSerializer(serializers.Serializer):
    """
    Serializer para refresh token.
    """
    refresh = serializers.CharField(required=True)

    def validate_refresh(self, value):
        """Valida o refresh token."""
        if not value:
            raise serializers.ValidationError("Refresh token é obrigatório.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para informações do perfil do usuário.
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 
            'full_name', 'phone', 'birth_date', 'bio', 'avatar',
            'is_staff', 'is_superuser', 'date_joined', 'last_login'
        )
        read_only_fields = ('id', 'email', 'is_staff', 'is_superuser', 'date_joined', 'last_login')

    def get_full_name(self, obj):
        """Retorna o nome completo do usuário."""
        return obj.full_name


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer para solicitação de reset de senha.
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Valida se o email existe no sistema."""
        if not User.objects.filter(email=value.lower(), is_active=True).exists():
            raise serializers.ValidationError("Não existe usuário ativo com este email.")
        return value.lower()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer para confirmação de reset de senha.
    """
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """Valida se as novas senhas coincidem."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs
