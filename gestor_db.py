import sqlite3

DATABASE = 'smartcity.db'

def obtener_conexion():
    """Establece la conexión con SQLite, configura el modo diccionario y crea las tablas necesarias."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    
    cursor = conn.cursor()
    
    # --- PARCHES DE SEGURIDAD EXISTENTES ---
    try:
        cursor.execute("ALTER TABLE incidencias ADD COLUMN foto_url TEXT;")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE incidencias ADD COLUMN ubicacion TEXT;")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE incidencias ADD COLUMN fecha_registro TEXT;")
        conn.commit()
    except sqlite3.OperationalError:
        pass
        
    # --- 🛠️ NUEVA TABLA DE AUDITORÍA (PUNTO 10) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auditoria (
            id_log INTEGER PRIMARY KEY AUTOINCREMENT,
            id_incidencia INTEGER,
            usuario TEXT,
            accion TEXT,
            detalle TEXT,
            fecha TEXT
        );
    ''')
    conn.commit()
        
    return conn


# --- 1. BUSCAR USUARIO ---
def buscar_usuario(nombre_usuario):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nombre_usuario, clave_hash, rol FROM usuarios WHERE nombre_usuario = ?;", (nombre_usuario,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario


# --- ✨ NUEVO: 1c. REGISTRAR / INSERTAR USUARIO (Para cuentas nuevas de vecinos) ---
def insertar_usuario(nombre_usuario, clave_hash, rol='vecino'):
    """Inserta un nuevo usuario en la tabla usuarios de forma segura."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO usuarios (nombre_usuario, clave_hash, rol)
            VALUES (?, ?, ?);
        ''', (nombre_usuario, clave_hash, rol))
        conn.commit()
        exito = True
    except Exception as e:
        print(f"❌ Error crítico al insertar usuario en BD: {e}")
        exito = False
    finally:
        conn.close()
    return exito


# --- 1b. ACTUALIZAR CLAVE DE USUARIO ---
def actualizar_clave_usuario(id_usuario, nuevo_hash):
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE usuarios SET clave_hash = ? WHERE id_usuario = ?;", (nuevo_hash, id_usuario))
        conn.commit()
        exito = True
    except Exception as e:
        print(f"❌ Error al actualizar la contraseña: {e}")
        exito = False
    finally:
        conn.close()
    return exito


# --- 2. LISTAR TODAS LAS INCIDENCIAS ---
def listar_incidencias():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id_incidencia, descripcion, ubicacion, estado, prioridad, foto_url, fecha_registro FROM incidencias;")
    filas = cursor.fetchall()
    conn.close()
    return filas


# --- 3. LISTAR INCIDENCIAS PROPIAS ---
def listar_incidencias_por_ciudadano(id_ciudadano):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id_incidencia, descripcion, ubicacion, estado, prioridad, foto_url, fecha_registro FROM incidencias WHERE id_ciudadano = ?;", (id_ciudadano,))
    filas = cursor.fetchall()
    conn.close()
    return filas


# --- 4. INSERTAR INCIDENCIA ---
def insertar_incidencia(desc, ubicacion, foto_url, id_ciudadano):
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        if id_ciudadano is None or id_ciudadano == 1:
            id_ciudadano = 102 

        cursor.execute('''
            INSERT INTO incidencias (descripcion, ubicacion, estado, prioridad, id_ciudadano, foto_url, fecha_registro)
            VALUES (?, ?, 'Abierta', 'Media', ?, ?, DATETIME('now', 'localtime'));
        ''', (desc, ubicacion, id_ciudadano, foto_url))
        conn.commit()
        
        id_autogenerado = cursor.lastrowid
        
        cursor.execute("SELECT fecha_registro FROM incidencias WHERE id_incidencia = ?;", (id_autogenerado,))
        fecha_guardada = cursor.fetchone()['fecha_registro']
        
        exito = {"id": id_autogenerado, "fecha": fecha_guardada}
    except Exception as e:
        print(f"❌ Error crítico al insertar en BD: {e}")
        exito = False
    finally:
        conn.close()
    return exito


# --- 5. ACTUALIZAR ESTADO (SELECTOR EN VIVO CON LOG) ---
def actualizar_estado_incidencia(id_inc, nuevo_estado, usuario_operario):
    """Actualiza el estado y registra el movimiento en la auditoría."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        # Recuperamos el estado anterior para guardarlo en el log
        cursor.execute("SELECT estado FROM incidencias WHERE id_incidencia = ?;", (id_inc,))
        fila = cursor.fetchone()
        estado_anterior = fila['estado'] if fila else 'Desconocido'

        cursor.execute("UPDATE incidencias SET estado = ? WHERE id_incidencia = ?;", (nuevo_estado, id_inc))
        
        # 📝 Insertamos en la bitácora de auditoría
        detalle = f"Cambio de estado: de '{estado_anterior}' a '{nuevo_estado}'"
        cursor.execute('''
            INSERT INTO auditoria (id_incidencia, usuario, accion, detalle, fecha)
            VALUES (?, ?, 'Actualizar Estado', ?, DATETIME('now', 'localtime'));
        ''', (id_inc, usuario_operario, detalle))
        
        conn.commit()
        exito = True
    except Exception as e:
        print(f"❌ Error al actualizar estado con auditoría: {e}")
        exito = False
    finally:
        conn.close()
    return exito


# --- 5b. ACTUALIZAR PRIORIDAD (SELECTOR EN VIVO CON LOG) ---
def actualizar_prioridad_incidencia(id_inc, nueva_prioridad, usuario_operario):
    """Actualiza la prioridad y registra el movimiento en la auditoría."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        # Recuperamos la prioridad anterior para el log
        cursor.execute("SELECT prioridad FROM incidencias WHERE id_incidencia = ?;", (id_inc,))
        fila = cursor.fetchone()
        prioridad_anterior = fila['prioridad'] if fila else 'Desconocido'

        cursor.execute("UPDATE incidencias SET prioridad = ? WHERE id_incidencia = ?;", (nueva_prioridad, id_inc))
        
        # 📝 Insertamos en la bitácora de auditoría
        detalle = f"Cambio de prioridad: de '{prioridad_anterior}' a '{nueva_prioridad}'"
        cursor.execute('''
            INSERT INTO auditoria (id_incidencia, usuario, accion, detalle, fecha)
            VALUES (?, ?, 'Actualizar Prioridad', ?, DATETIME('now', 'localtime'));
        ''', (id_inc, usuario_operario, detalle))
        
        conn.commit()
        exito = True
    except Exception as e:
        print(f"❌ Error al actualizar prioridad con auditoría: {e}")
        exito = False
    finally:
        conn.close()
    return exito


# --- 5c. NUEVO: LISTAR LOGS DE AUDITORÍA (PUNTO 10) ---
def listar_logs_auditoria():
    """Recupera los últimos 50 movimientos registrados en la bitácora."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id_log, id_incidencia, usuario, accion, detalle, fecha FROM auditoria ORDER BY id_log DESC LIMIT 50;")
    filas = cursor.fetchall()
    conn.close()
    return filas


# --- 6. ELIMINAR INCIDENCIA ---
def eliminar_incidencia(id_inc):
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM incidencias WHERE id_incidencia = ?;", (id_inc,))
        conn.commit()
        exito = True
    except Exception as e:
        print(f"❌ Error al eliminar incidencia: {e}")
        exito = False
    finally:
        conn.close()
    return exito


# --- 7. OBTENER ESTADISTICAS ---
def obtener_estadisticas():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidencias;")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM incidencias WHERE estado = 'Abierta';")
    abiertas = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM incidencias WHERE estado = 'En Proceso';")
    proceso = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM incidencias WHERE estado = 'Resuelta';")
    resueltas = cursor.fetchone()[0]
    conn.close()
    return {"total": total, "abiertas": abiertas, "proceso": proceso, "resueltas": resueltas}