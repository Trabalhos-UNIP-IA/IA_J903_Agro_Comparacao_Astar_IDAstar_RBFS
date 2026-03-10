import pygame
from config import (
    tela,
    BRANCO,
    LINHAS,
    COLUNAS,
    TAMANHO,
    PRETO,
    AZUL,
    AMARELO,
    VERDE,
    VERMELHO,
    CINZA,
)

from mapa import grid, start, goal
from algoritmos import custo
from ui import desenhar_ui


# =============================
# DESENHO
# =============================


def desenhar(path=None, drone=None):

    tela.fill(BRANCO)

    for i in range(LINHAS):
        for j in range(COLUNAS):

            rect = pygame.Rect(j * TAMANHO, i * TAMANHO, TAMANHO, TAMANHO)

            if grid[i][j] == 1:
                pygame.draw.rect(tela, PRETO, rect)

            elif grid[i][j] == 2:
                pygame.draw.rect(tela, AZUL, rect)

            elif grid[i][j] == 3:
                pygame.draw.rect(tela, AMARELO, rect)

            pygame.draw.rect(tela, CINZA, rect, 1)

    # caminho
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

    # drone
    if drone:
        x, y = drone

        pygame.draw.circle(
            tela,
            VERMELHO,
            (y * TAMANHO + TAMANHO // 2, x * TAMANHO + TAMANHO // 2),
            TAMANHO // 3,
        )


# =============================
# ANIMAÇÃO
# =============================


def animar(path, bateria):

    if not path:
        print("Nenhum caminho encontrado")
        return bateria

    for p in path:

        x, y = p
        gasto = custo(grid, x, y)

        if bateria - gasto < 0:
            print("Bateria insuficiente para continuar!")
            break

        bateria -= gasto

        desenhar(path, p)
        desenhar_ui(bateria)

        pygame.display.update()
        pygame.time.delay(70)

    return bateria
