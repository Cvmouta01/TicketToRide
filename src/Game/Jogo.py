import random
import pygame
from Mapa import Mapa
from Jogador import Jogador
from CartaTrem import CartaTrem
from CartaObjetivo import CartaObjetivo
from MapGraph import MapGraph

pygame.init()
width, height = 1366, 768  # 1600, 900

# Classe que segurará os objetos de jogo
class Jogo():
    # Jogadores é um array de cores
    def __init__(self, jogadores):
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Ticket to Ride")

        self.map_graph = MapGraph()
        self.mapa = Mapa(self.display)
        self.mapa.grafo_cidades = self.map_graph.graph

        self.baralho_trem = CartaTrem.criar_baralho_trem()
        self.baralho_objetivo = CartaObjetivo.criar_baralho_objetivo()
        random.shuffle(self.baralho_trem)
        random.shuffle(self.baralho_objetivo)

        self.cartas_trem_abertas = []
        for _ in range(5):
            self.cartas_trem_abertas.append(self.baralho_trem.pop())

        self.jogadores = []
        for cor in jogadores:
            jogador = Jogador(cor)
            for _ in range(4):
                jogador.cartas.append(self.baralho_trem.pop())
            for _ in range(3):
                jogador.objetivos.append(self.baralho_objetivo.pop())
            self.jogadores.append(jogador)

        self.jogadores[0].ativo = True
        self.jogador_atual_index = 0

    def game_loop(self):
        while True:
            # draw
            self.mapa.draw(self.display, self.jogadores, self.cartas_trem_abertas)

            # Ideia: onHover de uma rota, o jogador pode clicar para conquistá-la
            # Se tiver as cartas necessárias, ele conquista a rota e o turno passa pro prox jogador

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # avançar turno
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.jogadores[self.jogador_atual_index].ativo = False
                        self.jogador_atual_index = (self.jogador_atual_index + 1) % len(self.jogadores)
                        self.jogadores[self.jogador_atual_index].ativo = True
                    # visualize o grafo fora da janela pygame
                    elif event.key == pygame.K_v:
                        self.map_graph.visualize()

            pygame.display.update()


num_jogadores = max(2, min(5, 4))
cores_disponiveis = ["vermelho", "amarelo", "verde", "azul", "preto"]
cores_escolhidas = random.sample(cores_disponiveis, num_jogadores)

ticket_to_ride = Jogo(cores_escolhidas)
ticket_to_ride.game_loop()
