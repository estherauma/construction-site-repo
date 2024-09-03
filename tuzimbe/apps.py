from django.apps import AppConfig


class TuzimbeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tuzimbe"

    def ready(self):
        import tuzimbe.signals
