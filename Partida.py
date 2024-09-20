from Carta import Carta, Palo, Numero
import random
from Vuelta import Vuelta
def rotar_izquierda(lista):
    return lista[1:] + [lista[0]]
class Partida:
    def __init__(self, io, num_jugadores=None, id=None):
        self.num_jugadores = num_jugadores
        io.partida = self
        self.id = id
        self.indice_inicio_vuelta = 0
        self.ronda_actual = 0
        #self.pintas_en_10 = ["OROS", "COPAS", "ESPADAS", "BASTOS", "OROS", "COPAS", "ESPADAS", "BASTOS"]
        self.pintas_en_max = [Palo.OROS, Palo.COPAS, Palo.ESPADAS, Palo.BASTOS, Palo.OROS, Palo.COPAS, Palo.ESPADAS, Palo.BASTOS]
        self.indice_max = 0
        self.pinta_actual = None
        self.carta_pinta_actual = None
        self.num_cartas_actual = 0
        self.io = io
        self.rondas = [1,2,3,4,5,6,7,8,9,10,10,10,10,10,10,10,10,9,8,7,6,5,4,3,2,1] if self.num_jugadores==4 else [1,2,3,4,5,6,7,8,8,8,8,8,8,8,8,7,6,5,4,3,2,1] if self.num_jugadores else [1,2,3,4,5,6,7,8,9,10,11,12,12,12,12,12,12,12,12,11,10,9,8,7,6,5,4,3,2,1]
        self.cartas = []
        for palo in Palo:
            for numero in Numero:
                self.cartas.append(Carta(numero, palo))
        self.cartas_backup = self.cartas.copy()
    def preparar_ronda(self):
        self.carta_pinta_actual = None
        self.cartas = self.cartas_backup.copy()
        self.indice_inicio_vuelta = 0
        if self.ronda_actual == len(self.rondas):
            return False
        for jugador in self.jugadores:
            jugador.resetear()
        self.num_cartas_actual = self.rondas[self.ronda_actual]
        random.shuffle(self.cartas)
        for i in range(self.num_cartas_actual):
            for jugador in self.jugadores:
                jugador.recibir_carta(self.cartas.pop())
        if self.num_cartas_actual<max(self.rondas):
            self.carta_pinta_actual = self.cartas.pop()
            self.pinta_actual = self.carta_pinta_actual.palo
        else:
            self.pinta_actual = self.pintas_en_max[self.ronda_actual-10]
        return True
    def jugar_partida(self):
        random.shuffle(self.jugadores)
        while self.preparar_ronda():
            for jugador in self.jugadores:
                jugador.ordenar_mano(self.pinta_actual)
            self.io.anunciar_ronda(self.jugadores, self.num_cartas_actual, self.pinta_actual, self.carta_pinta_actual)
            self.io.obtener_vueltas_esperadas(self.jugadores,self.num_cartas_actual)
            for i in range(self.num_cartas_actual):
                vuelta = Vuelta(self.pinta_actual, self.carta_pinta_actual)
                for i in range(len(self.jugadores)):
                    jugador = self.jugadores[(self.indice_inicio_vuelta + i)%len(self.jugadores)]
                    carta = self.io.obtener_carta_a_jugar(jugador, vuelta)
                    jugador.jugar_carta(carta, vuelta)
                self.indice_inicio_vuelta = self.jugadores.index(vuelta.adherirse_a_ganador())
                self.io.mostrar_fin_vuelta(vuelta)
            self.finalizar_ronda()
            self.io.mostrar_stats(self.jugadores)
    def finalizar_ronda(self):
        for jugador in self.jugadores:
            jugador.actualizar_puntos(self.num_cartas_actual)
        self.ronda_actual += 1
        self.jugadores = rotar_izquierda(self.jugadores)