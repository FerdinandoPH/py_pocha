import subprocess, sys
if len(sys.argv)>1:
    num_jugadores = int(sys.argv[1])
else:
    num_jugadores = 4
tabla_llamadas=[
subprocess.Popen(["python", "Pocha_online_client.py", "Fernando", "crear", "4", "0"], creationflags=subprocess.CREATE_NEW_CONSOLE),
subprocess.Popen(["python", "Pocha_online_client.py", "Alberto", "unir", "1000", "1"], creationflags=subprocess.CREATE_NEW_CONSOLE),
subprocess.Popen(["python", "Pocha_online_client.py", "Carlos", "unir", "1000", "2"], creationflags=subprocess.CREATE_NEW_CONSOLE),
subprocess.Popen(["python", "Pocha_online_client.py", "Ana", "unir", "1000", "3"], creationflags=subprocess.CREATE_NEW_CONSOLE)]
for i in range(num_jugadores):
    tabla_llamadas[i]