from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('apps.usuarios.urls', namespace='usuario')),
    path("", TemplateView.as_view(template_name="base/home.html"), name="home"),
    path("artesanos/", include("apps.artesanos.urls"),),
    path("productos/", include("apps.productos.urls", namespace='productos')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
