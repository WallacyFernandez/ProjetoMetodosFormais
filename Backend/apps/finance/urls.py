"""
URLs para o app de finanças.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserBalanceViewSet

router = DefaultRouter()
router.register(r'balance', UserBalanceViewSet, basename='balance')

app_name = 'finance'

urlpatterns = [
    path('', include(router.urls)),
]
