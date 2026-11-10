C, G, Y, W = '\033[96m', '\033[92m', '\033[93m', '\033[0m'

class GrafoKruskalGrafico:
    def __init__(self, vertices):
        self.V = vertices
        self.aristas = []

    def agregar_arista(self, u, v, peso):
        self.aristas.append([u, v, peso])

    def buscar(self, padre, i):
        if padre[i] == i: return i
        return self.buscar(padre, padre[i])

    def unir(self, padre, rango, x, y):
        raiz_x = self.buscar(padre, x)
        raiz_y = self.buscar(padre, y)
        if rango[raiz_x] < rango[raiz_y]: padre[raiz_x] = raiz_y
        elif rango[raiz_x] > rango[raiz_y]: padre[raiz_y] = raiz_x
        else:
            padre[raiz_y] = raiz_x
            rango[raiz_x] += 1

    def kruskal(self):
        resultado = []
        i, e = 0, 0
        self.aristas = sorted(self.aristas, key=lambda item: item[2])
        padre = [nodo for nodo in range(self.V)]
        rango = [0] * self.V

        while e < self.V - 1:
            u, v, peso = self.aristas[i]
            i += 1
            x = self.buscar(padre, u)
            y = self.buscar(padre, v)

            if x != y:
                e += 1
                resultado.append([u, v, peso])
                self.unir(padre, rango, x, y)

        # --- IMPRESIÓN GRÁFICA ---
        print(f"{C}================================================={W}")
        print(f"{C} 🌳 KRUSKAL - ÁRBOL DE EXPANSIÓN MÍNIMA (MST) {W}")
        print(f"{C}================================================={W}")
        print(" ARISTA SELECCIONADA       │ PESO")
        print("───────────────────────────┼───────")
        
        costo_minimo = 0
        for u, v, peso in resultado:
            costo_minimo += peso
            print(f" {Y}Nodo {u}{W}  <======>  {Y}Nodo {v}{W} │  {G}{peso}{W}")
            
        print("───────────────────────────┴───────")
        print(f" {C}COSTO TOTAL DEL ÁRBOL:{W}        {G}{costo_minimo}{W}")
        print(f"{C}================================================={W}\n")

# Prueba
g = GrafoKruskalGrafico(4)
g.agregar_arista(0, 1, 10)
g.agregar_arista(0, 2, 6)
g.agregar_arista(0, 3, 5)
g.agregar_arista(1, 3, 15)
g.agregar_arista(2, 3, 4)

g.kruskal()