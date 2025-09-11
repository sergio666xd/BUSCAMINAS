import sys

print("¡Bienvenido al Buscaminas!")
print("")

playerName = input("Ingresa tu nombre: ")

gameRows = int(input("Ingresa número de filas: "))
gameColumns = int(input("Ingresa número de columnas: "))

print(f"Hola, {playerName}. Tu tablero de juego será de {gameRows}x{gameColumns}.")