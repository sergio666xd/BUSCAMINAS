"""Módulo central de estado global del juego"""

# Estado del menú
headMsg = ""
players = []
playerName = ""
savedGamesDir = ""

# Estado del juego
gameRows = 0
gameColumns = 0
gameMines = 0
gameMode = "normal"  # "normal" o "random"
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

# Estado del guardado
autosaveFile = ""
played = 0
