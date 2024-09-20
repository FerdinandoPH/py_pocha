import socket,sys,time
try:
    SERVER = socket.gethostbyname("casaperezholguin.ddns.net")
except OSError:
    SERVER = "127.0.0.1"
#SERVER = "127.0.0.1"
PORT = 20225
def main():
    auto = False
    if len(sys.argv)>1:
        auto = True
        nombre = sys.argv[1]
        crear_o_unir = 1 if sys.argv[2] == "crear" else 2
        if crear_o_unir == 1:
            num_jugadores = int(sys.argv[3])
        else:
            id = int(sys.argv[3])
        time.sleep(int(sys.argv[4]))
    print("Bienvenido a la pocha online")
    if not auto:
        nombre = ""
    while not nombre:
        nombre = input("¿Cómo te llamas? ")
    if len(nombre)>18:
        nombre = nombre[:18]
    if not auto:
        crear_o_unir = 0
    while crear_o_unir not in range(1,3):
        try:
            crear_o_unir = int(input("¿Quieres crear una partida o unirte a una?\n1. Crear\n2. Unir\n"))
            if crear_o_unir not in range(1,3):
                print("Por favor, introduce 1 o 2")
        except ValueError:
            print("Por favor, introduce 1 o 2")
            crear_o_unir = 0
    if crear_o_unir == 1:
        if not auto:
            num_jugadores = 0
        while num_jugadores not in range(3,6):
            try:
                num_jugadores = int(input("¿Cuántos jugadores? "))
                if num_jugadores not in range(3,6):
                    print("Por favor, introduce un número entre 3 y 5")
            except ValueError:
                print("Por favor, introduce un número entre 3 y 5")
                num_jugadores = 0
    else:
        if not auto:
            id = 0
        while id not in range(1000,9999):
            try:
                id = int(input("Introduce el id de la partida a la que quieres unirte (4 dígitos): "))
                if id not in range(1000,9999):
                    print("Por favor, introduce un número de 4 dígitos")
            except ValueError:
                print("Por favor, introduce un número de 4 dígitos")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER, PORT))
        if crear_o_unir == 1:
            s.send(f"N{num_jugadores}{nombre}".encode("UTF-8"))
        else:
            s.send(f"U{id}{nombre}".encode("UTF-8"))
        continuar = True
        while continuar:
            data = s.recv(4096).decode("UTF-8")
            if data:
                if data[0] == "E":
                    print(f"ERROR: {data[1:]}")
                    continuar = False
                elif data[0] == "M":
                    print(data[1:])
                elif data[0] == "I":
                    respuesta = input("Respuesta: ")
                    if len(respuesta)>18:
                        respuesta = respuesta[:18]
                    try:
                        s.send(respuesta.encode("UTF-8"))
                    except Exception as e:
                        print(f"Error al enviar la respuesta: {e}")
                        continuar = False
        s.close()
if __name__ == "__main__":
    main()