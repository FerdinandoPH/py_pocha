from Carta import Carta, Palo, Numero
from Vuelta import Vuelta
import random
def rotar_derecha(lista):
    return [lista[-1]] + lista[:-1]
class Partida():
    def __init__(self, jugadores):
        self.jugadores = jugadores
        for jugador in self.jugadores:
            jugador.partida = self
        random.shuffle(self.jugadores)
        self.ronda_actual = 0
        self.pintas_en_10 = ["OROS", "COPAS", "ESPADAS", "BASTOS", "OROS", "COPAS", "ESPADAS", "BASTOS"]
        self.pinta_actual = None
        self.num_cartas_actual = 0
        self.rondas = [1,2,3,4,5,6,7,8,9,10,10,10,10,10,10,10,10,9,8,7,6,5,4,3,2,1]
        self.cartas = []
        for palo in Palo:
            for numero in Numero:
                self.cartas.append(Carta(numero, palo))
    def preparar_ronda(self):
        if self.ronda_actual == len(self.rondas):
            return False
        for jugador in self.jugadores:
            jugador.resetear()
        self.num_cartas_actual = self.rondas[self.ronda_actual]
        random.shuffle(self.cartas)
        for i in range(self.num_cartas_actual):
            for jugador in self.jugadores:
                jugador.recibir_carta(self.cartas.pop())
        if self.num_cartas_actual<10:
            self.pinta_actual = self.cartas.pop().palo
        else:
            self.pinta_actual = self.pintas_en_10[self.ronda_actual-10]
        return True
    def finalizar_ronda(self):
        for jugador in self.jugadores:
            jugador.actualizar_puntos(self.num_cartas_actual)
        self.ronda_actual += 1
        self.jugadores = rotar_derecha(self.jugadores)