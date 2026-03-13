import random

import pygame
from config import LINHAS, COLUNAS, TAMANHO, BRANCO, PRETO, AZUL, AMARELO, VERDE, VERMELHO, CINZA


# =============================
# POSIÇÕES
# =============================


start = (1, 1)  # canto da área azul
goal = (10, 18)
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
    cx, cy = 5, 18
    r = 5

    for i in range(LINHAS):
        for j in range(COLUNAS):
            if (i - cx) ** 2 + (j - cy) ** 2 <= r**2:
                grid[i][j] = 3

    # obstáculos
    for i in range(LINHAS):
        for j in range(COLUNAS):

            if (grid[i][j] == 2 or grid[i][j] == 3) and random.random() < 0.15:
                grid[i][j] = 1
    #    detalhes do mapa
    for i in range(LINHAS):
        for j in range(COLUNAS):

            if grid[i][j] == 0 and random.random() < 0.18:
                grid[i][j] = 6

    for i in range(LINHAS):
        for j in range(COLUNAS):

            if grid[i][j] == 0 and random.random() < 0.18:
                grid[i][j] = 7
    # garantir start e goal livres
    grid[start[0]][start[1]] = 0
    grid[goal[0]][goal[1]] = 0

    return grid


def desenhar(tela,grid, drone=None):

    tela.fill(BRANCO)

    for i in range(LINHAS):
        for j in range(COLUNAS):

            rect = pygame.Rect(j * TAMANHO, i * TAMANHO, TAMANHO, TAMANHO)
            match grid[i][j]:
                case 0:
                     pygame.draw.rect(tela, [93,101,50], rect)
                case 1:
                    pygame.draw.rect(tela, [139,69,19], rect)
                case 2:
                    pygame.draw.rect(tela, AZUL, rect)
                case 3:
                    pygame.draw.rect(tela, AMARELO, rect)
                case 6:
                    pygame.draw.rect(tela, [0,100,0], rect)
                case 7:
                     pygame.draw.rect(tela, [120,250,120], rect)

    

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
