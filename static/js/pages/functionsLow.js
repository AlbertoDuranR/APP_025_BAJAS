// Variables
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

$(document).ready(function () {
    // botones deshabiliados
    disableButtons()

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
        bajaArchivo();
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
    console.log(response);

    // validar respuesta
    if (response.success){
        correcto("Éxito", response.message)
        carpetaPrincipal = response.data.file_path;
        updateProgressBar(elementos.barraProgresoCarga, 100)
        enableButton(elementos.botonProcesar)
    }else{
        error("Error", response.message)
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
