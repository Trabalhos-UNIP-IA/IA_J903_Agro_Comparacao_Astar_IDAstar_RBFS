import pygame

from mapa import gerar_mapa, start, goal
from ui import desenhar_ui
from algoritmos import astar, ida_star, run_rbfs
from config import clock
from vizualizacao import desenhar, animar
from performace import executar_algoritmo, mostrar_tabela


# =============================
# INICIALIZAÇÃO
# =============================

pygame.init()

grid = gerar_mapa()
path = None

running = True
E_MAX = 100  # energia máxima do drone
CUSTO_MOVIMENTO = 1  # custo de energia para cada movimento
bateria = E_MAX
largura_barra = 120


# =============================
# LOOP PRINCIPAL
# =============================

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # gerar novo mapa
            if event.key == pygame.K_r:
                grid = gerar_mapa()
                path = None

            # A*
            if event.key == pygame.K_1:
                bateria = E_MAX
                path, tempo, mem = executar_algoritmo("A*", astar, grid, start, goal)

                if path:
                    animar(path)

            # IDA*
            if event.key == pygame.K_2:
                bateria = E_MAX
                path, tempo, mem = executar_algoritmo(
                    "IDA*", ida_star, grid, start, goal
                )

                if path:
                    animar(path)

            # RBFS
            if event.key == pygame.K_3:
                bateria = E_MAX
                path, tempo, mem = executar_algoritmo(
                    "RBFS", run_rbfs, grid, start, goal
                )

                if path:
                    animar(path)

            # mostrar tabela de performance
            if event.key == pygame.K_t:
                mostrar_tabela()

            # sair
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                exit()

    # =============================
    # DESENHO NA TELA
    # =============================

    desenhar(path)
    desenhar_ui(bateria, largura_barra)

    pygame.display.update()


pygame.quit()
