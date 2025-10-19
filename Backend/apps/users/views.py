"""
Views para o app de usuários.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Profile
from .serializers import (
    UserSerializer, UserProfileSerializer, UserCreateSerializer,
    ProfileSerializer, ChangePasswordSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de usuários."""
    
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado baseado na ação."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        else:
            return UserProfileSerializer
    
    def get_permissions(self):
        """Define permissões baseadas na ação."""
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Retorna queryset filtrado por usuário logado."""
        if self.action == 'list' and not self.request.user.is_staff:
            # Usuários comuns só podem ver seu próprio perfil
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()
    
    def get_object(self):
        """Retorna o objeto específico."""
        if self.action == 'retrieve' and self.kwargs.get('pk') == 'me':
            return self.request.user
        return super().get_object()
    
    def list(self, request, *args, **kwargs):
        """Lista usuários (apenas para staff)."""
        if not request.user.is_staff:
            return Response(
                {'detail': 'Você não tem permissão para listar usuários.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Cria novo usuário."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            user = serializer.save()
        
        # Retornar dados do usuário criado sem a senha
        response_serializer = UserProfileSerializer(user)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Atualiza usuário."""
        instance = self.get_object()
        
        # Usuários comuns só podem atualizar seu próprio perfil
        if not request.user.is_staff and instance != request.user:
            return Response(
                {'detail': 'Você só pode atualizar seu próprio perfil.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete do usuário."""
        instance = self.get_object()
        
        # Usuários comuns só podem fazer soft delete de si mesmos
        if not request.user.is_staff and instance != request.user:
            return Response(
                {'detail': 'Você só pode excluir seu próprio perfil.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get', 'put', 'patch'], url_path='me')
    def current_user(self, request):
        """Retorna ou atualiza dados do usuário logado."""
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        else:  # PUT or PATCH
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        """Muda a senha do usuário logado."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {'detail': 'Senha alterada com sucesso.'},
            status=status.HTTP_200_OK
        )


class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de perfis."""
    
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna queryset filtrado por usuário logado."""
        if self.request.user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)
    
    def get_object(self):
        """Retorna o perfil do usuário logado."""
        if self.kwargs.get('pk') == 'me':
            profile, created = Profile.objects.get_or_create(
                user=self.request.user
            )
            return profile
        return super().get_object()
    
    def list(self, request, *args, **kwargs):
        """Lista perfis."""
        if not request.user.is_staff:
            return Response(
                {'detail': 'Você não tem permissão para listar perfis.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Cria perfil."""
        # Verificar se o usuário já tem um perfil
        if Profile.objects.filter(user=request.user).exists():
            return Response(
                {'detail': 'Você já possui um perfil.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save(user=request.user)
        
        return Response(
            self.get_serializer(profile).data,
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Atualiza perfil."""
        instance = self.get_object()
        
        # Usuários comuns só podem atualizar seu próprio perfil
        if not request.user.is_staff and instance.user != request.user:
            return Response(
                {'detail': 'Você só pode atualizar seu próprio perfil.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete do perfil."""
        instance = self.get_object()
        
        # Usuários comuns só podem fazer soft delete de seu próprio perfil
        if not request.user.is_staff and instance.user != request.user:
            return Response(
                {'detail': 'Você só pode excluir seu próprio perfil.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get', 'put', 'patch'], url_path='me')
    def current_profile(self, request):
        """Retorna ou atualiza perfil do usuário logado."""
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        else:  # PUT or PATCH
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)