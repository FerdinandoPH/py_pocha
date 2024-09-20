from Jugador import Jugador, Registro_puntos
class Jugador_online(Jugador):
    def __init__(self, nombre, conn, addr):
        self.conn = conn
        self.addr = addr
        super().__init__(nombre)