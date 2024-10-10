$(document).ready(function () {
    console.log("cargo");

    // obtener cookie actual
    getCookie()

    // actualizar cookie
    $("#botonActualizarCookie").click(function (e) { 
        e.preventDefault();
        updateCookie()
    });
    
});


async function getCookie(){
    let endpoint = "/sunat/getToken"
    let response = await getRequest(endpoint)

    // asignar valor a fecha
    $("#fecha").text(response.data.dateTime)
    $("#cookie").text(response.data.cookie)
    
}

async function updateCookie() {
    let endpoint = "/sunat/updateToken"
    let token = $("#nuevoToken").val().trim()

    // limpiar espacios al final
    let dataForm = new FormData();
    dataForm.append("cookie", token);

    // Petición POST
    let response = await postRequest(endpoint, dataForm);
    if (response.success) {
        texto("Éxito", response.message, "success");
        getCookie()
        $("#nuevoToken").val("")
    }
}