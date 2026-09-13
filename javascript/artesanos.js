const formulario = document.querySelector("form");

formulario.addEventListener("submit", function(event) {
    event.preventDefault();

    const nombre = document.querySelector("#nombre");

    if (nombre.value.trim() === "") {
        alert("Por favor, ingresá tu nombre.");
        return;
    }

    const apellido = document.querySelector("#apellido");

    if (apellido.value.trim() === "") {
        alert("Por favor, ingresá tu apellido.");
        return;
    }

    const email = document.querySelector("#email");

    if (email.value.trim() === "") {
        alert("Por favor, ingresá tu email.");
        return;
    }

    const formatoEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!formatoEmail.test(email.value)) {
        alert("Por favor, ingresá un email válido.");
        return;
    }

    const telefono = document.querySelector("#telefono");

    if (telefono.value.trim() === "") {
        alert("Por favor, ingresá tu teléfono.");
        return;
    }

    const formatoTelefono = /^[0-9\s()+-]+$/;

    if (!formatoTelefono.test(telefono.value)) {
        alert("Por favor, ingresá un teléfono válido.");
        return;
    }

    const localidad = document.querySelector("#localidad");

    if (localidad.value.trim() === "") {
        alert("Por favor, ingresá tu localidad.");
        return;
    }

    const emprendimiento = document.querySelector("#emprendimiento");

    if (emprendimiento.value.trim() === "") {
        alert("Por favor, ingresá el nombre del emprendimiento.");
        return;
    }

    const rubro = document.querySelector("#rubro");

    if (rubro.value === "") {
        alert("Por favor, seleccioná un rubro.");
        return;
    }

    const descripcion = document.querySelector("#descripcion");

    if (descripcion.value.trim() === "") {
        alert("Por favor, ingresá una descripción.");
        return;
    }

    if (descripcion.value.trim().length < 10) {
        alert("La descripción debe tener al menos 10 caracteres.");
        return;
    }

    const productos = document.querySelector("#productos");

    if (productos.value.trim() === "") {
        alert("Por favor, indicá qué productos comercializás.");
        return;
    }


alert("Solicitud enviada correctamente.");
});
