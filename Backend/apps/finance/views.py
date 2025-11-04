"""
Views para o app de finanças.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import transaction, models
from django.utils import timezone
from decimal import Decimal

from .models import UserBalance, BalanceHistory, Category, Transaction
from .serializers import (
    UserBalanceSerializer,
    BalanceOperationSerializer,
    BalanceSetSerializer,
    BalanceHistorySerializer,
    CategorySerializer,
    TransactionSerializer,
    TransactionCreateSerializer,
    MonthlyReportSerializer,
    MonthlySummarySerializer,
    CategorySummarySerializer,
    DashboardSerializer
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


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar categorias de transações.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category_type', 'is_default']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        """Retorna categorias disponíveis para o usuário (padrão + personalizadas)."""
        return Category.get_user_categories(self.request.user)

    @action(detail=False, methods=['get'])
    def defaults(self, request):
        """Retorna apenas as categorias padrão do sistema."""
        categories = Category.get_default_categories()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def custom(self, request):
        """Retorna apenas as categorias personalizadas do usuário."""
        categories = Category.objects.filter(user=request.user)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar transações financeiras.
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['transaction_type', 'category', 'is_recurring']
    search_fields = ['description', 'subcategory']
    ordering_fields = ['transaction_date', 'amount', 'created_at']
    ordering = ['-transaction_date', '-created_at']

    def get_queryset(self):
        """Retorna apenas as transações do usuário autenticado."""
        queryset = Transaction.objects.filter(
            user=self.request.user,
            is_active=True
        )
        
        # Filtros adicionais por query params
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        amount_min = self.request.query_params.get('amount_min')
        amount_max = self.request.query_params.get('amount_max')

        if year:
            queryset = queryset.filter(transaction_date__year=year)
        if month:
            queryset = queryset.filter(transaction_date__month=month)
        if date_from:
            queryset = queryset.filter(transaction_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(transaction_date__lte=date_to)
        if amount_min:
            queryset = queryset.filter(amount__gte=amount_min)
        if amount_max:
            queryset = queryset.filter(amount__lte=amount_max)

        return queryset

    def get_serializer_class(self):
        """Usa serializer específico para criação."""
        if self.action == 'create':
            return TransactionCreateSerializer
        return TransactionSerializer

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        """Retorna resumo mensal de transações."""
        # Pega ano e mês dos parâmetros ou usa atual
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))
        
        # Valida os parâmetros
        report_serializer = MonthlyReportSerializer(data={'year': year, 'month': month})
        if not report_serializer.is_valid():
            return Response(report_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Gera o resumo
        summary = Transaction.get_monthly_summary(request.user, year, month)
        serializer = MonthlySummarySerializer(summary)
        
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def category_summary(self, request):
        """Retorna resumo por categoria."""
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))
        
        # Valida os parâmetros
        report_serializer = MonthlyReportSerializer(data={'year': year, 'month': month})
        if not report_serializer.is_valid():
            return Response(report_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Gera o resumo por categoria
        category_data = Transaction.get_category_summary(request.user, year, month)
        
        # Calcula o total para porcentagens
        total_amount = sum(item['total'] for item in category_data)
        
        serializer = CategorySummarySerializer(
            category_data, 
            many=True,
            context={'total_amount': total_amount}
        )
        
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Retorna as transações mais recentes."""
        limit = int(request.query_params.get('limit', 10))
        transactions = self.get_queryset()[:limit]
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def dashboard_data(self, request):
        """Retorna dados completos para o dashboard."""
        # Verificar se há uma sessão de jogo ativa para usar a data do jogo
        from apps.game.models import GameSession
        
        current_date = timezone.now()
        
        try:
            game_session = GameSession.objects.filter(
                user=request.user,
                status='ACTIVE'
            ).first()
            
            if game_session:
                # Usar data do jogo se houver sessão ativa
                summary_date = game_session.current_game_date
                summary_year = summary_date.year
                summary_month = summary_date.month
            else:
                # Usar data real se não houver sessão de jogo
                summary_year = current_date.year
                summary_month = current_date.month
        except Exception:
            # Em caso de erro, usar data real
            summary_year = current_date.year
            summary_month = current_date.month
        
        # Saldo atual
        balance, _ = UserBalance.objects.get_or_create(
            user=request.user,
            defaults={'current_balance': Decimal('0.00')}
        )
        
        # Resumo mensal atual
        monthly_summary = Transaction.get_monthly_summary(
            request.user, 
            summary_year, 
            summary_month
        )
        
        # Resumo por categoria
        category_summary = Transaction.get_category_summary(
            request.user, 
            summary_year, 
            summary_month
        )
        
        # Transações recentes
        recent_transactions = Transaction.objects.filter(
            user=request.user,
            is_active=True
        ).order_by('-transaction_date', '-created_at')[:5]
        
        # Estatísticas gerais
        total_transactions = Transaction.objects.filter(
            user=request.user,
            is_active=True
        ).count()
        
        # Média mensal (últimos 6 meses)
        six_months_ago = current_date - timezone.timedelta(days=180)
        monthly_averages = Transaction.objects.filter(
            user=request.user,
            transaction_date__gte=six_months_ago,
            is_active=True
        ).values('transaction_type').annotate(
            avg_amount=models.Avg('amount')
        )
        
        avg_income = Decimal('0.00')
        avg_expense = Decimal('0.00')
        for avg in monthly_averages:
            if avg['transaction_type'] == 'INCOME':
                avg_income = avg['avg_amount'] or Decimal('0.00')
            else:
                avg_expense = avg['avg_amount'] or Decimal('0.00')

        # Prepara os dados
        dashboard_data = {
            'current_balance': balance.current_balance,
            'current_balance_formatted': balance.balance_formatted,
            'monthly_summary': monthly_summary,
            'category_summary': category_summary,
            'recent_transactions': recent_transactions,
            'total_transactions_count': total_transactions,
            'avg_monthly_income': avg_income,
            'avg_monthly_expense': avg_expense,
        }
        
        # Serializa os dados
        serializer = DashboardSerializer(dashboard_data)
        return Response(serializer.data)
