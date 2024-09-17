from Carta import Carta, Palo, Numero
class Jugador():
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.vueltas = []
        self.vueltas_ganadas_esperadas = 0
        self.registro = Registro_puntos({"historial_puntos":[],"historial_variacion":[]})
    def recibir_carta(self, carta):
        carta.jugador = self
        self.mano.append(carta)
    def obtener_cartas_jugables(self, vuelta):
        if vuelta.palo_inicial is None:
            return self.mano
        cartas_jugables = []
        if any(vuelta.supera_carta_actual(carta) for carta in self.mano):
            for carta in self.mano:
                if vuelta.supera_carta_actual(carta):
                    cartas_jugables.append(carta)
        elif any(carta.palo == vuelta.palo_inicial for carta in self.mano):
            for carta in self.mano:
                if carta.palo == vuelta.palo_inicial:
                    cartas_jugables.append(carta)
        else:
            return self.mano
        return cartas_jugables
    def jugar_carta(self, carta, vuelta):
        if carta in self.obtener_cartas_jugables(vuelta):
            self.mano.remove(carta)
            vuelta.jugar_carta(carta)
        else:
            raise ValueError("¡Renuncio! ¿Cómo ha pasado esto? ")
    def actualizar_puntos(self, num_cartas):
        puntos_de_ronda = 10 + self.vueltas_ganadas_esperadas*5*(2 if num_cartas == self.vueltas_ganadas_esperadas and num_cartas>4 else 1) if self.vueltas_ganadas_esperadas == len(self.vueltas) else -5*abs(self.vueltas_ganadas_esperadas - len(self.vueltas))
        self.registro["historial_variacion"].append(puntos_de_ronda)
        self.registro["historial_puntos"].append(self.registro["puntos"] + puntos_de_ronda)
    def __str__(self):
        return f"{self.nombre} ({self.registro} puntos) : {self.str_mano()}"
    def __repr__(self):
        return self.__str__()
    def str_mano(self):
        return ", ".join([carta.str_reducido() for carta in self.mano])
    def resetear(self):
        self.mano = []
        self.vueltas = []
        self.vueltas_ganadas_esperadas = 0
        self.registro = Registro_puntos({"historial_puntos":[],"historial_variacion":[]})
class Registro_puntos(dict):
    def __getitem__(self, key):
        if key == "puntos":
            try:
                return self["historial_puntos"][-1]
            except IndexError:
                return 0
        return super().__getitem__(key)
    def keys(self):
        llaves = super().keys()
        llaves.append("puntos")
        return llaves