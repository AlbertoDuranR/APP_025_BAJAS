// Variables

// Textos que cambiarán dinámicamente
let textosCarga = [
    "Localización de la carpeta...",
    "Identificando archivos...",
    "Iniciando la conexión a Selenium Grid...",
    "Se inicia el proceso de logueo...",
    "Se inicia el proceso de acceso a la sección Baja...",
    "Se inicia el proceso de acceso a la baja...",
    "Se inicia la carga de archivo...",
    "Se evalúan los resultados...",
    // Estos dos se repetirán
    "Se inicia la carga de archivo...",
    "Se evalúan los resultados..."
];

let indiceTexto = 0;


const elementos = {
    archivoInput: "#archivoInput",
    periodoInput: "#periodoInput",
    botonCargarArchivo: "#botonCargarArchivo",
    barraProgresoCarga: "#barraProgresoCarga",

    botonProcesar: "#botonProcesar",
    barraProgresoProcesar: "#barraProgresoProcesar",

    botonBaja: "#botonBaja",
    barraProgresoBaja: "#barraProgresoBaja",

    botonValidar: "#botonValidar",
    barraProgresoValidar: "#barraProgresoValidar",
};

let carpetaPrincipal = null;
let carpetaAcepta = null;
let carpetaSunat = null;

$(document).ready(function () {
    // botones deshabiliados
    // disableButtons()

    // Evento para cargar archivo
    $(elementos.botonCargarArchivo).click(function (e) {
        e.preventDefault();
        cargarArchivo();
    });

    // Evento para procesar archivo
    $(elementos.botonProcesar).click(function (e) {
        e.preventDefault();
        procesarArchivo();
    });

    // Evento para dar de baja archivo
    $(elementos.botonBaja).click(function (e) {
        e.preventDefault();
        // bajaArchivo();
        mostrarModalCarga()
        bajaArchivo()
    });

    // Evento para validar archivo
    $(elementos.botonValidar).click(function (e) {
        e.preventDefault();
        validarArchivo();
    });
});


// Función paso 1 - Cargar archivo
async function cargarArchivo() {
    // Obtener datos del archivo y periodo utilizando jQuery
    let archivo = $(elementos.archivoInput)[0].files[0];
    let periodo = $(elementos.periodoInput).val();

    // Añadir a FormData
    let dataForm = new FormData();
    dataForm.append("file", archivo);
    dataForm.append("period", periodo);

    // Petición POST
    let response = await postRequest("/low/upload", dataForm);

    // validar respuesta
    if (response.success) {
        correcto("Éxito", response.message)
        carpetaPrincipal = response.data.file_path;
        updateProgressBar(elementos.barraProgresoCarga, 100)
        enableButton(elementos.botonProcesar)
    } else {
        error("Error", response.message)
    }
}


// Función paso 2 - Procesar archivo
async function procesarArchivo() {
    // Añadir a FormData
    let dataForm = new FormData();
    dataForm.append("url_folder", carpetaPrincipal);

    // Petición POST
    let response = await postRequest("/low/processFile", dataForm);

    // validar respuesta
    if (response.success) {
        let mensaje = response.data.acepta_response.message + "<br>" + response.data.sunat_response.message;
        carpetaAcepta = response.data.acepta_response.folder_path;
        carpetaSunat = response.data.sunat_response.folder_path;

        texto("Éxito", mensaje, "success")
        updateProgressBar(elementos.barraProgresoProcesar, 100)
        enableButton(elementos.botonBaja)
    } else {
        error("Error", response.message)
    }
}

// Funcion pase 3 - Dar de baja en acepta
async function bajaArchivo() {
    // Añadir a FormData
    let dataForm = new FormData();
    dataForm.append("folder_path", carpetaAcepta);

    // Petición POST
    let response = await postRequest("/acepta/baja", dataForm);

    // validar respuesta
    if (response.success) {
        // Reemplazar \n por <br> en el mensaje para que los saltos de línea se respeten en HTML
        let formattedMessage = response.message.replace(/\n/g, "<br>");
        
        // Mostrar éxito con los saltos de línea correctamente formateados
        textoAcepta("Analiza la respuesta", formattedMessage, "info");
        
        updateProgressBar(elementos.barraProgresoBaja, 100);
        enableButton(elementos.botonValidar);
        ocultarModalCarga();
    } else {
        error("Error", response.message);
    }
}


// barra de progeso
function updateProgressBar(progressBarId, progress) {
    $(progressBarId).css("width", progress + "%");
}


// deshabilitar botones iniciales
function disableButtons() {
    $(elementos.botonProcesar).prop("disabled", true);
    $(elementos.botonBaja).prop("disabled", true);
    $(elementos.botonValidar).prop("disabled", true);
}

// habilitar boton
function enableButton(buttonId) {
    $(buttonId).prop("disabled", false);
}


// Función para iniciar el proceso de carga con cambio de textos

function mostrarModalCarga() {
    $('#loadingModal').modal('show');
    iniciarProcesoCarga();
}

function ocultarModalCarga() {
    $('#loadingModal').modal('hide');
}

function iniciarProcesoCarga() {
    let intervalo = setInterval(function () {
        // Hacer el texto más grande al comienzo
        $('#loading-text').css({
            'font-size': '2rem',  // Aumentar el tamaño
            'transition': 'font-size 0.5s ease'  // Transición suave
        });

        // Cambiar el texto
        $('#loading-text').text(textosCarga[indiceTexto]);
        indiceTexto++;

        // Si llegamos al final del array, repetimos los dos últimos textos
        if (indiceTexto >= textosCarga.length) {
            indiceTexto = 6; // Reiniciamos el índice para repetir los últimos dos pasos
        }

        // Después de 1 segundo, devolver el tamaño al normal
        setTimeout(function () {
            $('#loading-text').css({
                'font-size': '1rem',  // Tamaño normal
                'transition': 'font-size 0.5s ease'  // Transición suave
            });
        }, 1000);  // Después de 1 segundo

    }, 4000); // Cambiar texto cada 4 segundos
}


function textoAcepta(titulo, texto, icono) {
    Swal.fire({
        title: titulo || "Información",
        html: `<div style="max-height: 300px; overflow-y: auto; text-align: left;">${texto.replace(/Archivo:/g, '<strong>Archivo:</strong>')}</div>`,
        icon: icono || "info",
        showCancelButton: true,
        confirmButtonText: 'Continuar',
        cancelButtonText: 'Reiniciar',
        buttonsStyling: true
    }).then((result) => {
        if (result.isConfirmed) {
            // Acción si el usuario presiona "Continuar"
            console.log("El usuario eligió continuar.");
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            // Acción si el usuario presiona "Reiniciar"
            console.log("El usuario eligió reiniciar.");
            // Aquí podrías reiniciar el proceso o redirigir al usuario a otra página
            location.reload();
        }
    });
}
