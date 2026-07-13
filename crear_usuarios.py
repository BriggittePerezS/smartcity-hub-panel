from werkzeug.security import generate_password_hash
import sqlite3

# 1. Conectar a la base de datos existente
conexion = sqlite3.connect('smartcity.db')
cursor = conexion.cursor()

# 2. Crear la tabla de usuarios si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT UNIQUE NOT NULL,
        clave_hash TEXT NOT NULL,
        rol TEXT NOT NULL
    );
''')

# 3. Generar los hashes encriptados de nivel profesional
hash_admin = generate_password_hash("1234")
hash_vecino = generate_password_hash("abcd")
hash_briggitte = generate_password_hash("secreto123")  # 🌟 NUEVO

# 4. Insertar los usuarios uno a uno con bloques TRY independientes
# Así, si 'admin' ya existe, no bloqueará la creación de tu usuario nuevo.

# --- Registrar Admin ---
try:
    cursor.execute("INSERT INTO usuarios (nombre_usuario, clave_hash, rol) VALUES ('admin', ?, 'operario');", (hash_admin,))
    conexion.commit()
    print("✅ Usuario 'admin' registrado.")
except sqlite3.IntegrityError:
    print("👍 'admin' ya existía.")

# --- Registrar Vecino ---
try:
    cursor.execute("INSERT INTO usuarios (nombre_usuario, clave_hash, rol) VALUES ('vecino', ?, 'ciudadano');", (hash_vecino,))
    conexion.commit()
    print("✅ Usuario 'vecino' registrado.")
except sqlite3.IntegrityError:
    print("👍 'vecino' ya existía.")

# --- Registrar Briggitte (🌟 NUEVO) ---
try:
    cursor.execute("INSERT INTO usuarios (nombre_usuario, clave_hash, rol) VALUES ('briggitte', ?, 'ciudadano');", (hash_briggitte,))
    conexion.commit()
    print("✅ Usuario 'briggitte' registrado con éxito para pruebas dinámicas.")
except sqlite3.IntegrityError:
    print("👍 'briggitte' ya existía.")

conexion.close()
print("\n🔒 Base de datos sincronizada y segura.")