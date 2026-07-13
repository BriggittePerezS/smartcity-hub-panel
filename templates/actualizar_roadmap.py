import sqlite3

def actualizar_sistema():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    print("Prerando mejoras de base de datos...")
    
    # 1. Añadir columna prioridad a incidencias (si no existe)
    try:
        cursor.execute("ALTER TABLE incidencias ADD COLUMN prioridad TEXT DEFAULT 'Media';")
        print("-> Columna 'prioridad' añadida con éxito.")
    except sqlite3.OperationalError:
        print("-> La columna 'prioridad' ya existía.")
        
    # 2. Crear tabla de logs/auditoría
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_auditoria (
            id_log INTEGER PRIMARY KEY AUTOINCREMENT,
            id_incidencia INTEGER,
            usuario TEXT,
            accion TEXT,
            fecha_accion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_incidencia) REFERENCES incidencias(id_incidencia)
        )
    ''')
    print("-> Tabla de 'logs_auditoria' verificada/creada con éxito.")
    
    conn.commit()
    conn.close()
    print("¡Base de datos lista para el Roadmap Pro!")

if __name__ == '__main__':
    actualizar_sistema()