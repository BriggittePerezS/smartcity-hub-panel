# =====================================================================
# PROYECTO: SMARTCITY HUB - CONSULTA AVANZADA (JOIN)
# DESARROLLADORA: Ing. Briggitte Pérez
# =====================================================================

import sqlite3

# 1. Conectamos a la base de datos
conexion = sqlite3.connect('smartcity.db')
cursor = conexion.cursor()

print("--- INFORME INTEGRADO: INCIDENCIAS + CIUDADANOS ---")

# 2. El supercomando SQL: Unimos ambas tablas por el ID del ciudadano
consulta_join = '''
SELECT incidencias.id_incidencia, incidencias.descripcion, Ciudadanos.nombre, Ciudadanos.email
FROM incidencias
INNER JOIN Ciudadanos ON incidencias.id_ciudadano = Ciudadanos.id_ciudadano;
'''

cursor.execute(consulta_join)
resultados = cursor.fetchall()

# 3. Mostramos los datos cruzados por pantalla
for fila in resultados:
    print(f"🚨 Incidencia #{fila[0]}: {fila[1]}")
    print(f"   Reportada por: {fila[2]} ({fila[3]})")
    print("-" * 50)

# 4. Cerramos la conexión
conexion.close()