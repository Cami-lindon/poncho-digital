
// FUNCIÓN CONSTRUCTORA PRODUCTO


function Producto(id, nombre, categoria, rubro, descripcion,
                  precio, stock, peso, dimensiones, fecha, imagen, imagenesAdicionales) {

    this.id = id;
    this.nombre = nombre;
    this.categoria = categoria;
    this.rubro = rubro;
    this.descripcion = descripcion;
    this.precio = precio;
    this.stock = stock;
    this.peso = peso;
    this.dimensiones = dimensiones;
    this.fecha = fecha;
    this.imagen = imagen;
    this.imagenesAdicionales = imagenesAdicionales;
}



// ARRAY DE PRODUCTOS


let productos = [];

let contadorProductos = 1;

// VARIABLE PARA SABER QUÉ PRODUCTO
// ESTAMOS MODIFICANDO


let productoModificar = null;



// MOSTRAR PRODUCTOS EN LA TABLA


function mostrarProductos() {

    let tabla = document.querySelector("#sección-misproductos tbody");

    tabla.innerHTML = "";

    for (let i = 0; i < productos.length; i++) {

        let producto = productos[i];

        let fila = document.createElement("tr");

        // ID
        let celdaId = document.createElement("td");
        celdaId.textContent = producto.id;

        // Imagen
        let celdaImagen = document.createElement("td");

         if (producto.imagen != "") {
            let imgProducto = document.createElement("img");
            imgProducto.src = producto.imagen;
            imgProducto.classList.add("img-thumbnail");
            imgProducto.style.maxHeight = "60px";

            celdaImagen.appendChild(imgProducto);
        } else {
            celdaImagen.textContent = "Sin imagen";
        }

        // Nombre
        let celdaNombre = document.createElement("td");
        celdaNombre.textContent = producto.nombre;

        // Categoría
        let celdaCategoria = document.createElement("td");
        celdaCategoria.textContent = producto.categoria;

        // Rubro
        let celdaRubro = document.createElement("td");
        celdaRubro.textContent = producto.rubro;

        // Precio
        let celdaPrecio = document.createElement("td");
        celdaPrecio.textContent = formatearPrecio(producto.precio);

        // Stock
        let celdaStock = document.createElement("td");
        celdaStock.textContent = producto.stock;

        // Fecha
        let celdaFecha = document.createElement("td");
        celdaFecha.textContent = producto.fecha;

        // Acciones
        let celdaAcciones = document.createElement("td");

        let botonModificar = document.createElement("button");

        botonModificar.textContent = "Modificar";
        botonModificar.classList.add(
            "btn",
            "btn-sm",
            "btn-outline-primary",
            "me-1"
        );

        botonModificar.dataset.id = producto.id;

        let botonEliminar = document.createElement("button");

        botonEliminar.textContent = "Eliminar";
        botonEliminar.classList.add(
            "btn",
            "btn-sm",
            "btn-outline-danger"
        );

        botonEliminar.dataset.id = producto.id;

        celdaAcciones.appendChild(botonModificar);
        celdaAcciones.appendChild(botonEliminar);

        // Agregamos todas las celdas a la fila

        fila.appendChild(celdaId);
        fila.appendChild(celdaImagen);
        fila.appendChild(celdaNombre);
        fila.appendChild(celdaCategoria);
        fila.appendChild(celdaRubro);
        fila.appendChild(celdaPrecio);
        fila.appendChild(celdaStock);
        fila.appendChild(celdaFecha);
        fila.appendChild(celdaAcciones);

        tabla.appendChild(fila);
    }
}

function mostrarProductosEliminar() {

    let tablaEliminar = document.getElementById("tablaEliminarProductos");

    tablaEliminar.innerHTML = "";

    for (let i = 0; i < productos.length; i++) {

        let producto = productos[i];

        let fila = document.createElement("tr");

        let celdaCheck = document.createElement("td");
        let check = document.createElement("input");
        check.type = "checkbox";
        check.classList.add("form-check-input");
        check.value = producto.id;
        celdaCheck.appendChild(check);

        let celdaId = document.createElement("td");
        celdaId.textContent = producto.id;

        let celdaNombre = document.createElement("td");
        celdaNombre.textContent = producto.nombre;

        let celdaPrecio = document.createElement("td");
        celdaPrecio.textContent = formatearPrecio(producto.precio);

        fila.appendChild(celdaCheck);
        fila.appendChild(celdaId);
        fila.appendChild(celdaNombre);
        fila.appendChild(celdaPrecio);

        tablaEliminar.appendChild(fila);
    }
}

// AGREGAR PRODUCTO

function generarIdProducto() {
    let id = "PROD-2026-" + String(contadorProductos).padStart(3, "0");
    contadorProductos++;
    return id;
}

function obtenerFechaActual() {
    let fecha = new Date();

    let dia = String(fecha.getDate()).padStart(2, "0");
    let mes = String(fecha.getMonth() + 1).padStart(2, "0");
    let ano = fecha.getFullYear();

    return dia + "/" + mes + "/" + ano;
}

function agregarProducto() {

    let nombre = document.getElementById("nombre").value;
    let categoria = document.getElementById("categoria").value;
    let rubro = document.getElementById("rubro").value;
    let descripcion = document.getElementById("descripcion").value;
    let precio = document.getElementById("precio").value;
    let stock = document.getElementById("stock").value;
    let peso = document.getElementById("peso").value;
    let dimensiones = document.getElementById("dimensiones").value;

    if (nombre.trim() == "" || categoria == "" || rubro == "" ||
        descripcion.trim() == "" || precio == "" || stock == "") {

        mostrarMensaje("Complete todos los campos obligatorios.", "danger");

        return;
    }

        if (Number(precio) <= 0) {
        mostrarMensaje("El precio debe ser mayor a 0.", "danger");
        return;
    }

    if (Number(stock) <= 0 || !Number.isInteger(Number(stock))) {
        mostrarMensaje("El stock debe ser un número entero mayor a 0.", "danger");
        return;
    }

    if (descripcion.length < 10) {
        mostrarMensaje("La descripción debe tener al menos 10 caracteres.", "danger");
        return;
    }

    let imagenPrincipal = document.getElementById("imagenPrincipal");

    if (imagenPrincipal.files.length == 0) {
        mostrarMensaje("Debe seleccionar una imagen principal.", "warning");
        return;
    }
    let imagen = URL.createObjectURL(imagenPrincipal.files[0]);

    let inputsAdicionales = document.querySelectorAll(".imagen-adicional");
    let imagenesAdicionales = [];

        for (let i = 0; i < inputsAdicionales.length; i++) {

            if (inputsAdicionales[i].files.length > 0) {
        let imagenAdicional = URL.createObjectURL(inputsAdicionales[i].files[0]);
        imagenesAdicionales.push(imagenAdicional);
        }
}
    let nuevoId = generarIdProducto();

    let nuevoProducto = new Producto(
        nuevoId,
        nombre,
        categoria,
        rubro,
        descripcion,
        precio,
        stock,
        peso,
        dimensiones,
        obtenerFechaActual(),
        imagen,
        imagenesAdicionales
    );

    productos.push(nuevoProducto);

    mostrarProductos();
    mostrarProductosEliminar();

    mostrarMensaje("Producto agregado correctamente.", "success");

    document.getElementById("formAgregar").reset();

}



// CARGAR PRODUCTO PARA MODIFICAR


function cargarProducto(id) {

    for (let i = 0; i < productos.length; i++) {

        if (productos[i].id == id) {

            productoModificar = productos[i];

            document.getElementById("tituloModificar").textContent =
            "Editando: " + productoModificar.id + " - " + productoModificar.nombre;

            document.getElementById("idProductoMod").textContent =
                productoModificar.id;

            document.getElementById("fechaProductoMod").textContent =
                productoModificar.fecha;

            document.getElementById("btnGuardarCambios").disabled = false;

            let imagenActualMod = document.getElementById("imagenActualMod");

            if (productoModificar.imagen != "") {
                imagenActualMod.src = productoModificar.imagen;
                imagenActualMod.style.display = "block";
            } else {
                imagenActualMod.src = "";
                imagenActualMod.style.display = "none";
            }

            let tablaImagenesAdicionales = document.getElementById("imagenesAdicionalesMod");

                tablaImagenesAdicionales.innerHTML = "";

                for (let i = 0; i < productoModificar.imagenesAdicionales.length; i++) {

                    let fila = document.createElement("tr");

                    let celdaImagen = document.createElement("td");
                    let img = document.createElement("img");

                    img.src = productoModificar.imagenesAdicionales[i];
                    img.classList.add("img-thumbnail");
                    img.style.maxHeight = "60px";

                    celdaImagen.appendChild(img);

                    let celdaEliminar = document.createElement("td");
                    let check = document.createElement("input");

                    check.type = "checkbox";
                    check.classList.add("form-check-input");
                    check.dataset.indice = i;

                    celdaEliminar.appendChild(check);

                    fila.appendChild(celdaImagen);
                    fila.appendChild(celdaEliminar);

                    tablaImagenesAdicionales.appendChild(fila);
                }

            document.getElementById("nombre-mod").value =
                productoModificar.nombre;

            document.getElementById("categoria-mod").value =
                productoModificar.categoria;

            document.getElementById("rubro-mod").value =
                productoModificar.rubro;

            document.getElementById("descripcion-mod").value =
                productoModificar.descripcion;

            document.getElementById("precio-mod").value =
                productoModificar.precio;

            document.getElementById("stock-mod").value =
                productoModificar.stock;

            document.getElementById("peso-mod").value =
                productoModificar.peso;

            document.getElementById("dimensiones-mod").value =
                productoModificar.dimensiones;

            location.href = "#sección-modificar";

            break;
        }
    }
}



// GUARDAR CAMBIOS


function guardarCambios() {

    if (productoModificar == null) {

        mostrarMensaje("No hay ningún producto seleccionado.", "warning");

        return;
    }

    let nombreMod = document.getElementById("nombre-mod").value;
    let categoriaMod = document.getElementById("categoria-mod").value;
    let rubroMod = document.getElementById("rubro-mod").value;
    let descripcionMod = document.getElementById("descripcion-mod").value;
    let precioMod = document.getElementById("precio-mod").value;
    let stockMod = document.getElementById("stock-mod").value;

    if (nombreMod.trim() == "" || categoriaMod == "" || rubroMod == "" ||
        descripcionMod.trim() == "" || precioMod == "" || stockMod == "") {

        mostrarMensaje("Complete todos los campos obligatorios.", "danger");
        return;
    }

    if (Number(precioMod) <= 0) {
        mostrarMensaje("El precio debe ser mayor a 0.", "danger");
        return;
    }

    if (Number(stockMod) <= 0 || !Number.isInteger(Number(stockMod))) {
        mostrarMensaje("El stock debe ser un número entero mayor a 0.", "danger");
        return;
    }

    if (descripcionMod.length < 10) {
       mostrarMensaje("La descripción debe tener al menos 10 caracteres.", "danger");
        return;
    }

    productoModificar.nombre = nombreMod;
    productoModificar.categoria = categoriaMod;
    productoModificar.rubro = rubroMod;
    productoModificar.descripcion = descripcionMod;
    productoModificar.precio = precioMod;
    productoModificar.stock = stockMod;

        productoModificar.peso =
            document.getElementById("peso-mod").value;

        productoModificar.dimensiones =
            document.getElementById("dimensiones-mod").value;

    let checksEliminarImagenes =
    document.querySelectorAll("#imagenesAdicionalesMod input[type='checkbox']:checked");

        for (let i = checksEliminarImagenes.length - 1; i >= 0; i--) {

            let indice = Number(checksEliminarImagenes[i].dataset.indice);

            productoModificar.imagenesAdicionales.splice(indice, 1);
        }

        let nuevasImagenesMod = document.querySelectorAll(".nueva-imagen-mod");

        for (let i = 0; i < nuevasImagenesMod.length; i++) {

        if (nuevasImagenesMod[i].files.length > 0) {

        let nuevaImagen = URL.createObjectURL(nuevasImagenesMod[i].files[0]);

        productoModificar.imagenesAdicionales.push(nuevaImagen);
    }
}
        let eliminarImgPrinc = document.getElementById("eliminarImgPrinc");

        if (eliminarImgPrinc.checked) {
            productoModificar.imagen = "";
        }

        let nuevaImagenPrincipalMod = document.getElementById("nuevaImagenPrincipalMod");

        if (nuevaImagenPrincipalMod.files.length > 0) {
            productoModificar.imagen = URL.createObjectURL(nuevaImagenPrincipalMod.files[0]);
        } else if (eliminarImgPrinc.checked) {
            productoModificar.imagen = "";
        }
    mostrarProductos();
    mostrarProductosEliminar();

    mostrarMensaje("Producto modificado correctamente.", "success");

    limpiarFormularioModificar();
}
    function limpiarFormularioModificar() {

    document.getElementById("tituloModificar").textContent =
        "Seleccione un producto para modificar";

    document.getElementById("idProductoMod").textContent = "---";
    document.getElementById("fechaProductoMod").textContent = "---";

    document.querySelector("#sección-modificar form").reset();

    document.getElementById("btnGuardarCambios").disabled = true;

    let imagenActualMod = document.getElementById("imagenActualMod");
    imagenActualMod.src = "";
    imagenActualMod.style.display = "none";

    document.getElementById("imagenesAdicionalesMod").innerHTML = "";

    productoModificar = null;
}


// ELIMINAR PRODUCTO


function eliminarProducto(id) {

    let encontrado = false;

    let confirmar = confirm(
        "¿Está seguro de eliminar este producto?"
    );

    if (confirmar) {

        for (let i = 0; i < productos.length; i++) {

            if (productos[i].id == id) {

                productos.splice(i, 1);
                encontrado = true;

                break;
            }
        }

        if (encontrado) {
            mostrarProductos();
            mostrarProductosEliminar();
            limpiarFormularioModificar();
            document.getElementById("idEliminar").value = "";
            mostrarMensaje("Producto eliminado correctamente.", "success");
        } else {
            mostrarMensaje("No se encontró ningún producto con ese ID.", "danger");
        }
    }
}


// ==========================================
// EVENTO PARA AGREGAR
// ==========================================

let formularioAgregar =
    document.querySelector("#sección-agregar form");

formularioAgregar.addEventListener("submit", function(event) {

    event.preventDefault();

    agregarProducto();
});


// ==========================================
// EVENTO PARA MODIFICAR
// ==========================================

let formularioModificar =
    document.querySelector("#sección-modificar form");

formularioModificar.addEventListener("submit", function(event) {

    event.preventDefault();

    guardarCambios();
});


// ==========================================
// EVENTOS DE LOS BOTONES DE LA TABLA
// ==========================================

let tablaProductos =
    document.querySelector("#sección-misproductos tbody");

tablaProductos.addEventListener("click", function(event) {

    if (event.target.textContent == "Modificar") {

        let id = event.target.dataset.id;

        cargarProducto(id);
    }

    if (event.target.textContent == "Eliminar") {

        let id = event.target.dataset.id;

        eliminarProducto(id);
    }
});


let inputImagen = document.getElementById("imagenPrincipal");
let vistaPrevia = document.getElementById("vistaPreviaImagen");

inputImagen.addEventListener("change", function() {
    let archivo = inputImagen.files[0];

    if (archivo) {
        vistaPrevia.src = URL.createObjectURL(archivo);
        vistaPrevia.style.display = "block";
    } else {
        vistaPrevia.src = "";
        vistaPrevia.style.display = "none";
    }
});

formularioAgregar.addEventListener("reset", function() {
    vistaPrevia.src = "";
    vistaPrevia.style.display = "none";
});

let btnEliminarPorId = document.getElementById("btnEliminarPorId");

btnEliminarPorId.addEventListener("click", function() {

    let id = document.getElementById("idEliminar").value;

    if (id == "") {
        mostrarMensaje("Ingrese un ID para eliminar.", "warning");
        return;
    }

    eliminarProducto(id);
});

let btnEliminarSeleccionados = document.getElementById("btnEliminarSeleccionados");

    btnEliminarSeleccionados.addEventListener("click", function() {

    let checks = document.querySelectorAll("#tablaEliminarProductos input[type='checkbox']:checked");

    if (checks.length == 0) {
        mostrarMensaje("Seleccione al menos un producto.", "warning");
        return;
    }

    let confirmar = confirm("¿Está seguro de eliminar los productos seleccionados?");

    if (confirmar) {

        for (let i = 0; i < checks.length; i++) {

            let id = checks[i].value;

            for (let j = productos.length - 1; j >= 0; j--) {

                if (productos[j].id == id) {
                    productos.splice(j, 1);
                }
            }
        }

        mostrarProductos();
        mostrarProductosEliminar();
        limpiarFormularioModificar();
        mostrarMensaje("Productos eliminados correctamente.", "success");
    }
});

    function formatearPrecio(precio) {
    return "$" + Number(precio).toLocaleString("es-AR");
}

function mostrarMensaje(texto, tipo) {
    let modalTitulo = document.getElementById("modalMensajeTitulo");
    let modalTexto = document.getElementById("modalMensajeTexto");
    let modalContenido = document.querySelector("#modalMensaje .modal-content");

    modalTitulo.textContent = tipo == "success" ? "Correcto" : "Atención";
    modalTexto.textContent = texto;

    modalContenido.classList.remove("border-success", "border-danger", "border-warning", "border-info");

    if (tipo == "success") {
        modalContenido.classList.add("border", "border-success");
    } else if (tipo == "danger") {
        modalContenido.classList.add("border", "border-danger");
    } else if (tipo == "warning") {
        modalContenido.classList.add("border", "border-warning");
    } else {
        modalContenido.classList.add("border", "border-info");
    }

    let modal = new bootstrap.Modal(document.getElementById("modalMensaje"));
    modal.show();
}

let btnCancelarEdicion = document.getElementById("btnCancelarEdicion");

btnCancelarEdicion.addEventListener("click", function() {
    limpiarFormularioModificar();
});