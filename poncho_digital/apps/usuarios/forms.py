from django.contrib.auth.forms import UserCreationForm

from apps.usuarios.models import Usuario


class UsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields
