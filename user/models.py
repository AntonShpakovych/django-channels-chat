import datetime

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    photo = models.ImageField(upload_to="user_images/")

    @property
    def last_seen(self):
        return cache.get(f"seen_{self.username}")

    @property
    def is_online(self):
        last_seen = self.last_seen
        if last_seen:
            now = datetime.datetime.now()

            if now > last_seen + datetime.timedelta(
                    seconds=settings.USER_ONLINE_TIMEOUT
            ):
                return False
            return True
        return False
