class DroneAgricola:
    def __init__(self, posInicial, posFinal, energiaMaxima):
        self.posicaoAtual = posInicial 
        self.posicaoFinal = posFinal
        self.energiaMax = energiaMaxima
        
    def obter_vizinhos(self, posicao, mapa): 
        """Olha para as 8 direções e retorna uma lista de coordenadas válidas"""
        x, y = posicao
        vizinhosValidos = []
        movimentos = [
            (-1, 0),  # Cima
            (1, 0),   # Baixo
            (0, -1),  # Esquerda
            (0, 1),   # Direita
            (-1, -1), # Diagonal Superior Esquerda
            (-1, 1),  # Diagonal Superior Direita
            (1, -1),  # Diagonal Inferior Esquerda
            (1, 1)    # Diagonal Inferior Direita
        ]

        for dx, dy in movimentos:
            nx = x + dx
            ny = y + dy
            
            # Verificar se está dentro do mapa
            if 0 <= nx < mapa.linhas and 0 <= ny < mapa.colunas:
                # Verificar que não é um bloqueio
                if mapa.grid[nx, ny] != -1:
                    vizinhosValidos.append((nx, ny))
            
        return vizinhosValidos