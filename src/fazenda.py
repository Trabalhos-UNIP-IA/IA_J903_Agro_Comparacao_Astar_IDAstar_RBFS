import numpy as np
import random
import pygame

# Constantes de Cores para o Pygame
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)      # Região retangular
AMARELO = (255, 255, 0) # Região circular
PRETO = (0, 0, 0)       # Obstáculos
CINZA = (200, 200, 200) # Linhas de grade do grid

class FazendaGrid:
    def __init__(self, linhas_grid, colunas_grid, tamanho_celula=20):
        # Configurações do Grid Lógico
        self.linhas = linhas_grid
        self.colunas = colunas_grid
        self.tamanho_celula = tamanho_celula # Tamanho de cada 'pixel' quadrado na tela
        
        # 0 = Terreno vazio | 1 = Azul | 2 = Amarelo | -1 = Obstáculo
        self.grid = np.zeros((linhas_grid, colunas_grid), dtype=int)
        self.mascara_retangulo = np.zeros((linhas_grid, colunas_grid), dtype=bool)
        self.mascara_circulo = np.zeros((linhas_grid, colunas_grid), dtype=bool)

    def gerar_retangulo(self, inicio_linha, inicio_coluna, n_rows, n_cols):
        """Define a área azul na matriz."""
        fim_linha = min(inicio_linha + n_rows, self.linhas)
        fim_coluna = min(inicio_coluna + n_cols, self.colunas)
        
        self.grid[inicio_linha:fim_linha, inicio_coluna:fim_coluna] = 1
        self.mascara_retangulo[inicio_linha:fim_linha, inicio_coluna:fim_coluna] = True

    def gerar_circulo(self, cx, cy, r):
        """Define a área amarela na matriz usando a equação matemática do círculo."""
        for x in range(self.linhas):
            for y in range(self.colunas):
                if (x - cx)**2 + (y - cy)**2 <= r**2:
                    # Só sobrescreve se não for retângulo (opcional, dependendo de como você quer a sobreposição)
                    self.grid[x, y] = 2
                    self.mascara_circulo[x, y] = True

    def gerar_obstaculos(self, densidade_ret=0.2, densidade_circ=0.3):
        """Gera obstáculos (-1) respeitando a densidade de cada geometria."""
        for x in range(self.linhas):
            for y in range(self.colunas):
                if self.mascara_retangulo[x, y] and not self.mascara_circulo[x, y]:
                    if random.random() < densidade_ret:
                        self.grid[x, y] = -1
                elif self.mascara_circulo[x, y]:
                    if random.random() < densidade_circ:
                        self.grid[x, y] = -1

    def desenhar(self, tela):
        """Renderiza a matriz lógica na tela do Pygame."""
        for x in range(self.linhas):
            for y in range(self.colunas):
                # Define a cor baseada no valor da matriz lógica
                cor = BRANCO
                if self.grid[x, y] == -1:
                    cor = PRETO
                elif self.grid[x, y] == 1:
                    cor = AZUL
                elif self.grid[x, y] == 2:
                    cor = AMARELO
                    
                # No Pygame, o eixo X é horizontal (colunas) e Y é vertical (linhas)
                rect = pygame.Rect(y * self.tamanho_celula, x * self.tamanho_celula, 
                                self.tamanho_celula, self.tamanho_celula)
                
                pygame.draw.rect(tela, cor, rect)
                pygame.draw.rect(tela, CINZA, rect, 1) # Desenha a bordinha da célula