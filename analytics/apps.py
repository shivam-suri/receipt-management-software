from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analytics'
    def ready(self):
        # Ensures receivers are connected in every process
        from . import signals
