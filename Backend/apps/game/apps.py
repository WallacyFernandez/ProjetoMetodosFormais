"""
Apps de configuração para o jogo Supermercado Simulator.
"""

from django.apps import AppConfig


class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.game'
    verbose_name = 'Supermercado Simulator'
    
    def ready(self):
        """Executa quando o app está pronto."""
        # Importa os sinais aqui para evitar problemas de importação circular
        try:
            import apps.game.signals
        except ImportError:
            pass
