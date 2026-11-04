from django.contrib import admin
from .models import Artesano, Solicitud


@admin.register(Artesano)
class ArtesanoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "dni", "usuario")


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ("artesano", "emprendimiento", "rubro", "estado", "pabellon")
    list_filter = ("estado", "provincia", "rubro")
    search_fields = ("artesano__nombre", "artesano__apellido", "emprendimiento", "email")
