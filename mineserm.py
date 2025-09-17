import os
import random

def clear():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

def head(): # Encabezado
	clear()
	print(headMsg)

def NumTry(N): # Evaluar si es posible convertir el input srt en un int
	try :
		int(N)
		return False
	except :
		return True

def minesCheck(N): # Evaluar si la cantidad de minas está en el rango permitido
	if NumTry(N) == False :
		N = int(N)
		T = gameRows * gameColumns
		if 0 < N <= T :
			return False
		else :
			return True
	else :
		return True

def gameSel_Check(N,C): # Evaluar si la selección (fila o columna) está en el rango
	if NumTry(N) == False :
		N = int(N)
		if 0 < N <= C :
			return False
		else :
			return True
	else :
		return True

def gameBoard_New(): # Genera el tablero visible para el jugador
	Board = ["" for x in range(gameRows)]
	for r in range(gameRows):
			Board[r] = ["■" for x in range(gameColumns)] # ▣ ■ □ ⊠ 
	return Board

def gameMines_New(): # Genera la posición de las minas
	Mines = ["" for x in range(gameRows)]
	for r in range(gameRows):
		Mines[r] = [0 for x in range(gameColumns)]
	s = 0
	while s < gameMines :
		for r in range(gameRows):
			if s < gameMines :
				for i in range(gameColumns):
					N = random.randint(0, 2)
					if s == gameMines :
						break
					if Mines[r][i] != 1 :
						if N == 1 :
							Mines[r][i] = N
							s = s + Mines[r][i]
			else :
				break

	return Mines

def gameBoard(): # Muestra el tablero con los números de fila y columna
	if gameColumns >= 10 :
		row = "  "
		for c in range(gameColumns):
			y = c + 1
			if y//10 != 0 :
				row = f"{row} {y//10}"
			else :
				row = f"{row} {" "}"
		print(row)
		
	row = "  "

	for r in range(gameRows+1):
		if r == 0 :
			for c in range(gameColumns):
				if (c+1) >= 10 :
					row = f"{row} {(c+1)%10}"
				else :
					row = f"{row} {c+1}"
		else :
			y = r-1
			if r//10 != 0 :
				row = f"{r}"
			else :
				row = f"{" "}{r}"

			for c in range(gameColumns):
				row = f"{row} {Board[y][c]}"
		print(row)

### INICIO, SOLICITUD y VALIDACIÓN DE DATOS

headMsg = "¡Bienvenido al Buscaminas!\n"

head();
playerName = input("Ingresa tu nombre --> ")

headMsg = f"Hola, {playerName}. {headMsg}"

while playerName == "" :
	head()
	print("ERROR! El nombre no puede estar vacío\n")

	playerName = input("Ingresa tu nombre --> ")

head()
gameRows = input("Ingresa número de filas --> ")

while NumTry(gameRows) :
	head()
	print("ERROR! El número de filas debe ser un número entero mayor que cero\n")

	gameRows = int(input("Ingresa número de filas --> "))

gameRows = int(gameRows)

head()
print(f"Número de filas ingresado: {gameRows}\n")
gameColumns = int(input("Ingresa número de columnas --> "))

while NumTry(gameColumns) :
	head()
	print(f"Número de filas ingresado: {gameRows}\n")
	print("ERROR! El número de columnas debe ser un número entero mayor que cero\n")

	gameColumns = input("Ingresa número de columnas --> ")

gameColumns = int(gameColumns)

head()
print(f"Número de filas ingresado: {gameRows} | Número de columnas ingresado: {gameColumns}\n")
gameMines = input("Ingresa número de Minas --> ")

while minesCheck(gameMines) :
	head()
	print(f"Número de filas ingresado: {gameRows}\n")
	print("ERROR! El número de minas debe ser un número entero mayor que cero\n")

	gameMines = input("Ingresa número de Minas --> ")

gameMines = int(gameMines)

headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {gameRows}x{gameColumns} | Minas: {gameMines}\n"

### INICIO DEL JUEGO

Board = gameBoard_New()
Mines = gameMines_New()

onGame = True

while onGame == True : # Mostrar el tablero, seleccionar una casilla y modificar el tablero
	head()
	gameBoard()
	print("")

	selRow = input("Fila --> ")
	if selRow == "q" :
		onGame = False
		break
	while gameSel_Check(selRow,gameRows) :
		head()
		gameBoard()
		print(f"\nERROR! Fila incorrecta (1-{gameRows})\n")
		selRow = input("Fila --> ")
	selRow = int(selRow)

	selColumn = input("Fila --> ")
	while gameSel_Check(selColumn,gameColumns) :
		head()
		gameBoard()
		print(f"Fila: {selRow}\n")
		print(f"\nERROR! Columna incorrecta (1-{gameColumns})\n")
		selColumn = input("Columna --> ")
	selColumn = int(selColumn)

	if Mines[selRow-1][selColumn-1] == 0 :
		Board[selRow-1][selColumn-1] = "□"
	else :
		for i in range(gameRows):
			for c in range(gameColumns):
				if Mines[i][c] == 1 :
					Board[i][c] = "⊠"
		head()
		gameBoard()
		print("\nJuego terminado.")
		onGame = False