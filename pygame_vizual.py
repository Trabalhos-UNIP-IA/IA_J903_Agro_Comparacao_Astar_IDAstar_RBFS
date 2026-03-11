import pygame
import heapq
import random
import time
import tracemalloc
import matplotlib.pyplot as plt

# =============================
# CONFIGURAÇÃO
# =============================

pygame.init()

TAMANHO = 24
LINHAS = 30
COLUNAS = 30

LARGURA = COLUNAS * TAMANHO + 300
ALTURA = LINHAS * TAMANHO

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Planejamento de Rotas - Drone Agrícola")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 16)

E_MAX = 100  # energia máxima do drone
CUSTO_MOVIMENTO = 1  # custo de energia para cada movimento
bateria = E_MAX
largura_barra = 120


DIRECOES = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# =============================
# CORES
# =============================

BRANCO = (255, 255, 255)
PRETO = (30, 30, 30)
AZUL = (80, 140, 255)
AMARELO = (255, 220, 0)
VERDE = (0, 200, 100)
VERMELHO = (255, 50, 50)
CINZA = (200, 200, 200)

# =============================
# POSIÇÕES
# =============================

start = (1, 1)
goal = (26, 26)

# =============================
# GERAR MAPA
# =============================


def gerar_mapa():

    grid = [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]

    # região retangular
    for i in range(10):
        for j in range(12):
            grid[i][j] = 2

    # região circular
    cx, cy = 22, 22
    r = 6

    for i in range(LINHAS):
        for j in range(COLUNAS):
            if (i - cx) ** 2 + (j - cy) ** 2 <= r**2:
                grid[i][j] = 3

    # obstáculos
    # for i in range(LINHAS):
    #     for j in range(COLUNAS):

    #         if grid[i][j] == 0 and random.random() < 0.18:
    #             grid[i][j] = 1

    # garantir start e goal livres
    grid[start[0]][start[1]] = 0
    grid[goal[0]][goal[1]] = 0

    return grid


grid = gerar_mapa()

# =============================
# HEURÍSTICA
# =============================


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# =============================
# VIZINHOS
# =============================


def neighbors(n):

    x, y = n
    result = []

    for dx, dy in DIRECOES:

        nx = x + dx
        ny = y + dy

        if 0 <= nx < LINHAS and 0 <= ny < COLUNAS:

            if grid[nx][ny] != 1:
                result.append((nx, ny))

    return result


# =============================
# CUSTO
# =============================
def custo(x, y):

    if grid[x][y] == 2:
        return CUSTO_MOVIMENTO * 0.5
    elif grid[x][y] == 3:
        return CUSTO_MOVIMENTO * 1.5
    else:
        return CUSTO_MOVIMENTO


# =============================
# A*
# =============================


def astar(start, goal):

    open_list = []
    heapq.heappush(open_list, (0, start))

    came = {}
    g = {start: 0}

    closed = set()

    while open_list:

        _, current = heapq.heappop(open_list)

        if current in closed:
            continue

        closed.add(current)

        if current == goal:

            path = []

            while current in came:
                path.append(current)
                current = came[current]

            path.append(start)
            path.reverse()

            return path

        for n in neighbors(current):

            tentative = g[current] + custo(n[0], n[1])

            if tentative > bateria:
                continue

            if n not in g or tentative < g[n]:

                g[n] = tentative
                f = tentative + heuristic(n, goal)

                heapq.heappush(open_list, (f, n))
                came[n] = current

    return None


# =============================
# IDA*
# =============================


def ida_star(start, goal):

    bound = heuristic(start, goal)
    path = [start]

    def search(path, g, bound):

        node = path[-1]

        if g > E_MAX:
            return float("inf")

        f = g + heuristic(node, goal)

        if f > bound:
            return f

        if node == goal:
            return path.copy()

        minimum = float("inf")

        for n in neighbors(node):

            if n in path:
                continue

            path.append(n)

            t = search(path, g + 1, bound)

            if isinstance(t, list):
                return t

            if t < minimum:
                minimum = t

            path.pop()

        return minimum

    while True:

        t = search(path, 0, bound)

        if isinstance(t, list):
            return t

        if t == float("inf"):
            return None

        bound = t


# =============================
# RBFS
# =============================


def rbfs(node, goal, g, bound, path):

    f = g + heuristic(node, goal)

    if f > bound:
        return None, f

    if node == goal:
        return path, f

    successors = []

    for n in neighbors(node):

        if n in path:
            continue

        if g + 1 > E_MAX:
            continue

        successors.append((n, g + 1 + heuristic(n, goal)))

    if not successors:
        return None, float("inf")

    while True:

        successors.sort(key=lambda x: x[1])

        best, best_f = successors[0]

        if best_f > bound:
            return None, best_f

        alt = successors[1][1] if len(successors) > 1 else float("inf")

        result, new_f = rbfs(best, goal, g + 1, min(bound, alt), path + [best])

        successors[0] = (best, new_f)

        if result:
            return result, new_f


def run_rbfs(start, goal):

    path, _ = rbfs(start, goal, 0, float("inf"), [start])
    return path


# =============================
# PERFORMANCE
# =============================

performance = []


def executar_algoritmo(nome, func):

    tracemalloc.start()

    t0 = time.perf_counter()

    path = func(start, goal)

    t1 = time.perf_counter()

    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()

    tempo = t1 - t0
    energia = sum(custo(x, y) for x, y in path) if path else 0

    performance.append(
        {"algoritmo": nome, "tempo": tempo, "memoria": mem, "energia": energia}
    )

    return path, tempo, mem


# =============================
# SCORE
# =============================


def calcular_score(alpha=0.6, beta=0.4):

    tempos = [r["tempo"] for r in performance]
    mems = [r["memoria"] for r in performance]

    max_t = max(tempos) or 1
    max_m = max(mems) or 1

    for r in performance:

        tempo_norm = 1 - (r["tempo"] / max_t)
        mem_norm = 1 - (r["memoria"] / max_m)

        score = alpha * tempo_norm + beta * mem_norm

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
        "Tempo",
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


# =============================
# DESENHO
# =============================


def desenhar(path=None, drone=None):

    tela.fill(BRANCO)

    for i in range(LINHAS):
        for j in range(COLUNAS):

            rect = pygame.Rect(j * TAMANHO, i * TAMANHO, TAMANHO, TAMANHO)

            if grid[i][j] == 1:
                pygame.draw.rect(tela, [0,100,0], rect)

            elif grid[i][j] == 2:
                pygame.draw.rect(tela, AZUL, rect)

            elif grid[i][j] == 3:
                pygame.draw.rect(tela, AMARELO, rect)

            pygame.draw.rect(tela, CINZA, rect, 1)

    if path:

        for x, y in path:

            rect = pygame.Rect(y * TAMANHO, x * TAMANHO, TAMANHO, TAMANHO)
            pygame.draw.rect(tela, VERDE, rect)

    # start
    pygame.draw.circle(
        tela,
        (0, 255, 0),
        (start[1] * TAMANHO + TAMANHO // 2, start[0] * TAMANHO + TAMANHO // 2),
        TAMANHO // 3,
    )

    # goal
    pygame.draw.circle(
        tela,
        (255, 0, 0),
        (goal[1] * TAMANHO + TAMANHO // 2, goal[0] * TAMANHO + TAMANHO // 2),
        TAMANHO // 3,
    )

    if drone:

        x, y = drone

        pygame.draw.circle(
            tela,
            VERMELHO,
            (y * TAMANHO + TAMANHO // 2, x * TAMANHO + TAMANHO // 2),
            TAMANHO // 3,
        )


# =============================
# UI
# =============================

path = None


def desenhar_ui():

    global path, bateria, largura_barra

    x_offset = COLUNAS * TAMANHO + 20

    energia_restante = bateria

    textos = [
        "CONTROLES",
        "1 - A*",
        "2 - IDA*",
        "3 - RBFS",
        "R - Novo mapa",
        "T - Mostrar tabela",
    ]

    y = 20

    for t in textos:

        img = fonte.render(t, True, PRETO)
        tela.blit(img, (x_offset, y))
        y += 25

    y += 20

    bateria_texto = f"Bateria restante: {energia_restante}"
    img = fonte.render(bateria_texto, True, PRETO)
    tela.blit(img, (x_offset, y))

    # DESENHO BARRA DE ENERGIA

    pygame.draw.rect(tela, PRETO, (x_offset, y + 30, largura_barra, 20), 2)
    energia_visual = int((bateria / E_MAX) * largura_barra)
    pygame.draw.rect(tela, VERDE, (x_offset, y + 30, energia_visual, 20))


# =============================
# ANIMAÇÃO
# =============================


def animar(path):

    global bateria

    if not path:
        print("Nenhum caminho encontrado")
        return

    for p in path:

        x, y = p
        gasto = custo(x, y)

        if bateria - gasto < 0:
            print("Bateria insuficiente para continuar!")
            break

        bateria -= gasto

        desenhar(path, p)
        desenhar_ui()

        pygame.display.update()
        pygame.time.delay(70)


# =============================
# LOOP
# =============================

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                grid = gerar_mapa()
                path = None

            if event.key == pygame.K_1:

                bateria = E_MAX
                path, tempo, mem = executar_algoritmo("A*", astar)
                animar(path)

            if event.key == pygame.K_2:

                bateria = E_MAX
                path, tempo, mem = executar_algoritmo("IDA*", ida_star)
                animar(path)

            if event.key == pygame.K_3:

                bateria = E_MAX
                path, tempo, mem = executar_algoritmo("RBFS", run_rbfs)
                animar(path)

            if event.key == pygame.K_t:

                mostrar_tabela()
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                exit()

    desenhar(path, start)
    desenhar_ui()

    pygame.display.update()

pygame.quit()
