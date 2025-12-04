import os
import datetime
from . import globals

# Variables globales del módulo
autosaveFile = ""
played = 0

def deleteAutosave():
	"""Elimina el archivo de autosave al finalizar la partida"""
	global autosaveFile
	
	saveFilePath = f"{globals.savedGamesDir}/{autosaveFile}"
	try:
		os.remove(saveFilePath)
	except FileNotFoundError:
		pass

def saveGame(autosave):
	"""Guarda la partida actual en un archivo"""
	global autosaveFile

	try:
		os.mkdir(globals.savedGamesDir)
	except FileExistsError:
		pass

	if autosave == True:
		saveFilePath = f"{globals.savedGamesDir}/{autosaveFile}"
	else:
		now = datetime.datetime.now()
		deleteAutosave()
		saveFileName = f"game_{now.strftime('%d-%m-%Y_%H-%M-%S')}_{globals.playerName}_{globals.gameMode}.txt"
		saveFilePath = f"{globals.savedGamesDir}/{saveFileName}"

	with open(saveFilePath, 'w', encoding='utf-8') as saveFile:
		saveFile.write(f"{globals.startTime.strftime('%d-%m-%Y %H:%M:%S')}\n")
		saveFile.write(f"{globals.gameRows},{globals.gameColumns},{globals.gameMines}\n")
		saveFile.write(f"{globals.gameMode}\n")
		for r in range(globals.gameRows):
			row_data = ','.join(str(cell) for cell in globals.Board[r])
			saveFile.write(f"{row_data}\n")
		for r in range(globals.gameRows):
			row_data = ','.join(str(cell) for cell in globals.Mines[r])
			saveFile.write(f"{row_data}\n")
		checked_data = ';'.join(f"{cell[0]},{cell[1]}" for cell in globals.cellsChecked)
		saveFile.write(f"{checked_data}\n")
		free_data = ';'.join(f"{pos[0]},{pos[1]}" for pos in globals.freePositions)
		saveFile.write(f"{free_data}\n")

def loadGame(saveFileName):
	"""Carga una partida guardada desde un archivo"""
	global autosaveFile

	saveFilePath = f"{globals.savedGamesDir}/{saveFileName}"
	if saveFileName.endswith("_AUTOSAVE.txt"):
		autosaveFile = saveFileName

	with open(saveFilePath, 'r', encoding='utf-8') as saveFile:
		lines = saveFile.readlines()
		globals.startTime = datetime.datetime.strptime(lines[0].strip(), '%d-%m-%Y %H:%M:%S')
		dimensions = lines[1].strip().split(',')
		globals.gameRows = int(dimensions[0])
		globals.gameColumns = int(dimensions[1])
		globals.gameMines = int(dimensions[2])
		
		# Detectar si el archivo tiene gameMode (nueva versión)
		lineOffset = 2
		if len(lines) > 2 and lines[2].strip() in ["normal", "random"]:
			globals.gameMode = lines[2].strip()
			lineOffset = 3
		else:
			globals.gameMode = "normal"
			lineOffset = 2
		
		globals.Board = []
		for r in range(globals.gameRows):
			row_data = lines[lineOffset + r].strip().split(',')
			globals.Board.append([cell if cell in ["■", "▣", "□", "⊠"] else int(cell) for cell in row_data])
		
		globals.Mines = []
		for r in range(globals.gameRows):
			row_data = lines[lineOffset + globals.gameRows + r].strip().split(',')
			globals.Mines.append([int(cell) for cell in row_data])
		
		globals.cellsChecked = []
		checked_data = lines[lineOffset + 2 * globals.gameRows].strip().split(';')
		for cell in checked_data:
			if cell:
				parts = cell.split(',')
				if len(parts) == 2:
					r, c = map(int, parts)
					globals.cellsChecked.append([r, c])
		
		globals.freePositions = []
		free_data = lines[lineOffset + 2 * globals.gameRows + 1].strip().split(';')
		for pos in free_data:
			if pos:
				parts = pos.split(',')
				if len(parts) == 2:
					r, c = map(int, parts)
					globals.freePositions.append((r, c))

	globals.headMsg = f"BUSCAMINAS | Jugador: {globals.playerName}\n\nTablero {globals.gameRows}x{globals.gameColumns} | {globals.gameMines}\nModo: Descubrir"
	globals.onGame = True
	globals.selMode = True
	globals.gameStatus = 2
	globals.countMines = globals.gameMines

	from .game import game
	game()

def save():
	"""Guarda la partida automáticamente"""
	global autosaveFile

	now = datetime.datetime.now()
	try:
		deleteAutosave()
	except:
		pass
	autosaveFile = f"game_{now.strftime('%d-%m-%Y_%H-%M-%S')}_{globals.playerName}_{globals.gameMode}_AUTOSAVE.txt"
	saveGame(True)

def historyNew():
	"""Añade el tablero final al archivo playerHistory.txt"""
	global played
	from .board import gameBoard

	now = datetime.datetime.now()
	lines = gameBoard(0, 1)
	with open(f'./Game/players/{globals.playerName}/playerHistory.txt', 'a', encoding='utf-8') as playerHistory:
		playerHistory.write(f"\n-----------------------------------------------------\n")
		playerHistory.write(f"\n--- Partida N°{played} ({globals.finishStatus}) ---\n")
		playerHistory.write(f'\n-- Partida Iniciada el {globals.startTime.strftime("%d/%m/%Y a las %H:%M:%S")} --\n')
		playerHistory.write(f"\nTablero: {globals.gameRows}x{globals.gameColumns} | Minas: {globals.gameMines}\n\n")
		for line in lines:
			playerHistory.write(f"{line}\n")
		playerHistory.write(f'\n-- Partida Finalizada el {now.strftime("%d/%m/%Y a las %H:%M:%S")} --\n')

def newScore(s):
	"""Actualiza la puntuación en playerData.txt"""
	global played

	playerData_File = f'./Game/players/{globals.playerName}/playerData.txt'
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
