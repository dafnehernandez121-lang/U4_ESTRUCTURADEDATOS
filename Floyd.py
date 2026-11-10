INF = float('inf')
C, G, Y, W = '\033[96m', '\033[92m', '\033[93m', '\033[0m'

def imprimir_matriz(matriz, titulo):
    n = len(matriz)
    print(f"{C}=== {titulo} ==={W}")
    print("    │ " + " │ ".join([f"N{i}" for i in range(n)]) + " │")
    print("────" + "┼────" * n + "┤")
    for i in range(n):
        fila = []
        for val in matriz[i]:
            if val == INF: fila.append(f"{Y} ∞{W}")
            else: fila.append(f"{G}{val:2}{W}")
        print(f" N{i} │ " + " │ ".join(fila) + " │")
    print("────" + "┴────" * n + "┘\n")

def floyd_grafico(grafo_matriz):
    n = len(grafo_matriz)
    dist = [[grafo_matriz[i][j] for j in range(n)] for i in range(n)]
    
    imprimir_matriz(dist, "MATRIZ INICIAL (Distancias Directas)")

    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    imprimir_matriz(dist, "MATRIZ FINAL (Floyd-Warshall - Distancias Mínimas)")

# Prueba
matriz_grafo = [
    [0,   5, INF, 10],
    [INF, 0,   3, INF],
    [INF, INF, 0,   1],
    [INF, INF, INF, 0]
]
floyd_grafico(matriz_grafo)