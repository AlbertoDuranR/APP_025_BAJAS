// Variables

// Textos que cambiarán dinámicamente
let textosCargaAcepta = [
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

// Textos que cambiarán dinámicamente
let textosCargaSunat = [
    "Localización de la carpeta...",
    "Identificando archivos...",
    "Iniciando la comunicacion con la Api...",

    // Estos dos se repetirán
    "Realizando consulta...",
    "Reintentando consulta...",
];

let indiceTextoAcepta = 0;
let indiceTextoSunat = 0;

let modalAcepta = "#loadingModalAcepta"
let txtLoadingAcepta = "#txtLoadingAcepta"

let modalSunat = "#loadingModalSunat"
let txtLoadingSunat = "#txtLoadingSunat"


const elementos = {
    archivoInput: "#archivoInput",
    periodoInput: "#periodoInput",
    botonCargarArchivo: "#botonCargarArchivo",
    barraProgresoCarga: "#barraProgresoCarga",

    botonProcesar: "#botonProcesar",
    botonDescargarArchivos: "#botonDescargarArchivos",
    barraProgresoProcesar: "#barraProgresoProcesar",

    botonBaja: "#botonBaja",
    barraProgresoBaja: "#barraProgresoBaja",

    botonValidar: "#botonValidar",
    barraProgresoValidar: "#barraProgresoValidar",
};

let carpetaPrincipal = null;
let archivoPrincipal = null;
let carpetaAcepta = null;
let carpetaSunat = null;

$(document).ready(function () {

     // Inicializar DataTable cuando el documento esté listo
     $('#tableValidate').DataTable({
        responsive: true,
        autoWidth: false,
        pageLength: 10,
        scrollX: true,
        lengthMenu: [10, 25, 50, 75, 100],
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                title: 'Resultados de Validaciones en Sunat',
                text: 'Exportar a Excel',
                className: 'btn btn-success'
            }
        ],
        language: {
            search: "Buscar:",
            lengthMenu: "Mostrar _MENU_ entradas",
            info: "Mostrando _START_ a _END_ de _TOTAL_ entradas",
            paginate: {
                previous: "Anterior",
                next: "Siguiente"
            }
        }
    });

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

    // Evento par descargar archivos
    $(elementos.botonDescargarArchivos).click(function (e) {
        e.preventDefault();
        descargarArchivos();
    });

    // Evento para dar de baja archivo acepta
    $(elementos.botonBaja).click(function (e) {
        e.preventDefault();
        // bajaArchivo();
        mostrarModalAcepta()
        bajaArchivo()
    });

    // Evento para validar archivo sunat
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
    dataForm.append("functionApp", "low");

    // Petición POST
    let response = await postRequest("/low/upload", dataForm);

    // validar respuesta
    if (response.success) {
        correcto("Éxito", response.message)
        carpetaPrincipal = response.data.upload_folder;
        archivoPrincipal = response.data.file_path;

        numeroFilas = response.data.number_rows;
        $("#numberRows").text(numeroFilas + " Filas");
        updateProgressBar(elementos.barraProgresoCarga, 100)
        enableButton(elementos.botonProcesar)
        enableButton(elementos.botonDescargarArchivos)
    } else {
        error("Error", response.message)
    }
}


// Función paso 2 - Procesar archivo
async function procesarArchivo() {
    // Añadir a FormData
    let dataForm = new FormData();
    dataForm.append("url_folder", archivoPrincipal);

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


// Función para baja de archivo - Paso 3
// Función para baja de archivo - Paso 3
async function bajaArchivo() {
    // Añadir a FormData
    let dataForm = new FormData();
    dataForm.append("folder_path", carpetaAcepta);

    // Petición POST
    let response = await postRequest("/acepta/baja", dataForm);

    $("#loadingModalAcepta").modal('hide');

    // Validar respuesta
    if (response.success) {
        // Obtener la instancia de DataTable
        const table = $('#tableValidate').DataTable();
        
        // Limpiar la tabla antes de agregar datos nuevos
        table.clear();

        // Insertar cada resultado en una fila de la tabla
        response.data.resultados.forEach(resultado => {
            let fila = [
                resultado.archivo,
                resultado.respuestas.join("<br>")
            ];
            table.row.add(fila);
        });

        // Redibujar la tabla después de agregar las filas
        table.draw();

        updateProgressBar(elementos.barraProgresoBaja, 100);
        enableButton(elementos.botonValidar);
        ocultarModalAcepta();
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

    $(elementos.botonDescargarArchivos).prop("disabled", true);
}

// habilitar boton
function enableButton(buttonId) {
    $(buttonId).prop("disabled", false);
}


// Función para iniciar el proceso de carga con cambio de textos

function mostrarModalAcepta() {
    $(modalAcepta).modal('show');
    iniciarProcesoCargaAcepta();
}

function ocultarModalAcepta() {
    $(modalAcepta).modal('hide');
}


// Modales para api sunat
function mostrarModalSunat() {
    $(modalSunat).modal('show');
    iniciarProcesoCargaSunat()
}

function ocultarModalSunat() {
    $(modalSunat).modal('hide');
}

function iniciarProcesoCargaAcepta() {
    let intervalo = setInterval(function () {
        // Hacer el texto más grande al comienzo
        $(txtLoadingAcepta).css({
            'font-size': '2rem',  // Aumentar el tamaño
            'transition': 'font-size 0.5s ease'  // Transición suave
        });

        // Cambiar el texto
        $(txtLoadingAcepta).text(textosCargaAcepta[indiceTextoAcepta]);
        indiceTextoAcepta++;

        // Si llegamos al final del array, repetimos los dos últimos textos
        if (indiceTextoAcepta >= textosCargaAcepta.length) {
            indiceTextoAcepta = 6; // Reiniciamos el índice para repetir los últimos dos pasos
        }

        // Después de 1 segundo, devolver el tamaño al normal
        setTimeout(function () {
            $(txtLoadingAcepta).css({
                'font-size': '1rem',  // Tamaño normal
                'transition': 'font-size 0.5s ease'  // Transición suave
            });
        }, 1000);  // Después de 1 segundo

    }, 4000); // Cambiar texto cada 4 segundos
}

function iniciarProcesoCargaSunat() {
    let intervalo = setInterval(function () {
        // Hacer el texto más grande al comienzo
        $(txtLoadingSunat).css({
            'font-size': '2rem',  // Aumentar el tamaño
            'transition': 'font-size 0.5s ease'  // Transición suave
        });

        // Cambiar el texto
        $(txtLoadingSunat).text(textosCargaSunat[indiceTextoSunat]);
        indiceTextoSunat++;

        // Si llegamos al final del array, repetimos los dos últimos textos
        if (indiceTextoSunat >= textosCargaSunat.length) {
            indiceTextoSunat = 2; // Reiniciamos el índice para repetir los últimos dos pasos
        }

        // Después de 1 segundo, devolver el tamaño al normal
        setTimeout(function () {
            $(txtLoadingSunat).css({
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


async function descargarArchivos() {
    // Definir la carpeta que se enviará en el request
    // let url_folder = 'static/uploads/2024_10_09_16_59_00';  // Ajusta la carpeta deseada

    try {
        // Crear un objeto FormData para enviar la información
        let formData = new FormData();
        formData.append('url_folder', carpetaPrincipal);  // Añadir la ruta de la carpeta

        // Realizar la solicitud POST usando Axios
        const response = await axios({
            url: '/low/downloadFiles',   // La URL de tu API
            method: 'POST',
            data: formData,              // Enviar el objeto FormData
            responseType: 'blob',        // Indicamos que la respuesta es un archivo binario
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        // Crear un blob con la respuesta
        const blob = new Blob([response.data], { type: 'application/zip' });

        // Obtener el nombre del archivo desde los headers o asignar un nombre por defecto
        const contentDisposition = response.headers['content-disposition'];
        let filename = 'archivo.zip';  // Nombre por defecto

        if (contentDisposition && contentDisposition.includes('filename=')) {
            filename = contentDisposition.split('filename=')[1].replace(/['"]/g, '');
        }

        // Crear un enlace temporal para descargar el archivo
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        error('Error', 'Ocurrió un error al descargar los archivos.')
    }
}
