from enum import Enum
class Palo(Enum):
    OROS = 1
    COPAS = 2
    ESPADAS = 3
    BASTOS = 4
class Numero(Enum):
    DOS = 2
    CUATRO = 4
    CINCO = 5
    SEIS = 6
    SIETE = 7
    SOTA = 10
    CABALLO = 11
    REY = 12
    TRES = 13
    AS = 14
class Carta():
    def __init__(self, numero, palo, jugador=None):
        self.numero = numero
        self.palo = palo
        self.jugador = jugador
    def __str__(self):
        return f"{self.numero.name} de {self.palo.name}"
    def __repr__(self):
        return self.__str__()
    def str_reducido(self):
        tabla_numeros = {Numero.DOS: "2", Numero.TRES: "3", Numero.CUATRO: "4", Numero.CINCO: "5", Numero.SEIS: "6", Numero.SIETE: "7", Numero.SOTA: "S", Numero.CABALLO: "C", Numero.REY: "R", Numero.AS: "A"}
        return f"{tabla_numeros[self.numero]}{self.palo.name[0]}"