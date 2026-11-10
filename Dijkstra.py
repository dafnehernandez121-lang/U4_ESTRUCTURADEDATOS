import heapq

# Códigos de color para la terminal
C = '\033[96m' # Cyan
G = '\033[92m' # Verde
Y = '\033[93m' # Amarillo
W = '\033[0m'  # Reset

def dijkstra_grafico(grafo, origen):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0
    padres = {nodo: None for nodo in grafo} # Para rastrear el camino
    cola = [(0, origen)]

    while cola:
        dist_actual, nodo_actual = heapq.heappop(cola)
        if dist_actual > distancias[nodo_actual]: continue

        for vecino, peso in grafo[nodo_actual].items():
            distancia = dist_actual + peso
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                padres[vecino] = nodo_actual
                heapq.heappush(cola, (distancia, vecino))

    # --- IMPRESIÓN GRÁFICA ---
    print(f"{C}=================================================={W}")
    print(f"{C}   📍 ALGORITMO DE DIJKSTRA (Desde nodo '{origen}'){W}")
    print(f"{C}=================================================={W}")
    print("DESTINO\t│ DISTANCIA\t│ RUTA MÁS CORTA")
    print("────────┼───────────────┼─────────────────────────")
    
    for nodo in grafo:
        if distancias[nodo] == float('inf'):
            print(f"   {nodo}\t│      ∞\t│ Sin ruta")
        else:
            # Reconstruir camino
            camino = []
            actual = nodo
            while actual is not None:
                camino.insert(0, actual)
                actual = padres[actual]
            ruta_str = f" {Y}➞{W} ".join(camino)
            print(f"   {G}{nodo}{W}\t│      {G}{distancias[nodo]}{W}\t│ {ruta_str}")
    print(f"{C}=================================================={W}\n")

# Prueba
grafo_prueba = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}
dijkstra_grafico(grafo_prueba, 'A')