from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Core'
    
    def ready(self):
        """
        Importa os signals quando a aplicação estiver pronta.
        """
        try:
            import apps.core.signals  # noqa F401
        except ImportError:
            pass
