from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        #constante = valor que se almacena en la base de datos, etiqueta legible
        ADMINISTRADOR = "administrador", "Administrador"
        ARTESANO = "artesano", "Artesano"
        VISITANTE = "visitante", "Visitante"

    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.VISITANTE)
