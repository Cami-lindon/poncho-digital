from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from .forms import ArtesanoForm, SolicitudForm, GestionSolicitudForm
from .models import Solicitud

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import transaction
from django.utils.crypto import get_random_string


def gestionar_cuenta_artesano(artesano, email, nuevo_estado):
    """
    Gestiona la cuenta del artesano según el estado de su solicitud.
    - Aprobada: crea la cuenta si no existe (con clave provisoria) o reactiva la existente.
    - Pendiente, rechazada o modificaciones: desactiva la cuenta si existe.
    - Conserva usuarios, contraseñas y productos existentes.
    """
    Usuario = get_user_model()
    password_provisoria = None

    # CASO 1: SOLICITUD APROBADA
    if nuevo_estado == "aprobada":

        # Si el artesano todavía no tiene una cuenta, la creamos.
        if not artesano.usuario:
            username = artesano.dni

            # Evitamos crear un usuario duplicado.
            if Usuario.objects.filter(username=username).exists():
                raise ValueError(
                    f"Ya existe un usuario con el DNI {username} "
                    "como nombre de usuario."
                )

            # Generamos la contraseña provisoria
            password_provisoria = get_random_string(12)

            usuario = Usuario.objects.create_user(
                username=username,
                email=email,
                password=password_provisoria,
                debe_cambiar_password=True,
                is_active=True,
            )

            # Vinculamos el usuario con el artesano.
            artesano.usuario = usuario
            artesano.save(update_fields=["usuario"])

            accion = "creada"

        else:
            # Si ya existe, reutilizamos la misma cuenta.
            usuario = artesano.usuario

            if not usuario.is_active:
                usuario.is_active = True
                usuario.save(update_fields=["is_active"])
                accion = "reactivada"
            else:
                accion = "sin_cambios"

        # Garantizamos que el usuario tenga el grupo Artesanos.
        grupo, _ = Group.objects.get_or_create(name="Artesanos")

        # Obtenemos los permisos necesarios para gestionar productos.
        permisos = Permission.objects.filter(
            content_type__app_label="productos",
            codename__in=[
                "view_producto",
                "add_producto",
                "change_producto",
                "delete_producto",
            ],
        )

        # Garantizamos que el grupo tenga esos permisos y el usuario pertenezca a él.
        grupo.permissions.add(*permisos)
        usuario.groups.add(grupo)

        return usuario, accion, password_provisoria

    # CASO 2: SOLICITUD PENDIENTE, RECHAZADA O QUE REQUIERE MODIFICACIONES
    elif nuevo_estado in [
        "pendiente",
        "rechazada",
        "modificaciones",
    ]:
        # Si tiene una cuenta activa, la desactivamos.
        if artesano.usuario and artesano.usuario.is_active:
            artesano.usuario.is_active = False
            artesano.usuario.save(update_fields=["is_active"])
            return artesano.usuario, "desactivada", None

    return None, "sin_cambios", None


def registro_artesano(request):
    if request.method == "POST":
        artesano_form = ArtesanoForm(request.POST)
        solicitud_form = SolicitudForm(request.POST)

        if artesano_form.is_valid() and solicitud_form.is_valid():
            artesano = artesano_form.save(commit=False)
            artesano.save()

            solicitud = solicitud_form.save(commit=False)
            solicitud.artesano = artesano
            solicitud.save()

            messages.success(
                request,
                "Tu solicitud de registro se guardó correctamente."
            )

            return redirect("artesanos:registro_artesano")

    else:
        artesano_form = ArtesanoForm()
        solicitud_form = SolicitudForm()

    return render(
        request,
        "artesanos/registro_artesano.html",
        {
            "artesano_form": artesano_form,
            "solicitud_form": solicitud_form,
        },
    )


@staff_member_required
def panel_solicitudes(request):
    solicitudes = Solicitud.objects.all().order_by("-id")

    return render(
        request,
        "artesanos/panel_solicitudes.html",
        {"solicitudes": solicitudes},
    )


@staff_member_required
def detalle_solicitud(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)

    if request.method == "POST":
        estado_anterior = solicitud.estado

        formulario = GestionSolicitudForm(
            request.POST,
            instance=solicitud,
        )

        if formulario.is_valid():
            nuevo_estado = formulario.cleaned_data["estado"]

            try:
                with transaction.atomic():
                    # Guardamos los cambios de la solicitud.
                    formulario.save()

                    # Gestionamos la cuenta de artesano
                    _, accion, clave_provisoria = gestionar_cuenta_artesano(
                        solicitud.artesano,
                        solicitud.email,
                        nuevo_estado,
                    )

                    if accion == "creada":
                        messages.success(
                            request,
                            f"La solicitud se aprobó correctamente. "
                            f"Cuenta creada con usuario (DNI): {solicitud.artesano.dni} "
                            f"y Contraseña Provisoria: {clave_provisoria}"
                        )

                    elif accion == "reactivada":
                        messages.success(
                            request,
                            "La solicitud se aprobó nuevamente y "
                            "la cuenta existente fue reactivada (mantiene su contraseña anterior).",
                        )

                    elif accion == "desactivada":
                        messages.warning(
                            request,
                            "La cuenta del artesano fue desactivada. "
                            "Sus datos y productos se conservaron.",
                        )

                    elif nuevo_estado == estado_anterior:
                        messages.info(
                            request,
                            "La solicitud se guardó correctamente. "
                            "No hubo cambios de estado.",
                        )

                    else:
                        messages.success(
                            request,
                            "La solicitud se actualizó correctamente.",
                        )

            except ValueError as error:
                messages.error(request, str(error))

            return redirect(
                "artesanos:detalle_solicitud",
                pk=solicitud.pk,
            )

    else:
        formulario = GestionSolicitudForm(instance=solicitud)

    return render(
        request,
        "artesanos/detalle_solicitud.html",
        {
            "solicitud": solicitud,
            "formulario": formulario,
        },
    )
