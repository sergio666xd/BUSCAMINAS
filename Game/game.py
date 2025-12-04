import datetime
import random
from time import sleep
from . import globals
from .utils import head, gameSel_Check

def cellSelector():
	"""Controla la entrada del usuario para seleccionar casillas o cambiar de modo"""
	from .save import saveGame
	from .board import gameBoard

	if globals.gameStatus == 3:
		if globals.gameMode == "random":
			return cellSelector_Random()
		else:
			globals.selRow = input("\nFila --> ")
	else:
		if globals.gameMode == "random":
			print("\nOpciones: m = Cambiar modo | s = Guardar | q = Salir | r = Generar casilla | i = Ingresar casilla")
			selRow = input("Opción o Acción --> ")
		else:
			print("\nOpciones: m = Cambiar modo | s = Guardar | q = Salir")
			selRow = input("Opción o Fila --> ")
		
		if selRow == "q":
			saveAsk = input("\n¿Guardar partida antes de salir? (S/n) --> ")
			if saveAsk.lower() == "s":
				print("\nGuardando partida...")
				saveGame(False)
				sleep(2)
			globals.onGame = False
			return 0
		elif selRow == "s":
			saveAsk = input("\n¿Guardar partida? (S/n) --> ")
			if saveAsk.lower() == "s":
				print("\nGuardando partida...")
				saveGame(False)
				sleep(1)
			return 1
		elif selRow == "m":
			if globals.selMode == True:
				globals.selMode = False
				globals.headMsg = f"BUSCAMINAS | Jugador: {globals.playerName}\n\nTablero {globals.gameRows}x{globals.gameColumns} | {globals.countMines}\nModo: Marcar"
				return 1
			else:
				globals.selMode = True
				globals.headMsg = f"BUSCAMINAS | Jugador: {globals.playerName}\n\nTablero {globals.gameRows}x{globals.gameColumns} | {globals.countMines}\nModo: Descubrir"
				return 1
		elif globals.gameMode == "random" and selRow == "r":
			return cellSelector_Random()
		elif globals.gameMode == "random" and selRow == "i":
			globals.selRow = input("\nFila --> ")
		else:
			globals.selRow = selRow

	while gameSel_Check(globals.selRow, globals.gameRows):
		head()
		gameBoard(0, 0)
		print(f"\nERROR! Fila incorrecta (1-{globals.gameRows})\n")
		globals.selRow = input("Fila --> ")
	globals.selRow = int(globals.selRow)

	globals.selColumn = input("Columna --> ")
	while gameSel_Check(globals.selColumn, globals.gameColumns):
		head()
		gameBoard(0, 0)
		print(f"\nFila: {globals.selRow}")
		print(f"\nERROR! Columna incorrecta (1-{globals.gameColumns})\n")
		globals.selColumn = input("Columna --> ")
	globals.selColumn = int(globals.selColumn)

	return 2

def cellSelector_Random():
	"""Genera una casilla aleatoria válida y pregunta si desea jugar en ella"""
	from .board import gameBoard

	# Generar casilla aleatoria válida
	validCells = [(r+1, c+1) for r in range(globals.gameRows) for c in range(globals.gameColumns) if globals.Board[r][c] == "■"]
	
	if validCells:
		globals.selRow, globals.selColumn = random.choice(validCells)
		head()
		gameBoard(0, 0)
		print(f"\nCasilla generada aleatoriamente: Fila {globals.selRow}, Columna {globals.selColumn}")
		print("\n¿Deseas jugar en esta casilla?")
		print("1 -> Sí, jugar en esta casilla")
		print("2 -> No, ingresar una casilla manualmente")
		print("3 -> Generar otra casilla\n")
		
		response = input("Selecciona opción --> ")
		
		if response == "1":
			return 2
		elif response == "2":
			globals.selRow = input("\nFila --> ")
			while gameSel_Check(globals.selRow, globals.gameRows):
				head()
				gameBoard(0, 0)
				print(f"\nERROR! Fila incorrecta (1-{globals.gameRows})\n")
				globals.selRow = input("Fila --> ")
			globals.selRow = int(globals.selRow)

			globals.selColumn = input("Columna --> ")
			while gameSel_Check(globals.selColumn, globals.gameColumns):
				head()
				gameBoard(0, 0)
				print(f"\nFila: {globals.selRow}")
				print(f"\nERROR! Columna incorrecta (1-{globals.gameColumns})\n")
				globals.selColumn = input("Columna --> ")
			globals.selColumn = int(globals.selColumn)
			return 2
		elif response == "3":
			return cellSelector_Random()
		else:
			head()
			gameBoard(0, 0)
			return cellSelector_Random()
	else:
		head()
		gameBoard(0, 0)
		print("\nNo hay casillas válidas disponibles.\n")
		return cellSelector_Random()

def newGame():
	"""Inicia una nueva partida, solicita parámetros y valida entradas"""
	from .utils import NumTry, minesCheck
	from .board import gameBoard_New, gameMines_New, gameCell_Check, gameBoard

	head()

	globals.gameRows = input("Ingresa número de filas --> ")

	while NumTry(globals.gameRows):
		head()
		print("ERROR! El número de filas debe ser un número entero mayor que cero\n")
		globals.gameRows = int(input("Ingresa número de filas --> "))

	globals.gameRows = int(globals.gameRows)

	head()
	print(f"Número de filas ingresado: {globals.gameRows}\n")
	globals.gameColumns = input("Ingresa número de columnas --> ")

	while NumTry(globals.gameColumns):
		head()
		print(f"Número de filas ingresado: {globals.gameRows}\n")
		print("ERROR! El número de columnas debe ser un número entero mayor que cero\n")
		globals.gameColumns = input("Ingresa número de columnas --> ")

	globals.gameColumns = int(globals.gameColumns)

	head()
	print(f"Número de filas ingresado: {globals.gameRows} | Número de columnas ingresado: {globals.gameColumns}\n")

	if globals.gameRows * globals.gameColumns <= 9:
		globals.headMsg = "¡ADVERTENCIA! El tamaño del tablero es muy pequeño, lo que puede afectar la jugabilidad.\nTamaño mínimo recomendado: 4x4 (16 casillas)\n"
		head()
		input("Presiona Enter para volver...")
		newGame()
	else:
		globals.gameMines = input("Ingresa número de Minas --> ")

		while minesCheck(globals.gameMines):
			head()
			print(f"Número de filas ingresado: {globals.gameRows}\n")
			print("ERROR! El número de minas debe ser un número entero mayor que cero\n")
			globals.gameMines = input("Ingresa número de Minas --> ")

		globals.gameMines = int(globals.gameMines)

		# Seleccionar modo de juego
		head()
		print("-- Selecciona modo de juego --\n")
		print("1 -> Modo Normal (seleccionar casillas manualmente)")
		print("2 -> Modo Aleatorio (con opción de generar casillas aleatoriamente)\n")
		modeSelection = input("Selecciona modo --> ")
		
		while modeSelection not in ["1", "2"]:
			head()
			print("-- Selecciona modo de juego --\n")
			print("1 -> Modo Normal (seleccionar casillas manualmente)")
			print("2 -> Modo Aleatorio (con opción de generar casillas aleatoriamente)\n")
			print("ERROR! Selecciona una opción válida\n")
			modeSelection = input("Selecciona modo --> ")
		
		globals.gameMode = "normal" if modeSelection == "1" else "random"

		globals.headMsg = f"BUSCAMINAS | Jugador: {globals.playerName}\n\nTablero {globals.gameRows}x{globals.gameColumns} | Minas Restantes: {globals.gameMines}\nModo: Descubrir"

		globals.Board = gameBoard_New()

		head()
		gameBoard(0, 0)

		globals.cellsChecked = []
		globals.countMines = globals.gameMines

		globals.onGame = True
		globals.selMode = True

		globals.gameStatus = 3
		globals.gameStatus = cellSelector()

		globals.Mines = gameMines_New(globals.selRow, globals.selColumn)
		globals.T = 1
		gameCell_Check(globals.selRow, globals.selColumn)

		globals.startTime = datetime.datetime.now()

		game()

def game():
	"""Lógica principal del juego: ciclo de turnos, control de estado y condiciones de victoria/derrota"""
	from .board import gameBoard, gameCell_Check
	from .save import save, deleteAutosave, historyNew, newScore

	save()

	finishMsg = "\n-- Saliendo --\n"

	while globals.onGame == True:
		head()
		from .board import gameBoard
		gameBoard(0, 0)
		if globals.playerName == "admin":
			print("")
			print(globals.cellsChecked)
			print("")
			gameBoard(1, 0)
			print("")
		
		globals.gameStatus = cellSelector()
		save()
		if globals.gameStatus == 0:
			finishMsg = "\n-- Saliendo --\n"
			break
		elif globals.gameStatus == 1:
			continue
		elif globals.gameStatus == 2:
			if globals.selMode == True:
				if globals.Mines[globals.selRow-1][globals.selColumn-1] == 0:
					globals.T = 1
					gameCell_Check(globals.selRow, globals.selColumn)
				else:
					globals.Board[globals.selRow-1][globals.selColumn-1] = "⊠"
					head()
					gameBoard(0, 0)
					sleep(0.3)
					for i in range(globals.gameRows):
						for c in range(globals.gameColumns):
							if globals.Mines[i][c] == 1 and globals.Board[i][c] == "■":
								globals.Board[i][c] = "⊠"
								head()
								gameBoard(0, 0)
								sleep(0.3)
							elif globals.Mines[i][c] == 0 and globals.Board[i][c] == "▣":
								globals.Board[i][c] = "⊠"
								head()
								gameBoard(0, 0) 
								sleep(0.3)
					finishMsg = "\nPERDISTE :(\n"
					globals.finishStatus = "Perdida"
					print(finishMsg)
					newScore("d")
					historyNew()
					globals.onGame = False
			else:
				if globals.Board[globals.selRow-1][globals.selColumn-1] == "■":
					globals.Board[globals.selRow-1][globals.selColumn-1] = "▣"
					globals.countMines -= 1
					globals.headMsg = f"BUSCAMINAS | Jugador: {globals.playerName}\n\nTablero {globals.gameRows}x{globals.gameColumns} | {globals.countMines}\nModo: Marcar"
				elif globals.Board[globals.selRow-1][globals.selColumn-1] == "▣":
					globals.Board[globals.selRow-1][globals.selColumn-1] = "■"
					globals.countMines += 1
					globals.headMsg = f"BUSCAMINAS | Jugador: {globals.playerName}\n\nTablero {globals.gameRows}x{globals.gameColumns} | {globals.countMines}\nModo: Marcar"
				else:
					continue
				if globals.countMines == 0:
					checkMines = 0
					for r in range(globals.gameRows):
						for c in range(globals.gameColumns):
							if globals.Board[r][c] == "▣" and globals.Mines[r][c] == 1:
								checkMines += 1
		if globals.freePositions == []:
			for i in range(globals.gameRows):
				for c in range(globals.gameColumns):
					if globals.Board[i][c] == "▣":
						globals.Board[i][c] = "■"
						head()
						gameBoard(0, 0)
						sleep(0.3)
			finishMsg = "\n¡GANASTE!\n"
			globals.finishStatus = "Ganada"
			print(finishMsg)
			newScore("w")
			historyNew()
			globals.onGame = False

	head()
	from .board import gameBoard
	gameBoard(0, 0)

	if globals.playerName == "admin":
		print("")
		print(globals.cellsChecked)
		print("")
		gameBoard(1, 0)
		print("")

	print(finishMsg)
	deleteAutosave()
	sleep(3)
	from .menus import player_menu
	player_menu(globals.playerName)
