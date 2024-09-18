from Partida import Partida
from Jugador import Jugador
from Vuelta import Vuelta
from Io_manual import Io
def main():
    io = Io()
    #partida = Partida([Jugador("Fer"), Jugador("Alberto"), Jugador("Carlos"), Jugador("Ana")])
    partida = Partida([Jugador(nombre) for nombre in io.obtener_jugadores()])
    while partida.preparar_ronda():
        io.anunciar_ronda(partida.num_cartas_actual, partida.pinta_actual, partida.carta_pinta_actual)
        for jugador in partida.jugadores:
            jugador.ordenar_mano(partida.pinta_actual)
        io.obtener_vueltas_esperadas(partida.jugadores,partida.num_cartas_actual)
        for i in range(partida.num_cartas_actual):
            vuelta = Vuelta(partida.pinta_actual, partida.carta_pinta_actual)
            for i in range(len(partida.jugadores)):
                jugador = partida.jugadores[(partida.indice_inicio_vuelta + i)%len(partida.jugadores)]
                carta = io.obtener_carta_a_jugar(jugador, vuelta)
                jugador.jugar_carta(carta, vuelta)
            partida.indice_inicio_vuelta = partida.jugadores.index(vuelta.adherirse_a_ganador())
            io.mostrar_fin_vuelta(vuelta)
        partida.finalizar_ronda()
        io.mostrar_stats(partida.jugadores)
if __name__ == "__main__":
    main()