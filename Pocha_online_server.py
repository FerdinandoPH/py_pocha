from  Partida_online import Partida_online
from Jugador_online import Jugador_online
from Io_websocket import Io_websocket
import websockets, asyncio, threading, traceback
#SERVER = "localhost"
SERVER = "0.0.0.0"
PORT = 20225
partidas= []
partidas_lock = asyncio.Lock()
async def obtener_nuevo_id(partidas, partidas_lock):
    id = 1000
    async with partidas_lock:
        while any(partida.id == id for partida in partidas):
            id +=1
        return id
async def limpieza_partidas(partidas, partidas_lock):
    partidas_limpias=[]
    async with partidas_lock:
        for partida in partidas:
            if not partida.esta_empezada:
                try:
                    await partida.creador.conn.send("C")
                except Exception as e:
                    partida.esta_viva = False
            if partida.esta_viva:
                partidas_limpias.append(partida)
        return partidas_limpias
async def nueva_conn(conn, path):
    try:
        global partidas, partidas_lock
        cola_mensajes = asyncio.Queue()
        print("Se ha unido ", conn.remote_address)
        datos = None
        primera_vez = True
        partidas = await limpieza_partidas(partidas, partidas_lock)
        seguir = True
        while seguir:
            datos = await conn.recv()
            if datos:
                if primera_vez:
                    if datos[0] == "N":
                        
                        partida = Partida_online(Io_websocket(), int(datos[1]), Jugador_online(datos[2:], conn, conn.remote_address, cola_mensajes), await obtener_nuevo_id(partidas, partidas_lock))
                        partida.io.partida = partida
                        await partida.creador.conn.send(f"MEl id de la partida es {partida.id}")
                        async with partidas_lock:
                            partidas.append(partida)
                    elif datos[0] == "U":
                        try:
                            async with partidas_lock:
                                partida = next(partida for partida in partidas if partida.id == int(datos[1:5]))
                        except StopIteration:
                            await conn.send("EPartida no encontrada")
                            seguir = False
                            break
                        else:
                            asyncio.create_task(partida.añadir_jugador(Jugador_online(datos[5:], conn, conn.remote_address, cola_mensajes)))
                    primera_vez = False
                else:
                    cola_mensajes.put_nowait(datos)
        await conn.close()
    except Exception as e:
        if type(e)!=websockets.exceptions.ConnectionClosedOK:
            traceback.print_exc()
        partida.esta_viva = False
        print("Manejando error...")
        for jugador in partida.jugadores:
            try:
                await jugador.conn.send("EError en el servidor")
            except Exception as e:
                pass
        await conn.close()

async def main():
    print("Iniciando servidor...")
    async with websockets.serve(nueva_conn, SERVER, PORT): #type: ignore
        await asyncio.Future()
if __name__ == "__main__":
    asyncio.run(main())