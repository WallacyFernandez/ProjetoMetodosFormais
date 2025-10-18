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
                    # Buscar data atual do jogo
                    from apps.game.models import GameSession
                    game_session = GameSession.objects.get(user=request.user)
                    
                    Transaction.objects.create(
                        user=request.user,
                        amount=total_value,
                        transaction_type='INCOME',
                        category=vendas_category,
                        description=f'Venda: {product.name} - {quantity} unidades',
                        transaction_date=game_session.current_game_date
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

    @action(detail=False, methods=['get'])
    def sales_charts_data(self, request):
        """Retorna dados para gráficos de vendas."""
        from django.db.models import Sum, Count
        from datetime import datetime, timedelta
        from calendar import monthrange
        
        # Parâmetros de período
        period = request.GET.get('period', 'monthly')  # daily, weekly, monthly
        days_back = int(request.GET.get('days_back', 30))
        
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        # Dados para gráfico de vendas por período
        sales_by_period = []
        
        if period == 'daily':
            # Vendas por dia
            for i in range(days_back):
                current_date = start_date + timedelta(days=i)
                daily_sales = ProductStockHistory.objects.filter(
                    operation='SALE',
                    game_date=current_date
                ).aggregate(
                    total_quantity=Sum('quantity'),
                    total_revenue=Sum('total_value')
                )
                
                sales_by_period.append({
                    'period': current_date.strftime('%d/%m'),
                    'period_key': current_date.strftime('%Y-%m-%d'),
                    'total_quantity': daily_sales['total_quantity'] or 0,
                    'total_revenue': float(daily_sales['total_revenue'] or 0),
                    'revenue_formatted': f"R$ {float(daily_sales['total_revenue'] or 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                })
        
        elif period == 'weekly':
            # Vendas por semana
            current_date = start_date
            week_count = 0
            while current_date <= end_date:
                week_end = min(current_date + timedelta(days=6), end_date)
                weekly_sales = ProductStockHistory.objects.filter(
                    operation='SALE',
                    game_date__range=[current_date, week_end]
                ).aggregate(
                    total_quantity=Sum('quantity'),
                    total_revenue=Sum('total_value')
                )
                
                sales_by_period.append({
                    'period': f"Semana {week_count + 1}",
                    'period_key': f"{current_date.strftime('%Y-%m-%d')}_{week_end.strftime('%Y-%m-%d')}",
                    'total_quantity': weekly_sales['total_quantity'] or 0,
                    'total_revenue': float(weekly_sales['total_revenue'] or 0),
                    'revenue_formatted': f"R$ {float(weekly_sales['total_revenue'] or 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                })
                
                current_date += timedelta(days=7)
                week_count += 1
        
        else:  # monthly
            # Vendas por mês
            current_date = start_date.replace(day=1)
            while current_date <= end_date:
                # Último dia do mês
                last_day = monthrange(current_date.year, current_date.month)[1]
                month_end = current_date.replace(day=last_day)
                
                monthly_sales = ProductStockHistory.objects.filter(
                    operation='SALE',
                    game_date__year=current_date.year,
                    game_date__month=current_date.month
                ).aggregate(
                    total_quantity=Sum('quantity'),
                    total_revenue=Sum('total_value')
                )
                
                month_names = {
                    1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                    7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
                }
                
                sales_by_period.append({
                    'period': f"{month_names[current_date.month]} {current_date.year}",
                    'period_key': f"{current_date.year}-{current_date.month:02d}",
                    'total_quantity': monthly_sales['total_quantity'] or 0,
                    'total_revenue': float(monthly_sales['total_revenue'] or 0),
                    'revenue_formatted': f"R$ {float(monthly_sales['total_revenue'] or 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                })
                
                # Próximo mês
                if current_date.month == 12:
                    current_date = current_date.replace(year=current_date.year + 1, month=1)
                else:
                    current_date = current_date.replace(month=current_date.month + 1)
        
        # Produtos mais vendidos (top 10)
        top_products = ProductStockHistory.objects.filter(
            operation='SALE',
            game_date__range=[start_date, end_date]
        ).values(
            'product__id', 'product__name', 'product__category__name', 'product__category__color'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('total_value')
        ).order_by('-total_revenue')[:10]
        
        # Vendas por categoria
        sales_by_category = ProductStockHistory.objects.filter(
            operation='SALE',
            game_date__range=[start_date, end_date]
        ).values('product__category__name', 'product__category__color').annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('total_value')
        ).order_by('-total_revenue')
        
        return Response({
            'sales_by_period': sales_by_period,
            'top_products': list(top_products),
            'sales_by_category': list(sales_by_category),
            'period': period,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        })

    @action(detail=False, methods=['get'])
    def detailed_analysis(self, request):
        """Retorna análise detalhada de vendas."""
        from django.db.models import Sum, Count, Avg
        from datetime import timedelta
        
        # Parâmetros
        days_back = int(request.GET.get('days_back', 30))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        # Estatísticas gerais
        total_sales = ProductStockHistory.objects.filter(
            operation='SALE',
            game_date__range=[start_date, end_date]
        ).aggregate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('total_value'),
            avg_unit_price=Avg('unit_price'),
            total_transactions=Count('id')
        )
        
        # Produto com maior receita
        best_selling_product = ProductStockHistory.objects.filter(
            operation='SALE',
            game_date__range=[start_date, end_date]
        ).values('product__name').annotate(
            total_revenue=Sum('total_value')
        ).order_by('-total_revenue').first()
        
        # Produto mais vendido em quantidade
        most_sold_product = ProductStockHistory.objects.filter(
            operation='SALE',
            game_date__range=[start_date, end_date]
        ).values('product__name').annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity').first()
        
        # Vendas por dia da semana
        sales_by_weekday = []
        weekdays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        
        for i in range(7):
            weekday_sales = ProductStockHistory.objects.filter(
                operation='SALE',
                game_date__range=[start_date, end_date],
                game_date__week_day=i+2  # Django usa 2=Monday, 3=Tuesday, etc.
            ).aggregate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum('total_value')
            )
            
            sales_by_weekday.append({
                'weekday': weekdays[i],
                'total_quantity': weekday_sales['total_quantity'] or 0,
                'total_revenue': float(weekday_sales['total_revenue'] or 0)
            })
        
        # Crescimento de vendas (comparação com período anterior)
        previous_start = start_date - timedelta(days=days_back)
        previous_period_sales = ProductStockHistory.objects.filter(
            operation='SALE',
            game_date__range=[previous_start, start_date - timedelta(days=1)]
        ).aggregate(total_revenue=Sum('total_value'))
        
        current_revenue = float(total_sales['total_revenue'] or 0)
        previous_revenue = float(previous_period_sales['total_revenue'] or 0)
        
        growth_percentage = 0
        if previous_revenue > 0:
            growth_percentage = ((current_revenue - previous_revenue) / previous_revenue) * 100
        
        return Response({
            'general_stats': {
                'total_quantity': total_sales['total_quantity'] or 0,
                'total_revenue': current_revenue,
                'total_revenue_formatted': f"R$ {current_revenue:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                'avg_unit_price': float(total_sales['avg_unit_price'] or 0),
                'avg_unit_price_formatted': f"R$ {float(total_sales['avg_unit_price'] or 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                'total_transactions': total_sales['total_transactions'] or 0
            },
            'best_selling_product': best_selling_product,
            'most_sold_product': most_sold_product,
            'sales_by_weekday': sales_by_weekday,
            'growth_analysis': {
                'current_revenue': current_revenue,
                'previous_revenue': previous_revenue,
                'growth_percentage': growth_percentage,
                'growth_formatted': f"{growth_percentage:+.1f}%"
            },
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days_back': days_back
            }
        })


