# =====================================================================
# PROYECTO: SMARTCITY HUB - ACTUALIZACIÓN DE DATOS
# DESARROLLADORA: Ing. Briggitte Pérez
# =====================================================================

import sqlite3

# 1. Conectamos a la base de datos
conexion = sqlite3.connect('smartcity.db')
cursor = conexion.cursor()

print("--- MÓDULO DE MANTENIMIENTO: RESOLVER INCIDENCIA ---")

# ID de la incidencia que queremos arreglar (el semáforo de Gran Vía)
id_a_resolver = 1
nuevo_estado = "Resuelta"

# 2. Ejecutamos el comando SQL UPDATE
# Le decimos: "Modifica la tabla incidencias, PON el estado como 'Resuelta' DONDE el id sea 1"
cursor.execute('''
UPDATE incidencias 
SET estado = ? 
WHERE id_incidencia = ?;
''', (nuevo_estado, id_a_resolver))

# 3. ¡MUY IMPORTANTE! Al modificar datos, necesitamos guardar los cambios
conexion.commit()

print(f"\n¡Operación realizada! La incidencia #{id_a_resolver} ha sido marcada como '{nuevo_estado}'.")

# 4. Cerramos la conexión
conexion.close()