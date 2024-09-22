from Io import Io
class Io_websocket(Io):
    def __init__(self, creador = None):
        super().__init__()
        self.tipo = "SOCKET"
        self.creador = creador
        
    async def print(self, jugadores, mensaje):
        for jugador in jugadores:
            await jugador.conn.send("M"+mensaje)
    async def mandar_error(self, jugadores, error):
        for jugador in jugadores:
            try:
                await jugador.conn.send("E"+error)
            except Exception as e:
                print(f"Al mandar el mensaje de error a {jugador.nombre} ha ocurrido el error {e}. Ignorando...")
    async def anunciar_ronda(self, jugadores, num_cartas, pinta, carta_pinta):
        #await self.print(jugadores, f"Ronda con {num_cartas} vueltas, pinta{f"{" la" if carta_pinta.numero.value==10 else " el"} {str(carta_pinta)}" if carta_pinta is not None else f"n {pinta.name}"}")
        await self.print(jugadores, f"Ronda con {num_cartas} vueltas, pinta"+((" la " if carta_pinta.numero.value==10 else " el ")+ str(carta_pinta) if carta_pinta is not None else f"n {pinta.name}"))
        #print("El orden de los jugadores es: ",[jugador.nombre for jugador in jugadores],"\n")
        await self.print(jugadores, f"El orden de los jugadores es: {[jugador.nombre for jugador in jugadores]}\n")
    async def recibir_input(self, jugador):
        await jugador.conn.send("I")
        respuesta = await jugador.cola.get()
        return respuesta
    async def obtener_vueltas_esperadas(self, jugadores, num_cartas):
        await self.print(jugadores,f"{jugador.nombre}, tu mano es {jugador.str_mano()}")
        for i,jugador in enumerate(jugadores):
            await self.print([no_jugador for no_jugador in jugadores if no_jugador!=jugador], f"{jugador.nombre} está viendo cuántas pedir...")
            vueltas_esperadas = -1
            while vueltas_esperadas < 0 or vueltas_esperadas > num_cartas or (i == len(jugadores)-1 and sum([jugador.vueltas_ganadas_esperadas for jugador in jugadores]) + vueltas_esperadas == num_cartas):
                try:
                    await self.print([jugador],f"¿Cuántas vueltas esperas ganar, {jugador.nombre}? ")
                    vueltas_esperadas=int(await self.recibir_input(jugador))
                    if vueltas_esperadas < 0 or vueltas_esperadas > num_cartas:
                        await self.print([jugador],f"Por favor, introduce un número entre 0 y {num_cartas}")
                    elif i == len(jugadores)-1 and sum([jugador.vueltas_ganadas_esperadas for jugador in jugadores]) + vueltas_esperadas == num_cartas:
                        await self.print([jugador],f"No puedes elegir {vueltas_esperadas} vueltas porque eres postre, elige otra cosa")
                except ValueError:
                    await self.print([jugador],f"Por favor, introduce un número entre 0 y {num_cartas}")
                    vueltas_esperadas = -1
            jugador.vueltas_ganadas_esperadas = vueltas_esperadas
            await self.print([no_jugador for no_jugador in jugadores if no_jugador!=jugador], f"{jugador.nombre} ha pedido {jugador.vueltas_ganadas_esperadas}")
    async def obtener_carta_a_jugar(self, jugador, vuelta):
        await self.print(self.partida.jugadores, f"Vuelta: {vuelta}")
        await self.print(self.partida.jugadores, f"Mano: {jugador.str_mano()}")
        await self.print([no_jugador for no_jugador in self.partida.jugadores if no_jugador!=jugador], f"{jugador.nombre} está pensando...")
        cartas_jugables = jugador.obtener_cartas_jugables(vuelta)
        await self.print([jugador],f"Cartas jugables: "+str([f"{i}: {carta.str_reducido()}" for i,carta in enumerate(cartas_jugables,1)]))
        carta_a_jugar = -1
        while carta_a_jugar < 0 or carta_a_jugar >= len(cartas_jugables):
            try:
                await self.print([jugador], f"¿Qué carta quieres jugar, {jugador.nombre}? ")
                carta_a_jugar = int(await self.recibir_input(jugador))-1
                if carta_a_jugar < 0 or carta_a_jugar >= len(cartas_jugables):
                    await self.print([jugador],f"Por favor, introduce un número entre 1 y {len(cartas_jugables)}")
            except ValueError:
                print(f"Por favor, introduce un número entre 1 y {len(cartas_jugables)}")
                carta_a_jugar = -1
        return cartas_jugables[carta_a_jugar]
    async def mostrar_stats(self, jugadores):
        jugadores_ordenados = sorted(jugadores, key=lambda jugador: jugador.registro["puntos"], reverse=True)
        await self.print(jugadores, "-----------------------------")
        for jugador in jugadores_ordenados:
            #await self.print(jugadores, f"{jugador.nombre}: {len(jugador.vueltas)}/{jugador.vueltas_ganadas_esperadas}: ({"+" if jugador.registro["historial_variacion"][-1] >0 else ""}{jugador.registro["historial_variacion"][-1]}) => {jugador.registro["puntos"]}")
            await self.print(jugadores, f"{jugador.nombre}: {len(jugador.vueltas)}/{jugador.vueltas_ganadas_esperadas}: ("+("+" if jugador.registro["historial_variacion"][-1] >0 else "")+str(jugador.registro["historial_variacion"][-1])+") => "+str(jugador.registro["puntos"]))
        await self.print(jugadores, "-----------------------------")
    async def mostrar_fin_vuelta(self, vuelta):
        await self.print(self.partida.jugadores, str(vuelta))
        await self.print(self.partida.jugadores, f"Ahora {vuelta.ganador.nombre} tiene {len(vuelta.ganador.vueltas)}/{vuelta.ganador.vueltas_ganadas_esperadas} bazas\n")