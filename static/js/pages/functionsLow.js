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
let carpetaAcepta = null;
let carpetaSunat = null;

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


// Función paso 2 - Procesar archivo
async function procesarArchivo() {
    // Añadir a FormData
    let dataForm = new FormData();
    dataForm.append("url_folder", carpetaPrincipal);

    // Petición POST
    let response = await postRequest("/low/processFile", dataForm);

    console.log(response);
    

    // validar respuesta
    if (response.success){
        let mensaje = response.data.acepta_response.message + "<br>" + response.data.sunat_response.message; 
        carpetaAcepta = response.data.acepta_response.folder_path;
        carpetaSunat = response.data.sunat_response.folder_path;

        texto("Éxito", mensaje, "success")
        updateProgressBar(elementos.barraProgresoProcesar, 100)
        enableButton(elementos.botonBaja)
    }else{
        error("Error", response.message)
    }
}

// Funcion pase 3 - Dar de baja en acepta
// async function bajaArchivo() {
//     // Añadir a FormData
//     let dataForm = new FormData();
//     dataForm.append("url_folder", carpetaAcepta);

//     // Petición POST
//     let response = await postRequest("/low/bajaAcepta", dataForm);

//     // validar respuesta
//     if (response.success){
//         texto("Éxito", response.message, "success")
//         updateProgressBar(elementos.barraProgresoBaja, 100)
//         enableButton(elementos.botonValidar)
//     }else{
//         error("Error", response.message)
//     }
// }


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
