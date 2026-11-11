import random
import tkinter as tk
import customtkinter as ctk

# Configuración visual de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# =====================================================================
# 1. MÓDULO DE ALGORITMOS (Extensible)
# =====================================================================
def selection_sort(lista):
    """
    Tu algoritmo adaptado con 'yield'.
    Devuelve en cada paso un diccionario con los índices e información de color.
    """
    largoLista = len(lista)
    for i in range(largoLista):
        indice_minimo = i
        for j in range(i + 1, largoLista):
            # Amarillo: comparando | Rojo: mínimo actual | Verde: ya ordenado
            yield {
                j: "#F59E0B", 
                indice_minimo: "#EF4444", 
                **{k: "#10B981" for k in range(i)}
            }
            if lista[j] < lista[indice_minimo]:
                indice_minimo = j
                
        lista[i], lista[indice_minimo] = lista[indice_minimo], lista[i]
        yield {k: "#10B981" for k in range(i + 1)}

# Para añadir más algoritmos en el futuro, solo defines la función arriba
# y la registras en este diccionario:
ALGORITMOS = {
    "Selection Sort": selection_sort,
    # "Bubble Sort": bubble_sort,
    # "Quick Sort": quick_sort,
}


# =====================================================================
# 2. INTERFAZ GRÁFICA Y MOTOR DE VISUALIZACIÓN
# =====================================================================
class VisualizadorOrdenamiento(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Algoritmos")
        self.geometry("950x600")
        self.minsize(800, 500)

        self.lista = []
        self.generador = None
        self.ordenando = False
        self.after_id = None

        self._crear_interfaz()
        self.generar_datos()

    def _crear_interfaz(self):
        # Panel superior de controles
        panel = ctk.CTkFrame(self, corner_radius=10)
        panel.pack(fill="x", padx=15, pady=(15, 5))

        # Selector de Algoritmo
        ctk.CTkLabel(panel, text="Algoritmo:").pack(side="left", padx=(15, 5), pady=12)
        self.combo_algo = ctk.CTkOptionMenu(panel, values=list(ALGORITMOS.keys()), width=150)
        self.combo_algo.pack(side="left", padx=5)

        # Slider: Cantidad de elementos
        self.lbl_cantidad = ctk.CTkLabel(panel, text="Elementos: 50", width=95)
        self.lbl_cantidad.pack(side="left", padx=(20, 5))
        self.slider_cantidad = ctk.CTkSlider(
            panel, from_=10, to=250, number_of_steps=240, width=140, command=self._actualizar_cantidad
        )
        self.slider_cantidad.set(50)
        self.slider_cantidad.pack(side="left", padx=5)

        # Slider: Velocidad
        self.lbl_velocidad = ctk.CTkLabel(panel, text="Velocidad: 50%", width=95)
        self.lbl_velocidad.pack(side="left", padx=(20, 5))
        self.slider_velocidad = ctk.CTkSlider(
            panel, from_=1, to=100, number_of_steps=99, width=140, command=self._actualizar_velocidad
        )
        self.slider_velocidad.set(50)
        self.slider_velocidad.pack(side="left", padx=5)

        # Botones de acción
        self.btn_iniciar = ctk.CTkButton(panel, text="▶ Iniciar", width=90, command=self.iniciar_ordenamiento)
        self.btn_iniciar.pack(side="right", padx=(5, 15))

        self.btn_mezclar = ctk.CTkButton(
            panel, text="🔀 Mezclar", width=90, fg_color="#4B5563", hover_color="#374151", command=self.generar_datos
        )
        self.btn_mezclar.pack(side="right", padx=5)

        # Lienzo (Canvas) de alto rendimiento para dibujar las barras
        self.canvas = tk.Canvas(self, bg="#18181B", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=(10, 15))
        self.canvas.bind("<Configure>", lambda event: self.dibujar_barras())

    def _actualizar_cantidad(self, valor):
        self.lbl_cantidad.configure(text=f"Elementos: {int(valor)}")
        if not self.ordenando:
            self.generar_datos()

    def _actualizar_velocidad(self, valor):
        self.lbl_velocidad.configure(text=f"Velocidad: {int(valor)}%")

    def generar_datos(self):
        self.detener_ordenamiento()
        cantidad = int(self.slider_cantidad.get())
        self.lista = [random.randint(5, 100) for _ in range(cantidad)]
        self.dibujar_barras()

    def dibujar_barras(self, colores_destacados=None):
        if colores_destacados is None:
            colores_destacados = {}

        self.canvas.delete("all")
        ancho_canvas = self.canvas.winfo_width()
        alto_canvas = self.canvas.winfo_height()

        if ancho_canvas <= 1 or not self.lista:
            return

        n = len(self.lista)
        ancho_barra = ancho_canvas / n
        max_val = max(self.lista)
        # Si hay muchos elementos, quitamos el borde para que se vea limpio y rinda mejor
        espacio = 1 if n <= 100 else 0

        for i, val in enumerate(self.lista):
            x0 = i * ancho_barra
            y0 = alto_canvas - (val / max_val) * (alto_canvas - 25)
            x1 = (i + 1) * ancho_barra - espacio
            y1 = alto_canvas

            color = colores_destacados.get(i, "#3B82F6")  # Azul base
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    def iniciar_ordenamiento(self):
        if self.ordenando:
            return
        self.ordenando = True
        self.btn_iniciar.configure(state="disabled")
        self.slider_cantidad.configure(state="disabled")
        self.combo_algo.configure(state="disabled")

        nombre_algo = self.combo_algo.get()
        funcion_algo = ALGORITMOS[nombre_algo]
        self.generador = funcion_algo(self.lista)
        self._animar_paso()

    def detener_ordenamiento(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.ordenando = False
        self.btn_iniciar.configure(state="normal")
        self.slider_cantidad.configure(state="normal")
        self.combo_algo.configure(state="normal")

    def _animar_paso(self):
        if not self.ordenando:
            return

        velocidad = int(self.slider_velocidad.get())

        # Lógica de aceleración inteligente:
        # Vel 1 a 75: Ajusta la espera en milisegundos (1 paso por fotograma).
        # Vel 76 a 100: Espera mínima (1 ms) y salta múltiples pasos lógicos por fotograma.
        if velocidad <= 75:
            pasos_por_frame = 1
            retraso_ms = int(150 - (velocidad * 1.98))
        else:
            pasos_por_frame = int((velocidad - 74) ** 1.7)
            retraso_ms = 1

        colores = {}
        try:
            for _ in range(pasos_por_frame):
                colores = next(self.generador)
            self.dibujar_barras(colores)
            self.after_id = self.after(retraso_ms, self._animar_paso)
        except StopIteration:
            # Pintar todo de verde al terminar
            self.dibujar_barras({i: "#10B981" for i in range(len(self.lista))})
            self.detener_ordenamiento()


if __name__ == "__main__":
    app = VisualizadorOrdenamiento()
    app.mainloop()
