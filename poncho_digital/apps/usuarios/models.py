from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    debe_cambiar_password = models.BooleanField(default=False)
