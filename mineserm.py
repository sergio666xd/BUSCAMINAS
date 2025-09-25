import os
import platform
import subprocess
import shutil
import random
from time import sleep
import datetime

try:
	os.mkdir("saves") # Directorio para guardar los datos de los jugadores
except FileExistsError:
	print("Cargando Datos...")

def clear(): # Despeja la consola
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

def head(): # Encabezado
	clear()
	print(headMsg)

def menu(): # Menú para mostrar los jugadores guardados, o crear uno
	global saves
	global headMsg

	try:
		os.mkdir("./saves")
		print("Carpeta creada exitosamente.")
	except FileExistsError:
		print("Cargando Datos...")

	saves = os.listdir('./saves')

	headMsg = "¡Bienvenido al Buscaminas!\n"
	head()

	print("-- Jugadores --\n")
	for i in range(len(saves)) :
		print(f'{i+1} -> {saves[i]}')
	print("\n0 -> Nuevo Jugador")
	print("s -> Salir\n")

	menuSel = input("Selecciona opción -->")
	if menuSel == "s" :
		print("\n--- Salida exitosa ---")
		exit()
	else :
		try :
			menuSel = int(menuSel)
			check = True
		except :
			check = False

		if check == True :
			if 0 < menuSel <= len(saves) :
				player(saves[menuSel-1])
			elif menuSel == 0 :
				newPlayer()
			else :
				menu()
		else :
			menu()

def newPlayer(): # Crea un nuevo jugador
	global headMsg
	global playerName

	head()

	playerName = input("\nIngresa tu nombre --> ")

	headMsg = f"Hola, {playerName}. {headMsg}"

	while playerName == "" :
		head()
		print("ERROR! El nombre no puede estar vacío\n")

		playerName = input("Ingresa tu nombre --> ")

	if playerName in saves :
		for i in range(len(saves)) :
			if saves[i] == playerName:
				p = i
		player(saves[p])
	else :
		newDir = f'./saves/{playerName}'
		os.mkdir(newDir)
		print("Carpeta creada exitosamente.")
		playerData_File = f'./saves/{playerName}/playerData.txt'
		with open(playerData_File, 'w', encoding='utf-8') as playerData:
			playerData.write("0\n")
			playerData.write("0\n")
			playerData.write("0")
		
		now = datetime.datetime.now()

		with open(f'./saves/{playerName}/playerHistory.txt', 'w', encoding='utf-8') as playerHistory:
			playerHistory.write(f'--- Historial de Partidas (Jugador: "{playerName}") ---\n')
			playerHistory.write(f'Creado el {now.strftime("%d/%m/%Y a las %H:%M:%S")}\n')
		player(playerName)

def player(p): # Página del jugador
	global playerName
	global headMsg
	global pID

	playerName = p
	for i in range(len(saves)) :
		if saves[i] == playerName:
			pID = i

	playerData_File = f'./saves/{playerName}/playerData.txt'
	try:
		with open(playerData_File, 'r', encoding='utf-8') as playerData:
			Data = playerData.readlines()
			played = int(Data[0])
			wins = int(Data[1])
			defs = int(Data[2])
	except:
		with open(playerData_File, 'w', encoding='utf-8') as playerData:
				playerData.write("0\n")
				playerData.write("0\n")
				playerData.write("0")
		with open(playerData_File, 'r', encoding='utf-8') as playerData:
			Data = playerData.readlines()
			played = int(Data[0])
			wins = int(Data[1])
			defs = int(Data[2])


	headMsg = f"Hola, {playerName}. ¡Bienvenido al Buscaminas!\n"

	head()
	print(f'Partidas jugadas: {played}')
	print(f'Partidas ganadas: {wins}')
	print(f'Partidas perdidas: {defs}')

	print("\n-- Opciones --\n")
	print("1 -> Nueva Partida")
	print("2 -> Ver Historial")
	print("s -> Volver al Menú\n")
	print("0 -> Eliminar Jugador")

	menuSel = input("\nSelecciona opción -->")
	if menuSel == "s" :
		menu()
	else :
		try :
			menuSel = int(menuSel)
			check = True
		except :
			check = False

		if check == True :
			if menuSel == 1 or menuSel == 2 :
				if menuSel == 1 :
					newGame()
				else :
					file_path =f'./saves/{playerName}/playerHistory.txt'
					try :
						if platform.system() == "Windows":
							process = subprocess.run(["notepad.exe", file_path])
						elif platform.system() == "Darwin": # macOS
							process = subprocess.run(["open", file_path])
						else: # Linux and other Unix-like systems
							process = subprocess.run(["xdg-open", file_path])
					except FileNotFoundError:
						print(f"Error: No se encontró el archivo '{file_path}'.")
					except subprocess.CalledProcessError:
						print(f"Error al intentar abrir '{file_path}' con el Bloc de notas.")
					player(saves[pID])
			elif menuSel == 0 :
				head()
				check = input("¿Estás seguro que quieres eliminar el jugador? (S/n) --> ")
				if check == "S" :
					try:
						playerDir = f'./saves/{playerName}'
						shutil.rmtree(playerDir)
						print(f"Directorio '{playerDir}' eliminado correctamente.")
						menu()
					except OSError as e:
						print(f"Error al eliminar el directorio '{playerDir}': {e}")
				else :
					player(saves[pID])
			else :
				player(saves[pID])
		else :
			player(saves[pID])

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

def gameMines_New(R,C): # Genera la posición de las minas
	global Mines
	Mines = ["" for x in range(gameRows)]
	for r in range(gameRows):
		Mines[r] = [0 for x in range(gameColumns)]
	s = 0
	Mines[R-1][C-1] = 2
	for a in range(3):
		y = R - a
		if (gameRows-1) < y or y < 0 :
			continue
		else :
			for b in range(3):
				x = C - b
				if (gameColumns-1) < x or x < 0 :
					continue
				else :
					Mines[y][x] = 2
	while s < gameMines :
		for r in range(gameRows):
			if s < gameMines :
				for i in range(gameColumns):
					N = random.randint(0, 3)
					if s == int(gameMines/2) :
						break
					if Mines[r][i] == 0 :
						if N == 1 :
							Mines[r][i] = N
							s += 1
			else :
				break
		for r in range(gameRows-1, 1,-1):
			if s < gameMines :
				for i in range(gameColumns-1,1,-1):
					N = random.randint(0, 3)
					if s == gameMines :
						break
					if Mines[r][i] == 0 :
						if N == 1 :
							Mines[r][i] = N
							s += 1
			else :
				break
	for r in range(gameRows):
		for c in range(gameColumns):
			if Mines[r][c] == 2 :
				Mines[r][c] = 0
			else :
				continue
	return Mines

def gameBoard(T,H): # Muestra el tablero con los números de fila y columna
	historyLines = []
	if gameColumns >= 10 :
		row = "    "
		for c in range(gameColumns):
			y = c + 1
			if y//10 != 0 :
				row = f"{row} {y//10}"
			else :
				row = f'{row} {" "}'
		if H == 0 :
			print(row)
		else :
			historyLines.append(row)
		
	row = "    "

	for r in range(gameRows+1):
		if r == 0 :
			for c in range(gameColumns):
				if (c+1) >= 10 :
					row = f"{row} {(c+1)%10}"
				else :
					row = f"{row} {c+1}"
			if H == 0 :
				print(row)
			else :
				historyLines.append(row)
			row = "    "
			for c in range(gameColumns):
				row = f"{row}--"
		else :
			y = r-1
			if r//10 != 0 :
				row = f"{r} |"
			else :
				row = f'{" "}{r} |'

			for c in range(gameColumns):
				if T == 0 :
					if H == 0 :
						value = Board[y][c]
					else :
						if Board[y][c] == "⊠" :
							value = "X"
						elif Board[y][c] == "■" :
							value = "0"
						elif Board[y][c] == "▣" :
							value = "-"
						elif Board[y][c] == "□" :
							value = " "
						else :
							value = Board[y][c]
					row = f"{row} {value}"
				else :
					row = f"{row} {Mines[y][c]}"
		if H == 0 :
			print(row)
		else :
			historyLines.append(row)

	if H == 1 :
		return historyLines

def cellsChecked_Search(R,C): # Verifica si una casilla ya ha sido evaluada
	for i in range(len(cellsChecked)):
		if cellsChecked[i][0] == (R+1) and cellsChecked[i][1] == (C+1) :
			return True
	return False

def gameCell_Check(R,C): # Evalúa las casillas al rededor de la celda evaluada
	global T
	global cellsChecked

	if cellsChecked_Search((R-1),(C-1)) == False :
		cellsChecked.append([R,C])
	
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
									if cellsChecked_Search(y,x) == True :
										continue
									else :
										gameCell_Check((y+1), (x+1))
								else :
									continue
		return T
	else :
		return T

def cellSelector(): # Operador del juego (entrada)
	global onGame
	global selMode
	global selRow
	global selColumn
	global headMsg
	global countMines

	selRow = input("\nFila o Modo --> ")
	if selRow == "q" :
		onGame = False
		return 0
	elif selRow == "m" :
		if selMode == True :
			selMode = False
			headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {gameRows}x{gameColumns} | {countMines}\nModo: Marcar"
			return 1
		else :
			selMode = True
			headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {gameRows}x{gameColumns} | {countMines}\nModo: Descubrir"
			return 1

	while gameSel_Check(selRow,gameRows) :
		head()
		gameBoard(0,0)
		print(f"\nERROR! Fila incorrecta (1-{gameRows})\n")
		selRow = input("Fila --> ")
	selRow = int(selRow)

	selColumn = input("Columna --> ")
	while gameSel_Check(selColumn,gameColumns) :
		head()
		gameBoard(0,0)
		print(f"Fila: {selRow}\n")
		print(f"\nERROR! Columna incorrecta (1-{gameColumns})\n")
		selColumn = input("Columna --> ")
	selColumn = int(selColumn)

	return 2

def newGame(): # Inicia una nueva partida
	global headMsg
	global gameRows
	global gameColumns
	global gameMines
	global playerName

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

	game()

def game():
	global cellsChecked
	global Board
	global headMsg
	global gameMines
	global selMode
	global T
	global countMines
	global startTime

	Board = gameBoard_New()

	head()
	gameBoard(0,0)

	cellsChecked = []
	countMines = gameMines

	onGame = True
	selMode = True

	gameStatus = cellSelector()

	Mines = gameMines_New(selRow,selColumn)
	T = 1
	gameCell_Check(selRow,selColumn)

	startTime = datetime.datetime.now()

	while onGame == True : # Mostrar el tablero, seleccionar una casilla y modificar el tablero
		head()
		gameBoard(0,0)
		""" print(cellsChecked)
		print("")
		gameBoard(1,0) # Imprime el tablero de minas
		print("") """
		
		gameStatus = cellSelector()

		if gameStatus == 2 :
			if selMode == True :
				if Mines[selRow-1][selColumn-1] == 0 :
					T = 1
					gameCell_Check(selRow,selColumn)
				else :
					Board[selRow-1][selColumn-1] = "⊠"
					head()
					gameBoard(0,0)
					sleep(0.3)
					for i in range(gameRows):
						for c in range(gameColumns):
							if Mines[i][c] == 1 and Board[i][c] == "■" :
								Board[i][c] = "⊠"
								head()
								gameBoard(0,0)
								sleep(0.3)
							elif Mines[i][c] == 0 and Board[i][c] == "▣" :
								Board[i][c] = "⊠"
								head()
								gameBoard(0,0) 
								sleep(0.3)
					print("\nPERDISTE :(\n")
					historyNew()
					newScore("d")
					onGame = False
			else :
				if Board[selRow-1][selColumn-1] == "■" :
					Board[selRow-1][selColumn-1] = "▣"
					countMines -= 1
					headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {gameRows}x{gameColumns} | {countMines}\nModo: Marcar"
				elif Board[selRow-1][selColumn-1] == "▣" :
					Board[selRow-1][selColumn-1] = "■"
					countMines += 1
					headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {gameRows}x{gameColumns} | {countMines}\nModo: Marcar"
				else :
					continue
				if countMines == 0 :
					checkMines = 0
					for r in range(gameRows):
						for c in range(gameColumns):
							if Board[r][c] == "▣" and Mines[r][c] == 1 :
								checkMines += 1
					if checkMines == gameMines :
						print("\n¡GANASTE!\n")
						historyNew()
						newScore("w")
						onGame = False
	print("Guardando Datos...")
	sleep(5)
	player(saves[pID])

def	historyNew(): # Añade el trablero final al archivo playerHistory.txt
	now = datetime.datetime.now()
	lines = gameBoard(0,1)
	with open(f'./saves/{playerName}/playerHistory.txt', 'a', encoding='utf-8') as playerHistory:
		playerHistory.write(f"\n-------------------------------\n")
		playerHistory.write(f'\n-- Partida Iniciada el {startTime.strftime("%d/%m/%Y a las %H:%M:%S")} --\n')
		playerHistory.write(f"\nTablero: {gameRows}x{gameColumns} | Minas: {gameMines}\n\n")
		for line in lines :
			playerHistory.write(f"{line}\n")
		playerHistory.write(f'\n-- Partida Finalizada el {now.strftime("%d/%m/%Y a las %H:%M:%S")} --\n')

def newScore(s): # Actualiza la puntuación en playerData.txt
	playerData_File = f'./saves/{playerName}/playerData.txt'
	with open(playerData_File, 'r', encoding='utf-8') as playerData:
		Data = playerData.readlines()
		played = int(Data[0]) + 1
		wins = int(Data[1])
		defs = int(Data[2])
	with open(playerData_File, 'w', encoding='utf-8') as playerData:
		if s == "d" :
			defs += 1
		else :
			wins += 1
		playerData.write(f"{played}\n")
		playerData.write(f"{wins}\n")
		playerData.write(f"{defs}")

menu()