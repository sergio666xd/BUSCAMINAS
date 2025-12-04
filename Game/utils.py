import os
from . import globals

def clear():
	"""Despeja la consola"""
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

def head():
	"""Encabezado"""
	clear()
	print(globals.headMsg)

def NumTry(N):
	"""Evaluar si es posible convertir el input str en un int"""
	try:
		int(N)
		return False
	except:
		return True

def minesCheck(N):
	"""Evaluar si la cantidad de minas está en el rango permitido"""
	if NumTry(N) == False:
		N = int(N)
		T = globals.gameRows * globals.gameColumns
		if 0 < N <= T:
			return False
		else:
			return True
	else:
		return True

def gameSel_Check(N, C):
	"""Evaluar si la selección (fila o columna) está en el rango"""
	if NumTry(N) == False:
		N = int(N)
		if 0 < N <= C:
			return False
		else:
			return True
	else:
		return True
