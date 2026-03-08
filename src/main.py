import pygame
import sys
from fazenda import FazendaGrid
from drone import DroneAgricola
from algoritmos import busca_a_estrela

# Constantes da janela
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60
TAMANHO_CELULA = 20

# Cores adicionais para a interface
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Simulação IA - A* Drone Agrícola")
    relogio = pygame.time.Clock()

    linhas_grid = ALTURA_TELA // TAMANHO_CELULA
    colunas_grid = LARGURA_TELA // TAMANHO_CELULA

    # 1. Monta o Mapa
    mapa = FazendaGrid(linhas_grid, colunas_grid, TAMANHO_CELULA)
    mapa.gerar_retangulo(5, 5, 15, 20)
    mapa.gerar_circulo(15, 25, 8)
    mapa.gerar_obstaculos(densidade_ret=0.15, densidade_circ=0.25)

    # 2. Define Partida e Chegada (Regra: Uma numa geometria, outra na outra)
    posicaoInicial = (10, 10)  # Dentro do Retângulo Azul
    posicaoFinal = (15, 25)    # No centro do Círculo Amarelo
    
    # Garante que os pontos de spawn não caiam em cima de um obstáculo por azar
    mapa.grid[posicaoInicial[0], posicaoInicial[1]] = 1
    mapa.grid[posicaoFinal[0], posicaoFinal[1]] = 2

    # 3. Instancia o Drone (Testando com uma bateria folgada primeiro)
    drone = DroneAgricola(posInicial=posicaoInicial, posFinal=posicaoFinal, energiaMaxima=150)

    # 4. Executa a IA (Isso roda num piscar de olhos antes da tela abrir)
    print("Calculando rota com A*...")
    caminho_encontrado = busca_a_estrela(mapa, drone)
    
    if caminho_encontrado:
        print(f"Rota encontrada! Custo de energia (passos): {len(caminho_encontrado) - 1}")
    else:
        print("Nenhuma rota encontrada! (Caminho bloqueado ou bateria insuficiente)")

    # 5. Loop de Renderização
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        tela.fill((255, 255, 255))
        
        # Desenha a fazenda
        mapa.desenhar(tela)

        # Desenha a rota se a IA tiver encontrado uma
        if caminho_encontrado:
            for i in range(len(caminho_encontrado) - 1):
                p1 = caminho_encontrado[i]
                p2 = caminho_encontrado[i+1]
                
                # Conversão de Coordenadas: 
                # Matriz (Linha, Coluna) para Pygame (X horizontal, Y vertical)
                x1 = p1[1] * TAMANHO_CELULA + TAMANHO_CELULA // 2
                y1 = p1[0] * TAMANHO_CELULA + TAMANHO_CELULA // 2
                x2 = p2[1] * TAMANHO_CELULA + TAMANHO_CELULA // 2
                y2 = p2[0] * TAMANHO_CELULA + TAMANHO_CELULA // 2
                
                pygame.draw.line(tela, VERMELHO, (x1, y1), (x2, y2), 4)

            # Destaca o Início (Verde) e o Fim (Vermelho) com círculos
            pygame.draw.circle(tela, VERDE, (posicaoInicial[1] * TAMANHO_CELULA + TAMANHO_CELULA // 2, posicaoInicial[0] * TAMANHO_CELULA + TAMANHO_CELULA // 2), 8)
            pygame.draw.circle(tela, VERMELHO, (posicaoFinal[1] * TAMANHO_CELULA + TAMANHO_CELULA // 2, posicaoFinal[0] * TAMANHO_CELULA + TAMANHO_CELULA // 2), 8)

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()