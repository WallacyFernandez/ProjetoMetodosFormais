"""
Signals do app core.
"""

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)


# Exemplo de signal para log de criação de objetos
# @receiver(post_save)
# def log_object_creation(sender, instance, created, **kwargs):
#     """
#     Log quando um objeto é criado.
#     """
#     if created:
#         logger.info(f"Novo {sender.__name__} criado: {instance.pk}")


# Exemplo de signal para log de exclusão de objetos
# @receiver(pre_delete)
# def log_object_deletion(sender, instance, **kwargs):
#     """
#     Log quando um objeto é excluído.
#     """
#     logger.info(f"{sender.__name__} excluído: {instance.pk}")
