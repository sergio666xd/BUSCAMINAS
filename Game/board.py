import random

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
	from . import game
	Board = [["■" for c in range(game.gameColumns)] for r in range(game.gameRows)]
	return Board

def gameMines_New(R, C):
	"""Genera el tablero de minas, excluyendo el área protegida alrededor de la primera jugada"""
	from . import game

	protected = set()
	for r in range(-1, 2):
		for c in range(-1, 2):
			pr, pc = R - 1 + r, C - 1 + c
			if 0 <= pr < game.gameRows and 0 <= pc < game.gameColumns:
				protected.add((pr, pc))

	positions = [(r, c) for r in range(game.gameRows) for c in range(game.gameColumns) if (r, c) not in protected]
	minePositions = random.sample(positions, min(game.gameMines, len(positions)))

	Mines = [[0 for c in range(game.gameColumns)] for r in range(game.gameRows)]
	for r, c in minePositions:
		Mines[r][c] = 1

	game.freePositions = [(r, c) for r in range(game.gameRows) for c in range(game.gameColumns) if (r, c) not in minePositions]

	return Mines

def gameBoard(T, H):
	"""Imprime el tablero con numeración de filas y columnas, o lo retorna como lista de strings para historial"""
	from . import game

	print("")
	historyLines = []
	if game.gameColumns >= 10:
		row = "    "
		for c in range(game.gameColumns):
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

	for r in range(game.gameRows+1):
		if r == 0:
			for c in range(game.gameColumns):
				if (c+1) >= 10:
					row = f"{row} {(c+1)%10}"
				else:
					row = f"{row} {c+1}"
			if H == 0:
				print(row)
			else:
				historyLines.append(row)
			row = "    "
			for c in range(game.gameColumns):
				row = f"{row}--"
		else:
			y = r-1
			if r//10 != 0:
				row = f"{r} |"
			else:
				row = f'{" "}{r} |'

			for c in range(game.gameColumns):
				if T == 0:
					if H == 0:
						value = game.Board[y][c]
					else:
						if game.Board[y][c] == "⊠":
							value = "X"
						elif game.Board[y][c] == "■":
							value = "0"
						elif game.Board[y][c] == "▣":
							value = "-"
						elif game.Board[y][c] == "□":
							value = " "
						else:
							value = game.Board[y][c]
					row = f"{row} {value}"
				else:
					row = f"{row} {game.Mines[y][c]}"
		if H == 0:
			print(row)
		else:
			historyLines.append(row)

	if H == 1:
		return historyLines

def cellsChecked_Search(R, C):
	"""Verifica si una casilla ya ha sido evaluada"""
	from . import game

	for i in range(len(game.cellsChecked)):
		if game.cellsChecked[i][0] == (R+1) and game.cellsChecked[i][1] == (C+1):
			return True
	return False

def gameCell_Check(R, C):
	"""Descubre recursivamente las casillas alrededor de la seleccionada, siguiendo reglas de Buscaminas"""
	from . import game

	if (R-1, C-1) in game.freePositions:
		game.freePositions.remove((R-1, C-1))

	if cellsChecked_Search((R-1), (C-1)) == False:
		game.cellsChecked.append([R, C])
	
	game.T = game.T + 1
	if game.T <= (game.gameRows*game.gameColumns):
		minesAround = 0
		for a in range(3):
			y = R - a
			if (game.gameRows-1) < y or y < 0:
				continue
			else:
				for b in range(3):
					x = C - b
					if (game.gameColumns-1) < x or x < 0:
						continue
					else:
						if game.Mines[y][x] == 1:
							minesAround += 1
		if minesAround > 0:
			game.Board[R-1][C-1] = minesAround
		else:
			for a in range(3):
				y = R - a
				if (game.gameRows-1) < y or y < 0:
					continue
				else:
					for b in range(3):
						x = C - b
						if (game.gameColumns-1) < x or x < 0:
							continue
						else:
							if game.Mines[y][x] == 1:
								minesAround += 1
							else:
								if game.Board[y][x] == "■":
									game.Board[y][x] = "□"
									gameCell_Check((y+1), (x+1))
								elif game.Board[y][x] == "□":
									if cellsChecked_Search(y, x) == True:
										continue
									else:
										gameCell_Check((y+1), (x+1))
								else:
									continue
		return game.T
	else:
		return game.T
