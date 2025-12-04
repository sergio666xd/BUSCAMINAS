import os
import datetime
import platform
import subprocess
import shutil
from time import sleep
from . import globals
from .utils import head

def menu():
	"""Menú principal: muestra jugadores guardados o permite crear uno nuevo"""
	globals.players = os.listdir('./Game/players')
	globals.headMsg = "¡Bienvenido al Buscaminas!\n"
	head()

	print("-- Jugadores --\n")
	for i in range(len(globals.players)):
		print(f'{i+1} -> {globals.players[i]}')
	print("\n0 -> Nuevo Jugador")
	print("s -> Salir\n")

	menuSel = input("Selecciona opción --> ")
	if menuSel == "s":
		print("\n--- Salida exitosa ---")
		exit()
	else:
		try:
			menuSel = int(menuSel)
			check = True
		except:
			check = False

		if check == True:
			if 0 < menuSel <= len(globals.players):
				player_menu(globals.players[menuSel-1])
			elif menuSel == 0:
				newPlayer()
			else:
				menu()
		else:
			menu()

def newPlayer():
	"""Crea un nuevo jugador y su carpeta de guardado"""
	globals.headMsg = "¡Bienvenido al Buscaminas!\n"
	head()

	playerName = input("\nIngresa tu nombre --> ")
	globals.headMsg = f"Hola, {playerName}. ¡Bienvenido al Buscaminas!\n"

	while playerName == "":
		head()
		print("ERROR! El nombre no puede estar vacío\n")
		playerName = input("Ingresa tu nombre --> ")

	if playerName in globals.players:
		for i in range(len(globals.players)):
			if globals.players[i] == playerName:
				p = i
		player_menu(globals.players[p])
	else:
		newDir = f'./Game/players/{playerName}'
		os.mkdir(newDir)
		print("Carpeta creada exitosamente.")
		playerData_File = f'./Game/players/{playerName}/playerData.txt'
		with open(playerData_File, 'w', encoding='utf-8') as playerData:
			playerData.write("0\n")
			playerData.write("0\n")
			playerData.write("0")
		
		now = datetime.datetime.now()

		with open(f'./Game/players/{playerName}/playerHistory.txt', 'w', encoding='utf-8') as playerHistory:
			playerHistory.write(f'--- Historial de Partidas (Jugador: "{playerName}") ---\n')
			playerHistory.write(f'Creado el {now.strftime("%d/%m/%Y a las %H:%M:%S")}\n')
		player_menu(playerName)

def savedGames():
	"""Muestra las partidas guardadas del jugador y permite cargar una"""
	from .save import loadGame

	globals.headMsg = f"BUSCAMINAS | Jugador: {globals.playerName}\n\n-- Partidas Guardadas --\n"
	head()

	globals.savedGamesDir = f'./Game/players/{globals.playerName}/savedGames'
	try:
		os.mkdir(globals.savedGamesDir)
	except FileExistsError:
		pass

	savedGamesList = os.listdir(globals.savedGamesDir)

	if savedGamesList == []:
		print("No hay partidas guardadas.\n")
		print("\nVolviendo al Menú de Jugador...")
		sleep(2)
		player_menu(globals.playerName)
	else:
		try:
			savedGamesList.sort(key=lambda x: datetime.datetime.strptime(x.split('_')[1] + ' ' + x.split('_')[2], '%d-%m-%Y %H-%M-%S'))
		except:
			pass

		validGames = []
		for i in range(len(savedGamesList)):
			try:
				date_str = savedGamesList[i].split('_')[1]
				time_str = savedGamesList[i].split('_')[2]
				dt = datetime.datetime.strptime(date_str + ' ' + time_str, '%d-%m-%Y %H-%M-%S')
				with open(f'{globals.savedGamesDir}/{savedGamesList[i]}', 'r', encoding='utf-8') as saveFile:
					lines = saveFile.readlines()
					dimensions = lines[1].strip().split(',')
					rows = int(dimensions[0])
					columns = int(dimensions[1])
					mines = int(dimensions[2])
					gameMode = lines[2].strip() if len(lines) > 2 else "normal"
				
				modeLabel = "Aleatorio" if gameMode == "random" else "Normal"
				
				if "AUTOSAVE" in savedGamesList[i]:
					print(f'{i+1} -> {dt.strftime("%d/%m/%Y a las %H:%M:%S")} | {rows}x{columns} M={mines} | Modo: {modeLabel} | (AUTO GUARDADO)')
				else:
					print(f'{i+1} -> {dt.strftime("%d/%m/%Y a las %H:%M:%S")} | {rows}x{columns} M={mines} | Modo: {modeLabel}')
				validGames.append(i)
			except:
				print(f'Archivo no válido: {savedGamesList[i]}')
		print("\ns -> Volver\n")
		
		print("Número de partida | d = Eliminar partida")
		menuSel = input("Selecciona opción --> ")
		
		if menuSel == "s":
			player_menu(globals.playerName)
		elif menuSel == "d":
			delSel = input("\nNúmero de partida a eliminar --> ")
			try:
				delSel = int(delSel)
				check = True
			except:
				check = False

			if check == True:
				if 0 < delSel <= len(savedGamesList) and (delSel-1) in validGames:
					print(f"\nEliminando partida: {savedGamesList[delSel-1]}")
					saveFilePath = f'{globals.savedGamesDir}/{savedGamesList[delSel-1]}'
					try:
						os.remove(saveFilePath)
						print("Partida eliminada exitosamente.")
					except FileNotFoundError:
						print("Error: No se encontró el archivo de la partida.")
					sleep(2)
					savedGames()
				else:
					savedGames()
			else:
				savedGames()
		else:
			try:
				menuSel = int(menuSel)
				check = True
			except:
				check = False

			if check == True:
				if 0 < menuSel <= len(savedGamesList) and (menuSel-1) in validGames:
					print(f"Cargando partida: {savedGamesList[menuSel-1]}")
					sleep(2)
					loadGame(savedGamesList[menuSel-1])
					player_menu(globals.playerName)
				else:
					savedGames()
			else:
				savedGames()

def player_menu(p):
	"""Página principal del jugador: muestra estadísticas y opciones"""
	from .game import newGame

	globals.playerName = p
	globals.savedGamesDir = f'./Game/players/{globals.playerName}/savedGames'

	playerData_File = f'./Game/players/{globals.playerName}/playerData.txt'
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

	globals.headMsg = f"Hola, {globals.playerName}. ¡Bienvenido al Buscaminas!\n"

	head()
	print(f'Partidas jugadas: {played}\nPartidas ganadas: {wins}\nPartidas perdidas: {defs}')

	print("\n-- Opciones --\n")
	print("1 -> Nueva Partida")
	print("2 -> Partidas Guardadas")
	print("3 -> Ver Historial")
	print("s -> Volver al Menú")
	print("\n0 -> Eliminar Jugador")

	menuSel = input("\nSelecciona opción --> ")
	if menuSel == "s":
		menu()
	else:
		try:
			menuSel = int(menuSel)
			check = True
		except:
			check = False

		if check == True:
			if menuSel == 1:
				newGame()
			elif menuSel == 2:
				savedGames()
			elif menuSel == 3:
				file_path = f'./Game/players/{globals.playerName}/playerHistory.txt'
				try:
					if platform.system() == "Windows":
						subprocess.run(["notepad.exe", file_path])
					elif platform.system() == "Darwin":
						subprocess.run(["open", file_path])
					else:
						subprocess.run(["xdg-open", file_path])
				except FileNotFoundError:
					print(f"Error: No se encontró el archivo '{file_path}'.")
				except subprocess.CalledProcessError:
					print(f"Error al intentar abrir '{file_path}'.")
				player_menu(globals.playerName)
			elif menuSel == 0:
				globals.headMsg = f"Hola, {globals.playerName}. ¡Bienvenido al Buscaminas!\n"
				head()
				check = input("¿Estás seguro que quieres eliminar el jugador? (S/n) --> ")
				if check == "S":
					try:
						playerDir = f'./Game/players/{globals.playerName}'
						shutil.rmtree(playerDir)
						print(f"Directorio '{playerDir}' eliminado correctamente.")
						menu()
					except OSError as e:
						print(f"Error al eliminar el directorio '{playerDir}': {e}")
				else:
					player_menu(globals.playerName)
			else:
				player_menu(globals.playerName)
		else:
			player_menu(globals.playerName)
