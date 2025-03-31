import re
import tkinter as tk
from tkinter import messagebox

# Lista extendida de palabras comunes en correos spam
PALABRAS_SPAM = [
    "oferta", "gratis", "dinero", "ganaste", "premio", "compra", "urgente", "crédito", "descuento", "exclusivo", "millones",
    "promoción", "préstamo", "click aquí", "acceso inmediato", "tarjeta de crédito", "sin costo", "envío gratis", "reembolso",
    "ahorra", "rebaja", "limitado", "transferencia", "bitcoin", "inversión", "hacerse rico", "oportunidad"
]

def analizar_correo():
    """Analiza el texto ingresado y determina si es spam o legítimo basándose en palabras clave."""
    emisor = entrada_emisor.get().strip().lower()
    asunto = entrada_asunto.get().strip().lower()
    cuerpo = entrada_texto.get("1.0", tk.END).strip().lower()
    
    if not (emisor and asunto and cuerpo):
        messagebox.showwarning("Advertencia", "Todos los campos deben estar completos.")
        return
    
    # Evaluar la presencia de palabras spam en cada campo con diferentes pesos
    conteo_spam = 0
    conteo_spam += sum(3 for palabra in PALABRAS_SPAM if palabra in asunto)  # Mayor peso al asunto
    conteo_spam += sum(1 for palabra in PALABRAS_SPAM if palabra in cuerpo)
    if es_correo_sospechoso(emisor):
        conteo_spam += 2
    
    if conteo_spam >= 3:
        etiqueta_resultado.config(text="Spam", fg="red")
    else:
        etiqueta_resultado.config(text="Legítimo", fg="green")

def es_correo_sospechoso(email):
    patrones_sospechosos = [
        r"[^\w\d]+@",
        r"\d{4,}@",
        r"(free|money|win|prize|offer)@",
        r".*(tempmail|mailinator|disposable|spamgourmet)\..*"
    ]
    
    return any(re.search(patron, email) for patron in patrones_sospechosos)

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Detector de Spam")
ventana.geometry("400x400")

# Campos de entrada
tk.Label(ventana, text="Emisor:").pack(pady=2)
entrada_emisor = tk.Entry(ventana, width=50)
entrada_emisor.pack()

tk.Label(ventana, text="Asunto:").pack(pady=2)
entrada_asunto = tk.Entry(ventana, width=50)
entrada_asunto.pack()

# Etiqueta y cuadro de texto para el cuerpo del correo
tk.Label(ventana, text="Cuerpo del correo:").pack(pady=5)
entrada_texto = tk.Text(ventana, height=8, width=50)
entrada_texto.pack()

# Botón de análisis
boton_analizar = tk.Button(ventana, text="Analizar", command=analizar_correo)
boton_analizar.pack(pady=10)

# Etiqueta de resultado
etiqueta_resultado = tk.Label(ventana, text="", font=("Arial", 12, "bold"))
etiqueta_resultado.pack()

ventana.mainloop()