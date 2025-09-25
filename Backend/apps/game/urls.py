"""
URLs para o app de jogo.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GameSessionViewSet,
    ProductCategoryViewSet,
    GameDashboardViewSet,
    SupplierViewSet,
    ProductViewSet,
    ProductStockHistoryViewSet,
    ProductSalesViewSet
)

router = DefaultRouter()
router.register(r'sessions', GameSessionViewSet, basename='game-session')
router.register(r'categories', ProductCategoryViewSet, basename='product-category')
router.register(r'dashboard', GameDashboardViewSet, basename='game-dashboard')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'stock-history', ProductStockHistoryViewSet, basename='product-stock-history')
router.register(r'sales', ProductSalesViewSet, basename='product-sales')

urlpatterns = [
    path('', include(router.urls)),
]
