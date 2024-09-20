import traceback
from Partida import Partida
def rotar_izquierda(lista):
    return lista[1:] + [lista[0]]
class Partida_online(Partida):
    def __init__(self, io, num_jugadores, j1, id):
        super().__init__(io, num_jugadores, id)
        self.jugadores = [j1]
        self.creador = j1
        self.esta_viva = True
        self.io.print([j1], f"El id de la partida es {self.id}")
    def añadir_jugador(self, jugador):
        if len(self.jugadores) < self.num_jugadores:
            self.jugadores.append(jugador)
            self.io.print(self.jugadores, f"Se ha unido {jugador.nombre}")
            if len(self.jugadores) == self.num_jugadores:
                self.io.print(self.jugadores, "Comienza la partida")
                self.jugar_partida()
        else:
            self.io.mandar_error([jugador], "NoUnir")
    def jugar_partida(self):
        try:
            super().jugar_partida()
        except Exception as e:
            self.io.mandar_error(self.jugadores, "Error en el servidor")
            print("Error causante")
            traceback.print_exc()
        self.esta_viva = False
