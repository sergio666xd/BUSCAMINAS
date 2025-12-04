import os

# Crear directorio de jugadores si no existe
try:
	os.mkdir("./Game/players")
except FileExistsError:
	print("Cargando Datos...")

# Importar módulos
from Game.menus import menu

# Iniciar juego
menu()