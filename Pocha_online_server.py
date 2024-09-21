from  Partida_online import Partida_online
from Jugador_online import Jugador_online
from Io_socket import Io_socket
import socket, threading
#IP = "127.0.0.1"
IP = "192.168.1.118"
PORT = 20225

def obtener_nuevo_id(partidas):
    id = 1000
    while any(partida.id == id for partida in partidas):
        id +=1
    return id
def limpieza_partidas(partidas):
    partidas_limpias=[]
    for partida in partidas:
        if not partida.esta_empezada:
            try:
                partida.creador.conn.send("C".encode("UTF-8"))
            except Exception as e:
                partida.esta_viva = False
        if partida.esta_viva:
            partidas_limpias.append(partida)
    return partidas_limpias
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        partidas = []
        s.bind((IP, PORT))
        s.listen()
        print(f"Escuchando  en {IP}:{PORT}")
        while True:
            conn, addr = s.accept()
            print("Se ha unido ", addr)
            data = None
            partidas = limpieza_partidas(partidas)
            while not data:
                data = conn.recv(1024).decode("UTF-8")
                if data:
                    if data[0] == "N":
                        partida = Partida_online(Io_socket(), int(data[1]), Jugador_online(data[2:], conn, addr), obtener_nuevo_id(partidas))
                        partida.io.partida = partida
                        partidas.append(partida)
                    elif data[0] == "U":
                        try:
                            partida = next(partida for partida in partidas if partida.id == int(data[1:5]))
                        except StopIteration:
                            conn.send("EPartida no encontrada".encode("UTF-8"))
                        else:
                            hilo_jugador = threading.Thread(target=partida.añadir_jugador, args=(Jugador_online(data[5:], conn, addr),))
                            hilo_jugador.daemon = True
                            hilo_jugador.start()
if __name__ == "__main__":
    main()