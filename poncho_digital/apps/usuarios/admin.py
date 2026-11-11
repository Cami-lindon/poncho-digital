from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.usuarios.forms import UsuarioForm
from apps.usuarios.models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioForm
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2'), }),
    )
    search_fields = ('email', 'username',)
