import heapq
from config import LINHAS, COLUNAS, DIRECOES, CUSTO_MOVIMENTO, E_MAX
import tracemalloc
import time 

def neighbors(grid,n):

    x, y = n
    result = []

    for dx, dy in DIRECOES:

        nx = x + dx
        ny = y + dy

        if 0 <= nx < LINHAS and 0 <= ny < COLUNAS:

            # evita obstáculos
            if grid[nx][ny] != 1:
                result.append((nx, ny))

    return result
# =============================
# HEURÍSTICA
# =============================


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# =============================
# VIZINHOS
# =============================


def custo(valor,custo_movimento):

    if valor == 2 or valor == 3:
        return custo_movimento * 1.5
    else:
        return custo_movimento
# =============================
# CUSTO
# =============================

# =============================
# A*
# =============================


def astar(start, goal,grid):

    open_list = []
    heapq.heappush(open_list, (0, start))
    path = []
    came = {}
    g = {start: 0}

    while open_list:

        _, current = heapq.heappop(open_list)

        if current == goal:

            

            while current in came:
                path.append(current)
                current = came[current]

            path.append(start)
            path.reverse()

            return path

        for n in neighbors(grid,current):

            tentative = g[current] + custo(n[0], n[1])

            if tentative > E_MAX:
                continue

            if n not in g or tentative < g[n]:

                g[n] = tentative
                f = tentative + heuristic(n, goal)

                heapq.heappush(open_list, (f, n))
                came[n] = current

    return [] 
#search
def search(path, g, bound,goal,grid):

        node = path[-1]

        f = g + heuristic(node, goal)

        if f > bound:
            return f

        if node == goal:
            return path.copy()

        minimum = float("inf")

        for n in neighbors(grid,node):

            if n in path:
                continue

            cost = custo(n[0], n[1])

            path.append(n)

            t = search(path, g + cost, bound,goal,grid)

            if isinstance(t, list):
                return t

            if t < minimum:
                minimum = t

            path.pop()

        return minimum


# IDA*
def ida_star(start, goal,grid):

    bound = heuristic(start, goal)
    path = [start]


    while True:

        t = search(path, 0, bound,goal,grid)

        if isinstance(t, list):
            return t

        if t == float("inf"):
            return []

        bound = t

# RBFS
def rbfs(node, goal, g, bound, path,grid):

    f = g + heuristic(node, goal)

    if f > bound:
        return None, f

    if node == goal:
        return path, f

    successors = []

    for n in neighbors(grid,node):

        if n in path:
            continue

        cost = custo(n[0], n[1])

        successors.append((n, g + cost + heuristic(n, goal), cost))

    if not successors:
        return None, float("inf")

    while True:

        successors.sort(key=lambda x: x[1])

        best, best_f, best_cost = successors[0]

        if best_f > bound:
            return None, best_f

        alt = successors[1][1] if len(successors) > 1 else float("inf")

        result, new_f = rbfs(best, goal, g + best_cost, min(bound, alt), path + [best],grid)

        successors[0] = (best, new_f, best_cost)

        if result:
            return result, new_f

def run_rbfs(start, goal,grid):

    path, _ = rbfs(start, goal, 0, float("inf"), [start],grid)
    return path

# VARREDURA INTELIGENTE
def executar_algoritmo(start,goal,nome, func,grid,performance):
    ini = time.time()
    tracemalloc.start()
    t0 = time.perf_counter()

    area_ret = pegar_regiao(2,grid)
    area_circ = pegar_regiao(3,grid)

    # ir até a primeira área
    entrada = min(area_ret, key=lambda c: heuristic(start, c))
    path1 = func(start, entrada,grid)

    # cobrir área retangular
    path2 = cobrir_regiao(entrada, area_ret, func,grid)

    ultimo = path2[-1] if path2 else entrada

    # ir para área circular
    entrada2 = min(area_circ, key=lambda c: heuristic(ultimo, c))
    path3 = func(ultimo, entrada2,grid)

    # cobrir área circular
    path4 = cobrir_regiao(entrada2, area_circ, func,grid)
    #
    entrada3 = path4[-1] if path4 else entrada2
    path5 = func(entrada3,goal,grid)
    path = path1 + path2 + path3 + path4 + path5
    tempo = time.perf_counter() - t0

    current, peak = tracemalloc.get_traced_memory()
    mem = peak / 1024
    tracemalloc.stop()

    energia = sum(custo(x, y) for x, y in path)
    print(fr' esse foi o tempo{tempo}')
    performance.append(
        {"algoritmo": nome, "tempo": tempo, "memoria": mem, "energia": energia}
    )

    return path,performance 

def cobrir_regiao(start_pos, area, algoritmo,grid):

    caminho_total = []
    atual = start_pos

    area_restante = set(area)

    while area_restante:

        # escolher ponto mais próximo
        alvo = min(area_restante, key=lambda c: heuristic(atual, c))

        caminho = algoritmo(atual, alvo,grid)

        if not caminho:
            # se não encontrar caminho remove o ponto
            area_restante.remove(alvo)
            continue

        caminho_total += caminho[1:]

        atual = alvo

        area_restante.remove(alvo)

    return caminho_total

def pegar_regiao(tipo,grid):

    regiao = []

    for i in range(LINHAS):
        for j in range(COLUNAS):

            if grid[i][j] == tipo:
                regiao.append((i, j))

    return regiao