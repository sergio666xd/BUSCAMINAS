import os

def clear():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

def head(): # Encabezado
	clear()
	print(WelcomeMsg)

def NumTry(N): #Evaluar si es posible convertir el input srt en e
	try :
		int(N)
		return False
	except :
		return True

def MinasCheck(N):
	if NumTry(N) == False :
		N = int(N)
		T = gameRows * gameColumns
		print(T)
		if 0 < N <= T :
			return False
		else :
			return True
	else :
		return True

def gameBoard():
	Board = ["" for x in range(gameRows)]
	for r in range(gameRows+1):
		if r == 0 :
			row = " "
			for c in range(gameColumns):
				row = f"{row} {c+1}"
		else :
			y = r-1
			Board[y] = ["▣" for x in range(gameRows)]
			row = f"{r}"
			for c in range(gameColumns):
				row = f"{row} {Board[y][c]}"
		print(row)

WelcomeMsg = "¡Bienvenido al Buscaminas!\n"

head();
playerName = input("Ingresa tu nombre --> ")

WelcomeMsg = f"Hola, {playerName}. {WelcomeMsg}"

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
	print("ERROR! El número de columbas debe ser un número entero mayor que cero\n")

	gameColumns = input("Ingresa número de columnas --> ")

gameColumns = int(gameColumns)

head()
print(f"Número de filas ingresado: {gameRows} | Número de columnas ingresado: {gameColumns}\n")
gameMines = input("Ingresa número de Minas --> ")

while MinasCheck(gameMines) :
	head()
	print(f"Número de filas ingresado: {gameRows}\n")
	print("ERROR! El número de minas debe ser un número entero mayor que cero\n")

	gameMines = input("Ingresa número de Minas --> ")

gameMines = int(gameMines)

WelcomeMsg = f"BUSCAMINAS | Jugador: {playerName}\n"
head()
print(f"Tablero {gameRows}x{gameColumns} | Minas: {gameMines}\n")

gameBoard()