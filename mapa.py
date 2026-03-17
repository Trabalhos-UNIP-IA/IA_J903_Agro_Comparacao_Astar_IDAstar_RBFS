import random

import pygame
from config import LINHAS, COLUNAS, TAMANHO, BRANCO, PRETO, AZUL, AMARELO, VERDE, VERMELHO, CINZA

# GERAR MAPA
# =============================


def gerar_mapa(start:list , goal:list):

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


def desenhar(tela,grid,start:list , goal:list, drone=None):

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
                case 4:
                    pygame.draw.rect(tela, [0,191,255], rect)
                case 5:
                    pygame.draw.rect(tela, [255,255,50], rect)
                case 6:
                    pygame.draw.rect(tela, [0,100,0], rect)
                case 7:
                     pygame.draw.rect(tela, [120,250,120], rect)
                case 9:
                    pygame.draw.rect(tela, [255,165,0], rect)
    

    # start
    pygame.draw.circle(
        tela,
        (0, 255, 0),
        (start[1] * TAMANHO + TAMANHO // 2, start[0] * TAMANHO + TAMANHO // 2),
        TAMANHO //2,
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
        # pygame.draw.rect(
        #     tela,
        #     CINZA,
        #     ( y * TAMANHO  , x * TAMANHO 
        #      , TAMANHO*.7, TAMANHO*.5),
        #     )
                # Definindo o retângulo do corpo (centralizado no drone)
        largura_corpo = TAMANHO // 2
        altura_corpo = TAMANHO // 3

        # Desenha o retângulo preenchido (width=0) e com cantos levemente arredondados
        # 1. Definimos o centro da célula (onde o drone está)
        centro_x = y * TAMANHO + TAMANHO // 2
        centro_y = x * TAMANHO + TAMANHO // 2

        pygame.draw.rect(
            tela, 
            CINZA, 
            (centro_x - largura_corpo // 2, centro_y - altura_corpo // 2, largura_corpo, altura_corpo),
            width=0,
            border_radius=5
        )
        pygame.draw.rect(
            tela, 
            [255,255,0], 
            (centro_x - largura_corpo // 2, centro_y - altura_corpo // 2, largura_corpo*.7, altura_corpo*.7),
            width=2,
            border_radius=5
        )
        # 2. Definimos a distância do centro até as hélices (ajuste o 4 conforme desejar)
        deslocamento = TAMANHO // 4 

        # 3. Lista de direções: (horizontal, vertical)
        # (-1, -1) = Superior Esquerdo | (1, -1) = Superior Direito
        # (-1, 1)  = Inferior Esquerdo | (1, 1)  = Inferior Direito
        
        posicoes = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

        for dx, dy in posicoes:
            # Calcula a posição de cada hélice
            pos_helice = (centro_x + dx * deslocamento, centro_y + dy * deslocamento)
            
            # Desenha o círculo Amarelo (Externo)
            pygame.draw.circle(tela, CINZA, pos_helice, TAMANHO // 6,width=3)
            
            # Desenha o círculo Preto (Interno)
            pygame.draw.circle(tela, PRETO, pos_helice, TAMANHO // 8 ,width=2)
   