# =====================================================================
# PROYECTO: SMARTCITY HUB - ELIMINACIÓN DE DATOS
# DESARROLLADORA: Ing. Briggitte Pérez
# =====================================================================

import sqlite3

# 1. Conectamos a la base de datos
conexion = sqlite3.connect('smartcity.db')
cursor = conexion.cursor()

print("--- MÓDULO DE LIMPIEZA: BORRAR INCIDENCIA ---")

# Vamos a borrar la incidencia número 2 (el bache de la Calle Alcalá)
id_a_borrar = 2

# 2. Ejecutamos el comando SQL DELETE
# Le decimos: "BORRA DE la tabla incidencias DONDE el id sea 2"
cursor.execute('''
DELETE FROM incidencias 
WHERE id_incidencia = ?;
''', (id_a_borrar,))

# 3. Guardamos los cambios en el archivo duro
conexion.commit()

print(f"\n¡Limpieza realizada! La incidencia #{id_a_borrar} ha sido eliminada del sistema.")

# 4. Cerramos la conexión
conexion.close()