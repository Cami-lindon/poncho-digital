from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "categoria",
            "descripcion",
            "imagen_principal",
        ]
        error_messages = {
            "nombre": {
                "required": "El nombre del producto es obligatorio.",
            },
            "categoria": {
                "required": "Debés seleccionar una categoría.",
            },
            "descripcion": {
                "required": "La descripción es obligatoria.",
            },
            "imagen_principal": {
                "required": "Debés seleccionar una imagen.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            if isinstance(campo.widget, forms.Select):
                campo.widget.attrs["class"] = "form-select"
            elif isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs["class"] = "form-check-input"
            else:
                campo.widget.attrs["class"] = "form-control"

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()

        if not nombre:
            raise forms.ValidationError(
                "El nombre del producto es obligatorio."
            )

        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"].strip()

        if not descripcion:
            raise forms.ValidationError(
                "La descripción del producto es obligatoria."
            )

        if len(descripcion) < 10:
            raise forms.ValidationError(
                "La descripción debe tener al menos 10 caracteres."
            )

        return descripcion

    def clean_categoria(self):
        categoria = self.cleaned_data["categoria"]

        categorias_validas = dict(Producto.CATEGORIAS)

        if categoria not in categorias_validas:
            raise forms.ValidationError(
                "Seleccioná una categoría válida."
            )
        return categoria

    def clean_imagen_principal(self):
        imagen = self.cleaned_data.get("imagen_principal")

        if imagen:
            formatos_validos = ["jpg", "jpeg", "png", "webp"]

            extension = imagen.name.rsplit(".", 1)[-1].lower()

            if extension not in formatos_validos:
                raise forms.ValidationError(
                    "La imagen debe tener formato JPG, JPEG, PNG o WEBP."
                )

        return imagen