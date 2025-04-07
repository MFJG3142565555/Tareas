import tkinter as tk

# Función para bloquear o habilitar la opción de presupuesto alto
def actualizar_presupuesto():
    uso = uso_var.get()
    if uso == "Oficina":
        presupuesto_var.set("")  # Deseleccionar presupuesto alto si estaba seleccionado
        rb_presupuesto_alto.config(state="disabled")  # Deshabilitar radiobutton "Alto"
    else:
        rb_presupuesto_alto.config(state="normal")  # Habilitar radiobutton "Alto"

# Función para generar la configuración personalizada
def generar_configuracion():
    configuracion = {}

    # Verificar opciones seleccionadas
    uso = uso_var.get()
    movilidad = movilidad_var.get()
    presupuesto = presupuesto_var.get()

    # Validar que todas las opciones estén seleccionadas
    if not uso or not movilidad or not presupuesto:
        texto_resultado.config(state="normal")
        texto_resultado.delete(1.0, tk.END)
        texto_resultado.insert(tk.END, "Por favor, completa todas las opciones.")
        texto_resultado.config(state="disabled")
        return

    # Selección dinámica de CPU
    if uso == "Gaming":
        configuracion["CPU"] = "AMD Ryzen 7 (8 núcleos, 3.6 GHz)" if presupuesto == "Medio" else "AMD Ryzen 5 (6 núcleos, 3.2 GHz)" if presupuesto == "Bajo" else "AMD Ryzen 7 (8 núcleos, 3.6 GHz)"
    elif uso == "Diseño":
        configuracion["CPU"] = "Intel i7 (8 núcleos, 3.4 GHz)" if presupuesto == "Medio" else "Intel i5 (6 núcleos, 2.8 GHz)" if presupuesto == "Bajo" else "Intel i9 (10 núcleos, 3.8 GHz)"
    elif uso == "Oficina":
        configuracion["CPU"] = "Intel i3 (4 núcleos, 2.5 GHz)" if presupuesto == "Bajo" else "Intel i5 (6 núcleos, 2.9 GHz)"

    # Selección dinámica de RAM
    if uso == "Gaming":
        configuracion["RAM"] = "32 GB DDR5" if presupuesto == "Alto" else "16 GB DDR4" if presupuesto == "Medio" else "8 GB DDR4"
    elif uso == "Diseño":
        configuracion["RAM"] = "64 GB DDR5" if presupuesto == "Alto" else "32 GB DDR4" if presupuesto == "Medio" else "16 GB DDR4"
    else:
        configuracion["RAM"] = "16 GB DDR4" if presupuesto == "Medio" else "8 GB DDR4"

    # Selección dinámica de GPU
    if uso == "Gaming":
        configuracion["GPU"] = "Integrada" if presupuesto == "Bajo" else "NVIDIA RTX 3060 (6 GB VRAM)" if presupuesto == "Medio" else "NVIDIA RTX 4080 (12 GB VRAM)"
    elif uso == "Diseño":
        configuracion["GPU"] = "NVIDIA GTX 1650 (4 GB VRAM)" if presupuesto == "Bajo" else "NVIDIA RTX 4090 (24 GB VRAM)" if presupuesto == "Alto" else "NVIDIA RTX 3070 (8 GB VRAM)"
    elif uso == "Oficina":
        configuracion["GPU"] = "Integrada"

    # Selección dinámica de almacenamiento
    configuracion["Almacenamiento"] = "SSD 2 TB + HDD 4 TB" if presupuesto == "Alto" else "SSD 1 TB" if presupuesto == "Medio" else "SSD 512 GB"

    # Selección dinámica según movilidad
    if movilidad == "Laptop":
        configuracion["Pantalla"] = "17.3 pulgadas QHD" if presupuesto == "Alto" else "15.6 pulgadas Full HD"
        configuracion["Batería"] = "12 horas" if presupuesto == "Alto" else "8 horas" if presupuesto == "Medio" else "5 horas"
        configuracion["Peso"] = "2.5 kg"
        configuracion["Conectividad"] = "Wi-Fi 6, USB-C, Thunderbolt" if presupuesto == "Alto" else "Wi-Fi 5, USB 3.0"
    else:  # Escritorio
        configuracion["Gabinete"] = "ATX Compacto" if presupuesto == "Bajo" else "ATX Completo"
        configuracion["Conectividad"] = "Ethernet, USB 3.0, HDMI"

    # Mostrar resultado
    detalles = "\n".join([f"{clave}: {valor}" for clave, valor in configuracion.items()])
    texto_resultado.config(state="normal")
    texto_resultado.delete(1.0, tk.END)
    texto_resultado.insert(tk.END, detalles)
    texto_resultado.config(state="disabled")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Configurador Personalizado de Computadoras")

# Variables para radiobuttons
uso_var = tk.StringVar()
movilidad_var = tk.StringVar()
presupuesto_var = tk.StringVar()

# Opciones de Uso
tk.Label(ventana, text="Uso principal:").grid(row=0, column=0, padx=10, pady=5)
tk.Radiobutton(ventana, text="Gaming", variable=uso_var, value="Gaming", command=actualizar_presupuesto).grid(row=0, column=1, padx=5, pady=5)
tk.Radiobutton(ventana, text="Diseño", variable=uso_var, value="Diseño", command=actualizar_presupuesto).grid(row=0, column=2, padx=5, pady=5)
tk.Radiobutton(ventana, text="Oficina", variable=uso_var, value="Oficina", command=actualizar_presupuesto).grid(row=0, column=3, padx=5, pady=5)

# Opciones de Movilidad
tk.Label(ventana, text="Movilidad:").grid(row=1, column=0, padx=10, pady=5)
tk.Radiobutton(ventana, text="Laptop", variable=movilidad_var, value="Laptop").grid(row=1, column=1, padx=5, pady=5)
tk.Radiobutton(ventana, text="Escritorio", variable=movilidad_var, value="Escritorio").grid(row=1, column=2, padx=5, pady=5)

# Opciones de Presupuesto
tk.Label(ventana, text="Presupuesto:").grid(row=2, column=0, padx=10, pady=5)
rb_presupuesto_bajo = tk.Radiobutton(ventana, text="Bajo", variable=presupuesto_var, value="Bajo")
rb_presupuesto_bajo.grid(row=2, column=1, padx=5, pady=5)
rb_presupuesto_medio = tk.Radiobutton(ventana, text="Medio", variable=presupuesto_var, value="Medio")
rb_presupuesto_medio.grid(row=2, column=2, padx=5, pady=5)
rb_presupuesto_alto = tk.Radiobutton(ventana, text="Alto", variable=presupuesto_var, value="Alto")
rb_presupuesto_alto.grid(row=2, column=3, padx=5, pady=5)

# Cuadro de texto para mostrar el resultado
tk.Label(ventana, text="Configuración personalizada:").grid(row=3, column=0, padx=10, pady=10)
texto_resultado = tk.Text(ventana, height=12, width=60, state="disabled", wrap="word")
texto_resultado.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

# Botón para generar configuración
btn_configurar = tk.Button(ventana, text="Generar Configuración", command=generar_configuracion)
btn_configurar.grid(row=4, column=0, columnspan=4, pady=20)

# Ejecutar ventana
ventana.mainloop()