"""
Modelos base para o projeto.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class TimeStampedModel(models.Model):
    """
    Modelo abstrato que adiciona campos de timestamp.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """
    Modelo abstrato que usa UUID como chave primária.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel, UUIDModel):
    """
    Modelo base que combina timestamp e UUID.
    """
    is_active = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        abstract = True

    def soft_delete(self):
        """Executa um soft delete marcando is_active como False"""
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])

    def restore(self):
        """Restaura um registro soft deleted"""
        self.is_active = True
        self.save(update_fields=['is_active', 'updated_at'])


class ActiveManager(models.Manager):
    """
    Manager que retorna apenas objetos ativos.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class AllObjectsManager(models.Manager):
    """
    Manager que retorna todos os objetos, incluindo inativos.
    """
    pass