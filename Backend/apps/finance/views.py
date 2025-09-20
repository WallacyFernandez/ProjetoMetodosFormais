"""
Views para o app de finanças.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from decimal import Decimal

from .models import UserBalance, BalanceHistory
from .serializers import (
    UserBalanceSerializer,
    BalanceOperationSerializer,
    BalanceSetSerializer,
    BalanceHistorySerializer
)


class UserBalanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar o saldo do usuário.
    Fornece operações CRUD e ações específicas para manipulação do saldo.
    """
    serializer_class = UserBalanceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas o saldo do usuário autenticado."""
        return UserBalance.objects.filter(user=self.request.user)
    
    def get_object(self):
        """Retorna ou cria o saldo do usuário autenticado."""
        balance, created = UserBalance.objects.get_or_create(
            user=self.request.user,
            defaults={'current_balance': Decimal('0.00')}
        )
        return balance
    
    def list(self, request, *args, **kwargs):
        """Lista o saldo do usuário (sempre retorna apenas um item)."""
        balance = self.get_object()
        serializer = self.get_serializer(balance)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Retorna o saldo atual do usuário."""
        balance = self.get_object()
        serializer = self.get_serializer(balance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_amount(self, request):
        """Adiciona um valor ao saldo atual."""
        serializer = BalanceOperationSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            description = serializer.validated_data.get('description', '')
            
            with transaction.atomic():
                balance = self.get_object()
                previous_balance = balance.current_balance
                new_balance = balance.add_amount(amount)
                
                # Registra no histórico
                BalanceHistory.objects.create(
                    user_balance=balance,
                    operation='ADD',
                    amount=amount,
                    previous_balance=previous_balance,
                    new_balance=new_balance,
                    description=description or f'Adição de R$ {amount}'
                )
            
            response_serializer = UserBalanceSerializer(balance)
            return Response({
                'message': f'Valor de R$ {amount} adicionado com sucesso.',
                'balance': response_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def subtract_amount(self, request):
        """Subtrai um valor do saldo atual."""
        serializer = BalanceOperationSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            description = serializer.validated_data.get('description', '')
            
            with transaction.atomic():
                balance = self.get_object()
                
                # Verifica se há saldo suficiente
                if balance.current_balance < amount:
                    return Response({
                        'error': 'Saldo insuficiente para esta operação.',
                        'current_balance': str(balance.current_balance),
                        'requested_amount': str(amount)
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                previous_balance = balance.current_balance
                new_balance = balance.subtract_amount(amount)
                
                # Registra no histórico
                BalanceHistory.objects.create(
                    user_balance=balance,
                    operation='SUBTRACT',
                    amount=amount,
                    previous_balance=previous_balance,
                    new_balance=new_balance,
                    description=description or f'Subtração de R$ {amount}'
                )
            
            response_serializer = UserBalanceSerializer(balance)
            return Response({
                'message': f'Valor de R$ {amount} subtraído com sucesso.',
                'balance': response_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def set_balance(self, request):
        """Define um novo valor para o saldo."""
        serializer = BalanceSetSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            description = serializer.validated_data.get('description', '')
            
            with transaction.atomic():
                balance = self.get_object()
                previous_balance = balance.current_balance
                new_balance = balance.set_balance(amount)
                
                # Registra no histórico
                BalanceHistory.objects.create(
                    user_balance=balance,
                    operation='SET',
                    amount=amount,
                    previous_balance=previous_balance,
                    new_balance=new_balance,
                    description=description or f'Saldo definido para R$ {amount}'
                )
            
            response_serializer = UserBalanceSerializer(balance)
            return Response({
                'message': f'Saldo definido para R$ {amount} com sucesso.',
                'balance': response_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def reset_balance(self, request):
        """Reseta o saldo para zero."""
        with transaction.atomic():
            balance = self.get_object()
            previous_balance = balance.current_balance
            new_balance = balance.set_balance(Decimal('0.00'))
            
            # Registra no histórico
            BalanceHistory.objects.create(
                user_balance=balance,
                operation='RESET',
                amount=Decimal('0.00'),
                previous_balance=previous_balance,
                new_balance=new_balance,
                description='Saldo resetado para R$ 0,00'
            )
        
        response_serializer = UserBalanceSerializer(balance)
        return Response({
            'message': 'Saldo resetado para R$ 0,00 com sucesso.',
            'balance': response_serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Retorna o histórico de alterações do saldo."""
        balance = self.get_object()
        history = BalanceHistory.objects.filter(user_balance=balance)
        
        # Paginação
        page = self.paginate_queryset(history)
        if page is not None:
            serializer = BalanceHistorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BalanceHistorySerializer(history, many=True)
        return Response(serializer.data)
