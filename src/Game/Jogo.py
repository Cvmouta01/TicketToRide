import random
import pygame
from Mapa import Mapa
from Jogador import Jogador
from CartaTrem import CartaTrem
from CartaObjetivo import CartaObjetivo
from MapGraph import MapGraph
from Utils import *

# Classe que segurará os objetos de jogo
class Jogo():
    # Jogadores é um array de cores
    def __init__(self, jogadores, width, height):
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Ticket to Ride")

        self.map_graph = MapGraph()
        self.mapa = Mapa(self.display)
        self.map_graph.update_arestas(self.display, self.mapa) # Atualiza as arestas carregadas para as coordenadas novas
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

    def passar_turno(self):
        """
        Passa o turno pro proximo jogador da lista
        Volta pro começo caso tenha sido o turno do ultimo jogador da lista

        Precisa executar alguma lógica do tipo:
        Jogador amarelo está presente?
        Pra evitar que jogadores locais vejam as cartas uns dos outros
        """
        self.jogadores[self.jogador_atual_index].ativo = False

        self.jogador_atual_index += 1

        if self.jogador_atual_index >= len(self.jogadores):
            self.jogador_atual_index = 0

        self.jogadores[self.jogador_atual_index].ativo = True

    def game_loop(self):
        for u, v, key, data in self.map_graph.graph.edges(keys=True, data=True):
            print(f"Aresta {u}-{v} (key={key}): {data}")

        # Definindo pois pygame.mouse.get_pressed() retorna vários cliques por conta do loop
        mouse_clicado = False
        while True:
            mouse_pos = pygame.mouse.get_pos()

            # Draw ==================================================================

            # Passa pro desenho do mapa o display, os jogadores, as cartas abertas e informações sobre o mouse
            self.mapa.draw(self.display, self.jogadores, self.cartas_trem_abertas, [mouse_pos, mouse_clicado])

            # CONQUISTANDO ROTAS =====================================================

            # Ideia:
            # Jogador seleciona uma qtd de cartas na sua mão, elas ficam com uma borda
            # Jogador pode remover a seleção clicando novamente

            # Após selecionar as cartas, jogador pode clicar numa rota
            # Se ele selecionou as cartas necessárias, ele conquista a rota e o turno passa pro prox jogador

            # => SELECIONANDO CARTAS
            # A seleção das cartas já está implementado dentro de Mapa.py

            # => SELECIONANDO UMA ROTA
            # Passando por todos as arestas do grafo e definindo os poligonos na interface
            for u, v, key, data in self.map_graph.graph.edges(keys=True, data=True):
                for poligono in data['train_pos']:
                    if dentro_poligono(mouse_pos, data['train_pos'][poligono]):
                        if mouse_clicado:
                            # Por algum motivo nem todas as arestas tem a key "owned" então estou colocando manualmente (!!)
                            if not "owned" in self.map_graph.graph[u][v][key]: self.map_graph.graph[u][v][key]["owned"] = False

                            # Se a aresta não ta "owned"
                            if not self.map_graph.graph[u][v][key]["owned"]:
                                # Se o player pode conquistar a rota
                                if self.jogadores[self.jogador_atual_index].pode_conquistar(data):
                                    # Conquista de fato a rota
                                    self.jogadores[self.jogador_atual_index].conquistar_rota(data)

                                    # Seta a rota como owned
                                    self.map_graph.graph[u][v][key]['owned'] = True

                                    # Conquistou uma rota, é uma das ações possíveis do turno
                                    # Então finaliza o turno
                                    self.passar_turno()
                                else:
                                    print(f"Não foram selecionadas cartas que sejam suficientes para conquistar a rota {u}-{v}")
                            else:
                                print(f"A rota {u}-{v} já está conquistada!")

                        pygame.draw.polygon(self.display, (255, 0, 0), data['train_pos'][poligono], 5) # pode remover dps
                    else:
                        pygame.draw.polygon(self.display, (0, 255, 0), data['train_pos'][poligono], 5) # pode remover dps

            # EVENTOS ================================================================
            mouse_clicado = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # clique do mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicado = True

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
