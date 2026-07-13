from flask import Flask, render_template, request, redirect, flash, session, jsonify, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
import gestor_db

app = Flask(__name__)
app.secret_key = 'madrid_secreto_2026'

CARPETA_UPLOADS = os.path.join('static', 'uploads')
EXTENSIONES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = CARPETA_UPLOADS
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Crear la carpeta de uploads si no existe localmente
os.makedirs(CARPETA_UPLOADS, exist_ok=True)

def archivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS

@app.route('/')
def home():
    if 'usuario' not in session:
        flash('Debes iniciar sesión para acceder al panel.', 'warning')
        return redirect('/login')

    incidencias = gestor_db.listar_incidencias()
    stats = gestor_db.obtener_estadisticas()
    
    return render_template('index.html', 
                           datos_web=incidencias, 
                           usuario_actual=session['usuario'],
                           rol_actual=session['rol'],
                           stats=stats)

# --- ✨ NUEVA RUTA: ACCESO COMO INVITADO ---
@app.route('/login_invitado')
def login_invitado():
    session.clear()
    session['usuario'] = 'Invitado Anónimo'
    session['rol'] = 'vecino'
    session['id_usuario'] = None  # Al ser invitado, no tiene ID en BD
    flash('Has accedido en modo Invitado (Vecino).', 'info')
    return redirect('/')

# --- ✨ NUEVA RUTA: VISTA Y PROCESAMIENTO DE REGISTRO ---
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form.get('web_usuario').strip()
        clave = request.form.get('web_clave')
        
        if not usuario or not clave:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect('/registro')
            
        # Verificar si el usuario ya existe
        usuario_existente = gestor_db.buscar_usuario(usuario)
        if usuario_existente:
            flash('El nombre de usuario ya está registrado.', 'warning')
            return redirect('/registro')
            
        # Crear hash de la clave e insertar con rol 'vecino' por defecto
        clave_hash = generate_password_hash(clave)
        
        # Nota: Asume que tu 'gestor_db' tiene una función para insertar usuarios. 
        # Si tiene otro nombre en tu script (ej. registrar_usuario), cámbiala aquí.
        exito = gestor_db.insertar_usuario(usuario, clave_hash, 'vecino')
        
        if exito:
            flash('¡Cuenta creada con éxito! Ya puedes iniciar sesión.', 'success')
            return redirect('/login')
        else:
            flash('Error interno al registrar el usuario en la base de datos.', 'danger')
            return redirect('/registro')
            
    return render_template('registro.html')

# --- PERFIL DE USUARIO Y CAMBIO DE CLAVE ---
@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'usuario' not in session:
        flash('Debes iniciar sesión para acceder a tu perfil.', 'warning')
        return redirect('/login')
    
    # Bloqueo preventivo para que el invitado no intente romper la BD cambiando clave
    if session.get('id_usuario') is None:
        flash('Los usuarios invitados no pueden modificar perfiles.', 'warning')
        return redirect('/')
        
    if request.method == 'POST':
        clave_actual = request.form.get('web_clave_actual')
        nueva_clave = request.form.get('web_nueva_clave')
        
        registro = gestor_db.buscar_usuario(session['usuario'])
        
        if registro and check_password_hash(registro['clave_hash'], clave_actual):
            if nueva_clave and len(nueva_clave.strip()) >= 4:
                nuevo_hash = generate_password_hash(nueva_clave)
                exito = gestor_db.actualizar_clave_usuario(session['id_usuario'], nuevo_hash)
                
                if exito:
                    flash('Contraseña actualizada correctamente.', 'success')
                else:
                    flash('Error interno al actualizar en la base de datos.', 'danger')
            else:
                flash('La nueva contraseña debe tener al menos 4 caracteres.', 'warning')
        else:
            flash('La contraseña actual es incorrecta.', 'danger')
            
        return redirect('/perfil')
        
    return render_template('perfil.html', 
                           usuario_actual=session['usuario'], 
                           rol_actual=session['rol'])

# --- API REGISTRAR ---
@app.route('/api/registrar', methods=['POST'])
def api_registrar():
    if 'usuario' not in session:
        return jsonify({"success": False, "error": "No autorizado"}), 401
        
    desc = request.form.get('web_desc')
    ubicacion = request.form.get('web_ubicacion')
    id_usuario_actual = session.get('id_usuario') # Será None si es invitado
    
    if not desc or not ubicacion:
        return jsonify({"success": False, "error": "Campos obligatorios vacíos"}), 400

    nombre_foto_seguro = None
    if 'web_foto' in request.files:
        foto = request.files['web_foto']
        if foto and foto.filename != '':
            if archivo_permitido(foto.filename):
                import time
                nombre_original = secure_filename(foto.filename)
                nombre_foto_seguro = f"img_{int(time.time())}_{nombre_original}"
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_foto_seguro))
            else:
                return jsonify({"success": False, "error": "Formato no permitido"}), 400

    resultado_bd = gestor_db.insertar_incidencia(desc, ubicacion, nombre_foto_seguro, id_usuario_actual)
    
    if resultado_bd:
        return jsonify({
            "success": True, 
            "id": resultado_bd["id"], 
            "descripcion": desc, 
            "ubicacion": ubicacion, 
            "estado": "Abierta", 
            "prioridad": "Media",
            "foto_url": nombre_foto_seguro,
            "fecha_registro": resultado_bd["fecha"]
        })
    else:
        return jsonify({"success": False, "error": "Error interno al guardar en BD"}), 500

# --- API FILTRAR MIS REPORTES ---
@app.route('/api/mis_reportes')
def api_mis_reportes():
    if 'usuario' not in session:
        return jsonify({"success": False, "error": "No autorizado"}), 401
    
    id_usuario_actual = session.get('id_usuario')
    mis_incidencias = gestor_db.listar_incidencias_por_ciudadano(id_usuario_actual)
    
    lista_limpia = []
    for fila in mis_incidencias:
        lista_limpia.append({
            "id_incidencia": fila["id_incidencia"],
            "descripcion": fila["descripcion"],
            "ubicacion": fila["ubicacion"],
            "estado": fila["estado"],
            "prioridad": fila["prioridad"],
            "foto_url": fila["foto_url"],
            "fecha_registro": fila["fecha_registro"]
        })
    return jsonify({"success": True, "incidencias": lista_limpia})

@app.route('/api/todas_incidencias')
def api_todas_incidencias():
    if 'usuario' not in session:
        return jsonify({"success": False, "error": "No autorizado"}), 401
    todas = gestor_db.listar_incidencias()
    lista_limpia = [dict(fila) for fila in todas]
    return jsonify({"success": True, "incidencias": lista_limpia})

# --- API ACTUALIZAR ESTADO ---
@app.route('/api/actualizar_estado', methods=['POST'])
def api_actualizar_estado():
    if 'usuario' not in session or session.get('rol') != 'operario':
        return jsonify({"success": False, "error": "No autorizado"}), 403
    data = request.get_json()
    usuario_activo = session.get('usuario')
    exito = gestor_db.actualizar_estado_incidencia(data.get('web_id'), data.get('web_estado'), usuario_activo)
    return jsonify({"success": True}) if exito else jsonify({"success": False})

# --- API ACTUALIZAR PRIORIDAD ---
@app.route('/api/actualizar_prioridad', methods=['POST'])
def api_actualizar_prioridad():
    if 'usuario' not in session or session.get('rol') != 'operario':
        return jsonify({"success": False, "error": "No autorizado"}), 403
    data = request.get_json()
    usuario_activo = session.get('usuario')
    exito = gestor_db.actualizar_prioridad_incidencia(data.get('web_id'), data.get('web_prioridad'), usuario_activo)
    return jsonify({"success": True}) if exito else jsonify({"success": False})

# --- API OBTENER LOGS DE AUDITORÍA ---
@app.route('/api/auditoria')
def api_auditoria():
    if 'usuario' not in session or session.get('rol') != 'operario':
        return jsonify({"success": False, "error": "No autorizado"}), 403
    logs = gestor_db.listar_logs_auditoria()
    lista_limpia = [dict(fila) for fila in logs]
    return jsonify({"success": True, "logs": lista_limpia})

# --- API BORRAR ---
@app.route('/api/borrar/<id_incidencia>', methods=['DELETE'])
def api_borrar(id_incidencia):
    if 'usuario' not in session or session.get('rol') != 'operario':
        return jsonify({"success": False, "error": "No autorizado"}), 403
    
    exito = gestor_db.eliminar_incidencia(id_incidencia)
    if exito:
        stats_actualizadas = gestor_db.obtener_estadisticas()
        return jsonify({
            "success": True,
            "total": stats_actualizadas["total"],
            "abiertas": stats_actualizadas["abiertas"],
            "proceso": stats_actualizadas["proceso"],
            "resueltas": stats_actualizadas["resueltas"]
        })
    else:
        return jsonify({"success": False}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        registro = gestor_db.buscar_usuario(request.form['web_usuario'])
        if registro and check_password_hash(registro['clave_hash'], request.form['web_clave']):
            session['usuario'] = registro['nombre_usuario']
            session['rol'] = registro['rol']
            session['id_usuario'] = registro['id_usuario']
            return redirect('/')
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            return redirect('/login')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, port=5000)