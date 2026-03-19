# Importações e configurações
import pygame
import time
from copy import deepcopy
from config import  COLUNAS, TAMANHO, PRETO,ALTURA, LARGURA,CINZA
from mapa import gerar_mapa, desenhar
from Drone import Drone
import matplotlib.pyplot as plt
from algoritmos import executar_algoritmo,custo , ida_star,astar,run_rbfs

# Inicialização do Pygame e variáveis globais

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Drone Agrícola - Comparação de Algoritmos")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 16)
energia_consumida = 0
status_mensagem = ""
start = (12, 1)  # canto da área azul
goal = (12, 1)  # último bloco inferior da área amarela
performance = []
# GERAR MAPA

gridori = gerar_mapa(start=start, goal=goal)
grid = deepcopy(gridori)


# GRÁFICOS
def mostrar_graficos(performance):

    if not performance:
        return

    nomes = [r["algoritmo"] for r in performance]
    tempos = [r["tempo"] for r in performance]
    mems = [r["memoria"] for r in performance]
    energia = [r["energia"] for r in performance]

    plt.figure(figsize=(10, 5))

    plt.subplot(131)
    plt.bar(nomes, tempos)
    plt.title("Tempo")

    plt.subplot(132)
    plt.bar(nomes, mems)
    plt.title("Memória KB")

    plt.subplot(133)
    plt.bar(nomes, energia)
    plt.title("Energia")

    plt.show()

# def desenhar_bateria(x, y,bateria,e_max):


#     largura = 70
#     altura = 28

#     porcentagem = bateria / E_MAX

#     # cor da bateria
#     if porcentagem > 0.6:
#         cor = (0, 200, 0)
#     elif porcentagem > 0.3:
#         cor = (255, 200, 0)
#     else:
#         cor = (200, 0, 0)

#     # corpo da bateria
#     pygame.draw.rect(tela, PRETO, (x, y, largura, altura), 2)

#     # nível da bateria
#     nivel = int((largura - 4) * porcentagem)

#     pygame.draw.rect(tela, cor, (x + 2, y + 2, nivel, altura - 4))

#     # terminal da bateria
#     pygame.draw.rect(tela, PRETO, (x + largura, y + altura // 3, 6, altura // 3))

def desenhar_ui(status_mensagem,drone:Drone = None):

    x_offset = COLUNAS * TAMANHO + 20
    y = 20

    textos = [
        "CONTROLES",
        "",
        "1 - Executar A*",
        "2 - Executar IDA*",
        "3 - Executar RBFS",
        "",
        "R - Novo mapa",
        "G - Mostrar graficos",
        "",
        "ESC - Sair",
    ]

    for t in textos:

        img = fonte.render(t, True, PRETO)
        tela.blit(img, (x_offset, y))

        y += 25

    # -------------------------
    # STATUS
    # -------------------------

    y += 20

    titulo = fonte.render("STATUS:", True, PRETO)
    tela.blit(titulo, (x_offset, y))

    y += 25

    # cor dinâmica do status
    if "acabou" in status_mensagem or "Nenhum" in status_mensagem:
        cor = (200, 0, 0)
    elif "Executando" in status_mensagem:
        cor = (0, 0, 200)
    else:
        cor = (0, 120, 0)

    img = fonte.render(status_mensagem, True, cor)
    tela.blit(img, (x_offset, y))

    # -------------------------
    # BATERIA VISUAL
    # -------------------------
    if drone : 
        y += 40

        img = fonte.render("BATERIA", True, PRETO)
        tela.blit(img, (x_offset, y))

        y += 30

        drone.desenhar_bateria(x_offset, y,tela)

        y += 40

        texto = f"{int(drone.bateria)} / {drone.e_max}"
        img = fonte.render(texto, True, PRETO)
        tela.blit(img, (x_offset, y))

        y += 25

        # energia consumida
        texto_uso = f"Energia usada: {int(energia_consumida)}"
        img = fonte.render(texto_uso, True, PRETO)
        tela.blit(img, (x_offset, y))

# ANIMAÇÃO
def animar(path,grid,func=None):

    drone1 = Drone(CINZA,PRETO)
    if not path:
        status_mensagem = "Nenhum caminho encontrado"
        return
    energia_consumida = 0
    status_mensagem = "Drone executando..."
    desenhar_ui(status_mensagem,drone1)
    u = None
    for p in path:
        
        if u :
            # marcar caminho percorrido
            match grid[u[0]][u[1]] :
                case 2:
                    grid[u[0]][u[1]] = 4
                case 3:                   
                    grid[u[0]][u[1]] = 5
                case _:
                    grid[u[0]][u[1]] = 9
        x, y = p
        gasto = custo(grid[x][y],drone1.custo_de_deslocamento)

        # verificar bateria
        if drone1.bateria - gasto < 4:
            path2 = func(start, p,grid)  
            status_mensagem = "Bateria acabou!\r O Drone esta fazendo um pouso forçado \r chamando o drone de emergencia para resgate"
            desenhar_ui(status_mensagem,drone1)
            drone2 = Drone([0,0,255],[255,0,0])
            time.sleep(2)
            for p2 in path2:
                status_mensagem = "O drone de emergencia esta indo busca o drone sem bateria "
                desenhar(tela, grid,start, goal,cdrone=p, cdrone2=p2,drone=drone1,drone2=drone2)
                desenhar_ui(status_mensagem,drone1)
                pygame.display.update()
                pygame.time.delay(20)
                
            path3 = func(p, goal,grid)
            status_mensagem = "O drone de emergencia encontrou o drone sem bateria "
            desenhar_ui(status_mensagem,drone1)
            time.sleep(2)
            for p2 in path3:
                status_mensagem = "O drone de emergencia esta levando o drone sem bateria para a base "
                desenhar_ui(status_mensagem,drone1)
                desenhar(tela, grid,start, goal,cdrone=p2, cdrone2=p2,drone=drone1,drone2=drone2)
                pygame.display.update()
                pygame.time.delay(20)
            status_mensagem = "O drone principal esta na base recarregando e sofrendo atualizações"
        
            desenhar_ui(status_mensagem,drone1)
            return grid
        else:
            drone1.bateria -= gasto
            energia_consumida += gasto

            desenhar(tela, grid,start, goal,cdrone=p,drone=drone1,)
            desenhar_ui(status_mensagem,drone1)

            pygame.display.update()
            pygame.time.delay(60)
            u = p
            
    if drone1.bateria > 0:
        status_mensagem = "Missao concluida"
        desenhar(tela,grid,start,goal,drone=drone1)
        return grid

# LOOP
def escolher(start, goal,mensagem,algo,func,gridori,performance):
    grid = deepcopy(gridori)
    status_mensagem = mensagem
    path,performance = executar_algoritmo(start, goal,algo, func,grid,performance)

    grid = animar(path,grid,func)

    return grid , performance

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            match event.key:

                case pygame.K_r:
                    gridori = gerar_mapa(start=start, goal=goal)
                    status_mensagem = "Novo mapa gerado"
                    grid = deepcopy(gridori)
                    performance = []

                case pygame.K_1:
                    grid ,performance= escolher(start,goal,"Executando A*", "A*", astar,gridori,performance)


                case pygame.K_2:
                    grid,performance= escolher(start,goal,"Executando IDA*", "IDA*", ida_star,gridori,performance)


                case pygame.K_3:
                    grid,performance=escolher(start,goal,"Executando RBFS", "RBFS", run_rbfs,gridori,performance)

                case pygame.K_g:
                    status_mensagem = "Mostrando gráficos"
                    mostrar_graficos(performance)

                case pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    exit()

    # desenhar tela
    desenhar(tela, grid,start, goal)
    desenhar_ui(status_mensagem)

    pygame.display.update()

pygame.quit()
