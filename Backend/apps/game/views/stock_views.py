"""
Views para gerenciamento de histórico de estoque.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import ProductStockHistory
from ..serializers import ProductStockHistorySerializer


class ProductStockHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar histórico de estoque.
    """
    serializer_class = ProductStockHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductStockHistory.objects.select_related('product').order_by('-created_at')
