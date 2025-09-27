"""
Views para gerenciamento de produtos, categorias e fornecedores.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction, models
from decimal import Decimal
from datetime import date

from ..models import Product, ProductCategory, Supplier, ProductStockHistory
from ..serializers import (
    ProductSerializer, ProductCategorySerializer, SupplierSerializer,
    ProductPurchaseSerializer
)
from apps.finance.models import UserBalance, Transaction, Category, BalanceHistory


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


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar produtos.
    Consolidada das duas classes ProductViewSet originais.
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
