import os
import datetime

# Variables globales del módulo
autosaveFile = ""
played = 0

def deleteAutosave():
	"""Elimina el archivo de autosave al finalizar la partida"""
	from . import game
	from .menus import savedGamesDir
	
	saveFilePath = savedGamesDir+'/'+autosaveFile
	try:
		os.remove(saveFilePath)
	except FileNotFoundError:
		pass

def saveGame(autosave):
	"""Guarda la partida actual en un archivo"""
	from . import game
	from .menus import playerName, savedGamesDir

	try:
		os.mkdir(savedGamesDir)
	except FileExistsError:
		pass

	if autosave == True:
		saveFilePath = savedGamesDir+'/'+autosaveFile
	else:
		now = datetime.datetime.now()
		deleteAutosave()
		saveFileName = f"game_{now.strftime('%d-%m-%Y_%H-%M-%S')}_{playerName}.txt"
		saveFilePath = os.path.join(savedGamesDir, saveFileName)

	with open(saveFilePath, 'w', encoding='utf-8') as saveFile:
		saveFile.write(f"{game.startTime.strftime('%d-%m-%Y %H:%M:%S')}\n")
		saveFile.write(f"{game.gameRows},{game.gameColumns},{game.gameMines}\n")
		for r in range(game.gameRows):
			row_data = ','.join(str(cell) for cell in game.Board[r])
			saveFile.write(f"{row_data}\n")
		for r in range(game.gameRows):
			row_data = ','.join(str(cell) for cell in game.Mines[r])
			saveFile.write(f"{row_data}\n")
		checked_data = ';'.join(f"{cell[0]},{cell[1]}" for cell in game.cellsChecked)
		saveFile.write(f"{checked_data}\n")
		free_data = ';'.join(f"{pos[0]},{pos[1]}" for pos in game.freePositions)
		saveFile.write(f"{free_data}\n")

def loadGame(saveFileName):
	"""Carga una partida guardada desde un archivo"""
	from . import game
	from .menus import playerName, savedGamesDir

	saveFilePath = savedGamesDir+'/'+saveFileName
	if saveFileName.endswith("_AUTOSAVE.txt"):
		global autosaveFile
		autosaveFile = saveFileName

	with open(saveFilePath, 'r', encoding='utf-8') as saveFile:
		lines = saveFile.readlines()
		game.startTime = datetime.datetime.strptime(lines[0].strip(), '%d-%m-%Y %H:%M:%S')
		dimensions = lines[1].strip().split(',')
		game.gameRows = int(dimensions[0])
		game.gameColumns = int(dimensions[1])
		game.gameMines = int(dimensions[2])
		
		game.Board = []
		for r in range(game.gameRows):
			row_data = lines[2 + r].strip().split(',')
			game.Board.append([cell if cell in ["■", "▣", "□", "⊠"] else int(cell) for cell in row_data])
		
		game.Mines = []
		for r in range(game.gameRows):
			row_data = lines[2 + game.gameRows + r].strip().split(',')
			game.Mines.append([int(cell) for cell in row_data])
		
		game.cellsChecked = []
		checked_data = lines[2 + 2 * game.gameRows].strip().split(';')
		for cell in checked_data:
			if cell:
				r, c = map(int, cell.split(','))
				game.cellsChecked.append([r, c])
		
		game.freePositions = []
		free_data = lines[3 + 2 * game.gameRows].strip().split(';')
		for pos in free_data:
			if pos:
				r, c = map(int, pos.split(','))
				game.freePositions.append((r, c))

	game.headMsg = f"BUSCAMINAS | Jugador: {playerName}\n\nTablero {game.gameRows}x{game.gameColumns} | {game.gameMines}\nModo: Descubrir"
	game.onGame = True
	game.selMode = True
	game.gameStatus = 2
	game.countMines = game.gameMines

	game.game()

def save():
	"""Guarda la partida automáticamente"""
	from . import game
	from .menus import playerName
	global autosaveFile

	now = datetime.datetime.now()
	try:
		deleteAutosave()
	except:
		pass
	autosaveFile = f"game_{now.strftime('%d-%m-%Y_%H-%M-%S')}_{playerName}_AUTOSAVE.txt"
	saveGame(True)

def historyNew():
	"""Añade el tablero final al archivo playerHistory.txt"""
	from . import game
	from .menus import playerName
	from .board import gameBoard
	global played

	now = datetime.datetime.now()
	lines = gameBoard(0, 1)
	with open(f'./Game/players/{playerName}/playerHistory.txt', 'a', encoding='utf-8') as playerHistory:
		playerHistory.write(f"\n-----------------------------------------------------\n")
		playerHistory.write(f"\n--- Partida N°{played} ({game.finishStatus}) ---\n")
		playerHistory.write(f'\n-- Partida Iniciada el {game.startTime.strftime("%d/%m/%Y a las %H:%M:%S")} --\n')
		playerHistory.write(f"\nTablero: {game.gameRows}x{game.gameColumns} | Minas: {game.gameMines}\n\n")
		for line in lines:
			playerHistory.write(f"{line}\n")
		playerHistory.write(f'\n-- Partida Finalizada el {now.strftime("%d/%m/%Y a las %H:%M:%S")} --\n')

def newScore(s):
	"""Actualiza la puntuación en playerData.txt"""
	from .menus import playerName
	global played

	playerData_File = f'./Game/players/{playerName}/playerData.txt'
	with open(playerData_File, 'r', encoding='utf-8') as playerData:
		Data = playerData.readlines()
		played = int(Data[0]) + 1
		wins = int(Data[1])
		defs = int(Data[2])
	with open(playerData_File, 'w', encoding='utf-8') as playerData:
		if s == "d":
			defs += 1
		else:
			wins += 1
		playerData.write(f"{played}\n")
		playerData.write(f"{wins}\n")
		playerData.write(f"{defs}")
