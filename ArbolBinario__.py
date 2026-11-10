import tkinter as tk
from tkinter import messagebox

# ==========================================
# 1. ESTRUCTURA DE DATOS (Lógica del Árbol)
# ==========================================
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def buscar(self, valor):
        if not self.raiz: return None
        cola = [self.raiz]
        while cola:
            actual = cola.pop(0)
            if actual.valor == valor: return actual
            if actual.izquierda: cola.append(actual.izquierda)
            if actual.derecha: cola.append(actual.derecha)
        return None

    def insertar(self, valor_padre, nuevo_valor, lado):
        if self.raiz is None:
            self.raiz = Nodo(nuevo_valor)
            return True, f"Raíz establecida: '{nuevo_valor}'."

        padre = self.buscar(valor_padre)
        if not padre: return False, f"Padre '{valor_padre}' no encontrado."

        if lado.lower() == 'i':
            if padre.izquierda is None:
                padre.izquierda = Nodo(nuevo_valor)
                return True, f"'{nuevo_valor}' insertado a la izquierda de '{valor_padre}'."
            return False, "Ya existe un hijo izquierdo."
        elif lado.lower() == 'd':
            if padre.derecha is None:
                padre.derecha = Nodo(nuevo_valor)
                return True, f"'{nuevo_valor}' insertado a la derecha de '{valor_padre}'."
            return False, "Ya existe un hijo derecho."
        return False, "Lado inválido."

    def eliminar(self, valor):
        if self.raiz is None: return False, "El árbol está vacío."

        if self.raiz.izquierda is None and self.raiz.derecha is None:
            if self.raiz.valor == valor:
                self.raiz = None
                return True, "Raíz eliminada."
            return False, "Nodo no encontrado."

        cola = [self.raiz]
        nodo_a_eliminar = None
        actual = None

        while cola:
            actual = cola.pop(0)
            if actual.valor == valor: nodo_a_eliminar = actual
            if actual.izquierda: cola.append(actual.izquierda)
            if actual.derecha: cola.append(actual.derecha)

        if nodo_a_eliminar:
            valor_profundo = actual.valor
            self._eliminar_nodo_profundo(actual)
            nodo_a_eliminar.valor = valor_profundo
            return True, f"Nodo '{valor}' eliminado."
        return False, "Nodo no encontrado."

    def _eliminar_nodo_profundo(self, nodo_borrar):
        cola = [self.raiz]
        while cola:
            actual = cola.pop(0)
            if actual.izquierda:
                if actual.izquierda == nodo_borrar:
                    actual.izquierda = None
                    return
                cola.append(actual.izquierda)
            if actual.derecha:
                if actual.derecha == nodo_borrar:
                    actual.derecha = None
                    return
                cola.append(actual.derecha)

    def preorden(self, nodo, res=None):
        if res is None: res = []
        if nodo:
            res.append(nodo.valor)
            self.preorden(nodo.izquierda, res)
            self.preorden(nodo.derecha, res)
        return res

    def inorden(self, nodo, res=None):
        if res is None: res = []
        if nodo:
            self.inorden(nodo.izquierda, res)
            res.append(nodo.valor)
            self.inorden(nodo.derecha, res)
        return res

    def posorden(self, nodo, res=None):
        if res is None: res = []
        if nodo:
            self.posorden(nodo.izquierda, res)
            self.posorden(nodo.derecha, res)
            res.append(nodo.valor)
        return res

# ==========================================
# 2. INTERFAZ GRÁFICA (Ventanas y Canvas)
# ==========================================
class AplicacionArbol:
    def __init__(self, master):
        self.master = master
        self.master.title("Visualizador de Árbol Binario")
        self.master.geometry("900x700")
        self.master.config(bg="#f0f0f0")

        self.arbol = ArbolBinario()

        # Panel de Controles (Arriba)
        self.panel_control = tk.Frame(master, bg="#e0e0e0", pady=10)
        self.panel_control.pack(side=tk.TOP, fill=tk.X)

        tk.Label(self.panel_control, text="Valor a insertar:", bg="#e0e0e0").grid(row=0, column=0, padx=5)
        self.entrada_valor = tk.Entry(self.panel_control, width=10)
        self.entrada_valor.grid(row=0, column=1, padx=5)

        tk.Label(self.panel_control, text="Padre (vacío si es raíz):", bg="#e0e0e0").grid(row=0, column=2, padx=5)
        self.entrada_padre = tk.Entry(self.panel_control, width=10)
        self.entrada_padre.grid(row=0, column=3, padx=5)

        tk.Label(self.panel_control, text="Lado:", bg="#e0e0e0").grid(row=0, column=4, padx=5)
        self.var_lado = tk.StringVar(value="i")
        tk.Radiobutton(self.panel_control, text="Izquierda", variable=self.var_lado, value="i", bg="#e0e0e0").grid(row=0, column=5)
        tk.Radiobutton(self.panel_control, text="Derecha", variable=self.var_lado, value="d", bg="#e0e0e0").grid(row=0, column=6)

        tk.Button(self.panel_control, text="Insertar", command=self.accion_insertar, bg="#4CAF50", fg="white").grid(row=0, column=7, padx=10)
        
        # Panel Secundario (Eliminar y Recorridos)
        self.panel_secundario = tk.Frame(master, bg="#e0e0e0", pady=5)
        self.panel_secundario.pack(side=tk.TOP, fill=tk.X)

        tk.Label(self.panel_secundario, text="Valor a eliminar:", bg="#e0e0e0").grid(row=0, column=0, padx=5)
        self.entrada_eliminar = tk.Entry(self.panel_secundario, width=10)
        self.entrada_eliminar.grid(row=0, column=1, padx=5)
        tk.Button(self.panel_secundario, text="Eliminar", command=self.accion_eliminar, bg="#f44336", fg="white").grid(row=0, column=2, padx=10)

        tk.Button(self.panel_secundario, text="Mostrar Recorridos", command=self.accion_recorridos, bg="#2196F3", fg="white").grid(row=0, column=3, padx=20)

        # Lienzo (Canvas) para dibujar el árbol (Abajo)
        self.canvas = tk.Canvas(master, bg="white")
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # --- Acciones de Botones ---
    def accion_insertar(self):
        valor = self.entrada_valor.get().strip()
        padre = self.entrada_padre.get().strip()
        lado = self.var_lado.get()

        if not valor:
            messagebox.showwarning("Advertencia", "El valor a insertar no puede estar vacío.")
            return

        exito, mensaje = self.arbol.insertar(padre if padre else None, valor, lado)
        if exito:
            self.dibujar_arbol()
            self.entrada_valor.delete(0, tk.END)
        else:
            messagebox.showerror("Error", mensaje)

    def accion_eliminar(self):
        valor = self.entrada_eliminar.get().strip()
        if not valor:
            messagebox.showwarning("Advertencia", "Ingresa un valor para eliminar.")
            return

        exito, mensaje = self.arbol.eliminar(valor)
        if exito:
            self.dibujar_arbol()
            self.entrada_eliminar.delete(0, tk.END)
        else:
            messagebox.showerror("Error", mensaje)

    def accion_recorridos(self):
        if self.arbol.raiz is None:
            messagebox.showinfo("Recorridos", "El árbol está vacío.")
            return
            
        pre = " -> ".join(self.arbol.preorden(self.arbol.raiz))
        ino = " -> ".join(self.arbol.inorden(self.arbol.raiz))
        pos = " -> ".join(self.arbol.posorden(self.arbol.raiz))
        
        mensaje = f"PREORDEN:\n{pre}\n\nINORDEN:\n{ino}\n\nPOSORDEN:\n{pos}"
        messagebox.showinfo("Recorridos del Árbol", mensaje)

    # --- Lógica de Dibujo en el Canvas ---
    def dibujar_arbol(self):
        self.canvas.delete("all") # Limpia el lienzo antes de redibujar
        if self.arbol.raiz:
            # Iniciamos el dibujo desde el centro superior de la ventana
            ancho_canvas = self.canvas.winfo_width()
            if ancho_canvas == 1: ancho_canvas = 900 # Valor por defecto si aún no renderiza
            self._dibujar_nodo(self.arbol.raiz, ancho_canvas // 2, 50, ancho_canvas // 4)

    def _dibujar_nodo(self, nodo, x, y, desplazamiento_x):
        radio = 20
        espacio_vertical = 70

        # Dibujar línea hacia hijo izquierdo
        if nodo.izquierda:
            nx, ny = x - desplazamiento_x, y + espacio_vertical
            self.canvas.create_line(x, y, nx, ny, fill="black", width=2)
            self._dibujar_nodo(nodo.izquierda, nx, ny, desplazamiento_x // 1.8)

        # Dibujar línea hacia hijo derecho
        if nodo.derecha:
            nx, ny = x + desplazamiento_x, y + espacio_vertical
            self.canvas.create_line(x, y, nx, ny, fill="black", width=2)
            self._dibujar_nodo(nodo.derecha, nx, ny, desplazamiento_x // 1.8)

        # Dibujar el círculo del nodo (después de las líneas para que quede encima)
        self.canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill="#07EEFF", outline="black")
        # Dibujar el texto centrado
        self.canvas.create_text(x, y, text=str(nodo.valor), font=("Arial", 12, "bold"))

# Ejecución de la aplicación
if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacionArbol(raiz)
    raiz.mainloop()