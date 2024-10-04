function correcto(titulo, texto) {
    Swal.fire({
        title: titulo || "Éxito",
        text: texto || "La operación se realizó correctamente.",
        icon: "success",
        confirmButtonText: "OK"
    });
}


function error(titulo, texto) {
    Swal.fire({
        title: titulo || "Error",
        text: texto || "Ocurrió un error al realizar la operación.",
        icon: "error",
        confirmButtonText: "OK"
    });
}


function texto(titulo, texto, icono) {
    Swal.fire({
        title: titulo || "Información",
        html: texto || "Aquí hay más detalles de la operación.",
        icon: icono || "info",
        confirmButtonText: "OK"
    });
}


// cons
// success
// error
// warning
// info
// question