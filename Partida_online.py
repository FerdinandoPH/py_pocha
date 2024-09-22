import traceback, random
from Partida import Partida
from Vuelta import Vuelta
def rotar_izquierda(lista):
    return lista[1:] + [lista[0]]
class Partida_online(Partida):
    def __init__(self, io, num_jugadores, j1, id):
        super().__init__(io, num_jugadores, id)
        self.jugadores = [j1]
        self.creador = j1
        self.esta_viva = True
        self.esta_empezada = False
    async def añadir_jugador(self, jugador):
        if len(self.jugadores) < self.num_jugadores:
            self.jugadores.append(jugador)
            await self.io.print(self.jugadores, f"Se ha unido {jugador.nombre}")
            if len(self.jugadores) == self.num_jugadores:
                await self.io.print(self.jugadores, "Comienza la partida")
                await self.jugar_partida()
        else:
            await self.io.mandar_error([jugador], "NoUnir")
    async def jugar_partida(self):
        self.esta_empezada = True
        try:
            random.shuffle(self.jugadores)
            while self.preparar_ronda():
                for jugador in self.jugadores:
                    jugador.ordenar_mano(self.pinta_actual)
                await self.io.anunciar_ronda(self.jugadores, self.num_cartas_actual, self.pinta_actual, self.carta_pinta_actual)
                await self.io.obtener_vueltas_esperadas(self.jugadores,self.num_cartas_actual)
                for i in range(self.num_cartas_actual):
                    vuelta = Vuelta(self.pinta_actual, self.carta_pinta_actual)
                    for i in range(len(self.jugadores)):
                        jugador = self.jugadores[(self.indice_inicio_vuelta + i)%len(self.jugadores)]
                        carta = await self.io.obtener_carta_a_jugar(jugador, vuelta)
                        jugador.jugar_carta(carta, vuelta)
                    self.indice_inicio_vuelta = self.jugadores.index(vuelta.adherirse_a_ganador())
                    await self.io.mostrar_fin_vuelta(vuelta)
                self.finalizar_ronda()
                await self.io.mostrar_stats(self.jugadores)
        except Exception as e:
            await self.io.mandar_error(self.jugadores, "Error en el servidor")
            print("Error causante")
            traceback.print_exc()
        self.esta_viva = False
