# =====================================================================
# PROYECTO: SMARTCITY HUB - INTERFAZ GRÁFICA (SPRINT 5)
# DESARROLLADORA: Ing. Briggitte Pérez
# =====================================================================

import tkinter as tk
from tkinter import messagebox

# 1. Crear la ventana principal (el contenedor)
ventana = tk.Tk()
ventana.title("MadTech SmartCity Hub")
ventana.geometry("400x300") # Ancho x Alto de la ventana

# 2. Función que se ejecutará cuando pulsemos el botón
def saludar():
    messagebox.showinfo("Mensaje del Sistema", "¡Hola, Briggitte! Tu primera ventana funciona 🚀")

# 3. Crear un título (Label) dentro de la ventana
titulo = tk.Label(ventana, text="Bienvenida al Panel Visual", font=("Arial", 16, "bold"))
titulo.pack(pady=20) # 'pack' lo coloca en la pantalla y 'pady' da espacio arriba/abajo

# 4. Crear un botón (Button) que llama a la función saludar
boton = tk.Button(ventana, text="Hacer clic aquí", command=saludar, bg="green", fg="white", font=("Arial", 12))
boton.pack(pady=20)

# 5. Iniciar el bucle de la ventana (para que no se cierre sola)
ventana.mainloop()