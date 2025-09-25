"""
App de configuração para o jogo Supermercado Simulator.
"""

from django.apps import AppConfig


class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.game'
    verbose_name = 'Supermercado Simulator'
