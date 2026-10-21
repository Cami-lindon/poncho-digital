from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):

    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    peso_kg = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    imagen_principal = models.FileField(upload_to="productos/")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    publicado_por = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='productos_publicados')

    def __str__(self):
        return self.nombre