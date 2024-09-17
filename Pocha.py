from Partida import Partida
from Carta import Carta, Palo, Numero
from Jugador import Jugador
from Vuelta import Vuelta
from Io_manual import Io
def main():
    jugadores = [Jugador("Fer"), Jugador("Alberto"), Jugador("Carlos"), Jugador("Ana")]
    partida = Partida(jugadores)
    io = Io()
    while partida.preparar_ronda():
        io.anunciar_ronda(partida.num_cartas_actual, partida.pinta_actual)
        io.obtener_vueltas_esperadas(partida.jugadores,partida.num_cartas_actual)
        for i in range(partida.num_cartas_actual):
            vuelta = Vuelta(partida.pinta_actual)
            for jugador in partida.jugadores:
                carta = io.obtener_carta_a_jugar(jugador, vuelta)
                jugador.jugar_carta(carta, vuelta)
            vuelta.adherirse_a_ganador()
            io.mostrar_vuelta(vuelta)
        partida.finalizar_ronda()
        io.mostrar_stats(partida.jugadores)
if __name__ == "__main__":
    main()