import random
from config import LINHAS, COLUNAS


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
    for i in range(LINHAS):
        for j in range(COLUNAS):

            if grid[i][j] == 0 and random.random() < 0.18:
                grid[i][j] = 1

    # garantir start e goal livres
    grid[start[0]][start[1]] = 0
    grid[goal[0]][goal[1]] = 0

    return grid


grid = gerar_mapa()
