import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

imagens_cartas = {
    'vermelho': pygame.image.load(os.path.join(BASE_DIR, 'assets', 'Images', 'CartasTrens', 'vermelho.png')),
    'azul': pygame.image.load(os.path.join(BASE_DIR, 'assets', 'Images', 'CartasTrens', 'azul.png')),
    'verde': pygame.image.load(os.path.join(BASE_DIR, 'assets', 'Images', 'CartasTrens', 'verde.png')),
    'amarelo': pygame.image.load(os.path.join(BASE_DIR, 'assets', 'Images', 'CartasTrens', 'amarelo.png')),
    'preto': pygame.image.load(os.path.join(BASE_DIR, 'assets', 'Images', 'CartasTrens', 'preto.png')),
    'branco': pygame.image.load(os.path.join(BASE_DIR, 'assets', 'Images', 'CartasTrens', 'branco.png')),
    'laranja': pygame.image.load(os.path.join(BASE_DIR, 'assets', 'Images', 'CartasTrens', 'laranja.png')),
    'roxo': pygame.image.load(os.path.join(BASE_DIR, 'assets', 'Images', 'CartasTrens', 'roxo.png')),
    'coringa': pygame.image.load(os.path.join(BASE_DIR, 'assets', 'Images', 'CartasTrens', 'coringa.png')),
}


class CartaTrem():

    def __init__(self, cor):
        self.cor = cor
        self.imagem = imagens_cartas[cor]
        self.rect = self.imagem.get_rect()
        self.selecionada = False 

    @staticmethod
    def criar_baralho_trem():
        cores = ['vermelho', 'azul', 'verde', 'amarelo', 'preto', 'branco', 'laranja', 'roxo', 'coringa']
        baralho = []
        for cor in cores:
            for _ in range(12 if cor != 'coringa' else 14):
                baralho.append(CartaTrem(cor))
        return baralho
    
def desenhar_mao_jogador(tela, mao_jogador):
    largura_tela = tela.get_width()
    y = tela.get_height() - 75

    contagem_cores = {}
    primeira_carta_por_cor = {}
    for carta in mao_jogador:
        contagem_cores[carta.cor] = contagem_cores.get(carta.cor, 0) + 1
        if carta.cor not in primeira_carta_por_cor:
            primeira_carta_por_cor[carta.cor] = carta

    cores_unicas = list(contagem_cores.keys())

    carta_original = mao_jogador[0].imagem
    largura_original = carta_original.get_width()
    altura_original = carta_original.get_height()

    escala = 0.6
    largura_carta_red = int(largura_original * escala)
    altura_carta_red = int(altura_original * escala)

    espacamento = 10

    imagens_rot = []
    for cor in cores_unicas:
        imagem_red = pygame.transform.smoothscale(imagens_cartas[cor], (largura_carta_red, altura_carta_red))
        imagem_rot = pygame.transform.rotate(imagem_red, -90)
        imagens_rot.append(imagem_rot)

    total_largura = sum(imagem.get_width() for imagem in imagens_rot) + espacamento * (len(cores_unicas) - 1)
    x_inicial = (largura_tela - total_largura) // 2

    x = x_inicial
    fonte = pygame.font.SysFont(None, 24)

    for i, cor in enumerate(cores_unicas):
        imagem_rot = imagens_rot[i]
        tela.blit(imagem_rot, (x, y))
        rect = imagem_rot.get_rect()
        rect.topleft = (x, y)

        primeira_carta_por_cor[cor].rect = rect

        if any(carta.selecionada for carta in mao_jogador if carta.cor == cor):
            pygame.draw.rect(tela, (255, 255, 0), rect, 3)

        qtd = contagem_cores[cor]
        if qtd > 1:
            texto = fonte.render(str(qtd), True, (255, 255, 0))
            texto_rect = texto.get_rect()
            texto_rect.midtop = (rect.left + rect.width // 2, rect.top + 5)
            tela.blit(texto, texto_rect)

        x += imagem_rot.get_width() + espacamento

def desenhar_cartas_laterais(tela, cartas_laterais):
    x_inicial = tela.get_width() - 130  # Posição fixa na lateral direita
    y_inicial = 90
    espacamento = 5
    escala = 0.5

    largura_original = cartas_laterais[0].imagem.get_width()
    altura_original = cartas_laterais[0].imagem.get_height()
    largura_red = int(largura_original * escala)
    altura_red = int(altura_original * escala)

    for i, carta in enumerate(cartas_laterais):
        imagem_red = pygame.transform.smoothscale(carta.imagem, (largura_red, altura_red))
        x = x_inicial
        y = y_inicial + i * (altura_red + espacamento)

        tela.blit(imagem_red, (x, y))
        carta.rect = pygame.Rect(x, y, largura_red, altura_red)  # Atualiza o retângulo para clique
