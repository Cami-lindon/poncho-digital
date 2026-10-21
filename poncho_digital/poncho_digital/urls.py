
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        TemplateView.as_view(template_name="base/home.html"),
        name="home",
    ),
    path(
        "artesanos/",
        include("apps.artesanos.urls"),
    ),
]
