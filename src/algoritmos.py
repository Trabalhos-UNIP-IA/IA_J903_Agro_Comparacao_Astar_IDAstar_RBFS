import heapq

def distancia_chebyshev(posAtual, posObjetivo):
    """Heurística h(n) para grids com 8 direções onde o custo do movimento diagonal é 1. Retorna o valor máximo entre a diferença no eixo X e no eixo Y."""

    dx = abs(posAtual[0] - posObjetivo[0])
    dy = abs(posAtual[1] - posObjetivo[1])
    return max(dx,dy)

def reconstruirCaminho (came_from,atual):
    """Faz o caminho inverso do objetivo até ao início para gerar a rota final."""
    
    caminho = [atual]
    while atual in came_from:
        atual = came_from[atual]
        caminho.append(atual)
    caminho.reverse()
    return caminho 

def busca_a_estrela(mapa,drone):
    """Implementação do Algoritmo A* respeitando a restrição de bateria E_max."""
    
    inicio = drone.posicaoAtual
    objetivo = drone.posicaoFinal
    e_max = drone.energiaMax
    
    open_set = []
    heapq.heappush(open_set,(0,0,inicio))
    
    came_from = {}
    
    g_score ={inicio:0}
    
    while open_set: 
        _, custoAtual_g, atual = heapq.heappop(open_set)
        
        if atual == objetivo:
            return reconstruirCaminho(came_from, atual)
        for vizinho in drone.obter_vizinhos(atual, mapa):
            
            tentativa_g_score = custoAtual_g + 1

            if tentativa_g_score > e_max:
                continue

            if vizinho not in g_score or tentativa_g_score < g_score[vizinho]:
                came_from[vizinho] = atual
                g_score[vizinho] = tentativa_g_score
                
                h_score = distancia_chebyshev(vizinho, objetivo)
                f_score = tentativa_g_score + h_score
                
                heapq.heappush(open_set, (f_score, tentativa_g_score, vizinho))

    return None