
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

        let imgProducto = document.createElement("img");
        imgProducto.src = producto.imagen;
        imgProducto.classList.add("img-thumbnail");
        imgProducto.style.maxHeight = "60px";

        celdaImagen.appendChild(imgProducto);

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
        celdaPrecio.textContent = producto.precio;

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
        celdaPrecio.textContent = producto.precio;

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

        alert("Complete todos los campos obligatorios.");

        return;
    }

        if (Number(precio) <= 0) {
        alert("El precio debe ser mayor a 0.");
        return;
    }

    if (Number(stock) <= 0 || !Number.isInteger(Number(stock))) {
        alert("El stock debe ser un número entero mayor a 0.");
        return;
    }

    if (descripcion.length < 10) {
        alert("La descripción debe tener al menos 10 caracteres.");
        return;
    }

    let imagenPrincipal = document.getElementById("imagenPrincipal");

    if (imagenPrincipal.files.length == 0) {
        alert("Debe seleccionar una imagen principal.");
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
        "12/09/2026",
        imagen,
        imagenesAdicionales
    );

    productos.push(nuevoProducto);

    mostrarProductos();
    mostrarProductosEliminar();

    alert("Producto agregado correctamente.");

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

            imagenActualMod.src = productoModificar.imagen;
            imagenActualMod.style.display = "block";

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

        alert("No hay ningún producto seleccionado.");

        return;
    }

    productoModificar.nombre =
        document.getElementById("nombre-mod").value;

    productoModificar.categoria =
        document.getElementById("categoria-mod").value;

    productoModificar.rubro =
        document.getElementById("rubro-mod").value;

    productoModificar.descripcion =
        document.getElementById("descripcion-mod").value;

    productoModificar.precio =
        document.getElementById("precio-mod").value;

    productoModificar.stock =
        document.getElementById("stock-mod").value;

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
    mostrarProductos();
    mostrarProductosEliminar();

    alert("Producto modificado correctamente.");

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

    let confirmar = confirm(
        "¿Está seguro de eliminar este producto?"
    );

    if (confirmar) {

        for (let i = 0; i < productos.length; i++) {

            if (productos[i].id == id) {

                productos.splice(i, 1);

                break;
            }
        }

        mostrarProductos();
        mostrarProductosEliminar();
        alert("Producto eliminado correctamente.");
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
        alert("Ingrese un ID para eliminar.");
        return;
    }

    eliminarProducto(id);
});

let btnEliminarSeleccionados = document.getElementById("btnEliminarSeleccionados");

    btnEliminarSeleccionados.addEventListener("click", function() {

    let checks = document.querySelectorAll("#tablaEliminarProductos input[type='checkbox']:checked");

    if (checks.length == 0) {
        alert("Seleccione al menos un producto.");
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

        alert("Productos eliminados correctamente.");
    }
});