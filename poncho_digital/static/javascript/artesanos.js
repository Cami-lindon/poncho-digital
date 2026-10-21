
document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.querySelector("form");

    if (!formulario) return;

    const obtener = (id) => document.getElementById(`id_${id}`);
    const valor = (id) => obtener(id)?.value.trim() ?? "";

    const provincia = obtener("provincia");
    const localidad = obtener("localidad");

    const API_GEOREF = "https://apis.datos.gob.ar/georef/api";

    // Limpia un desplegable y agrega una opción inicial.
    function limpiarLista(select, mensaje) {
        select.replaceChildren(new Option(mensaje, ""));
    }

    // Carga las provincias de Argentina.
    async function cargarProvincias() {
        if (!provincia || !localidad) return;

        provincia.disabled = true;
        limpiarLista(provincia, "Cargando provincias...");
        limpiarLista(localidad, "Primero seleccioná una provincia");
        localidad.disabled = true;

        try {
            const respuesta = await fetch(
                `${API_GEOREF}/provincias?orden=nombre&max=100`
            );

            if (!respuesta.ok) {
                throw new Error("No se pudieron cargar las provincias.");
            }

            const datos = await respuesta.json();

            limpiarLista(provincia, "Seleccioná una provincia");

            datos.provincias.forEach((item) => {
                provincia.add(new Option(item.nombre, item.nombre));
            });

            provincia.disabled = false;
        } catch (error) {
            limpiarLista(provincia, "Error al cargar las provincias");
            console.error(error);
            alert("No se pudieron cargar las provincias. Revisá tu conexión e intentá recargar la página.");
        }
    }

    // Cuando se elige una provincia, carga sus localidades.
    if (provincia && localidad) {
        provincia.addEventListener("change", async () => {
            limpiarLista(localidad, "Cargando localidades...");
            localidad.disabled = true;

            if (!provincia.value) {
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

                datos.localidades.forEach((item) => {
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
                alert("No se pudieron cargar las localidades. Intentá seleccionar nuevamente la provincia.");
            }
        });

        cargarProvincias();
    }

    // Valida el formulario antes de enviarlo a Django.
    formulario.addEventListener("submit", (event) => {
        const validaciones = [
            ["nombre", "Ingresá tu nombre."],
            ["apellido", "Ingresá tu apellido."],
            ["dni", "Ingresá tu DNI."],
            ["fecha_nacimiento", "Ingresá tu fecha de nacimiento."],
            ["email", "Ingresá tu email."],
            ["telefono", "Ingresá tu teléfono."],
            ["provincia", "Seleccioná una provincia."],
            ["localidad", "Seleccioná una localidad."],
            ["emprendimiento", "Ingresá el nombre del emprendimiento."],
            ["rubro", "Ingresá el rubro."],
            ["descripcion", "Ingresá una descripción."],
            ["productos", "Indicá qué productos comercializás."]
        ];

        for (const [campo, mensaje] of validaciones) {
            if (!valor(campo)) {
                event.preventDefault();
                alert(mensaje);
                obtener(campo)?.focus();
                return;
            }
        }

        // Validar email.
        const email = valor("email");

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            event.preventDefault();
            alert("Ingresá un email válido.");
            obtener("email")?.focus();
            return;
        }

        // Validar teléfono.
        const telefono = valor("telefono");

        if (!/^[0-9\s()+-]+$/.test(telefono)) {
            event.preventDefault();
            alert("Ingresá un teléfono válido.");
            obtener("telefono")?.focus();
            return;
        }

        // Validar descripción.
        const descripcion = valor("descripcion");

        if (descripcion.length < 10) {
            event.preventDefault();
            alert("La descripción debe tener al menos 10 caracteres.");
            obtener("descripcion")?.focus();
            return;
        }

        // Validar DNI de 7 u 8 números.
        const dni = valor("dni");

        if (!/^\d{7,8}$/.test(dni)) {
            event.preventDefault();
            alert("Ingresá un DNI válido de 7 u 8 números.");
            obtener("dni")?.focus();
            return;
        }

        // Validar fecha de nacimiento.
        const fechaTexto = valor("fecha_nacimiento");
        const nacimiento = new Date(`${fechaTexto}T00:00:00`);
        const hoy = new Date();

        hoy.setHours(0, 0, 0, 0);

        if (
            Number.isNaN(nacimiento.getTime()) ||
            nacimiento > hoy
        ) {
            event.preventDefault();
            alert("Ingresá una fecha de nacimiento válida.");
            obtener("fecha_nacimiento")?.focus();
            return;
        }

        // Calcular edad.
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
            event.preventDefault();
            alert("Debés tener al menos 18 años para solicitar un stand.");
            obtener("fecha_nacimiento")?.focus();
            return;
        }

        // Si llegamos acá, no cancelamos el envío.
        // El formulario se envía a Django mediante POST.
    });
});
