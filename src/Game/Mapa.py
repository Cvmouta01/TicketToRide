import pygame
from Utils import *
import os
import random
from settings import cores

# Diretório base pra abrir as imagens com caminho relativo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Mapa():
    def __init__(self, surface):
        width, height = surface.get_width(), surface.get_height()
        # Carregando a img de fundo e dando resize
        self.map_img = pygame.image.load(BASE_DIR + "./assets/Images/Mapa/ticket_to_ride_map_sem_borda.png")
        self.map_img = resize_com_escala(self.map_img, width, height, 0.8, 0.8)

        # Carregando a img do avatar dos cards de jogadores e dando resize
        self.avatar = pygame.image.load(BASE_DIR + "./assets/Images/avatar_card.png")
        self.avatar = resize_com_escala(self.avatar, width, height, 0.04, 0.04)

        # Carregando a img do fundo das cartas de vagão e de destino
        self.fundo_vagao = pygame.image.load(BASE_DIR + "./assets/Images/Fundos/fundo_vagao.png")
        self.fundo_vagao = resize_com_escala(self.fundo_vagao, width, height, 0.12, 0.12)

        self.fundo_destino = pygame.image.load(BASE_DIR + "./assets/Images/Fundos/fundo_destino.png")
        self.fundo_destino = resize_com_escala(self.fundo_destino, width, height, 0.12, 0.12)
        self.fundo_destino = pygame.transform.rotate(self.fundo_destino, 90)

        # Carregando alguns trens, só para a demo (!!!) ****************************************
        self.trens = []
        for c in range(5):
            trem = pygame.image.load(BASE_DIR + "./assets/Images/CartasTrens/" + random.choice(os.listdir(BASE_DIR + "./assets/Images/CartasTrens")))
            trem = resize_com_escala(trem, width, height, 0.12, 0.12)
            self.trens.append(trem)

        # Mão do jogador, para a demo também (!!!)
        self.mão = []
        for c in range(5):
            trem = pygame.image.load(BASE_DIR + "./assets/Images/CartasTrens/" + random.choice(os.listdir(BASE_DIR + "./assets/Images/CartasTrens")))
            trem = pygame.transform.rotate(trem, 90)
            trem = resize_com_escala(trem, width, height, 0.12, 0.12)
            self.mão.append(trem)
        # *************************************************************************************


        self.grafo_cidades = None

    # Recebe uma superficie e a lista de jogadores
    # Desenha o mapa e os cards de jogadores com suas respectivas informações
    # Tem que desenhar os baralhos, cartas abertas, mão do jogador ativo e cartas de destino do jogador ativo
    def draw(self, surface, jogadores):
        # Preenchendo em um tom bege parecido com o do mapa, pode mudar depois (!!!)
        surface.fill((198, 197, 176))

        # O mapa se desenha no centro da tela colando na parte de cima
        surface.blit(self.map_img, (surface.get_width()//2 - self.map_img.get_width()//2, 0))


        # Desenhando os baralhos de vagão e destino
        # O destino vai no canto superior direito, metade pra fora da tela
        surface.blit(self.fundo_destino, (surface.get_width() - self.fundo_destino.get_width() - 10, 0 - self.fundo_destino.get_height()//2))
        # O vagão vai no canto inferior direito, 20% pra fora da tela
        surface.blit(self.fundo_vagao, (surface.get_width() - self.fundo_vagao.get_width()*0.8, surface.get_height() - self.fundo_vagao.get_height() - 10))


        # Desenhando os vagões abertos, só para a demo (!!!) **********************************
        trem_x, trem_y = surface.get_width() - self.fundo_vagao.get_width()*0.8, surface.get_height() - 2*self.fundo_vagao.get_height() - 20
        for trem in self.trens:
            surface.blit(trem, (trem_x, trem_y))

            trem_y -= trem.get_height() + 10
        # Desenhando a mão do jogador ativo, só pra demo (!!!)
        # A ideia é desenhar uma no centro e intercalar entre direita e esquerda
        mao_x = surface.get_width()//2 - self.mão[0].get_width() * len(self.mão)//2
        mao_y = surface.get_height() - self.mão[0].get_height()*0.3
        for trem in self.mão:
            surface.blit(trem, (mao_x, mao_y))

            mao_x += trem.get_width() + 10

        # ********************************************************************************


        # Desenhando os cards de jogadores
        cards_x, cards_y = -5, 100
        cards_w, cards_h = surface.get_width()/10, surface.get_height()/9 # Tamanho do card é equivalente a 1/10 do width e 1/9 do height da tela
        for jogador in jogadores:
            self.criar_card_jogador(surface, jogador, (cards_x, cards_y, cards_w, cards_h))

            cards_y += cards_h + 20

    # Retorna um card de jogador, contendo um fundo, um avatar na cor correta
    # Qtd de trens e pontos tem que vir da classe jogador!
    def criar_card_jogador(self, surface, jogador, rect):
        # Se for o turno do jogador, desenha uma borda branca no card
        if jogador.ativo:
            pygame.draw.rect(surface, 
                            (255, 255, 255),
                            (rect[0] - 10, rect[1] - 10, rect[2] + 20, rect[3] + 20))
        # Desenhando o fundo na cor certa
        pygame.draw.rect(surface, 
                         cores[jogador.cor],
                         rect, border_radius=5)
        
        # Desenhando o avatar

        surface.blit(self.avatar, (rect[0], rect[1])) # Desenhando na tela
        
        # Desenhando a qtd de pontos no canto superior direito do card
        pontos_txt = message_to_screen(surface, "P: "+ str(jogador.pontos), 20, rect[0], rect[1], (0, 0, 0), returning=True)
        p_x, p_y, p_w, p_h = pontos_txt["text_rect"]
        surface.blit(pontos_txt["text"], (p_x + rect[2] - p_w, p_y + p_h, p_w, p_h))

        # Desenhando a qtd de trens no canto inferior direito do card
        trens_txt = message_to_screen(surface, "T: " + str(jogador.trens), 20, rect[0], rect[1], (0, 0, 0), returning=True)
        t_x, t_y, t_w, t_h = trens_txt["text_rect"]
        surface.blit(trens_txt["text"], (t_x + rect[2] - t_w, t_y + rect[3] - t_h, t_w, t_h))