from django.apps import AppConfig
from django.core.signals import setting_changed


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    def ready(self):
        from user.signals import got_online, got_offline

        setting_changed.connect(got_online, got_offline)
