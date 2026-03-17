
# Importações e configurações

import pygame
import heapq
import time
import tracemalloc
from copy import deepcopy
from config import LINHAS, COLUNAS, TAMANHO, PRETO,ALTURA, LARGURA,CUSTO_MOVIMENTO ,E_MAX,DIRECOES
from mapa import gerar_mapa, desenhar
import matplotlib.pyplot as plt

# Inicialização do Pygame e variáveis globais

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Drone Agrícola - Comparação de Algoritmos")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 16)
bateria = E_MAX
energia_consumida = 0
status_mensagem = ""
start = (12, 1)  # canto da área azul
goal = (12, 1)  # último bloco inferior da área amarela

# GERAR MAPA

gridori = gerar_mapa(start=start, goal=goal)
grid = deepcopy(gridori)

# HEURÍSTICA
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# VIZINHOS
def neighbors(n):

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

# CUSTO
def custo(x, y):

    if grid[x][y] == 2:
        return CUSTO_MOVIMENTO * 0.5
    elif grid[x][y] == 3:
        return CUSTO_MOVIMENTO * 1.5
    else:
        return CUSTO_MOVIMENTO

# A*
def astar(start, goal):

    open_list = []
    heapq.heappush(open_list, (0, start))

    came = {}
    g = {start: 0}

    while open_list:

        _, current = heapq.heappop(open_list)

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

            if tentative > E_MAX:
                continue

            if n not in g or tentative < g[n]:

                g[n] = tentative
                f = tentative + heuristic(n, goal)

                heapq.heappush(open_list, (f, n))
                came[n] = current

    return None

# IDA*
def ida_star(start, goal):

    bound = heuristic(start, goal)
    path = [start]

    def search(path, g, bound):

        node = path[-1]

        f = g + heuristic(node, goal)

        if f > bound:
            return f

        if node == goal:
            return path.copy()

        minimum = float("inf")

        for n in neighbors(node):

            if n in path:
                continue

            cost = custo(n[0], n[1])

            path.append(n)

            t = search(path, g + cost, bound)

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

# RBFS
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

        result, new_f = rbfs(best, goal, g + best_cost, min(bound, alt), path + [best])

        successors[0] = (best, new_f, best_cost)

        if result:
            return result, new_f

def run_rbfs(start, goal):

    path, _ = rbfs(start, goal, 0, float("inf"), [start])
    return path

# VARREDURA INTELIGENTE
def cobrir_regiao(start_pos, area, algoritmo):

    caminho_total = []
    atual = start_pos

    area_restante = set(area)

    while area_restante:

        # escolher ponto mais próximo
        alvo = min(area_restante, key=lambda c: heuristic(atual, c))

        caminho = algoritmo(atual, alvo)

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

# PERFORMANCE

performance = []
def executar_algoritmo(nome, func,grid):

    tracemalloc.start()
    t0 = time.perf_counter()

    area_ret = pegar_regiao(2,grid)
    area_circ = pegar_regiao(3,grid)

    # ir até a primeira área
    entrada = min(area_ret, key=lambda c: heuristic(start, c))
    path1 = func(start, entrada)

    # cobrir área retangular
    path2 = cobrir_regiao(entrada, area_ret, func)

    ultimo = path2[-1] if path2 else entrada

    # ir para área circular
    entrada2 = min(area_circ, key=lambda c: heuristic(ultimo, c))
    path3 = func(ultimo, entrada2)

    # cobrir área circular
    path4 = cobrir_regiao(entrada2, area_circ, func)
    #
    entrada3 = path4[-1] if path4 else entrada2
    path5 = func(entrada3,goal)
    path = path1 + path2 + path3 + path4 + path5
    tempo = time.perf_counter() - t0

    current, peak = tracemalloc.get_traced_memory()
    mem = peak / 1024
    tracemalloc.stop()

    energia = sum(custo(x, y) for x, y in path)

    performance.append(
        {"algoritmo": nome, "tempo": tempo, "memoria": mem, "energia": energia}
    )

    return path

# COMPARAR ALGORITMOS
def comparar_algoritmos():

    global performance

    performance.clear()

    algoritmos = [("A*", astar), ("IDA*", ida_star), ("RBFS", run_rbfs)]

    for nome, func in algoritmos:

        print("Executando:", nome)

        path = executar_algoritmo(nome, func,gridori)

        if path:
            animar(path,gridori)
        else:
            print("Nenhum caminho encontrado para", nome)

    mostrar_graficos()

# GRÁFICOS
def mostrar_graficos():

    if not performance:
        return

    nomes = [r["algoritmo"] for r in performance]
    tempos = [r["tempo"] for r in performance]
    mems = [r["memoria"] for r in performance]
    energia = [r["energia"] for r in performance]

    plt.figure(figsize=(10, 5))

    plt.subplot(131)
    plt.bar(nomes, tempos)
    plt.title("Tempo")

    plt.subplot(132)
    plt.bar(nomes, mems)
    plt.title("Memória KB")

    plt.subplot(133)
    plt.bar(nomes, energia)
    plt.title("Energia")

    plt.show()

def desenhar_bateria(x, y):

    global bateria

    largura = 70
    altura = 28

    porcentagem = bateria / E_MAX

    # cor da bateria
    if porcentagem > 0.6:
        cor = (0, 200, 0)
    elif porcentagem > 0.3:
        cor = (255, 200, 0)
    else:
        cor = (200, 0, 0)

    # corpo da bateria
    pygame.draw.rect(tela, PRETO, (x, y, largura, altura), 2)

    # nível da bateria
    nivel = int((largura - 4) * porcentagem)

    pygame.draw.rect(tela, cor, (x + 2, y + 2, nivel, altura - 4))

    # terminal da bateria
    pygame.draw.rect(tela, PRETO, (x + largura, y + altura // 3, 6, altura // 3))

def desenhar_ui():

    global status_mensagem

    x_offset = COLUNAS * TAMANHO + 20
    y = 20

    textos = [
        "CONTROLES",
        "",
        "1 - Executar A*",
        "2 - Executar IDA*",
        "3 - Executar RBFS",
        "",
        "R - Novo mapa",
        "G - Mostrar graficos",
        "",
        "ESC - Sair",
    ]

    for t in textos:

        img = fonte.render(t, True, PRETO)
        tela.blit(img, (x_offset, y))

        y += 25

    # -------------------------
    # STATUS
    # -------------------------

    y += 20

    titulo = fonte.render("STATUS:", True, PRETO)
    tela.blit(titulo, (x_offset, y))

    y += 25

    # cor dinâmica do status
    if "acabou" in status_mensagem or "Nenhum" in status_mensagem:
        cor = (200, 0, 0)
    elif "Executando" in status_mensagem:
        cor = (0, 0, 200)
    else:
        cor = (0, 120, 0)

    img = fonte.render(status_mensagem, True, cor)
    tela.blit(img, (x_offset, y))

    # -------------------------
    # BATERIA VISUAL
    # -------------------------

    y += 40

    img = fonte.render("BATERIA", True, PRETO)
    tela.blit(img, (x_offset, y))

    y += 30

    desenhar_bateria(x_offset, y)

    y += 40

    texto = f"{int(bateria)} / {E_MAX}"
    img = fonte.render(texto, True, PRETO)
    tela.blit(img, (x_offset, y))

    y += 25

    # energia consumida
    texto_uso = f"Energia usada: {int(energia_consumida)}"
    img = fonte.render(texto_uso, True, PRETO)
    tela.blit(img, (x_offset, y))

# ANIMAÇÃO
def animar(path,grid):

    global bateria, energia_consumida, status_mensagem

    if not path:
        status_mensagem = "Nenhum caminho encontrado"
        return

    bateria = E_MAX
    energia_consumida = 0
    status_mensagem = "Drone executando..."
    u = None
    for p in path:
        
        if u :
            # marcar caminho percorrido
            match grid[u[0]][u[1]] :
                case 2:
                    grid[u[0]][u[1]] = 4
                case 3:                   
                    grid[u[0]][u[1]] = 5
                case _:
                    grid[u[0]][u[1]] = 9
        x, y = p
        gasto = custo(x, y)

        # verificar bateria
        if bateria - gasto < 0:
            status_mensagem = "Bateria acabou!"
            break

        bateria -= gasto
        energia_consumida += gasto

        desenhar(tela, grid,start, goal, p)
        desenhar_ui()

        pygame.display.update()
        pygame.time.delay(60)
        u = p
        if bateria <= 0:
            status_mensagem = "Bateria acabou!"
            break
    if bateria > 0:
        status_mensagem = "Missao concluida"
        return grid

# LOOP
def escolher(mensagem,algo,func,gridori):
    global status_mensagem
    grid = deepcopy(gridori)
    status_mensagem = mensagem
    path = executar_algoritmo(algo, func,grid=grid)
    grid = animar(path,grid)

    return grid

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            match event.key:

                case pygame.K_r:
                    gridori = gerar_mapa(start=start, goal=goal)
                    status_mensagem = "Novo mapa gerado"
                    grid = deepcopy(gridori)
                case pygame.K_1:
                    grid= escolher("Executando A*", "A*", astar,gridori)


                case pygame.K_2:
                    grid= escolher("Executando IDA*", "IDA*", ida_star,gridori)


                case pygame.K_3:
                    grid=escolher("Executando RBFS", "RBFS", run_rbfs,gridori)

                case pygame.K_g:
                    status_mensagem = "Mostrando gráficos"
                    mostrar_graficos()

                case pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    exit()

    # desenhar tela
    desenhar(tela, grid,start, goal)
    desenhar_ui()

    pygame.display.update()

pygame.quit()
