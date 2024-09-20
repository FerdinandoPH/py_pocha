from abc import ABC, abstractmethod
class Io:
    def __init__(self):
        self.tipo = None
        self.partida = None
    @abstractmethod
    def obtener_jugadores(self):
        pass
    @abstractmethod
    def obtener_vueltas_esperadas(self,jugadores,num_cartas):
        pass
    @abstractmethod
    def obtener_carta_a_jugar(self,jugador,vuelta):
        pass
    @abstractmethod
    def mostrar_stats(self, jugadores):
        pass
    @abstractmethod
    def mostrar_fin_vuelta(self, vuelta):
        pass
    @abstractmethod
    def anunciar_ronda(self, jugadores, num_cartas, pinta, carta_pinta):
        pass
