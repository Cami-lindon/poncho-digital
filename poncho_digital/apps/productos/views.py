from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm


@login_required
@permission_required("productos.view_producto", raise_exception=True)
def listar_productos(request):
    productos = Producto.objects.filter(publicado_por=request.user).order_by("-fecha_publicacion")
    return render(request, "productos/lista.html", {"productos": productos})


@login_required
@permission_required("productos.view_producto", raise_exception=True)
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, publicado_por=request.user)
    return render(request, "productos/detalle.html", {"producto": producto})


@login_required
@permission_required("productos.add_producto", raise_exception=True)
def crear_producto(request):
    if request.method == "POST":
        formulario = ProductoForm(request.POST, request.FILES)
        if formulario.is_valid():
            nuevo_producto = formulario.save(commit=False)
            nuevo_producto.publicado_por = request.user
            nuevo_producto.save()
            return redirect("productos:lista_productos")
    else:
        formulario = ProductoForm()
    return render(request, "productos/producto_form.html", {"formulario": formulario})


@login_required
@permission_required("productos.change_producto", raise_exception=True)
def editar_producto(request, pk):

    producto = get_object_or_404(Producto, pk=pk, publicado_por=request.user)

    if producto.publicado_por != request.user:
        messages.error(request, "No podés modificar este producto.")
        return redirect("productos:lista_productos")

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


@login_required
@permission_required("productos.delete_producto", raise_exception=True)
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, publicado_por=request.user)

    if producto.publicado_por != request.user:
        messages.error(request, "No podés modificar este producto.")
        return redirect("productos:lista_productos")

    if request.method == "POST":
        producto.delete()
        return redirect("productos:lista_productos")
    return render(
        request,
        "productos/producto_confirmar_eliminacion.html",
        {"producto": producto},
    )