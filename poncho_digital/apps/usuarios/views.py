from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.debe_cambiar_password:
                return redirect("usuarios:cambiar_password")

            return redirect(reverse("home"))
        else:
            return render(request, "usuario/login.html", {"msj": "Credenciales incorrectas"})

    return render(request, "usuario/login.html")


def logout_view(request):
    logout(request)
    return render(request, "usuario/login.html", {"msj": "Deslogueado"})

@login_required
def cambiar_password(request):
    if request.method == "POST":
        formulario = PasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if formulario.is_valid():
            usuario = formulario.save()

            usuario.debe_cambiar_password = False
            usuario.save(update_fields=["debe_cambiar_password"])

            update_session_auth_hash(request, usuario)

            messages.success(request, "Tu contraseña se cambió correctamente.")
            return redirect("home")
    else:
        formulario = PasswordChangeForm(user=request.user)

    return render(
        request,
        "usuario/cambiar_password.html",
        {"formulario": formulario}
    )