"""
Views para o app de jogo.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction, models
from decimal import Decimal

from .models import (
    GameSession, ProductCategory, Supplier, Product, ProductStockHistory
)
from .serializers import (
    GameSessionSerializer, ProductCategorySerializer, GameDashboardSerializer,
    SupplierSerializer, ProductSerializer, ProductStockHistorySerializer,
    ProductStockOperationSerializer, ProductPurchaseSerializer
)

# Importar modelos do sistema financeiro
from apps.finance.models import UserBalance, Transaction, Category


class GameSessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar sessões de jogo.
    """
    serializer_class = GameSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas a sessão do usuário logado."""
        return GameSession.objects.filter(user=self.request.user)

    def get_object(self):
        """Retorna a sessão do usuário logado."""
        return get_object_or_404(GameSession, user=self.request.user)

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Retorna a sessão atual do usuário."""
        try:
            game_session = GameSession.objects.get(user=request.user)
            # Atualiza o tempo do jogo
            game_session.update_game_time()
            
            serializer = self.get_serializer(game_session)
            return Response(serializer.data)
        except GameSession.DoesNotExist:
            return Response(
                {'error': 'Sessão de jogo não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def pause(self, request):
        """Pausa o jogo."""
        game_session = self.get_object()
        game_session.pause_game()
        
        serializer = self.get_serializer(game_session)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def resume(self, request):
        """Retoma o jogo."""
        game_session = self.get_object()
        game_session.resume_game()
        
        serializer = self.get_serializer(game_session)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def reset(self, request):
        """Reinicia o jogo."""
        game_session = self.get_object()
        game_session.reset_game()
        
        serializer = self.get_serializer(game_session)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def update_time(self, request):
        """Atualiza o tempo do jogo manualmente."""
        game_session = self.get_object()
        days_passed = game_session.update_game_time()
        
        serializer = self.get_serializer(game_session)
        return Response({
            'game_session': serializer.data,
            'days_passed': days_passed
        })


class SupermarketBalanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar o saldo do supermercado.
    """
    serializer_class = SupermarketBalanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas o saldo do usuário logado."""
        return SupermarketBalance.objects.filter(
            game_session__user=self.request.user
        )

    def get_object(self):
        """Retorna o saldo do usuário logado."""
        return get_object_or_404(
            SupermarketBalance,
            game_session__user=self.request.user
        )

    @action(detail=False, methods=['post'])
    def add(self, request):
        """Adiciona valor ao saldo."""
        serializer = BalanceOperationSerializer(data=request.data)
        if serializer.is_valid():
            supermarket_balance = self.get_object()
            
            with transaction.atomic():
                new_balance = supermarket_balance.add_amount(
                    serializer.validated_data['amount'],
                    serializer.validated_data.get('description', '')
                )
            
            response_serializer = self.get_serializer(supermarket_balance)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def subtract(self, request):
        """Subtrai valor do saldo."""
        serializer = BalanceOperationSerializer(data=request.data)
        if serializer.is_valid():
            supermarket_balance = self.get_object()
            
            with transaction.atomic():
                new_balance = supermarket_balance.subtract_amount(
                    serializer.validated_data['amount'],
                    serializer.validated_data.get('description', '')
                )
            
            response_serializer = self.get_serializer(supermarket_balance)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def set(self, request):
        """Define um novo valor para o saldo."""
        serializer = BalanceOperationSerializer(data=request.data)
        if serializer.is_valid():
            supermarket_balance = self.get_object()
            
            with transaction.atomic():
                new_balance = supermarket_balance.set_balance(
                    serializer.validated_data['amount'],
                    serializer.validated_data.get('description', '')
                )
            
            response_serializer = self.get_serializer(supermarket_balance)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BalanceHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar histórico de saldo.
    """
    serializer_class = BalanceHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas o histórico do usuário logado."""
        return BalanceHistory.objects.filter(
            supermarket_balance__game_session__user=self.request.user
        ).order_by('-created_at')


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar categorias de produtos.
    """
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna todas as categorias ativas."""
        return ProductCategory.objects.filter(is_active=True)


class GameDashboardViewSet(viewsets.ViewSet):
    """
    ViewSet para dados do dashboard do jogo.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def data(self, request):
        """Retorna dados completos do dashboard."""
        try:
            game_session = GameSession.objects.get(user=request.user)
            game_session.update_game_time()
            
            supermarket_balance = SupermarketBalance.objects.get(
                game_session=game_session
            )
            
            recent_transactions = BalanceHistory.objects.filter(
                supermarket_balance=supermarket_balance
            ).order_by('-created_at')[:10]
            
            categories = ProductCategory.objects.filter(is_active=True)
            
            data = {
                'game_session': GameSessionSerializer(game_session).data,
                'supermarket_balance': SupermarketBalanceSerializer(supermarket_balance).data,
                'recent_transactions': BalanceHistorySerializer(recent_transactions, many=True).data,
                'categories': ProductCategorySerializer(categories, many=True).data,
            }
            
            return Response(data)
            
        except (GameSession.DoesNotExist, SupermarketBalance.DoesNotExist):
            return Response(
                {'error': 'Dados do jogo não encontrados'},
                status=status.HTTP_404_NOT_FOUND
            )


class SupplierViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar fornecedores.
    """
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas fornecedores ativos."""
        return Supplier.objects.filter(is_active=True)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar produtos.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas produtos ativos."""
        return Product.objects.filter(is_active=True).select_related('category', 'supplier')

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Retorna produtos com estoque baixo."""
        products = self.get_queryset().filter(current_stock__lte=models.F('min_stock'))
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        """Retorna produtos fora de estoque."""
        products = self.get_queryset().filter(current_stock=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        """Compra produtos do fornecedor."""
        product = self.get_object()
        serializer = ProductPurchaseSerializer(data=request.data)
        
        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']
            unit_price = serializer.validated_data.get('unit_price', product.purchase_price)
            description = serializer.validated_data.get('description', f'Compra de {product.name}')
            
            try:
                with transaction.atomic():
                    # Verifica se tem saldo suficiente
                    game_session = GameSession.objects.get(user=request.user)
                    supermarket_balance = SupermarketBalance.objects.get(game_session=game_session)
                    
                    total_cost = unit_price * quantity
                    if supermarket_balance.current_balance < total_cost:
                        return Response(
                            {'error': 'Saldo insuficiente para esta compra'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Adiciona ao estoque
                    previous_stock = product.current_stock
                    product.add_stock(quantity)
                    
                    # Subtrai do saldo
                    supermarket_balance.subtract_amount(
                        total_cost,
                        f'Compra: {product.name} - {quantity} unidades'
                    )
                    
                    # Registra no histórico de estoque
                    ProductStockHistory.objects.create(
                        product=product,
                        operation='PURCHASE',
                        quantity=quantity,
                        previous_stock=previous_stock,
                        new_stock=product.current_stock,
                        unit_price=unit_price,
                        total_value=total_cost,
                        description=description
                    )
                    
                    return Response({
                        'message': 'Compra realizada com sucesso',
                        'product': ProductSerializer(product).data,
                        'total_cost': total_cost
                    })
                    
            except Exception as e:
                return Response(
                    {'error': f'Erro ao realizar compra: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductStockHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar histórico de estoque.
    """
    serializer_class = ProductStockHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna histórico de estoque."""
        return ProductStockHistory.objects.select_related('product').order_by('-created_at')


class ProductSalesViewSet(viewsets.ViewSet):
    """
    ViewSet para operações de vendas.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def simulate_sale(self, request):
        """Simula uma venda de produto."""
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        if not product_id:
            return Response(
                {'error': 'ID do produto é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            
            if product.current_stock < quantity:
                return Response(
                    {'error': 'Estoque insuficiente'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with transaction.atomic():
                # Remove do estoque
                previous_stock = product.current_stock
                product.remove_stock(quantity)
                
                # Calcula receita
                total_revenue = product.current_price * quantity
                
                # Adiciona ao saldo
                game_session = GameSession.objects.get(user=request.user)
                supermarket_balance = SupermarketBalance.objects.get(game_session=game_session)
                supermarket_balance.add_amount(
                    total_revenue,
                    f'Venda: {product.name} - {quantity} unidades'
                )
                
                # Registra no histórico de estoque
                ProductStockHistory.objects.create(
                    product=product,
                    operation='SALE',
                    quantity=quantity,
                    previous_stock=previous_stock,
                    new_stock=product.current_stock,
                    unit_price=product.current_price,
                    total_value=total_revenue,
                    description=f'Venda simulada de {quantity} unidades'
                )
                
                return Response({
                    'message': 'Venda realizada com sucesso',
                    'product': ProductSerializer(product).data,
                    'total_revenue': total_revenue,
                    'quantity_sold': quantity
                })
                
        except Product.DoesNotExist:
            return Response(
                {'error': 'Produto não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao realizar venda: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def sales_summary(self, request):
        """Retorna resumo de vendas."""
        try:
            game_session = GameSession.objects.get(user=request.user)
            
            # Busca vendas recentes
            recent_sales = ProductStockHistory.objects.filter(
                operation='SALE',
                created_at__gte=game_session.session_start_time
            ).select_related('product').order_by('-created_at')[:10]
            
            # Calcula estatísticas
            total_sales = recent_sales.count()
            total_revenue = sum(sale.total_value or 0 for sale in recent_sales)
            
            # Produtos mais vendidos
            from django.db.models import Sum
            top_products = ProductStockHistory.objects.filter(
                operation='SALE',
                created_at__gte=game_session.session_start_time
            ).values('product__name').annotate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum('total_value')
            ).order_by('-total_quantity')[:5]
            
            return Response({
                'total_sales': total_sales,
                'total_revenue': total_revenue,
                'recent_sales': ProductStockHistorySerializer(recent_sales, many=True).data,
                'top_products': list(top_products)
            })
            
        except GameSession.DoesNotExist:
            return Response(
                {'error': 'Sessão de jogo não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
