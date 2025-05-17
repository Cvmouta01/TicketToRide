import random
import pygame
from Mapa import Mapa
from Jogador import Jogador
from CartaTrem import *
from CartaObjetivo import CartaObjetivo

pygame.init()
width, height = 1366, 768 # 1600, 900

# Classe que segurará os objetos de jogo
class Jogo():
    # Jogadores é um array de cores
    def __init__(self, jogadores):
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Ticket to Ride")

        self.mapa = Mapa(self.display)

        # Criar baralhos de trem e de objetivos
        self.baralho_trem = CartaTrem.criar_baralho_trem()
        self.baralho_objetivo = CartaObjetivo.criar_baralho_objetivo()
        self.cartas_compradas_esse_turno = 0

        # Embaralhar
        random.shuffle(self.baralho_trem)
        random.shuffle(self.baralho_objetivo)

        self.cartas_laterais = [self.baralho_trem.pop() for _ in range(6)]
        # Criando os objetos jogadores
        self.jogadores = []
        for cor in jogadores:
            jogador = Jogador(cor)
            
            # Dar 4 cartas de trem
            for _ in range(4):
                jogador.cartas.append(self.baralho_trem.pop())
                
            # Dar 3 bilhetes de destino (objetivos)
            for _ in range(3):
                jogador.objetivos.append(self.baralho_objetivo.pop())

            self.jogadores.append(jogador)
        
        self.jogadores[0].ativo = True  # Primeiro jogador começa ativo
        self.jogador_atual_index = 0   # Salvar o índice atual
            

    def game_loop(self):
        while True:
            # Draw
            self.mapa.draw(self.display, self.jogadores) # Desenha os elementos da UI

            # Desenhar a mão do jogador atual
            jogador_atual = self.jogadores[self.jogador_atual_index]
            desenhar_mao_jogador(self.display, jogador_atual.cartas)
            desenhar_cartas_laterais(self.display, self.cartas_laterais)

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                #Avançar o turno apertando ESPAÇO (provisório)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        jogador_atual.ativo = False
                        self.jogador_atual_index = (self.jogador_atual_index + 1) % len(self.jogadores)
                        self.jogadores[self.jogador_atual_index].ativo = True
                #Clique com mouse esquerdo
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        clicou_em_compra = False

                        # Verifica clique nas cartas de compra (laterais)
                        for i, carta in enumerate(self.cartas_laterais):
                            if carta.rect.collidepoint(mouse_pos):
                                jogador_atual.cartas.append(carta)

                                # Regra: se carta coringa, turno acaba
                                if carta.cor == "coringa":
                                    self.cartas_compradas_esse_turno = 2
                                else:
                                    self.cartas_compradas_esse_turno += 1

                                # Substitui carta lateral
                                self.cartas_laterais[i] = self.baralho_trem.pop() if self.baralho_trem else None
                                self.cartas_laterais = [c for c in self.cartas_laterais if c is not None]
                                while len(self.cartas_laterais) < 6 and self.baralho_trem:
                                    self.cartas_laterais.append(self.baralho_trem.pop())

                                clicou_em_compra = True
                                break

                        # Só permite seleção se não clicou em compra
                        if not clicou_em_compra:
                            for carta in jogador_atual.cartas:
                                if carta.rect.collidepoint(mouse_pos):
                                    for c in jogador_atual.cartas:
                                        c.selecionada = False
                                    carta.selecionada = True
                                    break

            # Verifica se deve passar o turno
            if self.cartas_compradas_esse_turno >= 2:
                jogador_atual.ativo = False
                self.jogador_atual_index = (self.jogador_atual_index + 1) % len(self.jogadores)
                self.jogadores[self.jogador_atual_index].ativo = True
                self.cartas_compradas_esse_turno = 0


            # Update
            pygame.display.update()



num_jogadores = max(2, min(5, 4))  # Garante que o número fique entre 2 e 5
cores_disponiveis = ["vermelho", "amarelo", "verde", "azul", "preto"]
cores_escolhidas = random.sample(cores_disponiveis, num_jogadores)

ticket_to_ride = Jogo(cores_escolhidas)
ticket_to_ride.game_loop()
