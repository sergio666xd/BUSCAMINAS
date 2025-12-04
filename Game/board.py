import random
from . import globals

# Variables globales del módulo
gameRows = 0
gameColumns = 0
gameMines = 0
Board = []
Mines = []
cellsChecked = []
freePositions = []

def gameBoard_New():
	"""Genera el tablero visible para el jugador (solo casillas ocultas)"""
	Board = [["■" for c in range(globals.gameColumns)] for r in range(globals.gameRows)]
	return Board

def gameMines_New(R, C):
	"""Genera el tablero de minas, excluyendo el área protegida alrededor de la primera jugada"""
	protected = set()
	for r in range(-1, 2):
		for c in range(-1, 2):
			pr, pc = R - 1 + r, C - 1 + c
			if 0 <= pr < globals.gameRows and 0 <= pc < globals.gameColumns:
				protected.add((pr, pc))

	positions = [(r, c) for r in range(globals.gameRows) for c in range(globals.gameColumns) if (r, c) not in protected]
	minePositions = random.sample(positions, min(globals.gameMines, len(positions)))

	Mines = [[0 for c in range(globals.gameColumns)] for r in range(globals.gameRows)]
	for r, c in minePositions:
		Mines[r][c] = 1

	globals.freePositions = [(r, c) for r in range(globals.gameRows) for c in range(globals.gameColumns) if (r, c) not in minePositions]

	return Mines

def gameBoard(T, H):
	"""Imprime el tablero con numeración de filas y columnas, o lo retorna como lista de strings para historial"""
	print("")
	historyLines = []
	if globals.gameColumns >= 10:
		row = "    "
		for c in range(globals.gameColumns):
			y = c + 1
			if y//10 != 0:
				row = f"{row} {y//10}"
			else:
				row = f'{row} {" "}'
		if H == 0:
			print(row)
		else:
			historyLines.append(row)
	
	row = "    "

	for r in range(globals.gameRows+1):
		if r == 0:
			for c in range(globals.gameColumns):
				if (c+1) >= 10:
					row = f"{row} {(c+1)%10}"
				else:
					row = f"{row} {c+1}"
			if H == 0:
				print(row)
			else:
				historyLines.append(row)
			row = "    "
			for c in range(globals.gameColumns):
				row = f"{row}--"
		else:
			y = r-1
			if r//10 != 0:
				row = f"{r} |"
			else:
				row = f'{" "}{r} |'

			for c in range(globals.gameColumns):
				if T == 0:
					if H == 0:
						value = globals.Board[y][c]
					else:
						if globals.Board[y][c] == "⊠":
							value = "X"
						elif globals.Board[y][c] == "■":
							value = "0"
						elif globals.Board[y][c] == "▣":
							value = "-"
						elif globals.Board[y][c] == "□":
							value = " "
						else:
							value = globals.Board[y][c]
					row = f"{row} {value}"
				else:
					row = f"{row} {globals.Mines[y][c]}"
		if H == 0:
			print(row)
		else:
			historyLines.append(row)

	if H == 1:
		return historyLines

def cellsChecked_Search(R, C):
	"""Verifica si una casilla ya ha sido evaluada"""
	for i in range(len(globals.cellsChecked)):
		if globals.cellsChecked[i][0] == (R+1) and globals.cellsChecked[i][1] == (C+1):
			return True
	return False

def gameCell_Check(R, C):
	"""Descubre recursivamente las casillas alrededor de la seleccionada, siguiendo reglas de Buscaminas"""
	if (R-1, C-1) in globals.freePositions:
		globals.freePositions.remove((R-1, C-1))

	if cellsChecked_Search((R-1), (C-1)) == False:
		globals.cellsChecked.append([R, C])
	
	globals.T = globals.T + 1
	if globals.T <= (globals.gameRows*globals.gameColumns):
		minesAround = 0
		for a in range(3):
			y = R - a
			if (globals.gameRows-1) < y or y < 0:
				continue
			else:
				for b in range(3):
					x = C - b
					if (globals.gameColumns-1) < x or x < 0:
						continue
					else:
						if globals.Mines[y][x] == 1:
							minesAround += 1
		if minesAround > 0:
			globals.Board[R-1][C-1] = minesAround
		else:
			for a in range(3):
				y = R - a
				if (globals.gameRows-1) < y or y < 0:
					continue
				else:
					for b in range(3):
						x = C - b
						if (globals.gameColumns-1) < x or x < 0:
							continue
						else:
							if globals.Mines[y][x] == 1:
								minesAround += 1
							else:
								if globals.Board[y][x] == "■":
									globals.Board[y][x] = "□"
									gameCell_Check((y+1), (x+1))
								elif globals.Board[y][x] == "□":
									if cellsChecked_Search(y, x) == True:
										continue
									else:
										gameCell_Check((y+1), (x+1))
								else:
									continue
		return globals.T
	else:
		return globals.T
