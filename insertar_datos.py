# =====================================================================
# PROYECTO: SMARTCITY HUB - INSERCIÓN DE DATOS
# DESARROLLADORA: Ing. Briggitte Pérez
# =====================================================================

import sqlite3

# 1. Abrimos el canal con nuestra base de datos existente
conexion = sqlite3.connect('smartcity.db')
cursor = conexion.cursor()

print("Conectados para insertar datos...")

# 2. Insertamos un Ciudadano (Carlos Mendoza)
# Usamos el comando SQL que ya te sabes de memoria
cursor.execute('''
INSERT INTO Ciudadanos (id_ciudadano, nombre, email) 
VALUES (102, 'Carlos Mendoza', 'carlos@madtech.com');
''')

# 3. Insertamos la Incidencia del semáforo asignada a ese ciudadano (ID 102)
cursor.execute('''
INSERT INTO incidencias (id_incidencia, descripcion, estado, prioridad, id_ciudadano) 
VALUES (1, 'Semaforo roto en Gran Via', 'Abierta', 'Alta', 102);
''')

# 4. EL PASO CRUCIAL: Guardamos los cambios en el archivo
conexion.commit()

# 5. Cerramos la conexión
conexion.close()

print("¡Datos insertados con éxito en el sistema por la Ingeniera Briggitte!")