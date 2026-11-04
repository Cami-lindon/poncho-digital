from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from .forms import ArtesanoForm, SolicitudForm
from .models import Solicitud

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
        {"solicitudes": solicitudes}
    )

