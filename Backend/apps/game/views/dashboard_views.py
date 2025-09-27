"""
Views para dashboard do jogo.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models

from ..models import GameSession, Product, RealtimeSale
from ..serializers import GameSessionSerializer, RealtimeSaleSerializer
from apps.finance.models import UserBalance


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
