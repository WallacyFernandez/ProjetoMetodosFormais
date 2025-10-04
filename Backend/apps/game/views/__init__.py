"""
Views para o app de jogo organizadas em módulos.
"""

from .session_views import GameSessionViewSet
from .product_views import ProductViewSet, ProductCategoryViewSet, SupplierViewSet
from .stock_views import ProductStockHistoryViewSet
from .sales_views import ProductSalesViewSet
from .dashboard_views import GameDashboardViewSet

__all__ = [
    'GameSessionViewSet',
    'ProductViewSet', 
    'ProductCategoryViewSet',
    'SupplierViewSet',
    'ProductStockHistoryViewSet',
    'ProductSalesViewSet',
    'GameDashboardViewSet'
]

