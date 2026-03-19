import pygame
from config import PRETO
class Drone():
    def __init__(self,cor_primaria,cor_segundaria,custo_de_deslocamento=0.8,bateria=250):

        self.cor_primaria =cor_primaria
        self.cor_segundaria = cor_segundaria
        self.bateria = bateria
        self.custo_de_deslocamento = custo_de_deslocamento
        self.e_max = bateria
    
    def desenhar_drone(self,cortendas:list,tela, tamanho,):
        x, y = cortendas
        largura_corpo = tamanho // 2
        altura_corpo = tamanho // 3

        # Desenha o retângulo preenchido (width=0) e com cantos levemente arredondados
        # 1. Definimos o centro da célula (onde o drone está)
        centro_x = y * tamanho + tamanho // 2
        centro_y = x * tamanho + tamanho // 2

        pygame.draw.rect(
            tela, 
            self.cor_primaria, 
            (centro_x - largura_corpo // 2, centro_y - altura_corpo // 2, largura_corpo, altura_corpo),
            width=0,
            border_radius=5
        )
        pygame.draw.rect(
            tela, 
            self.cor_segundaria, 
            (centro_x - largura_corpo // 2, centro_y - altura_corpo // 2, largura_corpo*.7, altura_corpo*.7),
            width=2,
            border_radius=5
        )
        # 2. Definimos a distância do centro até as hélices (ajuste o 4 conforme desejar)
        deslocamento = tamanho // 4 
        
        posicoes = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

        for dx, dy in posicoes:
            # Calcula a posição de cada hélice
            pos_helice = (centro_x + dx * deslocamento, centro_y + dy * deslocamento)
            
            # Desenha o círculo Amarelo (Externo)
            pygame.draw.circle(tela, self.cor_primaria, pos_helice, tamanho // 6,width=3)
            
            # Desenha o círculo Preto (Interno)
            pygame.draw.circle(tela, self.cor_segundaria, pos_helice, tamanho // 8 ,width=2)
    def desenhar_bateria(self,x, y,tela):
        largura = 70
        altura = 28

        porcentagem = self.bateria /self.e_max

        # cor da bateria
        if porcentagem > 0.6:
            cor = (0, 200, 0)
        elif porcentagem > 0.3:
            cor = (255, 200, 0)
        else:
            cor = (200, 0, 0)

        # corpo da bateria
        rect = [x, y, largura, altura]
        pygame.draw.rect(tela, PRETO,rect , 2)

        # nível da bateria
        nivel = int((largura - 4) * porcentagem)

        pygame.draw.rect(tela, cor, (x + 2, y + 2, nivel, altura - 4))

        # terminal da bateria
        pygame.draw.rect(tela, PRETO, (x + largura, y + altura // 3, 6, altura // 3))
