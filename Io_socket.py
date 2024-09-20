from Io import Io
import time
class Io_socket(Io):
    def __init__(self, creador = None):
        super().__init__()
        self.tipo = "SOCKET"
        self.creador = creador
        
    def print(self, jugadores, mensaje):
        time.sleep(0.1)
        for jugador in jugadores:
            jugador.conn.send(("M"+mensaje).encode("UTF-8"))
    def mandar_error(self, jugadores, error):
        for jugador in jugadores:
            try:
                jugador.conn.send(("E"+error).encode("UTF-8"))
            except Exception as e:
                print(f"Al mandar el mensaje de error a {jugador.nombre} ha ocurrido el error {e}. Ignorando...")
    def anunciar_ronda(self, jugadores, num_cartas, pinta, carta_pinta):
        #self.print(jugadores, f"Ronda con {num_cartas} vueltas, pinta{f"{" la" if carta_pinta.numero.value==10 else " el"} {str(carta_pinta)}" if carta_pinta is not None else f"n {pinta.name}"}")
        self.print(jugadores, f"Ronda con {num_cartas} vueltas, pinta"+((" la " if carta_pinta.numero.value==10 else " el")+ str(carta_pinta) if carta_pinta is not None else f"n {pinta.name}"))
        #print("El orden de los jugadores es: ",[jugador.nombre for jugador in jugadores],"\n")
        self.print(jugadores, f"El orden de los jugadores es: {[jugador.nombre for jugador in jugadores]}\n")
    def recibir_input(self, jugador):
        jugador.conn.send("I".encode("UTF-8"))
        return jugador.conn.recv(1024).decode("UTF-8")
    def obtener_vueltas_esperadas(self, jugadores, num_cartas):
        for i,jugador in enumerate(jugadores):
            self.print([no_jugador for no_jugador in jugadores if no_jugador!=jugador], f"{jugador.nombre} está viendo cuántas pedir...")
            self.print([jugador],f"{jugador.nombre}, Tu mano es {jugador.str_mano()}")
            vueltas_esperadas = -1
            while vueltas_esperadas < 0 or vueltas_esperadas > num_cartas or (i == len(jugadores)-1 and sum([jugador.vueltas_ganadas_esperadas for jugador in jugadores]) + vueltas_esperadas == num_cartas):
                try:
                    self.print([jugador],f"¿Cuántas vueltas esperas ganar, {jugador.nombre}? ")
                    vueltas_esperadas=int(self.recibir_input(jugador))
                    if vueltas_esperadas < 0 or vueltas_esperadas > num_cartas:
                        self.print([jugador],f"Por favor, introduce un número entre 0 y {num_cartas}")
                    elif i == len(jugadores)-1 and sum([jugador.vueltas_ganadas_esperadas for jugador in jugadores]) + vueltas_esperadas == num_cartas:
                        self.print([jugador],f"No puedes elegir {vueltas_esperadas} vueltas porque eres postre, elige otra cosa")
                except ValueError:
                    self.print([jugador],f"Por favor, introduce un número entre 0 y {num_cartas}")
                    vueltas_esperadas = -1
            jugador.vueltas_ganadas_esperadas = vueltas_esperadas
            self.print([no_jugador for no_jugador in jugadores if no_jugador!=jugador], f"{jugador.nombre} ha pedido {jugador.vueltas_ganadas_esperadas}")
    def obtener_carta_a_jugar(self, jugador, vuelta):
        self.print(self.partida.jugadores, f"Vuelta: {vuelta}")
        self.print([no_jugador for no_jugador in self.partida.jugadores if no_jugador!=jugador], f"{jugador.nombre} está pensando...")
        cartas_jugables = jugador.obtener_cartas_jugables(vuelta)
        self.print([jugador], f"Mano: {jugador.str_mano()}")
        self.print([jugador],f"Cartas jugables: "+str([f"{i}: {carta.str_reducido()}" for i,carta in enumerate(cartas_jugables,1)]))
        carta_a_jugar = -1
        while carta_a_jugar < 0 or carta_a_jugar >= len(cartas_jugables):
            try:
                self.print([jugador], f"¿Qué carta quieres jugar, {jugador.nombre}? ")
                carta_a_jugar = int(self.recibir_input(jugador))-1
                if carta_a_jugar < 0 or carta_a_jugar >= len(cartas_jugables):
                    self.print([jugador],f"Por favor, introduce un número entre 1 y {len(cartas_jugables)}")
            except ValueError:
                print(f"Por favor, introduce un número entre 1 y {len(cartas_jugables)}")
                carta_a_jugar = -1
        return cartas_jugables[carta_a_jugar]
    def mostrar_stats(self, jugadores):
        jugadores_ordenados = sorted(jugadores, key=lambda jugador: jugador.registro["puntos"], reverse=True)
        self.print(jugadores, "-----------------------------")
        for jugador in jugadores_ordenados:
            #self.print(jugadores, f"{jugador.nombre}: {len(jugador.vueltas)}/{jugador.vueltas_ganadas_esperadas}: ({"+" if jugador.registro["historial_variacion"][-1] >0 else ""}{jugador.registro["historial_variacion"][-1]}) => {jugador.registro["puntos"]}")
            self.print(jugadores, f"{jugador.nombre}: {len(jugador.vueltas)}/{jugador.vueltas_ganadas_esperadas}: ("+("+" if jugador.registro["historial_variacion"][-1] >0 else "")+f"{jugador.registro["historial_variacion"][-1]}) => {jugador.registro["puntos"]}")
        self.print(jugadores, "-----------------------------")
    def mostrar_fin_vuelta(self, vuelta):
        self.print(self.partida.jugadores, str(vuelta))
        self.print(self.partida.jugadores, f"Ahora {vuelta.ganador.nombre} tiene {len(vuelta.ganador.vueltas)}/{vuelta.ganador.vueltas_ganadas_esperadas} bazas\n")
    def anunciar_ronda(self, jugadores, num_cartas, pinta, carta_pinta):
        self.print(jugadores, f"Ronda con {num_cartas} vueltas, pinta{f"{" la" if carta_pinta.numero.value==10 else " el"} {str(carta_pinta)}" if carta_pinta is not None else f"n {pinta.name}"}")
        self.print(jugadores, f"El orden de los jugadores es: {[jugador.nombre for jugador in jugadores]}\n")