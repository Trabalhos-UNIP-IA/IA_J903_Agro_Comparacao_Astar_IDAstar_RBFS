import pygame

pygame.init()

# =============================
# CONFIGURAÇÃO
# =============================

pygame.init()

TAMANHO = 24
LINHAS = 30
COLUNAS = 30

LARGURA = COLUNAS * TAMANHO + 300
ALTURA = LINHAS * TAMANHO

E_MAX = 100  # energia máxima do drone
CUSTO_MOVIMENTO = 0.8  # custo de energia para cada movimento



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
