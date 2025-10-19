"""
Serializers para o app de usuários.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Profile."""
    
    class Meta:
        model = Profile
        fields = [
            'id', 'document', 'address', 'city', 'state', 
            'zip_code', 'country', 'email_notifications', 
            'sms_notifications', 'language', 'created_at', 
            'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_active']
    
    def validate_document(self, value):
        """Valida o documento (CPF/CNPJ)."""
        if value:
            # Remove caracteres não numéricos
            document = ''.join(filter(str.isdigit, value))
            
            # Validação básica de tamanho
            if len(document) not in [11, 14]:
                raise serializers.ValidationError(
                    "Documento deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ)."
                )
        return value
    
    def validate_zip_code(self, value):
        """Valida o CEP."""
        if value:
            # Remove caracteres não numéricos
            zip_code = ''.join(filter(str.isdigit, value))
            
            # Validação básica de tamanho
            if len(zip_code) != 8:
                raise serializers.ValidationError(
                    "CEP deve ter 8 dígitos."
                )
            
            # Formatar CEP
            return f"{zip_code[:5]}-{zip_code[5:]}"
        return value
    
    def validate_state(self, value):
        """Valida o estado (UF)."""
        if value:
            # Converte para maiúsculas
            value = value.upper()
            
            # Lista de estados brasileiros
            brazilian_states = [
                'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
                'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
                'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
            ]
            
            if value not in brazilian_states:
                raise serializers.ValidationError(
                    "Estado deve ser uma UF válida do Brasil."
                )
        return value


class UserSerializer(serializers.ModelSerializer):
    """Serializer para o modelo User (informações básicas)."""
    
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'full_name', 'phone', 'birth_date', 'avatar', 'bio',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'email', 'username', 'is_active', 
            'created_at', 'updated_at'
        ]
    
    def validate_phone(self, value):
        """Valida o telefone."""
        if value:
            # Remove caracteres não numéricos exceto +
            phone = ''.join(filter(lambda x: x.isdigit() or x == '+', value))
            
            # Validação básica de tamanho
            if len(phone) < 10 or len(phone) > 15:
                raise serializers.ValidationError(
                    "Telefone deve ter entre 10 e 15 dígitos."
                )
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer completo do usuário com perfil."""
    
    profile = ProfileSerializer(required=False)
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'full_name', 'phone', 'birth_date', 'avatar', 'bio',
            'profile', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'email', 'username', 'is_active', 
            'created_at', 'updated_at'
        ]
    
    def update(self, instance, validated_data):
        """Atualiza usuário e perfil."""
        profile_data = validated_data.pop('profile', None)
        
        # Atualizar dados do usuário
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Atualizar ou criar perfil
        if profile_data:
            profile, created = Profile.objects.get_or_create(
                user=instance,
                defaults=profile_data
            )
            if not created:
                for attr, value in profile_data.items():
                    setattr(profile, attr, value)
                profile.save()
        
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de usuário."""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    profile = ProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name',
            'phone', 'birth_date', 'avatar', 'bio', 'password',
            'password_confirm', 'profile'
        ]
    
    def validate(self, attrs):
        """Validação geral."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password_confirm": "Senhas não coincidem."}
            )
        return attrs
    
    def validate_email(self, value):
        """Valida o email."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Já existe um usuário com este email."
            )
        return value
    
    def validate_username(self, value):
        """Valida o username."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Já existe um usuário com este username."
            )
        return value
    
    def create(self, validated_data):
        """Cria usuário e perfil."""
        profile_data = validated_data.pop('profile', None)
        validated_data.pop('password_confirm')
        
        # Criar usuário
        user = User.objects.create_user(**validated_data)
        
        # Criar perfil se dados foram fornecidos
        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para mudança de senha."""
    
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """Validação geral."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password_confirm": "Senhas não coincidem."}
            )
        return attrs
    
    def validate_old_password(self, value):
        """Valida a senha atual."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Senha atual incorreta.")
        return value
    
    def save(self, **kwargs):
        """Salva a nova senha."""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
