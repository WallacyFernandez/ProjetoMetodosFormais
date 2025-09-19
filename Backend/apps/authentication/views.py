"""
Views de autenticação.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from apps.users.models import User
from apps.core.utils import success_response, error_response
from .serializers import (
    LoginSerializer, 
    RegisterSerializer, 
    ChangePasswordSerializer,
    TokenRefreshSerializer
)
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Endpoint para autenticação de usuário.
    """
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return error_response(
            message='Dados inválidos',
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    # Autenticar usuário
    user = authenticate(request, username=email, password=password)
    
    if not user:
        return error_response(
            message='Credenciais inválidas',
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    if not user.is_active:
        return error_response(
            message='Conta desativada',
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    # Gerar tokens JWT
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    
    # Atualizar último login
    update_last_login(None, user)
    
    # Log da ação
    logger.info(f"Login realizado com sucesso para o usuário: {user.email}")
    
    data = {
        'user': {
            'id': str(user.id),
            'email': user.email,
            'full_name': user.full_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        },
        'tokens': {
            'access': str(access_token),
            'refresh': str(refresh),
        }
    }
    
    return success_response(
        data=data,
        message='Login realizado com sucesso',
        status_code=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Endpoint para registro de novo usuário.
    """
    serializer = RegisterSerializer(data=request.data)
    
    if not serializer.is_valid():
        return error_response(
            message='Dados inválidos',
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = serializer.save()
        
        # Gerar tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        # Log da ação
        logger.info(f"Novo usuário registrado: {user.email}")
        
        data = {
            'user': {
                'id': str(user.id),
                'email': user.email,
                'full_name': user.full_name,
            },
            'tokens': {
                'access': str(access_token),
                'refresh': str(refresh),
            }
        }
        
        return success_response(
            data=data,
            message='Usuário criado com sucesso',
            status_code=status.HTTP_201_CREATED
        )
        
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {str(e)}")
        return error_response(
            message='Erro interno do servidor',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Endpoint para logout do usuário.
    """
    try:
        refresh_token = request.data.get('refresh_token')
        
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        # Log da ação
        logger.info(f"Logout realizado para o usuário: {request.user.email}")
        
        return success_response(
            message='Logout realizado com sucesso',
            status_code=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Erro no logout: {str(e)}")
        return error_response(
            message='Erro ao fazer logout',
            status_code=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    Endpoint para refresh do token de acesso.
    """
    serializer = TokenRefreshSerializer(data=request.data)
    
    if not serializer.is_valid():
        return error_response(
            message='Token inválido',
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        refresh = RefreshToken(serializer.validated_data['refresh'])
        access_token = refresh.access_token
        
        data = {
            'access': str(access_token),
        }
        
        return success_response(
            data=data,
            message='Token atualizado com sucesso',
            status_code=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Erro ao atualizar token: {str(e)}")
        return error_response(
            message='Token inválido ou expirado',
            status_code=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Endpoint para alteração de senha.
    """
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    
    if not serializer.is_valid():
        return error_response(
            message='Dados inválidos',
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Log da ação
        logger.info(f"Senha alterada para o usuário: {user.email}")
        
        return success_response(
            message='Senha alterada com sucesso',
            status_code=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Erro ao alterar senha: {str(e)}")
        return error_response(
            message='Erro interno do servidor',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """
    Endpoint para obter informações do usuário logado.
    """
    user = request.user
    
    data = {
        'id': str(user.id),
        'email': user.email,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': user.full_name,
        'phone': user.phone,
        'birth_date': user.birth_date,
        'bio': user.bio,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    }
    
    return success_response(
        data=data,
        message='Dados do usuário carregados com sucesso',
        status_code=status.HTTP_200_OK
    )