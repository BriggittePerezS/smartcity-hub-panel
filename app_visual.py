# =====================================================================
# PROYECTO: SMARTCITY HUB - INTERFAZ COMPLETA (CON FUNCIÓN DE BORRADO)
# DESARROLLADORA: Ing. Briggitte Pérez
# =====================================================================

import tkinter as tk
from tkinter import messagebox
import sqlite3

# --- FUNCIÓN 1: CARGAR/LEER DATOS ---
def cargar_datos():
    caja_texto.delete("1.0", tk.END)
    conexion = sqlite3.connect('smartcity.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT id_incidencia, descripcion, estado FROM incidencias;")
    filas = cursor.fetchall()
    
    caja_texto.insert(tk.END, "--- LISTA DE INCIDENCIAS ---\n\n")
    for fila in filas:
        caja_texto.insert(tk.END, f"🚨 #{fila[0]}: {fila[1]} [{fila[2]}]\n")
        caja_texto.insert(tk.END, "-" * 45 + "\n")
    conexion.close()

# --- FUNCIÓN 2: GUARDAR NUEVA INCIDENCIA ---
def guardar_incidencia():
    id_inc = entrada_id.get()
    desc = entrada_desc.get()
    
    if id_inc == "" or desc == "":
        messagebox.showwarning("Atención", "Por favor, rellena todos los campos.")
        return

    conexion = sqlite3.connect('smartcity.db')
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO incidencias (id_incidencia, descripcion, estado, prioridad, id_ciudadano)
        VALUES (?, ?, 'Abierta', 'Media', 102);
    ''', (id_inc, desc))
    conexion.commit()
    conexion.close()
    
    messagebox.showinfo("Éxito", f"¡Incidencia #{id_inc} guardada correctamente!")
    entrada_id.delete(0, tk.END)
    entrada_desc.delete(0, tk.END)
    cargar_datos()

# --- FUNCIÓN 3: ELIMINAR INCIDENCIA (¡LA NUEVA!) ---
def eliminar_incidencia():
    id_borrar = entrada_borrar_id.get()
    
    if id_borrar == "":
        messagebox.showwarning("Atención", "Introduce un ID para borrar.")
        return

    # Conectamos a la BD y ejecutamos el DELETE de SQL
    conexion = sqlite3.connect('smartcity.db')
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM incidencias WHERE id_incidencia = ?;", (id_borrar,))
    conexion.commit()
    conexion.close()
    
    messagebox.showinfo("Eliminado", f"¡Incidencia #{id_borrar} eliminada del sistema!")
    entrada_borrar_id.delete(0, tk.END)
    
    # Recargamos la lista automáticamente
    cargar_datos()


# --- CONFIGURACIÓN DE LA INTERFAZ ---
ventana = tk.Tk()
ventana.title("MadTech SmartCity Hub - Panel de Control Pro")
ventana.geometry("550x630")

# Título Principal
titulo = tk.Label(ventana, text="SmartCity Hub Pro", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# --- ZONA DEL FORMULARIO (CAMPOS PARA ESCRIBIR) ---
frame_form = tk.LabelFrame(ventana, text=" Reportar Nueva Incidencia ", padx=10, pady=10)
frame_form.pack(pady=5, fill="x", padx=20)

tk.Label(frame_form, text="ID Incidencia:").grid(row=0, column=0, sticky="w")
entrada_id = tk.Entry(frame_form, width=10)
entrada_id.grid(row=0, column=1, sticky="w", pady=5)

tk.Label(frame_form, text="Descripción:").grid(row=1, column=0, sticky="w")
entrada_desc = tk.Entry(frame_form, width=40)
entrada_desc.grid(row=1, column=1, pady=5)

boton_guardar = tk.Button(frame_form, text="💾 Guardar en Base de Datos", command=guardar_incidencia, bg="#28a745", fg="white", font=("Arial", 10, "bold"))
boton_guardar.grid(row=2, column=1, pady=5, sticky="e")


# --- ZONA DE ACCIONES RÁPIDAS (BORRADO) ---
frame_acciones = tk.LabelFrame(ventana, text=" Zona de Peligro / Administración ", padx=10, pady=10)
frame_acciones.pack(pady=5, fill="x", padx=20)

tk.Label(frame_acciones, text="ID a Eliminar:").grid(row=0, column=0, sticky="w")
entrada_borrar_id = tk.Entry(frame_acciones, width=10)
entrada_borrar_id.grid(row=0, column=1, sticky="w", pady=5)

# Botón rojo para eliminar
boton_eliminar = tk.Button(frame_acciones, text="❌ Eliminar por ID", command=eliminar_incidencia, bg="#dc3545", fg="white", font=("Arial", 10, "bold"))
boton_eliminar.grid(row=0, column=2, padx=10, sticky="w")


# --- ZONA DE CONSULTA (VER DATOS) ---
boton_actualizar = tk.Button(ventana, text="🔄 Ver / Actualizar Listado", command=cargar_datos, bg="#007acc", fg="white", font=("Arial", 10, "bold"))
boton_actualizar.pack(pady=10)

caja_texto = tk.Text(ventana, width=60, height=10, font=("Courier", 10))
caja_texto.pack(pady=5)

# Carga inicial automática
cargar_datos()

ventana.mainloop()