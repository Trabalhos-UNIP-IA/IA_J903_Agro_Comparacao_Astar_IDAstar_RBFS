import time
import tracemalloc
import matplotlib.pyplot as plt
from algoritmos import custo

# =============================
# PERFORMANCE
# =============================

performance = []


def executar_algoritmo(nome, func, grid, start, goal):

    tracemalloc.start()

    t0 = time.perf_counter()

    path = func(grid, start, goal)

    t1 = time.perf_counter()

    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()

    tempo = t1 - t0

    # calcula energia usada
    energia = 0
    if path:
        for x, y in path[1:]:  # ignora posição inicial
            energia += custo(grid, x, y)

    performance.append(
        {"algoritmo": nome, "tempo": tempo, "memoria": mem, "energia": energia}
    )

    return path, tempo, mem


# =============================
# SCORE
# =============================


def calcular_score(alpha=0.5, beta=0.3, gamma=0.2):

    if not performance:
        return

    tempos = [r["tempo"] for r in performance]
    mems = [r["memoria"] for r in performance]
    energias = [r["energia"] for r in performance]

    max_t = max(tempos) or 1
    max_m = max(mems) or 1
    max_e = max(energias) or 1

    for r in performance:

        tempo_norm = 1 - (r["tempo"] / max_t)
        mem_norm = 1 - (r["memoria"] / max_m)
        energia_norm = 1 - (r["energia"] / max_e)

        score = alpha * tempo_norm + beta * mem_norm + gamma * energia_norm

        r["score"] = score


# =============================
# TABELA
# =============================


def mostrar_tabela():

    if not performance:
        return

    calcular_score()

    dados = []

    for r in performance:

        dados.append(
            [
                r["algoritmo"],
                "Retangular",
                "Circular",
                round(r["tempo"], 5),
                round(r["memoria"], 2),
                r["energia"],
                round(r["score"], 3),
            ]
        )

    colunas = [
        "Algoritmo",
        "Geom Inicial",
        "Geom Final",
        "Tempo (s)",
        "Memoria KB",
        "Energia",
        "Score",
    ]

    fig, ax = plt.subplots()

    ax.axis("off")

    tabela = ax.table(cellText=dados, colLabels=colunas, loc="center")

    tabela.scale(1.2, 1.5)

    plt.title("Matriz de Performance")

    plt.show()
# COMPARAR ALGORITMOS
def comparar_algoritmos(performance):

    performance.clear()

    algoritmos = [("A*", astar), ("IDA*", ida_star), ("RBFS", run_rbfs)]

    for nome, func in algoritmos:

        print("Executando:", nome)

        path ,performance= executar_algoritmo(nome, func,gridori)

        if path:
            animar(path,gridori)
        else:
            print("Nenhum caminho encontrado para", nome)

    mostrar_graficos(performance)