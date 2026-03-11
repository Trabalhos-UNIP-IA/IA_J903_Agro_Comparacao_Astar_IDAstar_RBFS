import pygame

from config import COLUNAS, TAMANHO, fonte, tela, PRETO, E_MAX, VERDE


def desenhar_ui(bateria, largura_barra):

    x_offset = COLUNAS * TAMANHO + 20

    energia_restante = bateria

    textos = [
        "CONTROLES",
        "1 - A*",
        "2 - IDA*",
        "3 - RBFS",
        "R - Novo mapa",
        "T - Mostrar tabela",
    ]

    y = 20

    for t in textos:

        img = fonte.render(t, True, PRETO)
        tela.blit(img, (x_offset, y))
        y += 25

    y += 20

    bateria_texto = f"Bateria restante: {energia_restante}"
    img = fonte.render(bateria_texto, True, PRETO)
    tela.blit(img, (x_offset, y))

    # barra da bateria

    pygame.draw.rect(tela, PRETO, (x_offset, y + 30, largura_barra, 20), 2)

    energia_visual = int((bateria / E_MAX) * largura_barra)

    pygame.draw.rect(tela, VERDE, (x_offset, y + 30, energia_visual, 20))
