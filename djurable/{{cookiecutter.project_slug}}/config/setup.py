from django.apps import AppConfig
from django.conf import settings

class SetupConfig(AppConfig):
    name = 'config'
    verbose_name = "App settup"

    def ready(self):
        if settings.configured:
            from .widgets import auto_register_widget_tags
            auto_register_widget_tags()
