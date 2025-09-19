"""
Serializers base para o projeto.
"""

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Serializer base para modelos que herdam de BaseModel.
    """
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        abstract = True
        fields = ['id', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TimestampSerializer(serializers.Serializer):
    """
    Serializer para campos de timestamp.
    """
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')


class PaginationSerializer(serializers.Serializer):
    """
    Serializer para informações de paginação.
    """
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = serializers.ListField()


class ResponseSerializer(serializers.Serializer):
    """
    Serializer para respostas padronizadas da API.
    """
    success = serializers.BooleanField(default=True)
    message = serializers.CharField(max_length=255, required=False)
    data = serializers.JSONField(required=False)
    errors = serializers.DictField(required=False)


class ErrorResponseSerializer(serializers.Serializer):
    """
    Serializer para respostas de erro padronizadas.
    """
    success = serializers.BooleanField(default=False)
    message = serializers.CharField(max_length=255)
    errors = serializers.DictField(required=False)
    error_code = serializers.CharField(max_length=50, required=False)
