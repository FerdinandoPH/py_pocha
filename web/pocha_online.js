var term = new Terminal({fontSize: 30});
var fitAddon = new FitAddon.FitAddon();
term.loadAddon(fitAddon);
term.open(document.getElementById('terminal'));
function alCargar(){
    console.log("Iniciando");
    var url_string = window.location.href;
    var url = new URL(url_string);
    var mensaje = url.searchParams.get("parametros");
    if (mensaje==null){
        alert("No se han introducido los parámetros correctamente");
        window.location.href = "index.html";
    }

    
    
    var input_activado = false;
    var input = "";
    var input_buffer = "";
    //let socket = new WebSocket("ws://casaperezholguin.ddns.net:20225");
    let socket = new WebSocket("ws://casaperezholguin.ddns.net:20225");
    socket.onopen = function(e) {
        console.log("Conexión establecida");
        socket.send(mensaje);
    };
    console.log("Hola???");
    socket.onerror=function (e){
        console.log("Error");
        console.log(e.data);
    }
    socket.onmessage = function(event) {
        console.log(`[message] Data received from server: ${event.data}`);
        var mensaje = event.data;
        if(mensaje[0]=="M"){
            newPrint(mensaje.substring(1));
        }
        else if (mensaje[0]=="I"){
            input_activado = true;
        }
        else if (mensaje[0] == "E"){
            console.log("Error: "+mensaje.substring(1));
            socket.close();
            window.location.href = "index.html?merror="+mensaje.substring(1);
        }
    };
    term.onData(function(data) {
        if (input_activado) {
          if (data === '\r') {
          newPrint('');
          input=input_buffer;
          input_buffer = "";
          console.log("Received user input is "+input)
          socket.send(input);
          input_activado = false;
          }
          else{
            if(data === '\u007F'){
              term.write('\b \b');
              input_buffer = input_buffer.slice(0, -1);
            }
            else{
            term.write(data);
            input_buffer += data;
            }
          }
        }

      });
    fitTerminal();
}
function newPrint(text){
    term.writeln(text);
    term.scrollToBottom();
  }
function fitTerminal(){
    fitAddon.fit();
  }
function alRefrescar(){
    fitTerminal();
  }
  window.onresize = alRefrescar;
  window.onload=alCargar;