"""
Views para gerenciamento de vendas.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone
from datetime import date

from ..models import Product, ProductStockHistory
from ..serializers import ProductStockOperationSerializer, ProductSerializer, ProductStockHistorySerializer
from apps.finance.models import UserBalance, Transaction, Category


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

