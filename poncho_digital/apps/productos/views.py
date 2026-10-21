from django.shortcuts import render, redirect, get_object_or_404

from apps.usuarios.models import Usuario
from .models import Producto
from .forms import ProductoForm


def listar_productos(request):
    usuario, _ = Usuario.objects.get_or_create(username="demo")
    productos = Producto.objects.filter(publicado_por=usuario).order_by("-fecha_publicacion")
    return render(request, "productos/lista.html", {"productos": productos})


def detalle_producto(request, pk):
    usuario, _ = Usuario.objects.get_or_create(username="demo")
    producto = get_object_or_404(Producto, pk=pk, publicado_por=usuario)
    return render(request, "productos/detalle.html", {"producto": producto})


def crear_producto(request):
    if request.method == "POST":
        formulario = ProductoForm(request.POST, request.FILES)
        if formulario.is_valid():
            nuevo_producto = formulario.save(commit=False)
            usuario, _ = Usuario.objects.get_or_create(username="demo")
            nuevo_producto.publicado_por = usuario
            nuevo_producto.save()
            return redirect("productos:lista_productos")
    else:
        formulario = ProductoForm()
    return render(request, "productos/producto_form.html", {"formulario": formulario})


def editar_producto(request, pk):
    usuario, _ = Usuario.objects.get_or_create(username="demo")
    producto = get_object_or_404(Producto, pk=pk, publicado_por=usuario)
    if request.method == "POST":
        formulario = ProductoForm(request.POST, request.FILES, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return redirect("productos:detalle_producto", pk=producto.pk)
    else:
        formulario = ProductoForm(instance=producto)
    return render(
        request,
        "productos/producto_form.html",
        {"formulario": formulario, "producto": producto},
    )


def eliminar_producto(request, pk):
    usuario, _ = Usuario.objects.get_or_create(username="demo")
    producto = get_object_or_404(Producto, pk=pk, publicado_por=usuario)
    if request.method == "POST":
        producto.delete()
        return redirect("productos:lista_productos")
    return render(
        request,
        "productos/producto_confirmar_eliminacion.html",
        {"producto": producto},
    )
