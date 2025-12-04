import datetime
from time import sleep

# Variables globales del módulo
headMsg = ""
playerName = ""
gameRows = 0
gameColumns = 0
gameMines = 0
Board = []
Mines = []
cellsChecked = []
freePositions = []
T = 0
countMines = 0
startTime = None
onGame = False
selMode = True
selRow = 0
selColumn = 0
gameStatus = 0
finishStatus = ""

def cellSelector():
	"""Controla la entrada del usuario para seleccionar casillas o cambiar de modo"""
	global onGame, selMode, selRow, selColumn, headMsg, countMines, gameStatus, playerName, gameRows, gameColumns
	from .utils import head, gameSel_Check
	from .save import saveGame

	if gameStatus == 3:
		selRow = input("\nFila --> ")
	else:
		print("\nOpciones: m = Cambiar modo | s = Guardar | q = Salir")
		selRow = input("Opción o Fila --> ")
		if selRow == "q":
			saveAsk = input("\n¿Guardar partida antes de salir? (S/n) --> ")
			if saveAsk.lower() == "s":
				print("\nGuardando partida...")
				saveGame(False)
				sleep(2)
			onGame = False
			return 0
		elif selRow == "s":
			saveAsk = input("\n¿Guardar partida? (S/n) --> ")
			if saveAsk.lower() == "s":
				print("\nGuardando partida...")
				saveGame(False)
				sleep(1)
			return 1
		elif selRow == "m":
			if selMode == True:
				selMode = False
				headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {gameRows}x{gameColumns} | {countMines}\nModo: Marcar"
				return 1
			else:
				selMode = True
				headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {gameRows}x{gameColumns} | {countMines}\nModo: Descubrir"
				return 1

	while gameSel_Check(selRow, gameRows):
		head()
		from .board import gameBoard
		gameBoard(0, 0)
		print(f"\nERROR! Fila incorrecta (1-{gameRows})\n")
		selRow = input("Fila --> ")
	selRow = int(selRow)

	selColumn = input("Columna --> ")
	while gameSel_Check(selColumn, gameColumns):
		head()
		from .board import gameBoard
		gameBoard(0, 0)
		print(f"\nFila: {selRow}")
		print(f"\nERROR! Columna incorrecta (1-{gameColumns})\n")
		selColumn = input("Columna --> ")
	selColumn = int(selColumn)

	return 2

def newGame():
	"""Inicia una nueva partida, solicita parámetros y valida entradas"""
	global headMsg, gameRows, gameColumns, gameMines, playerName, cellsChecked, Board, selMode, countMines, startTime, Mines, onGame, gameStatus
	from .utils import head, NumTry, minesCheck
	from .board import gameBoard_New, gameMines_New, gameCell_Check, gameBoard

	head()
	if 'errBoard' in globals():
		print(errBoard)
		del errBoard

	gameRows = input("Ingresa número de filas --> ")

	while NumTry(gameRows):
		head()
		print("ERROR! El número de filas debe ser un número entero mayor que cero\n")
		gameRows = int(input("Ingresa número de filas --> "))

	gameRows = int(gameRows)

	head()
	print(f"Número de filas ingresado: {gameRows}\n")
	gameColumns = input("Ingresa número de columnas --> ")

	while NumTry(gameColumns):
		head()
		print(f"Número de filas ingresado: {gameRows}\n")
		print("ERROR! El número de columnas debe ser un número entero mayor que cero\n")
		gameColumns = input("Ingresa número de columnas --> ")

	gameColumns = int(gameColumns)

	head()
	print(f"Número de filas ingresado: {gameRows} | Número de columnas ingresado: {gameColumns}\n")

	if gameRows * gameColumns <= 9:
		errBoard = "¡ADVERTENCIA! El tamaño del tablero es muy pequeño, lo que puede afectar la jugabilidad.\nTamaño mínimo recomendado: 4x4 (16 casillas)\n"
		newGame()
	else:
		gameMines = input("Ingresa número de Minas --> ")

		while minesCheck(gameMines):
			head()
			print(f"Número de filas ingresado: {gameRows}\n")
			print("ERROR! El número de minas debe ser un número entero mayor que cero\n")
			gameMines = input("Ingresa número de Minas --> ")

		gameMines = int(gameMines)

		headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {gameRows}x{gameColumns} | Minas Restantes: {gameMines}\nModo: Descubrir"

		Board = gameBoard_New()

		head()
		gameBoard(0, 0)

		cellsChecked = []
		countMines = gameMines

		onGame = True
		selMode = True

		gameStatus = 3
		gameStatus = cellSelector()

		Mines = gameMines_New(selRow, selColumn)
		T = 1
		gameCell_Check(selRow, selColumn)

		startTime = datetime.datetime.now()

		game()

def game():
	"""Lógica principal del juego: ciclo de turnos, control de estado y condiciones de victoria/derrota"""
	global cellsChecked, Board, headMsg, gameMines, selMode, T, countMines, startTime, Mines, onGame, playerName, gameStatus, freePositions, finishStatus
	from .utils import head
	from .board import gameBoard, gameCell_Check
	from .save import save, deleteAutosave, historyNew, newScore

	save()

	finishMsg = "\n-- Saliendo --\n"

	while onGame == True:
		head()
		gameBoard(0, 0)
		if playerName == "admin":
			print("")
			print(cellsChecked)
			print("")
			gameBoard(1, 0)
			print("")
		
		gameStatus = cellSelector()
		save()
		if gameStatus == 0:
			finishMsg = "\n-- Saliendo --\n"
			break
		elif gameStatus == 1:
			continue
		elif gameStatus == 2:
			if selMode == True:
				if Mines[selRow-1][selColumn-1] == 0:
					T = 1
					gameCell_Check(selRow, selColumn)
				else:
					Board[selRow-1][selColumn-1] = "⊠"
					head()
					gameBoard(0, 0)
					sleep(0.3)
					for i in range(gameRows):
						for c in range(gameColumns):
							if Mines[i][c] == 1 and Board[i][c] == "■":
								Board[i][c] = "⊠"
								head()
								gameBoard(0, 0)
								sleep(0.3)
							elif Mines[i][c] == 0 and Board[i][c] == "▣":
								Board[i][c] = "⊠"
								head()
								gameBoard(0, 0) 
								sleep(0.3)
					finishMsg = "\nPERDISTE :(\n"
					finishStatus = "Perdida"
					print(finishMsg)
					newScore("d")
					historyNew()
					onGame = False
			else:
				if Board[selRow-1][selColumn-1] == "■":
					Board[selRow-1][selColumn-1] = "▣"
					countMines -= 1
					headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {gameRows}x{gameColumns} | {countMines}\nModo: Marcar"
				elif Board[selRow-1][selColumn-1] == "▣":
					Board[selRow-1][selColumn-1] = "■"
					countMines += 1
					headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {gameRows}x{gameColumns} | {countMines}\nModo: Marcar"
				else:
					continue
				if countMines == 0:
					checkMines = 0
					for r in range(gameRows):
						for c in range(gameColumns):
							if Board[r][c] == "▣" and Mines[r][c] == 1:
								checkMines += 1
		if freePositions == []:
			for i in range(gameRows):
				for c in range(gameColumns):
					if Board[i][c] == "▣":
						Board[i][c] = "■"
						head()
						gameBoard(0, 0)
						sleep(0.3)
			finishMsg = "\n¡GANASTE!\n"
			finishStatus = "Ganada"
			print(finishMsg)
			newScore("w")
			historyNew()
			onGame = False

	head()
	gameBoard(0, 0)

	if playerName == "admin":
		print("")
		print(cellsChecked)
		print("")
		gameBoard(1, 0)
		print("")

	print(finishMsg)
	deleteAutosave()
	sleep(3)
	from .menus import player_menu
	player_menu(playerName)
