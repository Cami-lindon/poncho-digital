
from django.urls import path
from . import views

app_name = "artesanos"

urlpatterns = [
    path(
        "registro/",
        views.registro_artesano,
        name="registro_artesano",
    ),
]
