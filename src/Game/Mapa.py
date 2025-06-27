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
        self.original_width, self.original_height = self.map_img.get_width(), self.map_img.get_height() # Dimensões originais da img

        self.map_img = resize_com_escala(self.map_img, width, height, 0.8, 0.8)
        self.new_width, self.new_height = self.map_img.get_width(), self.map_img.get_height() # Novas dimensões da img

        # Carregando o fundo que fica atras de tudo
        self.background_img = pygame.image.load(BASE_DIR + "./assets/Images/Mapa/background.png")
        self.background_img = resize_com_escala(self.background_img, width, height, 1, 1)

        # Carregando a img do avatar dos cards de jogadores e dando resize
        self.avatar = pygame.image.load(BASE_DIR + "./assets/Images/avatar_card.png")
        self.avatar = resize_com_escala(self.avatar, width, height, 0.04, 0.04)

        self.pontos_img = pygame.image.load(BASE_DIR + "./assets/Images/pontos_img.png")
        self.pontos_img = resize_com_escala(self.pontos_img, width, height, 0.02, 0.02)

        self.qtd_trens_img = pygame.image.load(BASE_DIR + "./assets/Images/qtd_trens_img.png")
        self.qtd_trens_img = resize_com_escala(self.qtd_trens_img, width, height, 0.02, 0.02)

        # Carregando a img do fundo das cartas de vagão e de destino
        self.fundo_vagao = pygame.image.load(BASE_DIR + "./assets/Images/Fundos/fundo_vagao.png")
        self.fundo_vagao = resize_com_escala(self.fundo_vagao, width, height, 0.12, 0.12)

        self.fundo_destino = pygame.image.load(BASE_DIR + "./assets/Images/Fundos/fundo_destino.png")
        self.fundo_destino = resize_com_escala(self.fundo_destino, width, height, 0.12, 0.12)
        self.fundo_destino = pygame.transform.rotate(self.fundo_destino, 90)
        self.destino_rect = self.fundo_destino.get_rect()

        # Carregando as imagens dos trens, na horizontal e na vertical
        self.img_cartas_trem_horizontal = {}
        self.img_cartas_trem_vertical = {}
        for file in os.listdir(BASE_DIR + "./assets/Images/CartasTrens/"):
            trem = pygame.image.load(BASE_DIR + "./assets/Images/CartasTrens/" + file)

            trem_v = pygame.transform.rotate(trem, 90)
            trem_v = resize_com_escala(trem_v, width, height, 0.12, 0.12)

            trem_h = resize_com_escala(trem, width, height, 0.12, 0.12)

            card_name = file.split(".")[0]

            self.img_cartas_trem_vertical[card_name] = trem_v
            self.img_cartas_trem_horizontal[card_name] = trem_h
        
        # Adicionando botão save
        self.saveimg = pygame.image.load(BASE_DIR + "./assets/Images/save-64x64.png")

        self.grafo_cidades = None
        self.trilhos_conquistados = []

        self.barra_objetivos_ativa = False

    # Recebe uma superficie e a lista de jogadores
    # Desenha o mapa e os cards de jogadores com suas respectivas informações
    # Tem que desenhar os baralhos, cartas abertas, mão do jogador ativo e cartas de destino do jogador ativo
    def desenhar_mao_jogador(self, surface, mao_jogador, mouse_info):
        if not mao_jogador:
            return

        # Contar cartas por cor e guardar a primeira carta de cada cor
        contagem_cores = {}
        primeira_carta_por_cor = {}
        for carta in mao_jogador:
            cor = carta.cor
            contagem_cores[cor] = contagem_cores.get(cor, 0) + 1
            if cor not in primeira_carta_por_cor:
                primeira_carta_por_cor[cor] = carta

        cores_unicas = list(contagem_cores.keys())

        carta_base = self.img_cartas_trem_horizontal.get(cores_unicas[0])
        if not carta_base:
            return

        largura_original = carta_base.get_width()
        altura_original = carta_base.get_height()
        escala = 1
        largura_red = int(largura_original * escala)
        altura_red = int(altura_original * escala)

        espacamento = altura_red + 10  # cartas rotacionadas: altura será a nova largura
        largura_total = len(cores_unicas) * espacamento - 10
        x_inicial = (surface.get_width() - largura_total) // 2
        y_inicial = surface.get_height() - (largura_red / 2)

        fonte = pygame.font.SysFont(None, 24)

        for i, cor in enumerate(cores_unicas):
            imagem = self.img_cartas_trem_horizontal.get(cor)
            if not imagem:
                continue

            imagem_red = pygame.transform.smoothscale(imagem, (largura_red, altura_red))
            imagem_rot = pygame.transform.rotate(imagem_red, -90)

            x = x_inicial + i * espacamento
            y = y_inicial

            rect = pygame.Rect(x, y, altura_red, largura_red)  # largura e altura invertidos
            primeira_carta = primeira_carta_por_cor[cor]
            primeira_carta.rect = rect

            # Checar se alguma carta dessa cor foi clicada
            if dentro_poligono(mouse_info[0], [rect.topleft,
                                   (rect.right, rect.top),
                                   (rect.left, rect.bottom),
                                   (rect.right, rect.bottom)]):
                
                # Hover
                y -= 10
                rect[1], rect[3] = rect[1] - 10, rect[3] - 10
                 
                if mouse_info[1]:
                    nova_selecao = not primeira_carta_por_cor[cor].selecionada

                    for carta in mao_jogador:
                        if carta.cor == cor:
                            carta.selecionada = nova_selecao

            # Desenhando de fato a carta
            surface.blit(imagem_rot, (x, y))


            # Se qualquer carta dessa cor estiver selecionada, desenha borda
            if any(carta.selecionada for carta in mao_jogador if carta.cor == cor):
                pygame.draw.rect(surface, (255, 255, 0), rect, 3)

            # Mostrar quantidade de cartas se for mais de 1
            qtd = contagem_cores[cor]
            if qtd > 1:
                texto = fonte.render(str(qtd), True, (255, 255, 0))
                texto_rect = texto.get_rect(center=(rect.centerx, rect.top + 10))
                surface.blit(texto, texto_rect)


    def desenhar_bilhetes_destino(self, surface, bilhetes, mouse_info, grafo):
        
        if len(bilhetes) == 0: # N pode acontecer, eu acho
            return
        
        w_bi = bilhetes[0].imagem.get_width()
        h_bi = bilhetes[0].imagem.get_height()

        # Barra lateral dos bilhetes
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, w_bi + 20, surface.get_height()))

        for i, bilhete in enumerate(bilhetes):
            # Se tiver hover no bilhete, desenha uma borda no bilhete e da highlight
            # no grafo nas arestas do bilhete
            # Poligono do bilhete
            poligono_bilhete = [(10, 10 + h_bi * i + 10 * i), # sup esq
                                (10 + w_bi, 10 + h_bi * i + 10 * i), # sup dir
                                (10 + w_bi, 10 + h_bi * i + 10 * i + h_bi), # inf dir
                                (10, 10 + h_bi * i + 10 * i + h_bi)] #inf esq
            
            if dentro_poligono(mouse_info[0], poligono_bilhete):
                # borda
                pygame.draw.rect(surface, (0, 0, 0), (5, 10 + h_bi * i + 10 * i - 5, w_bi + 10, h_bi + 10))

                print(grafo.graph.nodes[bilhete.origem]["pos"])

                # highlight no grafo
                pygame.draw.circle(surface, (0, 0, 0), grafo.graph.nodes[bilhete.origem]["pos"], 12)
                pygame.draw.circle(surface, (255, 255, 0), grafo.graph.nodes[bilhete.origem]["pos"], 10)

                pygame.draw.circle(surface, (0, 0, 0), grafo.graph.nodes[bilhete.destino]["pos"], 12)
                pygame.draw.circle(surface, (255, 255, 0), grafo.graph.nodes[bilhete.destino]["pos"], 10)

            if bilhete.concluido:
                pygame.draw.rect(surface, (0, 150, 0), (5, 10 + h_bi * i + 10 * i - 5, w_bi + 10, h_bi + 10))

            surface.blit(bilhete.imagem, (10, 10 + h_bi * i + 10 * i))


    def desenhar_cartas_laterais(self, surface, cartas_laterais, mouse_info):
        carta_base = self.img_cartas_trem_horizontal.get(cartas_laterais[0].cor)
        if not carta_base:
            return

        largura_carta = carta_base.get_width()
        altura_carta = carta_base.get_height()

        x_inicial = surface.get_width() - largura_carta*0.8
        y_inicial = 90
        espacamento = 5
        escala = 0.9

        # Obtém a imagem de uma carta pela cor da primeira carta
        primeira_carta = cartas_laterais[0]
        imagem_base = self.img_cartas_trem_horizontal.get(primeira_carta.cor)
        if not imagem_base:
            return  # não tem imagem para essa cor

        largura_original = imagem_base.get_width()
        altura_original = imagem_base.get_height()
        largura_red = int(largura_original * escala)
        altura_red = int(altura_original * escala)

        for i, carta in enumerate(cartas_laterais):
            imagem = self.img_cartas_trem_horizontal.get(carta.cor)
            if imagem is None:
                continue

            imagem_red = pygame.transform.smoothscale(imagem, (largura_red, altura_red))
            x = x_inicial
            y = y_inicial + i * (altura_red + espacamento)

            rect = pygame.Rect(x, y, largura_red, altura_red)
            carta.rect = rect

            if dentro_poligono(mouse_info[0], [rect.topleft,
                                            (rect.right, rect.top),
                                            (rect.left, rect.bottom),
                                            (rect.right, rect.bottom)]):
                x -= 10

            surface.blit(imagem_red, (x, y))
            
                 


    def draw(self, surface, jogadores, cartas_trem_abertas, mouse_info, grafo):
        surface.fill((198, 197, 176))

        surface.blit(self.background_img, (0, 0)) # Colando o fundo

        surface.blit(self.map_img, (surface.get_width()//2 - self.map_img.get_width()//2, 0))

        # Desenha baralhos destino e vagão (igual antes)
        surface.blit(self.fundo_destino, (surface.get_width() - self.fundo_destino.get_width() - 10, 0 - self.fundo_destino.get_height()//2))
        # Atualizando o rect do baralho de destinos
        self.destino_rect[0], self.destino_rect[1] = surface.get_width() - self.fundo_destino.get_width() - 10, 0 - self.fundo_destino.get_height()//2

        surface.blit(self.fundo_vagao, (surface.get_width() - self.fundo_vagao.get_width()*0.8, surface.get_height() - self.fundo_vagao.get_height() - 10))

        # Desenhando os trilhos pitandos (conquistados)
        for track in self.trilhos_conquistados:
            pygame.draw.polygon(surface, cores[track[4]], track[:4])
        self.rect_baralho_vagao = pygame.Rect(
            surface.get_width() - self.fundo_vagao.get_width()*0.8,
            surface.get_height() - self.fundo_vagao.get_height() - 10,
            self.fundo_vagao.get_width()*0.8,
            self.fundo_vagao.get_height()
        )
        # Desenha cartas abertas na lateral
        self.desenhar_cartas_laterais(surface, cartas_trem_abertas, mouse_info)

        # Desenha mão do jogador ativo
        for jogador in jogadores:
            if jogador.ativo:
                self.desenhar_mao_jogador(surface, jogador.cartas, mouse_info)

        # Desenha cards dos jogadores (igual antes)
        cards_x, cards_y = -5, 100
        cards_w, cards_h = surface.get_width()/10, surface.get_height()/9
        for jogador in jogadores:
            self.criar_card_jogador(surface, jogador, (cards_x, cards_y, cards_w, cards_h))
            cards_y += cards_h + 20
        
        # Desenha botão
        surface.blit(self.saveimg,(5, 5))

        # Bilhetes de destino
        if self.barra_objetivos_ativa:
            for jogador in jogadores:
                if jogador.ativo:
                    self.desenhar_bilhetes_destino(surface, jogador.objetivos, mouse_info, grafo)

    # Retorna um card de jogador, contendo um fundo, um avatar na cor correta
    # Qtd de trens e pontos tem que vir da classe jogador!
    def criar_card_jogador(self, surface, jogador, rect):
        # Se for o turno do jogador, desenha uma borda branca no card
        if jogador.ativo:
            pygame.draw.rect(surface, 
                            (255, 255, 255),
                            (rect[0] - 10, rect[1] - 10, rect[2] + 20, rect[3] + 20),
                            border_radius=5)
        # Desenhando o fundo na cor certa
        pygame.draw.rect(surface, 
                         cores[jogador.cor],
                         rect, border_radius=5)
        
        # Desenhando o avatar

        surface.blit(self.avatar, (rect[0], rect[1])) # Desenhando na tela

        
        # Desenhando a qtd de pontos no canto superior direito do card
        pontos_txt = message_to_screen(surface, str(jogador.pontos), 20, rect[0], rect[1], (0, 0, 0), returning=True)
        p_x, p_y, p_w, p_h = pontos_txt["text_rect"]

        surface.blit(pontos_txt["text"], (p_x + rect[2] - p_w - self.pontos_img.get_width(), p_y + p_h, p_w, p_h))
        surface.blit(self.pontos_img, (p_x + rect[2] - self.pontos_img.get_width(), p_y + p_h - self.pontos_img.get_height()/3))

        # Desenhando a qtd de trens no canto inferior direito do card
        trens_txt = message_to_screen(surface, str(jogador.trens), 20, rect[0], rect[1], (0, 0, 0), returning=True)
        t_x, t_y, t_w, t_h = trens_txt["text_rect"]

        surface.blit(trens_txt["text"], (t_x + rect[2] - t_w - self.qtd_trens_img.get_width(), t_y + rect[3] - t_h, t_w, t_h))
        surface.blit(self.qtd_trens_img, (t_x + rect[2] - self.qtd_trens_img.get_width(), t_y + rect[3] - t_h - self.qtd_trens_img.get_height()/3))
        
        # Se for o turno do jogador, escreve "Vez" centralizado horizontalmente com base no avatar
        if jogador.ativo:
            jogando_txt = message_to_screen(surface, "Turno", 12, rect[0], rect[1], (0, 0, 0), returning=True)
            j_x, j_y, j_w, j_h = jogando_txt["text_rect"]
            avatar_center_x = rect[0] + self.avatar.get_width() // 2
            surface.blit(jogando_txt["text"], (avatar_center_x - j_w // 2, rect[1] + self.avatar.get_height() + 2))

    def ajustar_ponto(self, surface, ponto):
        # Recebe uma superfície e um ponto
        # Executa um ajuste de coordenadas pra achar a coordenada certa do ponto visto que o mapa teve resize
        ponto_ajustado = []
        for point in ponto:
            x = point[0] * (self.new_width / self.original_width) + (surface.get_width()//2 - self.new_width//2)
            y = point[1] * (self.new_height / self.original_height)
            ponto_ajustado.append((x, y))

        return ponto_ajustado
    
     
    def atualizar_trens(self, trilhos, cor):
        for track_id in trilhos:
            track_info = trilhos[track_id].copy()
            track_info.append(cor)
            self.trilhos_conquistados.append(track_info)