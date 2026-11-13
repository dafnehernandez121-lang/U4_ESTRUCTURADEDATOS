import tkinter as tk
from tkinter import messagebox
from collections import deque

class Nodo:
    def __init__(self, dato: int = 0):
        self.dato = dato
        self.izquierdoPtr = None
        self.derechoPtr = None


class Arbol:
    def __init__(self):
        self.raizPtr = None

    def __del__(self):
        self.raizPtr = self.podarArbol(self.raizPtr)

    def esVacio(self):
        return self.raizPtr is None

    def regresaRaiz(self):
        return self.raizPtr

    def insertarNodo(self, valor, nodoPtr):
        if nodoPtr is None:
            return Nodo(valor)
        if valor < nodoPtr.dato:
            nodoPtr.izquierdoPtr = self.insertarNodo(valor, nodoPtr.izquierdoPtr)
        elif valor > nodoPtr.dato:
            nodoPtr.derechoPtr = self.insertarNodo(valor, nodoPtr.derechoPtr)
        return nodoPtr

    def muestraAcostado(self, nivel, nodoPtr):
        if nodoPtr is None:
            return ""
        derecha = self.muestraAcostado(nivel + 1, nodoPtr.derechoPtr)
        actual = ("      " * nivel) + f"└── {nodoPtr.dato}\n" if nivel > 0 else f"[Raíz] {nodoPtr.dato}\n"
        izquierda = self.muestraAcostado(nivel + 1, nodoPtr.izquierdoPtr)
        return derecha + actual + izquierda

    def graficarArbol(self, canvas, nodoPtr, x, y, n, dx=170, resaltado=None):
        if nodoPtr is None:
            return
        for hijo, sig_x in ((nodoPtr.izquierdoPtr, x - dx), (nodoPtr.derechoPtr, x + dx)):
            if hijo:
                canvas.create_line(x, y, sig_x, y + 65, width=2, fill="#475569", arrow=tk.LAST)
                self.graficarArbol(canvas, hijo, sig_x, y + 65, n + 1, max(32, dx / 2), resaltado)

        es_hoja = (nodoPtr.izquierdoPtr is None and nodoPtr.derechoPtr is None)
        if nodoPtr.dato == resaltado:
            color = "#f87171"  
        elif n == 1:
            color = "#fbbf24"  
        elif es_hoja:
            color = "#4ade80"  
        else:
            color = "#93c5fd"  

        tag_valor = str(nodoPtr.dato)
        canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline="#1e293b", width=2, tags=tag_valor)
        canvas.create_text(x, y, text=tag_valor, font=("Segoe UI", 10, "bold"), tags=tag_valor)

    def busqueda(self, x, nodoPtr):
        if nodoPtr is None:
            return False
        if x == nodoPtr.dato:
            return True
        if x < nodoPtr.dato:
            return self.busqueda(x, nodoPtr.izquierdoPtr)
        return self.busqueda(x, nodoPtr.derechoPtr)

    def preOrden(self, n):
        if n is None:
            return ""
        return f"{n.dato} - " + self.preOrden(n.izquierdoPtr) + self.preOrden(n.derechoPtr)

    def inOrden(self, n):
        if n is None:
            return ""
        return self.inOrden(n.izquierdoPtr) + f"{n.dato} - " + self.inOrden(n.derechoPtr)

    def postOrden(self, n):
        if n is None:
            return ""
        return self.postOrden(n.izquierdoPtr) + self.postOrden(n.derechoPtr) + f"{n.dato} - "

    def buscaMenor(self, n):
        return n if (n is None or n.izquierdoPtr is None) else self.buscaMenor(n.izquierdoPtr)

    def buscaMayor(self, n):
        return n if (n is None or n.derechoPtr is None) else self.buscaMayor(n.derechoPtr)

    def eliminarPredecesor(self, x, n):
        if n is None:
            return None
        if x < n.dato:
            n.izquierdoPtr = self.eliminarPredecesor(x, n.izquierdoPtr)
        elif x > n.dato:
            n.derechoPtr = self.eliminarPredecesor(x, n.derechoPtr)
        elif n.izquierdoPtr and n.derechoPtr:
            mayor = self.buscaMayor(n.izquierdoPtr)
            n.dato = mayor.dato
            n.izquierdoPtr = self.eliminarPredecesor(mayor.dato, n.izquierdoPtr)
        else:
            n = n.izquierdoPtr if n.izquierdoPtr else n.derechoPtr
        return n

    def eliminarSucesor(self, x, n):
        if n is None:
            return None
        if x < n.dato:
            n.izquierdoPtr = self.eliminarSucesor(x, n.izquierdoPtr)
        elif x > n.dato:
            n.derechoPtr = self.eliminarSucesor(x, n.derechoPtr)
        elif n.izquierdoPtr and n.derechoPtr:
            menor = self.buscaMenor(n.derechoPtr)
            n.dato = menor.dato
            n.derechoPtr = self.eliminarSucesor(menor.dato, n.derechoPtr)
        else:
            n = n.izquierdoPtr if n.izquierdoPtr else n.derechoPtr
        return n

    def recorridoNiveles(self, nodoPtr):
        if nodoPtr is None:
            return ""
        colaAuxiliar, visitados = deque([nodoPtr]), []
        while colaAuxiliar:
            nodoAuxiliar = colaAuxiliar.popleft()
            visitados.append(str(nodoAuxiliar.dato))
            if nodoAuxiliar.izquierdoPtr:
                colaAuxiliar.append(nodoAuxiliar.izquierdoPtr)
            if nodoAuxiliar.derechoPtr:
                colaAuxiliar.append(nodoAuxiliar.derechoPtr)
        return " - ".join(visitados) + " -"

    def altura(self, n):
        return 0 if n is None else 1 + max(self.altura(n.izquierdoPtr), self.altura(n.derechoPtr))

    def contarHojas(self, n):
        if n is None:
            return 0
        if n.izquierdoPtr is None and n.derechoPtr is None:
            return 1
        return self.contarHojas(n.izquierdoPtr) + self.contarHojas(n.derechoPtr)

    def contarNodos(self, n):
        return 0 if n is None else 1 + self.contarNodos(n.izquierdoPtr) + self.contarNodos(n.derechoPtr)

    def arbolEspejo(self, n):
        if n is None:
            return None
        espejo = Nodo(n.dato)
        espejo.izquierdoPtr = self.arbolEspejo(n.derechoPtr)
        espejo.derechoPtr = self.arbolEspejo(n.izquierdoPtr)
        return espejo

    def esCompleto(self, nodoPtr):
        if nodoPtr is None:
            return True
        colaAuxiliar, nodoNoLleno = deque([nodoPtr]), False
        while colaAuxiliar:
            nodoAuxiliar = colaAuxiliar.popleft()
            for hijo in (nodoAuxiliar.izquierdoPtr, nodoAuxiliar.derechoPtr):
                if hijo:
                    if nodoNoLleno:
                        return False
                    colaAuxiliar.append(hijo)
                else:
                    nodoNoLleno = True
        return True

    def esLleno(self, n):
        if n is None or (n.izquierdoPtr is None and n.derechoPtr is None):
            return True
        if n.izquierdoPtr and n.derechoPtr:
            return self.esLleno(n.izquierdoPtr) and self.esLleno(n.derechoPtr)
        return False

    def podarArbol(self, n):
        if n:
            self.podarArbol(n.izquierdoPtr)
            self.podarArbol(n.derechoPtr)
        return None


# =====================================================================
# 2. INTERFAZ GRÁFICA INTUITIVA (Tkinter)
# =====================================================================
class InterfazArbol:
    def __init__(self, root):
        self.arbol = Arbol()
        root.title("Simulador Visual de Árbol Binario de Búsqueda (ABB)")
        root.geometry("1100x680")
        root.configure(bg="#f8fafc")

        panel = tk.Frame(root, bg="#f8fafc", padx=12, pady=10, width=280)
        panel.pack(side=tk.LEFT, fill=tk.Y)

        g1 = tk.LabelFrame(panel, text=" 1. Nodos (Escribe o haz clic en el dibujo) ", font=("Segoe UI", 9, "bold"), bg="white", padx=8, pady=8)
        g1.pack(fill=tk.X, pady=(0, 8))

        tk.Label(g1, text="Valor o lista (ej: 8, 3, 20):", font=("Segoe UI", 8), bg="white", fg="#475569").pack(anchor="w")
        self.entrada = tk.Entry(g1, font=("Segoe UI", 11), justify="center", bg="#f1f5f9")
        self.entrada.pack(fill=tk.X, pady=4)
        self.entrada.bind("<Return>", lambda e: self.insertar())

        tk.Button(g1, text=" Insertar (Enter)", command=self.insertar, bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), relief="flat").pack(fill=tk.X, pady=2)
        tk.Button(g1, text=" Buscar nodo", command=self.buscar, bg="#0284c7", fg="white", font=("Segoe UI", 9, "bold"), relief="flat").pack(fill=tk.X, pady=2)
        tk.Button(g1, text=" Eliminar por Predecesor", command=lambda: self.eliminar(predecesor=True), bg="#dc2626", fg="white", font=("Segoe UI", 9), relief="flat").pack(fill=tk.X, pady=2)
        tk.Button(g1, text=" Eliminar por Sucesor", command=lambda: self.eliminar(predecesor=False), bg="#e11d48", fg="white", font=("Segoe UI", 9), relief="flat").pack(fill=tk.X, pady=2)

        g2 = tk.LabelFrame(panel, text=" 2. Recorridos del Árbol ", font=("Segoe UI", 9, "bold"), bg="white", padx=8, pady=6)
        g2.pack(fill=tk.X, pady=(0, 8))

        tk.Button(g2, text=" PreOrden (Raíz - Izq - Der)", command=lambda: self.recorrer(5), bg="#e2e8f0", relief="flat").pack(fill=tk.X, pady=2)
        tk.Button(g2, text=" InOrden (Ascendente)", command=lambda: self.recorrer(6), bg="#e2e8f0", relief="flat").pack(fill=tk.X, pady=2)
        tk.Button(g2, text=" PostOrden (Izq - Der - Raíz)", command=lambda: self.recorrer(7), bg="#e2e8f0", relief="flat").pack(fill=tk.X, pady=2)
        tk.Button(g2, text=" Por Niveles (Amplitud)", command=lambda: self.recorrer(10), bg="#e2e8f0", relief="flat").pack(fill=tk.X, pady=2)

        g3 = tk.LabelFrame(panel, text=" 3. Vistas y Utilidades ", font=("Segoe UI", 9, "bold"), bg="white", padx=8, pady=6)
        g3.pack(fill=tk.X)

        tk.Button(g3, text=" Ver Árbol Original", command=self.actualizar_todo, bg="#0d9488", fg="white", relief="flat").pack(fill=tk.X, pady=2)
        tk.Button(g3, text=" Ver Árbol Espejo", command=self.ver_espejo, bg="#7c3aed", fg="white", relief="flat").pack(fill=tk.X, pady=2)
        tk.Button(g3, text=" Mostrar Acostado (Texto)", command=self.ver_acostado, bg="#475569", fg="white", relief="flat").pack(fill=tk.X, pady=2)
        tk.Button(g3, text=" Cargar Ejemplo de Clase", command=self.cargar_ejemplo, bg="#fef08a", fg="#854d0e", font=("Segoe UI", 9, "bold"), relief="flat").pack(fill=tk.X, pady=(6, 2))
        tk.Button(g3, text=" Vaciar / Podar Árbol", command=self.podar, bg="#991b1b", fg="white", relief="flat").pack(fill=tk.X, pady=2)

        der = tk.Frame(root, bg="#f8fafc", padx=10, pady=10)
        der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.lbl_metricas = tk.Label(der, text="", font=("Segoe UI", 10, "bold"), bg="#1e293b", fg="white", pady=8)
        self.lbl_metricas.pack(fill=tk.X, pady=(0, 6))

        self.canvas = tk.Canvas(der, bg="white", height=440, highlightthickness=1, highlightbackground="#cbd5e1", cursor="hand2")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.clic_en_nodo)

        self.consola = tk.Text(der, height=7, bg="#0f172a", fg="#38bdf8", font=("Consolas", 10), padx=10, pady=8)
        self.consola.pack(fill=tk.X, pady=(8, 0))

        self.actualizar_todo()
        self.escribir(" Tip: Escribe varios números separados por coma (ej. 8, 3, 1, 20) o presiona '⚡ Cargar Ejemplo de Clase'.")

    def escribir(self, texto):
        self.consola.delete("1.0", tk.END)
        self.consola.insert(tk.END, texto)

    def clic_en_nodo(self, event):
        item = self.canvas.find_withtag("current")
        if item:
            tags = self.canvas.gettags(item[0])
            if tags and tags[0].lstrip("-").isdigit():
                self.entrada.delete(0, tk.END)
                self.entrada.insert(0, tags[0])
                self.actualizar_todo(resaltado=int(tags[0]))
                self.escribir(f"Nodo [{tags[0]}] seleccionado. Ahora puedes eliminarlo con los botones rojos.")

    def actualizar_todo(self, nodo_raiz=None, resaltado=None):
        self.canvas.delete("all")
        r = self.arbol.regresaRaiz()
        nodo_dibujo = nodo_raiz if nodo_raiz is not None else r

        if self.arbol.esVacio():
            self.lbl_metricas.config(text="Árbol Vacío  |  [11] Altura: 0  |  [12] Hojas: 0  |  [13] Nodos: 0")
            self.canvas.create_text(380, 200, text="Árbol vacío.\nUsa el panel izquierdo para insertar valores.", font=("Segoe UI", 12), fill="#94a3b8", justify="center")
            return

        self.canvas.create_text(15, 15, anchor="nw", fill="#475569", font=("Segoe UI", 8, "bold"),
                                text=" Raíz     Rama     Hoja     Seleccionado (Haz clic en cualquier nodo para seleccionarlo)")

        self.arbol.graficarArbol(self.canvas, nodo_dibujo, 390, 50, 1, 175, resaltado)

        alt = self.arbol.altura(r)
        hojas = self.arbol.contarHojas(r)
        nodos = self.arbol.contarNodos(r)
        comp = "SÍ" if self.arbol.esCompleto(r) else "NO"
        lleno = "SÍ" if self.arbol.esLleno(r) else "NO"
        self.lbl_metricas.config(
            text=f" Altura: {alt}   |    Hojas: {hojas}   |    Nodos: {nodos}   |    ¿Completo?: {comp}   |    ¿Lleno?: {lleno}"
        )

    def insertar(self):
        texto = self.entrada.get().replace(",", " ").split()
        if not texto:
            return messagebox.showwarning("Atención", "Escribe al menos un número entero.")
        try:
            valores = [int(x) for x in texto]
            for v in valores:
                self.arbol.raizPtr = self.arbol.insertarNodo(v, self.arbol.regresaRaiz())
            self.entrada.delete(0, tk.END)
            self.actualizar_todo(resaltado=valores[-1])
            self.escribir(f" Se insertó correctamente: {valores}")
        except ValueError:
            messagebox.showerror("Error", "Ingresa únicamente números enteros válidos.")

    def buscar(self):
        try:
            x = int(self.entrada.get().strip())
            existe = self.arbol.busqueda(x, self.arbol.regresaRaiz())
            self.actualizar_todo(resaltado=x if existe else None)
            self.escribir(f" Búsqueda de {x}: {'¡ENCONTRADO! (Resaltado en rojo)' if existe else 'NO existe en el árbol.'}")
        except ValueError:
            messagebox.showwarning("Atención", "Escribe un número entero a buscar.")

    def eliminar(self, predecesor=True):
        try:
            x = int(self.entrada.get().strip())
            r = self.arbol.regresaRaiz()
            if not self.arbol.busqueda(x, r):
                return self.escribir(f" El nodo {x} no existe en el árbol.")
            if predecesor:
                self.arbol.raizPtr = self.arbol.eliminarPredecesor(x, r)
                metodo = " PREDECESOR (mayor del subárbol izquierdo)"
            else:
                self.arbol.raizPtr = self.arbol.eliminarSucesor(x, r)
                metodo = " SUCESOR (menor del subárbol derecho)"
            self.entrada.delete(0, tk.END)
            self.actualizar_todo()
            self.escribir(f" Nodo {x} eliminado usando {metodo}.")
        except ValueError:
            messagebox.showwarning("Atención", "Escribe o haz clic sobre el nodo que deseas eliminar.")

    def recorrer(self, op):
        if self.arbol.esVacio():
            return self.escribir("El árbol está vacío.")
        r = self.arbol.regresaRaiz()
        if op == 5:
            self.escribir(f" Recorrido PreOrden (Raíz - Izquierdo - Derecho):\n\n   {self.arbol.preOrden(r)}")
        elif op == 6:
            self.escribir(f" Recorrido InOrden (Izquierdo - Raíz - Derecho):\n\n   {self.arbol.inOrden(r)}")
        elif op == 7:
            self.escribir(f" Recorrido PostOrden (Izquierdo - Derecho - Raíz):\n\n   {self.arbol.postOrden(r)}")
        elif op == 10:
            self.escribir(f" Recorrido por Niveles (Amplitud con Cola):\n\n   {self.arbol.recorridoNiveles(r)}")

    def ver_acostado(self):
        if self.arbol.esVacio():
            return self.escribir("El árbol está vacío.")
        self.escribir(" Árbol acostado con la raíz a la izquierda:\n\n" + self.arbol.muestraAcostado(0, self.arbol.regresaRaiz()))

    def ver_espejo(self):
        if self.arbol.esVacio():
            return self.escribir("El árbol está vacío.")
        espejo = self.arbol.arbolEspejo(self.arbol.regresaRaiz())
        self.actualizar_todo(nodo_raiz=espejo)
        self.escribir(" Mostrando Árbol Espejo en pantalla (subárboles izquierdo y derecho invertidos):\n\n" + self.arbol.muestraAcostado(0, espejo))

    def cargar_ejemplo(self):
        self.arbol.raizPtr = self.arbol.podarArbol(self.arbol.regresaRaiz())
        ejemplo = [8, 3, 1, 20, 5, 10, 7, 4]
        for v in ejemplo:
            self.arbol.raizPtr = self.arbol.insertarNodo(v, self.arbol.regresaRaiz())
        self.actualizar_todo()
        self.escribir(f" Árbol de ejemplo de las diapositivas cargado: {ejemplo}\nHaz clic sobre cualquier círculo del dibujo para seleccionarlo.")

    def podar(self):
        self.arbol.raizPtr = self.arbol.podarArbol(self.arbol.regresaRaiz())
        self.actualizar_todo()
        self.escribir(" Árbol eliminado (podado) por completo.")


if __name__ == "__main__":
    ventana = tk.Tk()
    InterfazArbol(ventana)
    ventana.mainloop()
