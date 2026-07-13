# =====================================================================
# PROYECTO: SMARTCITY HUB - LECTURA DE DATOS
# DESARROLLADORA: Ing. Briggitte Pérez
# =====================================================================

import sqlite3

# 1. Abrimos la conexión con la base de datos
conexion = sqlite3.connect('smartcity.db')
cursor = conexion.cursor()

print("--- INFORME DE INCIDENCIAS EN TIEMPO REAL ---")

# 2. Le pedimos al cursor que ejecute un SELECT completo
cursor.execute("SELECT id_incidencia, descripcion, estado, prioridad FROM incidencias;")

# 3. EL NUEVO INGREDIENTE: fetchall()
# 'fetchall' significa "tráeme todo". Le dice a Python que guarde todas 
# las filas que encontró el SELECT dentro de una variable llamada 'filas'.
filas = cursor.fetchall()

# 4. Recorremos las filas una a una para mostrarlas bonitas en la pantalla
for fila in filas:
    print(f"🚨 Incidencia #{fila[0]}: {fila[1]}")
    print(f"   Estado: {fila[2]} | Prioridad: {fila[3]}")
    print("-" * 40)

# 5. Cerramos la conexión (aquí no hace falta .commit() porque solo estamos leyendo, no guardando nada nuevo)
conexion.close()