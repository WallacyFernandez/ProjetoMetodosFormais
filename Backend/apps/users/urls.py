"""
URLs para o app de usuários.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet

# Router para ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', ProfileViewSet, basename='profile')

app_name = 'users'

urlpatterns = [
    # Incluir rotas do router
    path('', include(router.urls)),
]
