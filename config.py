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
