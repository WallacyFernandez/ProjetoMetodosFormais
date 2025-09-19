"""
Views base para o projeto.
"""

from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet base com funcionalidades comuns para todos os modelos.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = []
    filterset_fields = []
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Retorna queryset filtrado por objetos ativos por padrão.
        """
        if hasattr(self.get_serializer().Meta.model, 'objects'):
            if hasattr(self.get_serializer().Meta.model.objects, 'active'):
                return self.get_serializer().Meta.model.objects.active()
        return super().get_queryset()

    def perform_destroy(self, instance):
        """
        Executa soft delete em vez de delete real.
        """
        if hasattr(instance, 'soft_delete'):
            instance.soft_delete()
        else:
            instance.delete()

    @action(detail=True, methods=['post'], url_path='restore')
    def restore(self, request, pk=None):
        """
        Restaura um objeto que foi soft deleted.
        """
        instance = self.get_object()
        if hasattr(instance, 'restore'):
            instance.restore()
            return Response(
                {'message': 'Objeto restaurado com sucesso.'}, 
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'Este objeto não suporta restauração.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    def create_response(self, data=None, message='', success=True, status_code=status.HTTP_200_OK):
        """
        Cria uma resposta padronizada.
        """
        response_data = {
            'success': success,
            'message': message,
        }
        if data is not None:
            response_data['data'] = data
        return Response(response_data, status=status_code)

    def error_response(self, message='Erro interno', errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Cria uma resposta de erro padronizada.
        """
        response_data = {
            'success': False,
            'message': message,
        }
        if errors:
            response_data['errors'] = errors
        return Response(response_data, status=status_code)


class ReadOnlyModelViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    ViewSet para operações apenas de leitura e criação.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-created_at']


class CachedModelViewSet(BaseModelViewSet):
    """
    ViewSet com cache automático para operações de listagem.
    """
    cache_timeout = 300  # 5 minutos

    @method_decorator(cache_page(cache_timeout))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Limpa o cache após criação.
        """
        super().perform_create(serializer)
        self.clear_cache()

    def perform_update(self, serializer):
        """
        Limpa o cache após atualização.
        """
        super().perform_update(serializer)
        self.clear_cache()

    def perform_destroy(self, instance):
        """
        Limpa o cache após exclusão.
        """
        super().perform_destroy(instance)
        self.clear_cache()

    def clear_cache(self):
        """
        Limpa o cache relacionado a este viewset.
        """
        cache_key = f"{self.__class__.__name__}_list"
        cache.delete(cache_key)