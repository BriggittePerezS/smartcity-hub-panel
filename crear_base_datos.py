# =====================================================================
# PROYECTO: SMARTCITY HUB
# DESARROLLADORA: Ing. Briggitte Pérez
# EMPRESA: MadTech Solutions
# =====================================================================

# Importamos la librería nativa para bases de datos
import sqlite3

# Conectamos al archivo. 
# Si no existe, Python lo creará mágicamente en nuestra carpeta.
conexion = sqlite3.connect('smartcity.db')

#Creamos el cursor (nuestro intermediario)
cursor = conexion.cursor()

print("¡Conexión establecida con éxito en MadTech Solutions!")

#Creamos la tabla de Ciudadanos si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS Ciudadanos (
    id_ciudadano INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL
);
''')

#Creamos la tabla de Incidencias si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS incidencias (
    id_incidencia INTEGER PRIMARY KEY,
    descripcion TEXT NOT NULL,
    estado TEXT NOT NULL,
    prioridad TEXT NOT NULL,
    id_ciudadano INTEGER,
    FOREIGN KEY (id_ciudadano) REFERENCES Ciudadanos(id_ciudadano)
);
''')

#Guardamos los cambios de forma definitiva
conexion.commit()

# Cerramos la conexión para liberar memoria
conexion.close()

print("¡Base de datos y tablas inicializadas correctamente por la Ingeniera Briggitte!")