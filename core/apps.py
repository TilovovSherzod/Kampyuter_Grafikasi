from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = "Ta'lim materiallari"

    def ready(self):
        # import signal handlers
        try:
            import core.signals  # noqa: F401
        except Exception:
            pass
