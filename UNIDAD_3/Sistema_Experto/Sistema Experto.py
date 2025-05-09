import tkinter as tk
from tkinter import ttk
from sklearn.tree import DecisionTreeClassifier 
from sklearn.preprocessing import LabelEncoder 
import pandas as pd 
import joblib
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree 

# Datos simulados para entrenar el modelo
DATA = [
    ["simple", "lanceolada", "entero", ">10m", "no", "no", "no", "ribera", "Álamo"],
    ["compuesta", "palmeada", "entero", ">10m", "sí", "sí", "sí", "cerro", "Ceiba"],
    ["compuesta", "lineal", "entero", "5-10m", "no", "sí", "sí", "urbano", "Tamarindo"],
    ["compuesta", "lineal", "entero", "5-10m", "no", "sí", "sí", "cerro", "Guamúchil"],
    ["compuesta", "lanceolada", "dentado", "5-10m", "no", "sí", "sí", "urbano", "Neem"],
    ["compuesta", "elíptica", "entero", "<5m", "sí", "sí", "sí", "cerro", "Ébano"],
    ["simple", "ovada", "entero", ">10m", "no", "no", "no", "ribera", "Amate blanco"],
    ["compuesta", "lineal", "entero", ">10m", "no", "sí", "sí", "urbano", "Jacaranda"],
    ["compuesta", "ovada", "entero", "5-10m", "no", "sí", "sí", "jardín", "Trébol de olor"],
    ["compuesta", "lineal", "entero", "<5m", "sí", "sí", "sí", "cerro", "Huizache"]
]

# Columnas del dataset
COLUMNAS = ["hoja", "forma_hoja", "margen", "altura", "espinas", "fruto", "flor", "habitat", "arbol"]

df = pd.DataFrame(DATA, columns=COLUMNAS)

# Codificar datos
le_dict = {}
X = df.drop("arbol", axis=1)
y = df["arbol"]
X_encoded = X.copy()

for col in X.columns:
    le = LabelEncoder()
    X_encoded[col] = le.fit_transform(X[col])
    le_dict[col] = le

le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)

# Entrenar modelo
model = DecisionTreeClassifier(random_state=42)
model.fit(X_encoded, y_encoded)

# Interfaz
class SistemaAprendizajeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto - Modelo de Árboles")
        self.root.geometry("500x600")
        self.root.resizable(True, True)

        self.campos = {}

        frame = ttk.Frame(root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        self.crear_combobox(frame, "Tipo de hoja", ["simple", "compuesta"])
        self.crear_combobox(frame, "Forma de hoja", ["ovada", "elíptica", "lanceolada", "palmeada", "lineal"])
        self.crear_combobox(frame, "Margen", ["entero", "dentado", "lobulado"])
        self.crear_combobox(frame, "Altura del árbol", ["<5m", "5-10m", ">10m"])
        self.crear_combobox(frame, "Presencia de espinas", ["sí", "no"])
        self.crear_combobox(frame, "¿Tiene frutos visibles?", ["sí", "no"])
        self.crear_combobox(frame, "¿Está floreando?", ["sí", "no"])
        self.crear_combobox(frame, "Hábitat", ["urbano", "cerro", "ribera", "jardín"])

        ttk.Button(frame, text="Evaluar árbol", command=self.evaluar).pack(pady=20)
        self.resultado = tk.Label(
            frame,
            text="",
            font=("Arial", 12),
            justify="left",
            wraplength=550,  # Ajusta a tu preferencia
            anchor="w",
            bg="white",
            relief="solid",
            padx=10,
            pady=10
        )
        self.resultado.pack(fill="x", pady=10)

    def crear_combobox(self, frame, texto, opciones):
        ttk.Label(frame, text=texto).pack(anchor="w", pady=(10, 0))
        var = tk.StringVar()
        combo = ttk.Combobox(frame, textvariable=var, values=opciones, state="readonly")
        combo.pack(fill="x")
        self.campos[texto] = var

    def evaluar(self):
        entrada = {
            "hoja": self.campos["Tipo de hoja"].get(),
            "forma_hoja": self.campos["Forma de hoja"].get(),
            "margen": self.campos["Margen"].get(),
            "altura": self.campos["Altura del árbol"].get(),
            "espinas": self.campos["Presencia de espinas"].get(),
            "fruto": self.campos["¿Tiene frutos visibles?"].get(),
            "flor": self.campos["¿Está floreando?"].get(),
            "habitat": self.campos["Hábitat"].get()
        }

        if "" in entrada.values():
            self.resultado.config(text="Completa todos los campos.", foreground="red")
            return

        entrada_codificada = []
        for k in X.columns:
            entrada_codificada.append(le_dict[k].transform([entrada[k]])[0])

        # Obtener predicción y probabilidad
        proba = model.predict_proba([entrada_codificada])[0]
        pred_index = proba.argmax()
        confianza = proba[pred_index]

        if confianza >= 0.6:  # Umbral de confianza
            arbol = le_target.inverse_transform([pred_index])[0]
            self.resultado.config(
                text=f"Predicción: {arbol} (confianza: {confianza:.2f})",
                foreground="green"
            )
        else:
            self.resultado.config(
                text="No se ha encontrado el tipo de árbol con suficiente certeza.",
                foreground="orange"
            )
        
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaAprendizajeApp(root)
    root.mainloop()

plt.figure(figsize=(20, 10))
plot_tree(model, feature_names=X.columns, class_names=le_target.classes_, filled=True)
plt.show()