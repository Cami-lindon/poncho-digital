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

    const dni = document.querySelector("#dni");

    if (!/^\d{7,8}$/.test(dni.value.trim())) {
        alert("Ingresá un DNI válido de 7 u 8 números.");
        return;
    }

    const fechaNacimiento = document.querySelector("#fechaNacimiento");
    const nacimiento = new Date(fechaNacimiento.value + "T00:00:00");
    const hoy = new Date();

    if (
        !fechaNacimiento.value ||
        Number.isNaN(nacimiento.getTime()) ||
        nacimiento > hoy
    ) {
        alert("Ingresá una fecha de nacimiento válida.");
        return;
    }

    let edad = hoy.getFullYear() - nacimiento.getFullYear();

    const aunNoCumplio =
        hoy.getMonth() < nacimiento.getMonth() ||
        (
            hoy.getMonth() === nacimiento.getMonth() &&
            hoy.getDate() < nacimiento.getDate()
        );

    if (aunNoCumplio) {
        edad--;
    }

    if (edad < 18) {
        alert("Debés ser mayor de edad para solicitar un stand.");
        return;
    }


alert("Solicitud enviada correctamente.");
});


const provincia = document.querySelector("#provincia");
const localidad = document.querySelector("#localidad");

const API_GEOREF = "https://apis.datos.gob.ar/georef/api";

function limpiarLista(select, mensaje) {
    select.innerHTML = "";
    select.add(new Option(mensaje, ""));
}

async function cargarProvincias() {
    limpiarLista(provincia, "Cargando provincias...");
    provincia.disabled = true;

    try {
        const respuesta = await fetch(
            `${API_GEOREF}/provincias?orden=nombre&max=100`
        );

        if (!respuesta.ok) {
            throw new Error("No se pudieron cargar las provincias.");
        }

        const datos = await respuesta.json();

        limpiarLista(provincia, "Seleccioná una provincia");

        datos.provincias.forEach(function (item) {
            provincia.add(new Option(item.nombre, item.nombre));
        });

        provincia.disabled = false;
    } catch (error) {
        limpiarLista(provincia, "Error al cargar las provincias");
        console.error(error);
    }
}

provincia.addEventListener("change", async function () {
    limpiarLista(localidad, "Cargando localidades...");
    localidad.disabled = true;

    if (provincia.value === "") {
        limpiarLista(
            localidad,
            "Primero seleccioná una provincia"
        );
        return;
    }

    try {
        const url =
            `${API_GEOREF}/localidades` +
            `?provincia=${encodeURIComponent(provincia.value)}` +
            "&orden=nombre&max=5000";

        const respuesta = await fetch(url);

        if (!respuesta.ok) {
            throw new Error("No se pudieron cargar las localidades.");
        }

        const datos = await respuesta.json();

        limpiarLista(localidad, "Seleccioná una localidad");

        datos.localidades.forEach(function (item) {
            localidad.add(new Option(item.nombre, item.nombre));
        });

        if (datos.localidades.length === 0) {
            limpiarLista(
                localidad,
                "No se encontraron localidades"
            );
            return;
        }

        localidad.disabled = false;
    } catch (error) {
        limpiarLista(localidad, "Error al cargar las localidades");
        console.error(error);
    }
});

cargarProvincias();
