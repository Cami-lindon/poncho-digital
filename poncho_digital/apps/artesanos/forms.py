
from django import forms
from django.utils import timezone
from .models import Artesano, Solicitud


class ArtesanoForm(forms.ModelForm):
    class Meta:
        model = Artesano
        fields = ["nombre", "apellido", "dni", "fecha_nacimiento"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingresá tu nombre",
            }),
            "apellido": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingresá tu apellido",
            }),
            "dni": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej.: 30123456",
            }),

            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get("fecha_nacimiento")

        if fecha and fecha > timezone.localdate():
            raise forms.ValidationError(
                "La fecha de nacimiento no puede ser futura."
            )

        if fecha:
            hoy = timezone.localdate()
            edad = hoy.year - fecha.year

            if (hoy.month, hoy.day) < (fecha.month, fecha.day):
                edad -= 1

            if edad < 18:
                raise forms.ValidationError(
                    "Debés tener al menos 18 años para solicitar un stand."
                )

        return fecha



class SolicitudForm(forms.ModelForm):
    rubro = forms.ChoiceField(
        choices=[
            ("", "Seleccione un rubro"),
            ("artesania", "Artesanía"),
            ("textil", "Textil"),
            ("gastronomia", "Gastronomía"),
            ("bebidas", "Bebidas"),
            ("regionales", "Productos regionales"),
            ("decoracion", "Decoración"),
            ("joyeria", "Joyería"),
            ("otro", "Otro"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Solicitud
        fields = [
            "email", "telefono", "provincia", "localidad",
            "emprendimiento", "rubro", "descripcion", "productos",
            "variedad", "observaciones",
        ]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Ej.: nombre@correo.com",
            }),
            "telefono": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej.: 383 4123456",
            }),
            "provincia": forms.Select(attrs={
                "class": "form-select",
            }),
            "localidad": forms.Select(attrs={
                "class": "form-select",
            }),
            "emprendimiento": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre de tu emprendimiento",
            }),
            "descripcion": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-control",
                "placeholder": "Contanos brevemente sobre tu emprendimiento...",
            }),
            "productos": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-control",
                "placeholder": "Indicá los principales productos que comercializás...",
            }),
            "variedad": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej.: tejidos, cerámicas, dulces regionales...",
            }),
            "observaciones": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-control",
                "placeholder": "¿Hay algo más que quieras contarnos?",
            }),
        }
