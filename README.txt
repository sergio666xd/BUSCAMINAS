BUSCAMINAS - Juego Interactivo en Terminal
==========================================

Autor: Sergio Muñoz Marín
Semestre: 2025-2 | Universidad Nacional de Colombia, Sede Medellín

Repositorio Github:
https://github.com/sergio666xd/BUSCAMINAS

DESCRIPCIÓN DEL JUEGO
=====================
Buscaminas es una implementación clásica del juego Minesweeper en terminal, 
desarrollado en Python. El objetivo es descubrir todas las casillas seguras 
sin detonar ninguna mina.

CARACTERÍSTICAS PRINCIPALES
===========================

1. GESTIÓN DE JUGADORES
   - Crear nuevos jugadores
   - Cargar jugadores existentes
   - Eliminar jugadores y su historial
   - Estadísticas de partidas (jugadas, ganadas, perdidas)

2. CONFIGURACIÓN DE PARTIDA
   - Definir dimensiones del tablero (filas x columnas)
   - Seleccionar cantidad de minas
   - Elegir modo de juego

3. MODOS DE JUEGO
   
   a) Modo Normal:
      - Seleccionar manualmente cada casilla (fila y columna)
      - Revelar o marcar casillas
      - Control total sobre las selecciones
   
   b) Modo Aleatorio:
      - Generar casillas aleatoriamente
      - Opción de aceptar, rechazar o generar nuevamente
      - Posibilidad de ingresar casillas manualmente en cualquier momento

4. MECÁNICA DEL JUEGO
   - Revelar casillas: descubre la casilla seleccionada
   - Marcar casillas: marca como sospechosa de contener mina
   - Cambiar modo: alterna entre revelar y marcar
   - Reveladera automática: descubre recursivamente casillas adyacentes
     sin minas cuando se revela una casilla sin minas cercanas

5. SISTEMA DE GUARDADO
   - Guardado automático después de cada jugada
   - Guardado manual de partidas en cualquier momento
   - Carga de partidas guardadas
   - Eliminación de partidas guardadas
   - Historial completo de partidas con tableros finales

6. HISTORIAL
   - Registro de todas las partidas jugadas
   - Información de inicio y fin de cada partida
   - Tablero final de cada partida
   - Visualización en editor de texto del sistema

REQUISITOS
==========
- Python 3.6 o superior
- Sistema operativo: Windows, macOS o Linux

INSTALACIÓN
===========
1. Clonar el repositorio:
   git clone https://github.com/sergio666xd/BUSCAMINAS

2. Navegar a la carpeta del proyecto:
   cd BUSCAMINAS

3. Ejecutar el juego:
   python main.py

ESTRUCTURA DEL PROYECTO
=======================
BUSCAMINAS/
├── main.py              # Punto de entrada del programa
├── Game/
│   ├── __init__.py
│   ├── globals.py       # Variables globales del estado del juego
│   ├── utils.py         # Funciones auxiliares
│   ├── menus.py         # Gestión de menús y jugadores
│   ├── game.py          # Lógica principal del juego
│   ├── board.py         # Gestión del tablero y algoritmos
│   └── save.py          # Sistema de guardado y carga
├── Game/players/        # Almacenamiento de datos de jugadores
└── README.txt           # Este archivo

CONTROLES EN JUEGO
==================
Modo Normal:
  - Fila: número de fila (1 a N)
  - Columna: número de columna (1 a N)
  - m: cambiar modo (revelar/marcar)
  - s: guardar partida
  - q: salir (con opción de guardar)

Modo Aleatorio:
  - r: generar casilla aleatoria
  - i: ingresar casilla manualmente
  - m: cambiar modo (revelar/marcar)
  - s: guardar partida
  - q: salir (con opción de guardar)

REGLAS DEL JUEGO
================
1. El objetivo es revelar todas las casillas sin minas
2. Las minas nunca aparecen en la primera casilla revelada
3. Los números indican cuántas minas hay adyacentes a esa casilla
4. Las casillas en blanco indican que no hay minas cercanas
5. Marcar casillas ayuda a identificar minas sospechosas
6. El juego termina cuando:
   - Se revela una mina (PERDIDA)
   - Se revelan todas las casillas seguras (VICTORIA)

NOTAS TÉCNICAS
==============
- Los datos se almacenan en archivos de texto en ./Game/players/
- El guardado automático ocurre después de cada jugada
- Las partidas se pueden cargar desde cualquier estado
- El historial se mantiene permanentemente por jugador
