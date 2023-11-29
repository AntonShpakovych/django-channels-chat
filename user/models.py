from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_online = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="user_images/")
