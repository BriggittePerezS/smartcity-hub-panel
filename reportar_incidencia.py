# =====================================================================
# PROYECTO: SMARTCITY HUB - REPORTE DINÁMICO
# DESARROLLADORA: Ing. Briggitte Pérez
# =====================================================================

import sqlite3

# 1. Conectamos a la base de datos
conexion = sqlite3.connect('smartcity.db')
cursor = conexion.cursor()

print("--- SISTEMA DE REPORTE DE INCIDENCIAS URBANAS ---")
print("Por favor, introduce los datos de la nueva incidencia:")

# 2. EL NUEVO INGREDIENTE: input()
# Esta función muestra un mensaje en la terminal y se queda esperando 
# a que el usuario escriba algo y pulse Enter. Lo que escriba se guarda en la variable.
id_inc = input("1. Introduce el número (ID) de la incidencia: ")
texto_descripcion = input("2. Describe brevemente el problema: ")
nivel_prioridad = input("3. Introduce la prioridad (Baja, Media, Alta): ")

# Dejamos estos valores fijos por ahora para agilizar las pruebas
estado_inicial = "Abierta"
id_ciudadano_anonimo = 102 

# 3. Insertamos los datos en la tabla usando las variables del usuario
# Los signos de interrogación '?' son huecos que Python rellenará con lo que escribió el usuario
cursor.execute('''
INSERT INTO incidencias (id_incidencia, descripcion, estado, prioridad, id_ciudadano)
VALUES (?, ?, ?, ?, ?);
''', (id_inc, texto_descripcion, estado_inicial, nivel_prioridad, id_ciudadano_anonimo))

# 4. Guardamos los cambios de forma definitiva en el archivo
conexion.commit()

print("\n¡Procesando...!")
print(f"¡Éxito! La incidencia '{texto_descripcion}' ha sido guardada en la base de datos.")

# 5. Cerramos la conexión
conexion.close() 