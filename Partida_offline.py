from Jugador import Jugador
from Partida import Partida
def rotar_izquierda(lista):
    return lista[1:] + [lista[0]]
class Partida_offline(Partida):
    def __init__(self, io, num_jugadores=None, id=None):
        self.jugadores = [Jugador(nombre) for nombre in io.obtener_jugadores()]
        for jugador in self.jugadores:
            jugador.partida = self
        self.num_jugadores = num_jugadores
        super().__init__(io, num_jugadores, id)