
from django.db import models
from django.conf import settings


class Artesano(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artesano",
        null=True,
        blank=True
    )

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.nombre} {self.apellido} - DNI {self.dni}"


class Solicitud(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("aprobada", "Aprobada"),
        ("rechazada", "Rechazada"),
        ("modificaciones", "Requiere modificaciones"),
    ]

    artesano = models.ForeignKey(
        Artesano,
        on_delete=models.CASCADE,
        related_name="solicitudes"
    )

    email = models.EmailField()
    telefono = models.CharField(max_length=30)

    provincia = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)

    emprendimiento = models.CharField(max_length=150)
    rubro = models.CharField(max_length=100)
    descripcion = models.TextField()
    productos = models.TextField()

    variedad = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente"
    )

    pabellon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.emprendimiento} - {self.get_estado_display()}"

