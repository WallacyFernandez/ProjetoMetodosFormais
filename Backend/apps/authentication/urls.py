"""
URLs do app de autenticação.
"""

from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('refresh/', views.refresh_token, name='refresh_token'),
    path('change-password/', views.change_password, name='change_password'),
    path('me/', views.me, name='me'),
]
