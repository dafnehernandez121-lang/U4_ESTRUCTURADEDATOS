import tkinter as tk
from tkinter import ttk, messagebox
import random

class GrafoAppNativo:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Gráfico de Grafos (Sin Librerías Externas)")
        self.root.geometry("880x680")
        self.root.configure(bg="#f8fafc")
        
        # ==========================================
        # 1. ESTRUCTURA DE DATOS: GRAFO BASE Y COORDENADAS
        # ==========================================
        self.grafo = {
            'Quintana Roo': {'Yucatán': 300, 'Campeche': 380},
            'Yucatán': {'Quintana Roo': 300, 'Campeche': 180},
            'Campeche': {'Quintana Roo': 380, 'Yucatán': 180, 'Tabasco': 390},
            'Tabasco': {'Campeche': 390, 'Chiapas': 250, 'Veracruz': 480},
            'Chiapas': {'Tabasco': 250, 'Veracruz': 600, 'Oaxaca': 500},
            'Veracruz': {'Tabasco': 480, 'Chiapas': 600, 'Oaxaca': 260},
            'Oaxaca': {'Chiapas': 500, 'Veracruz': 260}
        }
        
        # Coordenadas estáticas (X, Y) para dibujar los nodos iniciales ordenadamente en el lienzo (Canvas)
        self.coords = {
            'Quintana Roo': (650, 150), 'Yucatán': (500, 80), 'Campeche': (450, 250),
            'Tabasco': (300, 300), 'Chiapas': (350, 450), 'Veracruz': (150, 200), 'Oaxaca': (200, 400)
        }

        self.construir_ui()

    # ==========================================
    # 2. INTERFAZ GRÁFICA (MENÚS Y BOTONES)
    # ==========================================
    def construir_ui(self):
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
        tk.Label(self.root, text="📍 Gestor Visual de Rutas (Estructura de Datos)", font=("Segoe UI", 16, "bold"), bg="#f8fafc").pack(pady=15)

        # Panel Superior: Agregar, Modificar y Eliminar
        panel_gestion = ttk.LabelFrame(self.root, text=" Gestión Dinámica de Nodos y Aristas ")
        panel_gestion.pack(fill=tk.X, padx=20, pady=10, ipady=10)

        # Fila 1: Agregar
        ttk.Label(panel_gestion, text="Origen:").grid(row=0, column=0, padx=5, pady=5)
        self.cb_origen_add = ttk.Combobox(panel_gestion, width=15)
        self.cb_origen_add.grid(row=0, column=1, padx=5)

        ttk.Label(panel_gestion, text="Destino:").grid(row=0, column=2, padx=5, pady=5)
        self.cb_destino_add = ttk.Combobox(panel_gestion, width=15)
        self.cb_destino_add.grid(row=0, column=3, padx=5)

        ttk.Label(panel_gestion, text="Costo (Km):").grid(row=0, column=4, padx=5, pady=5)
        self.entry_costo = ttk.Entry(panel_gestion, width=8)
        self.entry_costo.grid(row=0, column=5, padx=5)

        ttk.Button(panel_gestion, text="➕ Guardar Conexión", command=self.agregar_modificar).grid(row=0, column=6, padx=15)

        # Fila 2: Eliminar
        ttk.Label(panel_gestion, text="Eliminar Estado:").grid(row=1, column=0, padx=5, pady=15)
        self.cb_eliminar = ttk.Combobox(panel_gestion, width=15, state="readonly")
        self.cb_eliminar.grid(row=1, column=1, padx=5)
        ttk.Button(panel_gestion, text="🗑️ Borrar Nodo", command=self.eliminar_estado).grid(row=1, column=2, columnspan=2, sticky="w", padx=5)

        # Panel Inferior: Operaciones
        panel_operaciones = ttk.LabelFrame(self.root, text=" Operaciones de la Rúbrica ")
        panel_operaciones.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Botones básicos
        frame_btns = tk.Frame(panel_operaciones, bg="#f8fafc")
        frame_btns.pack(pady=10)
        ttk.Button(frame_btns, text="📊 Ver Relaciones (Punto 5)", width=30, command=self.mostrar_tabla).grid(row=0, column=0, padx=10)
        ttk.Button(frame_btns, text="🗺️ Dibujar Grafo (Punto 4)", width=30, command=lambda: self.dibujar_grafo()).grid(row=0, column=1, padx=10)

        # Resolución de Tarea Principal (Puntos 1, 2 y 3)
        frame_tarea = ttk.LabelFrame(panel_operaciones, text=" Resolver Tarea (Visitar TODOS los estados) ")
        frame_tarea.pack(fill=tk.X, padx=20, pady=10, ipady=10)
        ttk.Button(frame_tarea, text="Ejecutar Algoritmo (Puntos 1, 2 y 3)", command=self.resolver_tarea_principal).pack(pady=10)

        # Extra: Ruta libre
        frame_ruta = ttk.LabelFrame(panel_operaciones, text=" Extra: Trazar Ruta Óptima entre 2 puntos (Dijkstra) ")
        frame_ruta.pack(fill=tk.X, padx=20, pady=10, ipady=10)
        
        ttk.Label(frame_ruta, text="Inicio:").grid(row=0, column=0, padx=10, pady=5)
        self.cb_ruta_origen = ttk.Combobox(frame_ruta, width=15, state="readonly")
        self.cb_ruta_origen.grid(row=0, column=1, padx=5)
        
        ttk.Label(frame_ruta, text="Fin:").grid(row=0, column=2, padx=10, pady=5)
        self.cb_ruta_destino = ttk.Combobox(frame_ruta, width=15, state="readonly")
        self.cb_ruta_destino.grid(row=0, column=3, padx=5)
        
        ttk.Button(frame_ruta, text="🚀 Calcular Ruta", command=self.calcular_ruta_libre).grid(row=0, column=4, padx=20)

        self.actualizar_combos()

    # ==========================================
    # 3. LÓGICA DE DICCIONARIOS (ACTUALIZACIÓN)
    # ==========================================
    def actualizar_combos(self):
        estados = sorted(list(self.grafo.keys()))
        for cb in [self.cb_origen_add, self.cb_destino_add, self.cb_eliminar, self.cb_ruta_origen, self.cb_ruta_destino]:
            cb['values'] = estados
            cb.set('')

    def agregar_modificar(self):
        origen, destino = self.cb_origen_add.get().strip().title(), self.cb_destino_add.get().strip().title()
        try: costo = float(self.entry_costo.get())
        except: return messagebox.showerror("Error", "El costo debe ser numérico.")

        if not origen or not destino: return messagebox.showwarning("Aviso", "Faltan datos.")

        # Actualiza el diccionario bidireccional
        for nodo in (origen, destino):
            if nodo not in self.grafo:
                self.grafo[nodo] = {}
                # Genera coordenadas aleatorias si es un nodo nuevo para poder dibujarlo
                self.coords[nodo] = (random.randint(50, 700), random.randint(50, 500))

        self.grafo[origen][destino] = costo
        self.grafo[destino][origen] = costo
        self.actualizar_combos()
        self.entry_costo.delete(0, tk.END)
        messagebox.showinfo("Éxito", f"Arista agregada: {origen} ↔ {destino}")

    def eliminar_estado(self):
        estado = self.cb_eliminar.get()
        if not estado: return
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar nodo '{estado}'?"):
            del self.grafo[estado]
            for nodo in self.grafo:
                if estado in self.grafo[nodo]:
                    del self.grafo[nodo][estado]
            if estado in self.coords: del self.coords[estado]
            self.actualizar_combos()

    # ==========================================
    # 4. VISUALIZACIÓN NATIVA (TABLA Y CANVAS)
    # ==========================================
    def mostrar_tabla(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Tabla de Relaciones")
        ventana.geometry("450x300")
        
        tabla = ttk.Treeview(ventana, columns=("O", "D", "C"), show='headings')
        tabla.heading("O", text="Origen"); tabla.heading("D", text="Destino"); tabla.heading("C", text="Costo (km)")
        tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for origen, destinos in self.grafo.items():
            for destino, costo in destinos.items():
                tabla.insert("", tk.END, values=(origen, destino, costo))

    def dibujar_grafo(self, ruta_resaltar=None):
        """Dibuja el grafo matemáticamente usando coordenadas y el Canvas nativo de Tkinter."""
        if not self.grafo: return messagebox.showwarning("Aviso", "Grafo vacío.")
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Mapa Visual del Grafo")
        
        canvas = tk.Canvas(ventana, width=800, height=600, bg="white")
        canvas.pack(padx=10, pady=10)

        aristas_dibujadas = set()
        
        # Convertimos la ruta en una lista de pares [(A, B), (B, C)] para identificarlos al pintar
        pares_ruta = []
        if ruta_resaltar:
            pares_ruta = [(ruta_resaltar[i], ruta_resaltar[i+1]) for i in range(len(ruta_resaltar)-1)]

        # 1. Dibujar Líneas (Aristas)
        for origen, destinos in self.grafo.items():
            x1, y1 = self.coords[origen]
            for destino, costo in destinos.items():
                x2, y2 = self.coords[destino]
                arista = frozenset([origen, destino])
                
                # Checar si esta línea forma parte de la ruta resaltada
                es_ruta = (origen, destino) in pares_ruta or (destino, origen) in pares_ruta
                color_linea = "red" if es_ruta else "#cccccc"
                grosor = 4 if es_ruta else 2

                if arista not in aristas_dibujadas:
                    canvas.create_line(x1, y1, x2, y2, fill=color_linea, width=grosor)
                    # Texto del costo en el medio de la línea
                    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                    canvas.create_text(mid_x, mid_y - 10, text=str(costo), fill="blue", font=("Arial", 9, "bold"))
                    aristas_dibujadas.add(arista)

        # 2. Dibujar Círculos (Nodos) encima de las líneas
        for nodo, (x, y) in self.coords.items():
            es_nodo_ruta = ruta_resaltar and (nodo in ruta_resaltar)
            color_nodo = "#ffcccc" if es_nodo_ruta else "#add8e6"
            
            canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color_nodo, outline="black")
            canvas.create_text(x, y + 30, text=nodo, font=("Arial", 9, "bold"), fill="black")

    # ==========================================
    # 5. ALGORITMOS DE BÚSQUEDA (DFS Y DIJKSTRA)
    # ==========================================
    def resolver_tarea_principal(self):
        """Cumple los puntos 1, 2 y 3: Búsqueda en Profundidad (DFS) para encontrar un camino Hamiltoniano."""
        nodos_totales = len(self.grafo)
        if nodos_totales < 2: return
        
        ruta_sin_repetir = None
        for inicio in self.grafo:
            ruta = self.dfs_recursivo(inicio, [inicio])
            if ruta:
                ruta_sin_repetir = ruta
                break

        if not ruta_sin_repetir:
            return messagebox.showerror("Sin solución", "El grafo actual no permite visitar todos los nodos seguidos. Agrega más aristas.")

        # Inciso A (Sin Repetir)
        costo_a = sum(self.grafo[ruta_sin_repetir[i]][ruta_sin_repetir[i+1]] for i in range(len(ruta_sin_repetir) - 1))
        
        # Inciso B (Repitiendo un estado: Forzamos un regreso en el primer nodo)
        ruta_repitiendo = [ruta_sin_repetir[0], ruta_sin_repetir[1], ruta_sin_repetir[0]] + ruta_sin_repetir[1:]
        costo_b = sum(self.grafo[ruta_repitiendo[i]][ruta_repitiendo[i+1]] for i in range(len(ruta_repitiendo) - 1))

        mensaje = (
            f"✅ A) SIN REPETIR ESTADOS (Puntos 1 y 3):\n{' ➔ '.join(ruta_sin_repetir)}\nCosto Total: {costo_a} km\n\n"
            f"🔁 B) REPITIENDO ESTADOS (Puntos 2 y 3):\n{' ➔ '.join(ruta_repitiendo)}\nCosto Total: {costo_b} km\n\n"
            "Presiona Aceptar para ver la Ruta A dibujada en rojo."
        )
        messagebox.showinfo("Resultados", mensaje)
        self.dibujar_grafo(ruta_resaltar=ruta_sin_repetir)

    def dfs_recursivo(self, actual, camino):
        """Algoritmo recursivo de Backtracking"""
        if len(camino) == len(self.grafo): return camino
        for vecino in self.grafo[actual]:
            if vecino not in camino:
                res = self.dfs_recursivo(vecino, camino + [vecino])
                if res: return res
        return None

    def calcular_ruta_libre(self):
        """Algoritmo de Dijkstra manual para el camino más corto entre dos nodos."""
        origen, destino = self.cb_ruta_origen.get(), self.cb_ruta_destino.get()
        if not origen or not destino: return
        
        distancias = {nodo: float('inf') for nodo in self.grafo}
        previos = {nodo: None for nodo in self.grafo}
        distancias[origen] = 0
        no_visitados = list(self.grafo.keys())
        
        while no_visitados:
            actual = min(no_visitados, key=lambda n: distancias[n])
            if distancias[actual] == float('inf') or actual == destino: break
            no_visitados.remove(actual)
            
            for vecino, costo in self.grafo[actual].items():
                ruta_alt = distancias[actual] + costo
                if ruta_alt < distancias[vecino]:
                    distancias[vecino] = ruta_alt
                    previos[vecino] = actual
                    
        if previos[destino] is None and origen != destino:
            return messagebox.showerror("Sin Ruta", f"No hay conexión entre {origen} y {destino}.")
            
        camino = []
        nodo_actual = destino
        while nodo_actual:
            camino.insert(0, nodo_actual)
            nodo_actual = previos[nodo_actual]
            
        messagebox.showinfo("Ruta Encontrada", f"{' ➔ '.join(camino)}\n\nCosto: {distancias[destino]} km")
        self.dibujar_grafo(ruta_resaltar=camino)

if __name__ == "__main__":
    root = tk.Tk()
    app = GrafoAppNativo(root)
    root.mainloop()