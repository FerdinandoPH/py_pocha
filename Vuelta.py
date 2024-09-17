from Carta import Carta, Palo, Numero
class Vuelta:
    def __init__(self, pinta):
        self.pinta = pinta
        self.palo_inicial = None
        self.cartas = []
        self.carta_ganadora = None
        self.ganador = None
    def jugar_carta(self, carta):
        if self.palo_inicial is None:
            self.palo_inicial = carta.palo
        self.cartas.append(carta)
        if self.supera_carta_actual(carta):
            self.carta_ganadora = carta
    def supera_carta_actual(self, carta):
        if self.carta_ganadora is None:
            return True
        elif self.carta_ganadora.palo == self.pinta:
            if carta.palo == self.pinta and carta.numero.value > self.carta_ganadora.numero.value:
                return True
        elif carta.palo == self.pinta:
            return True
        elif carta.palo == self.palo_inicial and carta.numero.value > self.carta_ganadora.numero.value:
            return True
        return False
    def adherirse_a_ganador(self):
        self.carta_ganadora.jugador.vueltas.append(self)
        self.ganador = self.carta_ganadora.jugador
        return self.ganador
    def __str__(self):
        cadena = "["
        for i, carta in enumerate(self.cartas):
            cadena += f"{carta.str_reducido()} ({carta.jugador.nombre})"
            if carta == self.carta_ganadora:
                cadena += "*"
            if i < len(self.cartas) - 1:
                cadena += ", "
        cadena += "]"
        return cadena
    def __repr__(self):
        return self.__str__()
