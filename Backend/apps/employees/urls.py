"""
URLs do app de funcionários.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeePositionViewSet, EmployeeViewSet, PayrollViewSet, PayrollHistoryViewSet
)
from .game_views import EmployeeGameIntegrationViewSet

app_name = 'employees'

router = DefaultRouter()
router.register(r'positions', EmployeePositionViewSet, basename='employee-position')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'payrolls', PayrollViewSet, basename='payroll')
router.register(r'payroll-history', PayrollHistoryViewSet, basename='payroll-history')
router.register(r'game', EmployeeGameIntegrationViewSet, basename='employee-game')

urlpatterns = [
    path('', include(router.urls)),
]
