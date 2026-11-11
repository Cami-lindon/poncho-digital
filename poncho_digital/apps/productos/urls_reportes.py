from django.urls import path
from . import views

app_name = "reportes"

urlpatterns = [
    path("", views.lista_reportes, name="lista_reportes"),
    path("artesanos/pdf/",views.reporte_artesanos_pdf,name="reporte_artesanos_pdf",),
    path("artesanos/excel/",views.reporte_artesanos_excel,name="reporte_artesanos_excel",),
    path("localidad/pdf/", views.reporte_artesanos_localidad_pdf,name="reporte_artesanos_localidad_pdf",),
    path("localidad/excel/",views.reporte_artesanos_localidad_excel,name="reporte_artesanos_localidad_excel"),
    path("rubro/pdf/", views.reporte_artesanos_rubro_pdf, name="reporte_artesanos_rubro_pdf"),
    path("rubro/excel/",views.reporte_artesanos_rubro_excel,name="reporte_artesanos_rubro_excel"),
    path("productos-artesano/pdf/",views.reporte_productos_por_artesano_pdf,name="reporte_productos_por_artesano_pdf"),
    path("productos-artesano/excel/",views.reporte_productos_por_artesano_excel,name="reporte_productos_por_artesano_excel"),
]