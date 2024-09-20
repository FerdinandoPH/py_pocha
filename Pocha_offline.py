from Partida_offline import Partida_offline
from Io_manual import Io_manual
def main():
    io = Io_manual()
    #partida = Partida([Jugador("Fer"), Jugador("Alberto"), Jugador("Carlos"), Jugador("Ana")])
    partida = Partida_offline(io)
    partida.jugar_partida()
if __name__ == "__main__":
    main()