from Jugador import Jugador
class Jugador_online(Jugador):
    def __init__(self, nombre, conn, addr, cola):
        self.conn = conn
        self.addr = addr
        self.cola = cola
        super().__init__(nombre)