import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Datos ampliados de árboles con forma de la copa
data = {
    "Altura (m)": [5, 10, 8, 15, 7, 12, 6, 14, 9, 11, 13, 16],
    "Diámetro (cm)": [30, 50, 40, 60, 35, 55, 32, 58, 42, 45, 65, 70],
    "Tipo de Hoja": [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],  # 0: Pequeña, 1: Grande
    "Resistencia a sequía": [1, 2, 1, 3, 2, 3, 1, 2, 3, 1, 2, 3],  # 1: Baja, 2: Media, 3: Alta
    "Forma de la copa": [0, 1, 2, 3, 1, 2, 3, 0, 1, 3, 2, 0],  # 0: Piramidal, 1: Redonda, 2: Extendida, 3: Irregular
    "Especie": [
        "Mezquite", "Palo Verde", "Huizache", "Encino", "Guaje", "Sabino",
        "Tepehuaje", "Ebano", "Ceiba", "Nopal", "Biznaga", "Tepehuaje"
    ]
}

# Convertir a DataFrame
df = pd.DataFrame(data)
X = df.drop("Especie", axis=1)
y = df["Especie"]

# Entrenar modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Función para hacer la predicción
def clasificar_arbol():
    altura = float(altura_entry.get())
    diametro = float(diametro_entry.get())
    tipo_hoja = hoja_var.get()
    resistencia = sequia_var.get()
    forma_copa = copa_var.get()

    datos_usuario = np.array([[altura, diametro, tipo_hoja, resistencia, forma_copa]])
    prediccion = model.predict(datos_usuario)[0]
    
    resultado_label.config(text=f"El árbol más probable es: {prediccion}")

# Crear ventana
ventana = tk.Tk()
ventana.title("Clasificador de Árboles")

# Crear etiquetas y campos de entrada
ttk.Label(ventana, text="Altura (m):").grid(row=0, column=0)
altura_entry = ttk.Entry(ventana)
altura_entry.grid(row=0, column=1)

ttk.Label(ventana, text="Diámetro (cm):").grid(row=1, column=0)
diametro_entry = ttk.Entry(ventana)
diametro_entry.grid(row=1, column=1)

# Tipo de Hoja (RadioButtons)
ttk.Label(ventana, text="Tipo de Hoja:").grid(row=2, column=0)
hoja_var = tk.IntVar()
tk.Radiobutton(ventana, text="Hoja pequeña", variable=hoja_var, value=0).grid(row=2, column=1)
tk.Radiobutton(ventana, text="Hoja grande", variable=hoja_var, value=1).grid(row=3, column=1)

# Resistencia a Sequía (RadioButtons)
ttk.Label(ventana, text="Resistencia a Sequía:").grid(row=4, column=0)
sequia_var = tk.IntVar()
tk.Radiobutton(ventana, text="Baja", variable=sequia_var, value=1).grid(row=4, column=1)
tk.Radiobutton(ventana, text="Media", variable=sequia_var, value=2).grid(row=5, column=1)
tk.Radiobutton(ventana, text="Alta", variable=sequia_var, value=3).grid(row=6, column=1)

# Forma de la Copa (RadioButtons)
ttk.Label(ventana, text="Forma de la Copa:").grid(row=7, column=0)
copa_var = tk.IntVar()
tk.Radiobutton(ventana, text="Piramidal", variable=copa_var, value=0).grid(row=7, column=1)
tk.Radiobutton(ventana, text="Redonda", variable=copa_var, value=1).grid(row=8, column=1)
tk.Radiobutton(ventana, text="Extendida", variable=copa_var, value=2).grid(row=9, column=1)
tk.Radiobutton(ventana, text="Irregular", variable=copa_var, value=3).grid(row=10, column=1)

# Botón para clasificar
clasificar_btn = ttk.Button(ventana, text="Clasificar Árbol", command=clasificar_arbol)
clasificar_btn.grid(row=11, column=0, columnspan=2)

# Etiqueta de resultado
resultado_label = ttk.Label(ventana, text="El árbol aparecerá aquí.")
resultado_label.grid(row=12, column=0, columnspan=2)

# Ejecutar ventana
ventana.mainloop()
