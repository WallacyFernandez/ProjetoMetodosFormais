"""
Views para o app de jogo.
Integrado com o sistema financeiro existente.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction, models
from django.utils import timezone
from decimal import Decimal
from datetime import date

from .models import (
    GameSession, ProductCategory, Supplier, Product, ProductStockHistory, RealtimeSale
)
from .serializers import (
    GameSessionSerializer, ProductCategorySerializer, GameDashboardSerializer,
    SupplierSerializer, ProductSerializer, ProductStockHistorySerializer,
    ProductStockOperationSerializer, ProductPurchaseSerializer, RealtimeSaleSerializer
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
        return GameSession.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(
            GameSession,
            user=self.request.user
        )

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Retorna a sessão atual do usuário."""
        game_session = self.get_object()
        serializer = self.get_serializer(game_session)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def update_time(self, request):
        """Atualiza o tempo do jogo."""
        game_session = self.get_object()
        days_passed = game_session.update_game_time()
        serializer = self.get_serializer(game_session)
        return Response({
            'game_session': serializer.data,
            'days_passed': days_passed
        })

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
    def start(self, request):
        """Inicia o jogo."""
        game_session = self.get_object()
        game_session.start_game()
        serializer = self.get_serializer(game_session)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def reset(self, request):
        """Reinicia o jogo completamente."""
        game_session = self.get_object()
        game_session.reset_game()
        serializer = self.get_serializer(game_session)
        return Response(serializer.data)


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar categorias de produtos.
    """
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductCategory.objects.filter(is_active=True)


class SupplierViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar fornecedores.
    """
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Supplier.objects.filter(is_active=True)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar produtos.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
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
            try:
                with transaction.atomic():
                    # Obter dados da compra
                    quantity = serializer.validated_data['quantity']
                    unit_price = serializer.validated_data.get('unit_price', product.purchase_price)
                    description = serializer.validated_data.get('description', f'Compra de {product.name}')
                    total_value = unit_price * quantity
                    
                    # Verificar saldo disponível
                    user_balance = UserBalance.objects.get(user=request.user)
                    if user_balance.current_balance < total_value:
                        return Response(
                            {'error': 'Saldo insuficiente'}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Subtrair do saldo
                    user_balance.subtract_amount(total_value)
                    
                    # Adicionar ao estoque
                    product.add_stock(quantity)
                    
                    # Registrar no histórico de estoque
                    ProductStockHistory.objects.create(
                        product=product,
                        operation='PURCHASE',
                        quantity=quantity,
                        previous_stock=product.current_stock - quantity,
                        new_stock=product.current_stock,
                        unit_price=unit_price,
                        total_value=total_value,
                        description=description
                    )
                    
                    # Criar transação financeira
                    compras_category, _ = Category.objects.get_or_create(
                        name='Compras',
                        defaults={
                            'description': 'Compras de produtos dos fornecedores',
                            'color': '#EF4444',
                            'icon': '🛒'
                        }
                    )
                    Transaction.objects.create(
                        user=request.user,
                        amount=total_value,
                        transaction_type='EXPENSE',
                        category=compras_category,
                        description=f'Compra: {product.name} - {quantity} unidades',
                        transaction_date=date.today()
                    )
                    
                    return Response({
                        'message': 'Compra realizada com sucesso',
                        'product': ProductSerializer(product).data,
                        'total_value': total_value
                    })
                    
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
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
        return ProductStockHistory.objects.select_related('product').order_by('-created_at')


class ProductSalesViewSet(viewsets.ViewSet):
    """
    ViewSet para operações de vendas.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def simulate_sale(self, request):
        """Simula uma venda de produto."""
        serializer = ProductStockOperationSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    product_id = request.data.get('product_id')
                    quantity = serializer.validated_data['quantity']
                    description = serializer.validated_data.get('description', f'Venda de {quantity} unidades')
                    
                    product = Product.objects.get(id=product_id, is_active=True)
                    
                    # Verificar estoque
                    if product.current_stock < quantity:
                        return Response(
                            {'error': 'Estoque insuficiente'}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Calcular valor da venda
                    unit_price = product.current_price
                    total_value = unit_price * quantity
                    
                    # Remover do estoque
                    product.remove_stock(quantity)
                    
                    # Adicionar ao saldo
                    user_balance = UserBalance.objects.get(user=request.user)
                    user_balance.add_amount(total_value)
                    
                    # Registrar no histórico de estoque
                    ProductStockHistory.objects.create(
                        product=product,
                        operation='SALE',
                        quantity=quantity,
                        previous_stock=product.current_stock + quantity,
                        new_stock=product.current_stock,
                        unit_price=unit_price,
                        total_value=total_value,
                        description=description
                    )
                    
                    # Criar transação financeira
                    vendas_category, _ = Category.objects.get_or_create(
                        name='Vendas',
                        defaults={
                            'description': 'Receitas de vendas de produtos',
                            'color': '#10B981',
                            'icon': '💰'
                        }
                    )
                    Transaction.objects.create(
                        user=request.user,
                        amount=total_value,
                        transaction_type='INCOME',
                        category=vendas_category,
                        description=f'Venda: {product.name} - {quantity} unidades',
                        transaction_date=date.today()
                    )
                    
                    return Response({
                        'message': 'Venda realizada com sucesso',
                        'product': ProductSerializer(product).data,
                        'total_value': total_value
                    })
                    
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def sales_summary(self, request):
        """Retorna resumo de vendas."""
        from django.db.models import Sum, Count
        
        # Vendas recentes (últimos 30 dias)
        from datetime import timedelta
        recent_sales = ProductStockHistory.objects.filter(
            operation='SALE',
            created_at__gte=timezone.now() - timedelta(days=30)
        ).order_by('-created_at')[:10]
        
        # Produtos mais vendidos
        top_products = ProductStockHistory.objects.filter(
            operation='SALE'
        ).values('product__name').annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('total_value')
        ).order_by('-total_quantity')[:5]
        
        # Totais
        total_sales = ProductStockHistory.objects.filter(
            operation='SALE'
        ).aggregate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('total_value')
        )
        
        return Response({
            'total_sales': total_sales['total_quantity'] or 0,
            'total_revenue': total_sales['total_revenue'] or 0,
            'recent_sales': ProductStockHistorySerializer(recent_sales, many=True).data,
            'top_products': list(top_products)
        })


class GameDashboardViewSet(viewsets.ViewSet):
    """
    ViewSet para dados do dashboard do jogo.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def data(self, request):
        """Retorna dados do dashboard do jogo."""
        try:
            # Sessão de jogo
            game_session = GameSession.objects.get(user=request.user)
            
            # Saldo do usuário (Caixa da Loja)
            user_balance = UserBalance.objects.get(user=request.user)
            
            # Estatísticas de produtos
            total_products = Product.objects.filter(is_active=True).count()
            low_stock_products = Product.objects.filter(
                is_active=True,
                current_stock__lte=models.F('min_stock')
            ).count()
            out_of_stock_products = Product.objects.filter(
                is_active=True,
                current_stock=0
            ).count()
            
            # Resumo de vendas da sessão atual
            from django.db.models import Sum
            sales_summary = RealtimeSale.objects.filter(
                game_session=game_session
            ).aggregate(
                total_sales=Sum('quantity'),
                total_revenue=Sum('total_value')
            )
            
            # Alertas de estoque
            low_stock_products = Product.objects.filter(
                is_active=True,
                current_stock__lte=models.F('min_stock'),
                current_stock__gt=0
            ).count()
            
            out_of_stock_products = Product.objects.filter(
                is_active=True,
                current_stock=0
            ).count()
            
            # Busca vendas em tempo real apenas do dia atual do jogo (últimas 20)
            realtime_sales = RealtimeSale.objects.filter(
                game_session=game_session,
                game_date=game_session.current_game_date
            ).select_related('product', 'product__category').order_by('-game_time')[:20]
            
            return Response({
                'game_session': GameSessionSerializer(game_session).data,
                'balance': {
                    'current_balance': user_balance.current_balance,
                    'balance_formatted': user_balance.balance_formatted
                },
                'products': {
                    'total': total_products,
                    'low_stock': low_stock_products,
                    'out_of_stock': out_of_stock_products
                },
                'sales': {
                    'total_sales': sales_summary['total_sales'] or 0,
                    'total_revenue': sales_summary['total_revenue'] or 0
                },
                'stock_alerts': {
                    'low_stock_count': low_stock_products,
                    'out_of_stock_count': out_of_stock_products,
                    'has_alerts': low_stock_products > 0 or out_of_stock_products > 0
                },
                'realtime_sales': RealtimeSaleSerializer(realtime_sales, many=True).data
            })
            
        except GameSession.DoesNotExist:
            return Response(
                {'error': 'Sessão de jogo não encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except UserBalance.DoesNotExist:
            return Response(
                {'error': 'Saldo do usuário não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar produtos.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    @action(detail=False, methods=['post'])
    def restock_all(self, request):
        """
        Repõe todo o estoque para sua capacidade máxima.
        Calcula o valor total e debita do saldo do usuário.
        """
        try:
            # Obter saldo do usuário
            user_balance = UserBalance.objects.get(user=request.user)
            
            # Obter todos os produtos ativos
            products = Product.objects.filter(is_active=True)
            
            total_cost = Decimal('0.00')
            restocked_products = []
            
            with transaction.atomic():
                for product in products:
                    # Calcular quantidade necessária para repor ao máximo
                    quantity_needed = product.max_stock - product.current_stock
                    
                    if quantity_needed > 0:
                        # Calcular custo total para este produto
                        product_cost = product.purchase_price * quantity_needed
                        total_cost += product_cost
                        
                        # Atualizar estoque
                        old_stock = product.current_stock
                        product.current_stock = product.max_stock
                        product.save()
                        
                        # Registrar no histórico de estoque
                        ProductStockHistory.objects.create(
                            product=product,
                            operation='PURCHASE',
                            quantity=quantity_needed,
                            previous_stock=old_stock,
                            new_stock=product.current_stock,
                            unit_price=product.purchase_price,
                            total_value=product_cost,
                            description=f'Reposição automática para estoque máximo',
                            game_date=date.today()
                        )
                        
                        restocked_products.append({
                            'id': product.id,
                            'name': product.name,
                            'quantity_added': quantity_needed,
                            'new_stock': product.current_stock,
                            'cost': float(product_cost)
                        })
                
                # Verificar se o usuário tem saldo suficiente
                if total_cost > user_balance.current_balance:
                    return Response(
                        {
                            'error': 'Saldo insuficiente',
                            'required_amount': float(total_cost),
                            'current_balance': float(user_balance.current_balance),
                            'shortfall': float(total_cost - user_balance.current_balance)
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Debitar do saldo do usuário
                previous_balance = user_balance.current_balance
                user_balance.current_balance -= total_cost
                user_balance.save()
                
                # Registrar transação financeira (sem atualizar saldo automaticamente)
                # Buscar categoria de Compras ou usar a primeira disponível
                category = Category.objects.filter(name='Compras').first()
                if not category:
                    category = Category.objects.filter(category_type='EXPENSE').first()
                if not category:
                    category = Category.objects.first()
                
                if not category:
                    raise Exception("Nenhuma categoria encontrada para registrar a transação")
                
                financial_transaction = Transaction(
                    user=request.user,
                    amount=total_cost,  # Valor positivo para despesa
                    description=f'Reposição automática de estoque - {len(restocked_products)} produtos',
                    category=category,
                    transaction_type='EXPENSE',
                    balance_updated=True  # Marca como já atualizado para evitar duplo débito
                )
                financial_transaction.save()
                
                # Registrar no histórico de saldo
                from apps.finance.models import BalanceHistory
                BalanceHistory.objects.create(
                    user_balance=user_balance,
                    operation='SUBTRACT',
                    amount=total_cost,
                    previous_balance=previous_balance,
                    new_balance=user_balance.current_balance,
                    description=f"Reposição automática de estoque - {len(restocked_products)} produtos"
                )
                
                return Response({
                    'success': True,
                    'message': f'Estoque reposto com sucesso! {len(restocked_products)} produtos foram reabastecidos.',
                    'total_cost': float(total_cost),
                    'restocked_products': restocked_products,
                    'new_balance': float(user_balance.current_balance)
                })
                
        except UserBalance.DoesNotExist:
            return Response(
                {'error': 'Saldo do usuário não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao repor estoque: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def restock_cost(self, request):
        """
        Calcula o custo total para repor todo o estoque ao máximo.
        """
        try:
            products = Product.objects.filter(is_active=True)
            
            total_cost = Decimal('0.00')
            products_needing_restock = []
            
            for product in products:
                quantity_needed = product.max_stock - product.current_stock
                
                if quantity_needed > 0:
                    product_cost = product.purchase_price * quantity_needed
                    total_cost += product_cost
                    
                    products_needing_restock.append({
                        'id': product.id,
                        'name': product.name,
                        'current_stock': product.current_stock,
                        'max_stock': product.max_stock,
                        'quantity_needed': quantity_needed,
                        'unit_price': float(product.purchase_price),
                        'total_cost': float(product_cost)
                    })
            
            return Response({
                'total_cost': float(total_cost),
                'products_count': len(products_needing_restock),
                'products_needing_restock': products_needing_restock
            })
            
        except Exception as e:
            return Response(
                {'error': f'Erro ao calcular custo: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
