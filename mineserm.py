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
					N = random.randint(0, 3)
					if s == gameMines :
						break
					if Mines[r][i] != 1 :
						if N == 1 :
							Mines[r][i] = N
							s += 1
			else :
				break

	return Mines

def gameBoard(T): # Muestra el tablero con los números de fila y columna
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
				if T == 0 :
					row = f"{row} {Board[y][c]}"
				else :
					row = f"{row} {Mines[y][c]}"
		print(row)

def gameCell_Check(R,C):
	global T
	T = T + 1
	if T <= (gameRows*gameColumns): # El número de repeticiones no puede ser mayor al numero de casillas
		minesAround = 0
		for a in range(3) : # Cuenta las minas alrededor de la casilla seleccionada
			y = R - a
			if (gameRows-1) < y or y < 0 :
				continue
			else :
				for b in range(3) :
					x = C - b
					if (gameColumns-1) < x or x < 0 :
						continue
					else :
						if Mines[y][x] == 1 :
							minesAround += 1
		if minesAround > 0 : # Evalúa si hay minas y 
			Board[R-1][C-1] = minesAround
		else :
			for a in range(3) :
				y = R - a
				if (gameRows-1) < y or y < 0 :
					continue
				else :
					for b in range(3) :
						x = C - b
						if (gameColumns-1) < x or x < 0 :
							continue
						else :
							if Mines[y][x] == 1 :
								minesAround += 1
							else :
								if Board[y][x] == "■" :
									Board[y][x] = "□"
									# print(T) # imprime la cantidad de veces que se ha repetido la función
									gameCell_Check((y+1), (x+1))
								elif Board[y][x] == "□" :
									continue
								else :
									break
			Board[R-1][C-1] = "□"
		return T
	else :
		return T

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

headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {gameRows}x{gameColumns} | Minas Restantes: {gameMines}\nModo: Descubrir"

### INICIO DEL JUEGO

Board = gameBoard_New()
Mines = gameMines_New()

onGame = True
selMode = True

while onGame == True : # Mostrar el tablero, seleccionar una casilla y modificar el tablero
	head()
	gameBoard(0)
	print("")
	# gameBoard(1) # Imprime el tablero de minas
	# print("")

	selRow = input("Fila --> ")
	if selRow == "q" :
		onGame = False
		break
	elif selRow == "m" :
		if selMode == True :
			selMode == False
			headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {gameRows}x{gameColumns} | Minas Restantes: {gameMines}\nModo: Marcar"
			continue
		else :
			selMode = True
			headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {gameRows}x{gameColumns} | Minas Restantes: {gameMines}\nModo: Descubrir"
			continue

	while gameSel_Check(selRow,gameRows) :
		head()
		gameBoard(0)
		print(f"\nERROR! Fila incorrecta (1-{gameRows})\n")
		selRow = input("Fila --> ")
	selRow = int(selRow)

	selColumn = input("Columna --> ")
	while gameSel_Check(selColumn,gameColumns) :
		head()
		gameBoard(0)
		print(f"Fila: {selRow}\n")
		print(f"\nERROR! Columna incorrecta (1-{gameColumns})\n")
		selColumn = input("Columna --> ")
	selColumn = int(selColumn)

	if Mines[selRow-1][selColumn-1] == 0 :
		T = 1
		print(T)
		gameCell_Check(selRow,selColumn)
	else :
		for i in range(gameRows):
			for c in range(gameColumns):
				if Mines[i][c] == 1 :
					Board[i][c] = "⊠"
		head()
		gameBoard(0)
		print("\nJuego terminado.")
		onGame = False