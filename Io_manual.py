class Io:
    def __init__(self):
        self.tipo = "INPUT"
    def obtener_vueltas_esperadas(self,jugadores,num_cartas):
        for i,jugador in enumerate(jugadores):
            #input("Dale cuando estés solo")
            print(f"Tu mano es {jugador.str_mano()}")
                # vueltas_esperadas = int(input(f"¿Cuántas vueltas esperas ganar, {jugador.nombre}? "))
                # while vueltas_esperadas < 0 or vueltas_esperadas > num_cartas or (i == len(jugadores)-1 and sum([jugador.vueltas_ganadas_esperadas for jugador in jugadores]) + vueltas_esperadas == num_cartas):
                #     vueltas_esperadas = int(input(f"Por favor, introduce un número entre 0 y {num_cartas}: " if vueltas_esperadas < 0 or vueltas_esperadas > num_cartas else f"No puedes elegir {vueltas_esperadas} vueltas porque eres postre, elige otra cosa: "))
            vueltas_esperadas = -1
            while vueltas_esperadas < 0 or vueltas_esperadas > num_cartas or (i == len(jugadores)-1 and sum([jugador.vueltas_ganadas_esperadas for jugador in jugadores]) + vueltas_esperadas == num_cartas):
                try:
                    vueltas_esperadas = int(input(f"¿Cuántas vueltas esperas ganar, {jugador.nombre}? "))
                    if vueltas_esperadas < 0 or vueltas_esperadas > num_cartas:
                        print(f"Por favor, introduce un número entre 0 y {num_cartas}")
                    elif i == len(jugadores)-1 and sum([jugador.vueltas_ganadas_esperadas for jugador in jugadores]) + vueltas_esperadas == num_cartas:
                        print(f"No puedes elegir {vueltas_esperadas} vueltas porque eres postre, elige otra cosa")
                except ValueError:
                    print(f"Por favor, introduce un número entre 0 y {num_cartas}")
            jugador.vueltas_ganadas_esperadas = vueltas_esperadas
    def obtener_carta_a_jugar(self,jugador,vuelta):
        print("Vuelta: ",vuelta)
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
                carta_a_jugar = int(input(f"¿Qué carta quieres jugar, {jugador.nombre}? ")) - 1
                if carta_a_jugar < 0 or carta_a_jugar >= len(cartas_jugables):
                    print(f"Por favor, introduce un número entre 1 y {len(cartas_jugables)}")
            except ValueError:
                print(f"Por favor, introduce un número entre 1 y {len(cartas_jugables)}")
        return cartas_jugables[carta_a_jugar]
    def mostrar_stats(self, jugadores):
        jugadores_ordenados = sorted(jugadores, key=lambda jugador: jugador.registro["puntos"], reverse=True)
        for jugador in jugadores_ordenados:
            print(f"{jugador.nombre}: {len(jugador.vueltas)}/{jugador.vueltas_ganadas_esperadas}: ({"+" if jugador.registro["historial_variacion"][-1] >0 else ""}{jugador.registro["historial_variacion"][-1]}) => {jugador.registro["puntos"]}")
    def mostrar_vuelta(self, vuelta):
        print(vuelta)
        print(f"Ahora {vuelta.ganador.nombre} tiene {len(vuelta.ganador.vueltas)}/{vuelta.ganador.vueltas_ganadas_esperadas} bazas")
    def anunciar_ronda(self, num_cartas, pinta):
        print(f"Ronda con {num_cartas} vueltas, pintan {pinta.name}")