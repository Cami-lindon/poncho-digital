
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ArtesanoForm, SolicitudForm


def registro_artesano(request):
    if request.method == "POST":
        artesano_form = ArtesanoForm(request.POST)
        solicitud_form = SolicitudForm(request.POST)

        if artesano_form.is_valid() and solicitud_form.is_valid():
            artesano = artesano_form.save()
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

