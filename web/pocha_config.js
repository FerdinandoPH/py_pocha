function obtener_datos(){
    var nombre= document.getElementById("campo_nombre").value;
    if (nombre == ""){
        return false;
    }
    else if (nombre.length > 18){
        nombre = nombre.substring(0, 18);
    }
    if(document.querySelector('input[name="crear_o_unir"]:checked')==null){
        return false;
    }
    var crear_o_unir = document.querySelector('input[name="crear_o_unir"]:checked').value;
    var codigo = document.getElementById("campo_jug_o_id").value;
    if (codigo == ""){
        return false;
    }
    else{
        codigo=(parseInt(codigo)%10000).toString();
    }
    return crear_o_unir+codigo+nombre;
}
function iniciar_juego(){
    if (obtener_datos()!=false){
        window.location.href = "pocha_juego.html?parametros="+obtener_datos();
    }
    else{
        alert("Por favor, rellena todos los campos");
    }
}
function cambio_radio(){
    document.getElementById("jug_o_id").style.display = "block";
    if(document.querySelector('input[name="crear_o_unir"]:checked').value == "U"){
        document.getElementById("jug_o_id").innerHTML = "Código de la partida: <input type='text' id='campo_jug_o_id' >";
    }
    else{
        document.getElementById("jug_o_id").innerHTML = "Número de jugadores: <input type='number' id='campo_jug_o_id' >";
    }
}
function al_cargar(){
    var url_string = window.location.href;
    var url = new URL(url_string);
    var mensaje_error = url.searchParams.get("merror");
    alert(mensaje_error);
    document.getElementById("boton").addEventListener("click", iniciar_juego);
    var botones_radio = document.querySelectorAll('input[name="crear_o_unir"]');
    botones_radio.forEach(function(radio){
        radio.addEventListener("change", cambio_radio);
        radio.checked = false;
    })
    document.getElementById("campo_nombre").value = "";
    document.getElementById("campo_jug_o_id").value = "";
}
window.onload = al_cargar;