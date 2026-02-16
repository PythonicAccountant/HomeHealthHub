from django.apps import AppConfig


class TrackerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home_health_hub.tracker"

    def ready(self):
        import tracker.signal  # noqa
