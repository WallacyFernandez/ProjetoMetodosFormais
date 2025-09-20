"""
URLs para o app de finanças.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserBalanceViewSet, CategoryViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'balance', UserBalanceViewSet, basename='balance')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'transactions', TransactionViewSet, basename='transactions')

app_name = 'finance'

urlpatterns = [
    path('', include(router.urls)),
]
