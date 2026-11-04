from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm
from ..artesanos.models import Artesano
from apps.artesanos.models import Solicitud
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Prefetch

#para reportes

from io import BytesIO
from xml.sax.saxutils import escape

from django.db.models import Count
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from reportlab.lib import colors,units
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

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

    producto = get_object_or_404(Producto, pk=pk)

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
    producto = get_object_or_404(Producto, pk=pk)

    if producto.publicado_por != request.user:
        messages.error(request, "No podés eliminar este producto.")
        return redirect("productos:lista_productos")

    if request.method == "POST":
        producto.delete()
        return redirect("productos:lista_productos")
    return render(
        request,
        "productos/producto_confirmar_eliminacion.html",
        {"producto": producto},
    )


def catalogo_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/catalogo_productos.html', {'productos': productos})


def detalle_artesano(request, usuario_id):
    artesano = get_object_or_404(Artesano, usuario_id=usuario_id,)

    solicitud = (artesano.solicitudes.filter(estado="aprobada").order_by("-pk").first())
    if solicitud is None:
        raise Http404

    return render(request, "productos/detalle_artesano.html", {"artesano": artesano, "solicitud": solicitud, },)


#reportes
@staff_member_required
def lista_reportes(request):
    return render(request, "productos/lista_reportes.html")

#<--------------------reporte artesanos registrados -------------------------->
@staff_member_required
def reporte_artesanos_pdf(request):
    solicitudes = (
        Solicitud.objects
        .filter(estado="aprobada")
        .select_related("artesano")
        .order_by("artesano__apellido", "artesano__nombre")
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="artesanos_registrados.pdf"'
    )

    documento = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=20,
        leftMargin=20,
        topMargin=30,
        bottomMargin=30,
    )

    estilos = getSampleStyleSheet()
    elementos = [
        Paragraph("Reporte de artesanos registrados", estilos["Title"])
    ]

    datos = [[
        "Apellido",
        "Nombre",
        "DNI",
        "Fecha de nacimiento",
        "Teléfono",
        "Emprendimiento",
        "Provincia",
        "Localidad",
    ]]

    for solicitud in solicitudes:
        artesano = solicitud.artesano
        datos.append([
            artesano.apellido,
            artesano.nombre,
            artesano.dni,
            artesano.fecha_nacimiento.strftime("%d/%m/%Y"),
            solicitud.telefono,
            solicitud.emprendimiento,
            solicitud.provincia,
            solicitud.localidad,
        ])

    tabla = Table(
        datos,
        repeatRows=1,
        colWidths=[
            75, 75, 65, 85, 80, 130, 90, 90
        ],
    )

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#29324f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b1bddd")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor("#f1f1f1"),
        ]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elementos.append(tabla)
    documento.build(elementos)

    return response

@staff_member_required
def reporte_artesanos_excel(request):
    solicitudes = (
        Solicitud.objects
        .filter(estado="aprobada")
        .select_related("artesano")
        .order_by("artesano__apellido", "artesano__nombre")
    )

    libro = Workbook()
    hoja = libro.active
    hoja.title = "Artesanos registrados"

    encabezados = [
        "Apellido",
        "Nombre",
        "DNI",
        "Fecha de nacimiento",
        "Teléfono",
        "Emprendimiento",
        "Provincia",
        "Localidad",
    ]

    hoja.append(encabezados)

    for solicitud in solicitudes:
        artesano = solicitud.artesano

        hoja.append([
            artesano.apellido,
            artesano.nombre,
            artesano.dni,
            artesano.fecha_nacimiento,
            solicitud.telefono,
            solicitud.emprendimiento,
            solicitud.provincia,
            solicitud.localidad,
        ])

    # Estilo de encabezados
    for celda in hoja[1]:
        celda.font = Font(bold=True, color="FFFFFF")
        celda.fill = PatternFill(
            fill_type="solid",
            fgColor="29324F"
        )
        celda.alignment = Alignment(horizontal="center")

    # Formato de fecha
    for fila in hoja.iter_rows(min_row=2):
        fila[3].number_format = "DD/MM/YYYY"

    # Ajustar el ancho de las columnas
    for columna in hoja.columns:
        max_largo = max(
            len(str(celda.value or ""))
            for celda in columna
        )
        letra = get_column_letter(columna[0].column)
        hoja.column_dimensions[letra].width = max_largo + 3

    hoja.freeze_panes = "A2"
    hoja.auto_filter.ref = hoja.dimensions

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )
    response["Content-Disposition"] = (
        'attachment; filename="artesanos_registrados.xlsx"'
    )

    libro.save(response)
    return response


#<---------------------------------------------------->

#<-----------reporte de artesanos registrados por localidad------------>
@staff_member_required
def reporte_artesanos_localidad_pdf(request):
    reporte = (
        Solicitud.objects
        .filter(estado="aprobada")
        .values("provincia", "localidad")
        .annotate(cantidad=Count("artesano", distinct=True))
        .order_by("-cantidad", "provincia", "localidad")
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="artesanos_por_localidad.pdf"'
    )

    documento = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    estilos = getSampleStyleSheet()
    elementos = [
        Paragraph(
            "Cantidad de artesanos registrados por localidad",
            estilos["Title"]
        )
    ]

    datos = [[
        "Provincia",
        "Localidad",
        "Cantidad de artesanos"
    ]]

    for registro in reporte:
        datos.append([
            registro["provincia"],
            registro["localidad"],
            registro["cantidad"],
        ])

    tabla = Table(
        datos,
        colWidths=[130, 170, 180],
        repeatRows=1
    )

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#29324f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b1bddd")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor("#f1f1f1"),
        ]),
        ("ALIGN", (2, 1), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    elementos.append(tabla)
    documento.build(elementos)

    return response


@staff_member_required
def reporte_artesanos_localidad_excel(request):

    # Obtener artesanos de solicitudes aprobadas,
    # agrupados por provincia y localidad.
    reporte = (
        Solicitud.objects
        .filter(estado="aprobada")
        .values("provincia", "localidad")
        .annotate(cantidad=Count("artesano", distinct=True))
        .order_by("-cantidad", "provincia", "localidad")
    )

    # Crear el libro de Excel.
    libro = Workbook()
    hoja = libro.active
    hoja.title = "Artesanos por localidad"

    # Encabezados.
    encabezados = [
        "Provincia",
        "Localidad",
        "Cantidad de artesanos"
    ]

    hoja.append(encabezados)

    # Aplicar formato a los encabezados.
    for celda in hoja[1]:
        celda.font = Font(bold=True, color="FFFFFF")
        celda.fill = PatternFill(
            fill_type="solid",
            fgColor="29324F"
        )
        celda.alignment = Alignment(horizontal="center")

    # Cargar los datos.
    for registro in reporte:
        hoja.append([
            registro["provincia"],
            registro["localidad"],
            registro["cantidad"]
        ])

    # Ajustar automáticamente el ancho de las columnas.
    for columna in hoja.columns:
        maximo = 0
        letra = get_column_letter(columna[0].column)

        for celda in columna:
            if celda.value is not None:
                maximo = max(maximo, len(str(celda.value)))

        hoja.column_dimensions[letra].width = maximo + 4

    # Alinear las cantidades al centro.
    for fila in range(2, hoja.max_row + 1):
        hoja.cell(row=fila, column=3).alignment = Alignment(
            horizontal="center"
        )

    # Congelar encabezados y activar filtros.
    hoja.freeze_panes = "A2"
    hoja.auto_filter.ref = hoja.dimensions

    # Preparar la respuesta para descargar el Excel.
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="artesanos_por_localidad.xlsx"'
    )

    libro.save(response)

    return response

#<---------------------------------------->

#<--------------Reporte de artesanos registrados por rubro -------------------------->

@staff_member_required
def reporte_artesanos_rubro_pdf(request):

    reporte = (
        Solicitud.objects
        .filter(estado="aprobada")
        .values("rubro")
        .annotate(cantidad=Count("artesano", distinct=True))
        .order_by("-cantidad", "rubro")
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="artesanos_por_rubro.pdf"'
    )

    documento = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=40,
        bottomMargin=40,
    )

    estilos = getSampleStyleSheet()

    elementos = [
        Paragraph(
            "Cantidad de artesanos registrados por rubro",
            estilos["Title"]
        )
    ]

    datos = [
        ["Rubro", "Cantidad de artesanos"]
    ]

    for registro in reporte:
        datos.append([
            registro["rubro"],
            registro["cantidad"]
        ])

    tabla = Table(
        datos,
        colWidths=[230, 200],
        repeatRows=1
    )

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#29324f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b1bddd")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor("#f1f1f1"),
        ]),
        ("ALIGN", (1, 1), (1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    elementos.append(tabla)

    documento.build(elementos)

    return response

@staff_member_required
def reporte_artesanos_rubro_excel(request):

    reporte = (
        Solicitud.objects
        .filter(estado="aprobada")
        .values("rubro")
        .annotate(cantidad=Count("artesano", distinct=True))
        .order_by("-cantidad", "rubro")
    )

    libro = Workbook()
    hoja = libro.active
    hoja.title = "Artesanos por rubro"

    encabezados = [
        "Rubro",
        "Cantidad de artesanos"
    ]

    hoja.append(encabezados)

    # Formato de encabezados.
    for celda in hoja[1]:
        celda.font = Font(bold=True, color="FFFFFF")
        celda.fill = PatternFill(
            fill_type="solid",
            fgColor="29324F"
        )
        celda.alignment = Alignment(horizontal="center")

    # Cargar los datos.
    for registro in reporte:
        hoja.append([
            registro["rubro"],
            registro["cantidad"]
        ])

    # Ajustar ancho de columnas.
    for columna in hoja.columns:
        maximo = 0
        letra = get_column_letter(columna[0].column)

        for celda in columna:
            if celda.value is not None:
                maximo = max(maximo, len(str(celda.value)))

        hoja.column_dimensions[letra].width = maximo + 4

    # Centrar las cantidades.
    for fila in range(2, hoja.max_row + 1):
        hoja.cell(row=fila, column=2).alignment = Alignment(
            horizontal="center"
        )

    hoja.freeze_panes = "A2"
    hoja.auto_filter.ref = hoja.dimensions

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="artesanos_por_rubro.xlsx"'
    )

    libro.save(response)

    return response

#<-------------------------------------------------------------->

#<--------------Reporte de productos publicados por artesano --------------->
def obtener_productos_agrupados_por_artesano():

    solicitudes_aprobadas = Solicitud.objects.filter(
        estado="aprobada"
    ).order_by("id")

    productos = (
        Producto.objects
        .filter(
            publicado_por__artesano__isnull=False,
            publicado_por__artesano__solicitudes__estado="aprobada"
        )
        .select_related(
            "publicado_por",
            "publicado_por__artesano"
        )
        .prefetch_related(
            Prefetch(
                "publicado_por__artesano__solicitudes",
                queryset=solicitudes_aprobadas,
                to_attr="solicitudes_aprobadas"
            )
        )
        .distinct()
        .order_by(
            "publicado_por__artesano__apellido",
            "publicado_por__artesano__nombre",
            "nombre"
        )
    )

    grupos = {}

    for producto in productos:
        artesano = producto.publicado_por.artesano

        if artesano.id not in grupos:
            solicitudes = artesano.solicitudes_aprobadas

            emprendimiento = (
                solicitudes[0].emprendimiento
                if solicitudes
                else "Sin emprendimiento registrado"
            )

            grupos[artesano.id] = {
                "artesano": artesano,
                "emprendimiento": emprendimiento,
                "productos": []
            }

        grupos[artesano.id]["productos"].append(producto)

    return grupos.values()

@staff_member_required
def reporte_productos_por_artesano_pdf(request):

    grupos = obtener_productos_agrupados_por_artesano()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="productos_por_artesano.pdf"'
    )

    documento = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    estilos = getSampleStyleSheet()

    elementos = [
        Paragraph(
            "Productos publicados por artesano",
            estilos["Title"]
        ),
        Spacer(1, 20)
    ]

    if not grupos:
        elementos.append(
            Paragraph(
                "No hay productos publicados por artesanos aprobados.",
                estilos["Normal"]
            )
        )

    for grupo in grupos:

        artesano = grupo["artesano"]
        emprendimiento = grupo["emprendimiento"]

        elementos.append(
            Paragraph(
                f"<b>Artesano:</b> {escape(artesano.apellido)}, "
                f"{escape(artesano.nombre)}",
                estilos["Heading2"]
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Emprendimiento:</b> {escape(emprendimiento)}",
                estilos["Normal"]
            )
        )

        elementos.append(Spacer(1, 8))

        datos = [[
            "Producto",
            "Categoría",
            "Fecha de publicación"
        ]]

        for producto in grupo["productos"]:
            datos.append([
                producto.nombre,
                producto.get_categoria_display(),
                producto.fecha_publicacion.strftime("%d/%m/%Y")
            ])

        tabla = Table(
            datos,
            colWidths=[330, 250, 140],
            repeatRows=1
        )

        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#29324f")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b1bddd")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                colors.white,
                colors.HexColor("#f1f1f1"),
            ]),
            ("ALIGN", (2, 1), (2, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("PADDING", (0, 0), (-1, -1), 8),
        ]))

        elementos.append(tabla)
        elementos.append(Spacer(1, 20))

    documento.build(elementos)

    return response


@staff_member_required
def reporte_productos_por_artesano_excel(request):

    grupos = obtener_productos_agrupados_por_artesano()

    libro = Workbook()
    hoja = libro.active
    hoja.title = "Productos por artesano"

    for grupo in grupos:

        artesano = grupo["artesano"]
        emprendimiento = grupo["emprendimiento"]

        # Encabezado del artesano.
        fila_artesano = hoja.max_row + 1

        hoja.append([
            f"Artesano: {artesano.apellido}, {artesano.nombre}"
        ])

        hoja.merge_cells(
            start_row=fila_artesano,
            start_column=1,
            end_row=fila_artesano,
            end_column=3
        )

        celda = hoja.cell(row=fila_artesano, column=1)
        celda.font = Font(bold=True, color="FFFFFF", size=12)
        celda.fill = PatternFill(
            fill_type="solid",
            fgColor="29324F"
        )

        # Nombre del emprendimiento.
        hoja.append([
            "Emprendimiento:",
            emprendimiento
        ])

        hoja.cell(
            row=hoja.max_row,
            column=1
        ).font = Font(bold=True)

        # Encabezados de los productos.
        hoja.append([
            "Producto",
            "Categoría",
            "Fecha de publicación"
        ])

        for celda in hoja[hoja.max_row]:
            celda.font = Font(bold=True, color="FFFFFF")
            celda.fill = PatternFill(
                fill_type="solid",
                fgColor="734435"
            )
            celda.alignment = Alignment(horizontal="center")

        # Productos del artesano.
        for producto in grupo["productos"]:
            hoja.append([
                producto.nombre,
                producto.get_categoria_display(),
                producto.fecha_publicacion
            ])

            hoja.cell(
                row=hoja.max_row,
                column=3
            ).number_format = "DD/MM/YYYY"

        # Espacio entre artesanos.
        hoja.append([])

    # Si no hay productos.
    if hoja.max_row == 1 and hoja.cell(1, 1).value is None:
        hoja.append(["No hay productos publicados por artesanos aprobados."])

    # Ajustar ancho de las columnas.
    for columna in hoja.columns:
        maximo = 0
        letra = get_column_letter(columna[0].column)

        for celda in columna:
            if celda.value is not None:
                maximo = max(maximo, len(str(celda.value)))

        hoja.column_dimensions[letra].width = maximo + 4

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="productos_por_artesano.xlsx"'
    )

    libro.save(response)

    return response

