import random
import pygame
from Mapa import Mapa
from Jogador import Jogador
from CartaTrem import CartaTrem
from CartaObjetivo import CartaObjetivo
from MapGraph import MapGraph
from Utils import *
import os
import pickle
from tkinter import Tk, filedialog

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Classe que segurará os objetos de jogo
class Jogo():
    # Jogadores é um array de cores
    def __init__(self, jogadores, width, height):
        self.width = width
        self.height = height
        self.baralho_trem = CartaTrem.criar_baralho_trem()
        self.baralho_objetivo = CartaObjetivo.criar_baralho_objetivo()
        random.shuffle(self.baralho_trem)
        random.shuffle(self.baralho_objetivo)
        self.cartas_compradas_esse_turno = 0
        self.cartas_abertas_compradas_nesse_turno = 0

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
        #Iniciando o que não pode ser serializado
        pygame.init()
        display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ticket to Ride")

        #Iniciando mapa
        self.map_graph = MapGraph()
        mapa = Mapa(display)
        self.map_graph.update_arestas(display, mapa) # Atualiza as arestas carregadas para as coordenadas novas
        mapa.grafo_cidades = self.map_graph.graph
        
        #Carregando audio
        pygame.mixer.init()

        train_horn_sound = pygame.mixer.Sound(BASE_DIR + "./assets/sounds/train_horn.wav")

        background_music = pygame.mixer.music.load(BASE_DIR + "./assets/sounds/background_music.wav")
        pygame.mixer.music.set_volume(0.01)

        card_draw_sound = pygame.mixer.Sound(BASE_DIR + "./assets/sounds/card_draw.wav")

        train_horn_sound.play()




        # Tocando som de fundo
        pygame.mixer.music.play(loops=-1)

        for u, v, key, data in self.map_graph.graph.edges(keys=True, data=True):
            print(f"Aresta {u}-{v} (key={key}): {data}")

        # Definindo pois pygame.mouse.get_pressed() retorna vários cliques por conta do loop
        mouse_clicado = False
        while True:
            mouse_pos = pygame.mouse.get_pos()

            # Draw ==================================================================

            # Passa pro desenho do mapa o display, os jogadores, as cartas abertas e informações sobre o mouse
            mapa.draw(display, self.jogadores, self.cartas_trem_abertas, [mouse_pos, mouse_clicado])
            
            # CONQUISTANDO ROTAS =====================================================

            # Ideia:
            # Jogador seleciona uma qtd de cartas na sua mão, elas ficam com uma borda
            # Jogador pode remover a seleção clicando novamente

            # Após selecionar as cartas, jogador pode clicar numa rota
            # Se ele selecionou as cartas necessárias, ele conquista a rota e o turno passa pro prox jogador

            # => SELECIONANDO CARTAS
            # A seleção das cartas já está implementado dentro de Mapa.py

            # => SELECIONANDO UMA ROTA
            # => SELECIONANDO UMA ROTA
            # Passando por todos as arestas do grafo e definindo os poligonos na interface
            for u, v, key, data in self.map_graph.graph.edges(keys=True, data=True):
                for poligono in data['train_pos']:
                    if self.map_graph.graph[u][v][key]['owned']:
                        pygame.draw.polygon(display, (0, 0, 0), data['train_pos'][poligono], 2)
                    else:
                        if dentro_poligono(mouse_pos, data['train_pos'][poligono]):
                            if mouse_clicado:

                                # Se a aresta não ta "owned"
                                if not self.map_graph.graph[u][v][key]["owned"]:
                                    # Se o player pode conquistar a rota
                                    conquista_possivel = self.jogadores[self.jogador_atual_index].pode_conquistar(data)
                                    if conquista_possivel != None:
                                        # Conquista de fato a rota
                                        self.jogadores[self.jogador_atual_index].conquistar_rota(data, conquista_possivel)

                                        # Seta a rota como owned
                                        self.map_graph.graph[u][v][key]['owned'] = True

                                        # Avisa o mapa que tem que pintar o trilho com a cor do jogador
                                        mapa.atualizar_trens(data['train_pos'], self.jogadores[self.jogador_atual_index].cor)

                                        print(f"Rota {u}-{v} conquistada pelo jogador {self.jogadores[self.jogador_atual_index].cor}")

                                        # Conquistou uma rota, é uma das ações possíveis do turno
                                        # Então finaliza o turno
                                        self.passar_turno()
                                    else:
                                        print(f"Não foram selecionadas cartas que sejam suficientes para conquistar a rota {u}-{v}")
                                else:
                                    print(f"A rota {u}-{v} já está conquistada!")

                            pygame.draw.polygon(display, (255, 0, 0), data['train_pos'][poligono], 2) # pode remover dps
                        else:
                            pygame.draw.polygon(display, (0, 255, 0), data['train_pos'][poligono], 2) # pode remover dps

            # INTERAÇÕES COM CARTAS ====================================================
            if mouse_clicado:
                jogador_atual = self.jogadores[self.jogador_atual_index]
                clicou_em_compra = False
                # --- CLICOU EM CARTA FECHADA (baralho de vagão) ---
                if mapa.rect_baralho_vagao.collidepoint(mouse_pos):
                    jogador_atual = self.jogadores[self.jogador_atual_index]

                    # Só permite comprar se ainda não pegou 2 cartas
                    if self.cartas_compradas_esse_turno < 2:
                        if self.baralho_trem:
                            carta_comprada = self.baralho_trem.pop()
                            jogador_atual.cartas.append(carta_comprada)
                            self.cartas_compradas_esse_turno += 1
                            print(f"{jogador_atual.cor} comprou uma carta fechada ({carta_comprada.cor})")
                            
                            # Tocando o som
                            card_draw_sound.play()
                        else:
                            print("O baralho de trem está vazio.")
                    else:
                        print("Você já comprou 2 cartas neste turno.")

                # Clicou em carta lateral
                for i, carta in enumerate(self.cartas_trem_abertas):
                    if carta.rect.collidepoint(mouse_pos):
                        # Se não clicou num coringa aberto, ou se clicou num coringa aberto e ainda não comprou nenhuma aberta
                        if carta.cor != "coringa" or (carta.cor == "coringa" and self.cartas_abertas_compradas_nesse_turno == 0):
                            jogador_atual.cartas.append(carta) # Compra a carta

                            self.cartas_compradas_esse_turno += 1
                            self.cartas_abertas_compradas_nesse_turno += 1

                            if carta.cor == "coringa": # Se a carta for um coringa, adiciona novamente pra terminar o turno
                                self.cartas_compradas_esse_turno += 1
                                self.cartas_abertas_compradas_nesse_turno += 1

                            # Substitui carta lateral
                            if self.baralho_trem:
                                self.cartas_trem_abertas[i] = self.baralho_trem.pop()
                            else:
                                self.cartas_trem_abertas.pop(i)

                            clicou_em_compra = True

                            # Tocando o som
                            card_draw_sound.play()
                            break

                # Se não clicou em carta de compra, verifica a seleção da mão
                # Seleção da mão já está implementado em Mapa -> desenhar_mao_jogador()
                if not clicou_em_compra:
                    for carta in jogador_atual.cartas:
                        if carta.rect is not None and carta.rect.collidepoint(mouse_pos):
                            cor_clicada = carta.cor
                            for c in jogador_atual.cartas:
                                c.selecionada = (c.cor == cor_clicada or c.cor == "coringa")
                            break
                
                #Clicou botão salvar
                if mouse_pos[0] < 53 and mouse_pos[1] < 53:
                    salvar_jogo(self)

      

                # Passa o turno se necessário
                if self.cartas_compradas_esse_turno >= 2:
                    self.passar_turno()
                    self.cartas_compradas_esse_turno = 0
                    self.cartas_abertas_compradas_nesse_turno = 0

            # EVENTOS ================================================================
            mouse_clicado = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # clique do mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_clicado = True

                # avançar turno
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.passar_turno()
                        self.cartas_compradas_esse_turno = 0
                    elif event.key == pygame.K_v:
                        self.map_graph.visualize()



            pygame.display.update()



def salvar_jogo(jogo):
    root = Tk()
    root.withdraw()

    caminho_arquivo = filedialog.asksaveasfilename(
        title="Salvar jogo",
        defaultextension=".pkl",
        filetypes=[("Arquivos de jogo", "*.pkl")]
    )

    if not caminho_arquivo:
        print("Salvamento cancelado.")
        return

    with open(caminho_arquivo, 'wb') as f:
        pickle.dump(jogo, f)

    print(f"Jogo salvo em: {caminho_arquivo}")

def carregar_jogo():
    root = Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter

    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo de jogo salvo",
        filetypes=[("Arquivos de jogo", "*.pkl")]
    )

    if not caminho_arquivo:
        print("Nenhum arquivo selecionado.")
        return None

    with open(caminho_arquivo, 'rb') as f:
        jogo = pickle.load(f)

    return jogo