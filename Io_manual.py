import sys
from Io import Io
class Io_manual(Io):
    def __init__(self):
        self.tipo = "INPUT"
    def obtener_vueltas_esperadas(self,jugadores,num_cartas):
        for i,jugador in enumerate(jugadores):
            #input("Dale cuando estés solo")
            print(f"{jugador.nombre}, Tu mano es {jugador.str_mano()}")
                # vueltas_esperadas = int(input(f"¿Cuántas vueltas esperas ganar, {jugador.nombre}? "))
                # while vueltas_esperadas < 0 or vueltas_esperadas > num_cartas or (i == len(jugadores)-1 and sum([jugador.vueltas_ganadas_esperadas for jugador in jugadores]) + vueltas_esperadas == num_cartas):
                #     vueltas_esperadas = int(input(f"Por favor, introduce un número entre 0 y {num_cartas}: " if vueltas_esperadas < 0 or vueltas_esperadas > num_cartas else f"No puedes elegir {vueltas_esperadas} vueltas porque eres postre, elige otra cosa: "))
            vueltas_esperadas = -1
            while vueltas_esperadas < 0 or vueltas_esperadas > num_cartas or (i == len(jugadores)-1 and sum([jugador.vueltas_ganadas_esperadas for jugador in jugadores]) + vueltas_esperadas == num_cartas):
                try:
                    vueltas_esperadas = input(f"¿Cuántas vueltas esperas ganar, {jugador.nombre}? ")
                    vueltas_esperadas = int(vueltas_esperadas)
                    if vueltas_esperadas < 0 or vueltas_esperadas > num_cartas:
                        print(f"Por favor, introduce un número entre 0 y {num_cartas}")
                    elif i == len(jugadores)-1 and sum([jugador.vueltas_ganadas_esperadas for jugador in jugadores]) + vueltas_esperadas == num_cartas:
                        print(f"No puedes elegir {vueltas_esperadas} vueltas porque eres postre, elige otra cosa")
                except ValueError:
                    if not self.comando(vueltas_esperadas,jugador):
                        print(f"Por favor, introduce un número entre 0 y {num_cartas}")
                    vueltas_esperadas = -1
            jugador.vueltas_ganadas_esperadas = vueltas_esperadas
    def obtener_carta_a_jugar(self,jugador,vuelta):
        print("Vuelta: ",vuelta)
        print(f"Turno de {jugador.nombre}")
        
        cartas_jugables = jugador.obtener_cartas_jugables(vuelta)
        print("Bazas: ",len(jugador.vueltas),"/",jugador.vueltas_ganadas_esperadas)
        print("Mano: ",jugador.str_mano())
        print("Cartas jugables: ",[f"{i}: {carta.str_reducido()}" for i,carta in enumerate(cartas_jugables,1)])
        # if len(cartas_jugables) == 1:
        #     carta_a_jugar = 0
        #     print(f"Jugando {cartas_jugables[carta_a_jugar].str_reducido()} de forma obligada")
        # else:
        carta_a_jugar = -1
        while carta_a_jugar < 0 or carta_a_jugar >= len(cartas_jugables):
            try:
                carta_a_jugar = input(f"¿Qué carta quieres jugar, {jugador.nombre}? ")
                carta_a_jugar = int(carta_a_jugar) -1
                if carta_a_jugar < 0 or carta_a_jugar >= len(cartas_jugables):
                    print(f"Por favor, introduce un número entre 1 y {len(cartas_jugables)}")
            except ValueError:
                if not self.comando(carta_a_jugar, jugador):
                    print(f"Por favor, introduce un número entre 1 y {len(cartas_jugables)}")
                carta_a_jugar = -1
        print()
        return cartas_jugables[carta_a_jugar]
    def mostrar_stats(self, jugadores):
        jugadores_ordenados = sorted(jugadores, key=lambda jugador: jugador.registro["puntos"], reverse=True)
        print("-----------------------------")
        for jugador in jugadores_ordenados:
            print(f"{jugador.nombre}: {len(jugador.vueltas)}/{jugador.vueltas_ganadas_esperadas}: ({"+" if jugador.registro["historial_variacion"][-1] >0 else ""}{jugador.registro["historial_variacion"][-1]}) => {jugador.registro["puntos"]}")
        print("-----------------------------")
    def mostrar_fin_vuelta(self, vuelta):
        print(vuelta)
        print(f"Ahora {vuelta.ganador.nombre} tiene {len(vuelta.ganador.vueltas)}/{vuelta.ganador.vueltas_ganadas_esperadas} bazas\n")
    def anunciar_ronda(self, jugadores, num_cartas, pinta, carta_pinta):
        print(f"Ronda con {num_cartas} vueltas, pinta{f"{" la" if carta_pinta.numero.value==10 else " el"} {str(carta_pinta)}" if carta_pinta is not None else f"n {pinta.name}"}")
        print("El orden de los jugadores es: ",[jugador.nombre for jugador in jugadores],"\n")
    def comando(self, comando, jugador):
        if comando=="v":
            print(jugador.str_mano(False))
            return True
        elif comando=="q":
            print("Saliendo...")
            sys.exit(0)
        return False
    def obtener_jugadores(self):
        num_jug = 0
        while num_jug not in range(3,6):
            try:
                num_jug = input("¿Cuántos jugadores? ")
                num_jug = int(num_jug)
                if num_jug not in range(3,6):
                    print("Por favor, introduce un número entre 3 y 5")
            except ValueError:
                print("Por favor, introduce un número entre 3 y 5")
                num_jug = 0
        jugadores = []
        for i in range(num_jug):
            nombre = input(f"Nombre del jugador {i+1}: ")
            jugadores.append(nombre)
        print("Jugadores: ",[nombre for nombre in jugadores])
        print("¡Que empiece la partida!\n")
        return jugadores
