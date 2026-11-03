from django.db import models

class Producto(models.Model):

    nombre = models.CharField(max_length=150)
    CATEGORIAS = [
        ("indumentaria", "Indumentaria y Calzado"),
        ("accesorios", "Accesorios y Joyería"),
        ("hogar", "Hogar, Cocina y Decoración"),
        ("mates", "Mates y Marroquinería"),
        ("arte", "Arte y Colección"),
    ]
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    descripcion = models.TextField()
    imagen_principal = models.FileField(upload_to="productos/")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    publicado_por = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='productos_publicados')

    def __str__(self):
        return self.nombre