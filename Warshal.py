C, G, R, W = '\033[96m', '\033[92m', '\033[91m', '\033[0m'

def imprimir_alcanzabilidad(matriz, titulo):
    n = len(matriz)
    print(f"{C}=== {titulo} ==={W}")
    for i in range(n):
        fila_str = ""
        for j in range(n):
            if matriz[i][j] == 1:
                fila_str += f" [{G}✓{W}] " # Conexión
            else:
                fila_str += f" [{R}-{W}] " # Sin conexión
        print(f" Nodo {i} ➞ " + fila_str)
    print()

def warshall_grafico(matriz_adyacencia):
    n = len(matriz_adyacencia)
    alcanzabilidad = [[matriz_adyacencia[i][j] for j in range(n)] for i in range(n)]
    
    imprimir_alcanzabilidad(alcanzabilidad, "GRAFO ORIGINAL (Conexiones Directas)")

    for k in range(n):
        for i in range(n):
            for j in range(n):
                alcanzabilidad[i][j] = alcanzabilidad[i][j] or (alcanzabilidad[i][k] and alcanzabilidad[k][j])

    imprimir_alcanzabilidad(alcanzabilidad, "CIERRE TRANSITIVO (Todas las rutas posibles)")

# Prueba
matriz_booleana = [
    [1, 1, 0, 1],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]
warshall_grafico(matriz_booleana)