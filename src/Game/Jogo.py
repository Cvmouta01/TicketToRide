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
import copy
from IA import IA

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Classe que segurará os objetos de jogo
class Jogo():
    # Jogadores é um array de cores
    def __init__(self, jogadores, width, height):
        self.width = width
        self.height = height
        self.baralho_trem = CartaTrem.criar_baralho_trem()
        self.baralho_objetivo = CartaObjetivo.criar_baralho_objetivo(self.width, self.height)
        random.shuffle(self.baralho_trem)
        random.shuffle(self.baralho_objetivo)
        self.cartas_compradas_esse_turno = 0
        self.cartas_abertas_compradas_nesse_turno = 0

        self.cartas_trem_abertas = []
        for _ in range(5):
            self.cartas_trem_abertas.append(self.baralho_trem.pop())

        self.jogadores = []
        for tupla in jogadores:
            if tupla[1]:
                jogador = Jogador(tupla[0])
            else:
                jogador = IA(tupla[0])
            for _ in range(4):
                jogador.cartas.append(self.baralho_trem.pop())
            for _ in range(3):
                jogador.objetivos.append(self.baralho_objetivo.pop())
            self.jogadores.append(jogador)

        self.jogadores[0].ativo = True
        self.jogador_atual_index = 0

        self.finalizando_jogo = False
        self.jogador_fim = -1
        self.termino_jogo = False

        self.map_graph = None
        

    def passar_turno(self, display, mapa):
        """
        Passa o turno pro proximo jogador da lista
        Volta pro começo caso tenha sido o turno do ultimo jogador da lista

        Precisa executar alguma lógica do tipo:
        Jogador amarelo está presente?
        Pra evitar que jogadores locais vejam as cartas uns dos outros
        """
        msg_popup(display, "Passando Turno", 32, (0, 0, 0), 1, (150, 0, 0))

        self.jogadores[self.jogador_atual_index].ativo = False

        self.jogador_atual_index += 1

        if self.jogador_atual_index >= len(self.jogadores):
            self.jogador_atual_index = 0

        self.jogadores[self.jogador_atual_index].ativo = True

        # Checa se o jogador atual é IA, se for chama seu metodo para escolher uma acao
        if self.jogadores[self.jogador_atual_index].identificador == False:
            acao = self.jogadores[self.jogador_atual_index].escolher_acao(self.map_graph.graph)
            self.processa_turno_IA(acao, display, mapa)
            
            

    def game_loop(self):
        #Iniciando o que não pode ser serializado
        pygame.init()
        display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ticket to Ride")

        mapa = Mapa(display)
        #Iniciando mapa, caso o mapa não exista
        if self.map_graph is None:
            print("Iniciando novo mapa...")
            self.map_graph = MapGraph()
            self.map_graph.update_arestas(display, mapa)
            self.map_graph.update_vertices(display, mapa)
        else:
            # Caso o Mapa já exista (jogo sendo carregado)
            print("Sincronizando mapa carregado...")
            self.map_graph.update_arestas(display, mapa)
            self.map_graph.update_vertices(display, mapa)
            
            # Percorre as rotas e atualiza a cor no mapa visual
            for u, v, key, data in self.map_graph.graph.edges(keys=True, data=True):
                if data.get('owned'): 
                    # Encontra o jogador que possui a rota
                    cor_jogador = None
                    for jogador in self.jogadores:
                        if jogador.mapa_conquistado.grafo.has_edge(u, v):
                           cor_jogador = jogador.cor
                           break
                    
                    if cor_jogador and 'train_pos' in data:
                        mapa.atualizar_trens(data['train_pos'], cor_jogador)

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

            # Checando pra ver se o jogo acabou
            self.verif_fim_de_jogo(display)

            # Draw ==================================================================

            # Passa pro desenho do mapa o display, os jogadores, as cartas abertas e informações sobre o mouse
            mapa.draw(display, self.jogadores, self.cartas_trem_abertas, [mouse_pos, mouse_clicado], self.map_graph)
            
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
                                        if self.jogadores[self.jogador_atual_index].conquistar_rota(data, conquista_possivel):
                                            # Seta a rota como owned
                                            self.map_graph.graph[u][v][key]['owned'] = True

                                            # Avisa o mapa que tem que pintar o trilho com a cor do jogador
                                            mapa.atualizar_trens(data['train_pos'], self.jogadores[self.jogador_atual_index].cor)

                                            print(f"Rota {u}-{v} conquistada pelo jogador {self.jogadores[self.jogador_atual_index].cor}")

                                            msg_popup(display, "Rota conqusitada!", 32, (0, 0, 0), 1, (0, 150, 0))

                                            # Marca rota no mapa do jogador
                                            self.jogadores[self.jogador_atual_index].mapa_conquistado.adicionar_rota(u, v, data['length'])
                                            print(self.jogadores[self.jogador_atual_index].mapa_conquistado.grafo.edges(data=True))

                                            # Verificando se concluiu algum objetivo
                                            for destino in self.jogadores[self.jogador_atual_index].objetivos:
                                                if self.jogadores[self.jogador_atual_index].mapa_conquistado.tem_caminho(destino.origem, destino.destino):
                                                    destino.concluido = True

                                            # Verificando fim de jogo
                                            self.verif_fim_de_jogo(display)

                                            # Conquistou uma rota, é uma das ações possíveis do turno
                                            # Então finaliza o turno
                                            self.passar_turno(display,mapa)
                                    else:
                                        print(f"Não foram selecionadas cartas que sejam suficientes para conquistar a rota {u}-{v}")
                                        msg_popup(display, "Cartas insuficientes!", 32, (0, 0, 0), 1, (150, 0, 0))
                                else:
                                    print(f"A rota {u}-{v} já está conquistada!")
                                    msg_popup(display, "A rota já esta conquistada!", 32, (0, 0, 0), 1, (150, 0, 0))

                            pygame.draw.polygon(display, (255, 0, 0), data['train_pos'][poligono], 2) # pode remover dps
                        else:
                            pygame.draw.polygon(display, (0, 255, 0), data['train_pos'][poligono], 2) # pode remover dps

            # INTERAÇÕES COM CARTAS DE DESTINO ==================================================
            # Ideia: Ao clicar nos bilhetes de destino, serão exibidos 3 para o usuário
            # O usuário pode escolher ficar com 1-3 bilhetes. O restante vai para o fim do baralho
            if mouse_clicado:
                if mapa.destino_rect.collidepoint(mouse_pos):
                    print("Clicou no baralho de destinos!")

                    self.comprando_destinos(display)

                    self.passar_turno(display, mapa) # após comprar bilhetes de destino, passa o turno

            # Desenhando um dos bilhetes de destino que abre a lista
            if button(display, f"Objetivos: {len(self.jogadores[self.jogador_atual_index].objetivos)}", 20, pygame.Rect(10, display.get_height()-10-70, 150, 50), (0, 150, 0), (0, 255, 0)):
                if mouse_clicado:
                    mapa.barra_objetivos_ativa = not mapa.barra_objetivos_ativa


            # INTERAÇÕES COM CARTAS DE VAGÃO ====================================================
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
                        msg_popup(display, "Você já comprou 2 cartas neste turno", 32, (0, 0, 0), 1, (150, 0, 0))

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
                    self.passar_turno(display, mapa)
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

                elif event.type == pygame.KEYDOWN:
                    # avançar turno
                    if event.key == pygame.K_SPACE:
                        self.passar_turno(display, mapa)
                        self.cartas_compradas_esse_turno = 0

                    elif event.key == pygame.K_v:
                        self.map_graph.visualize()

                    # forçando um fim de jogo
                    elif event.key == pygame.K_o:
                        self.jogadores[self.jogador_atual_index].trens = 3



            pygame.display.update()


    def comprando_destinos(self, display):
        comprando = True

        bilhetes = [self.baralho_objetivo.pop(0) for _ in range(3)] # Compra 3 bilhetes de destino

        w_bi = bilhetes[0].imagem.get_width()
        h_bi = bilhetes[0].imagem.get_height()

        bilhetes_comprados = 0
        while comprando:
            mouse_pos = pygame.mouse.get_pos()

            # Barra lateral de compra de bilhetes
            pygame.draw.rect(display, (255, 255, 255), (0, 0, w_bi + 20, self.height))

            # Desenhando os bilhetes
            for i, bilhete in enumerate(bilhetes):
                # Poligono do bilhete
                poligono_bilhete = [(10, 50 + h_bi * i + 20 * i), # sup esq
                                    (10 + w_bi, 50 + h_bi * i + 20 * i), # sup dir
                                    (10 + w_bi, 50 + h_bi * i + 20 * i + h_bi), # inf dir
                                    (10, 50 + h_bi * i + 20 * i + h_bi)] #inf esq

                if dentro_poligono(mouse_pos, poligono_bilhete):
                    # Desenhando a borda onhover
                    pygame.draw.rect(display, (0, 0, 0), (5, 50 + h_bi * i + 20 * i - 5, w_bi + 10, h_bi + 10))

                    if mouse_clicado:
                        # Se clicou o mouse, compra o bilhete de destino
                        self.jogadores[self.jogador_atual_index].objetivos.append(bilhete)

                        bilhetes.remove(bilhete)

                        bilhetes_comprados += 1

                display.blit(bilhete.imagem, (10, 50 + h_bi * i + 20 * i))


            # Botão de sair
            if button(display, "Concluído", 20, pygame.Rect((w_bi+20)//2 - 50, 50 + h_bi * 2 + 20 * 2 + h_bi + 25, 100, 50), (200, 0, 0), (255, 0, 0)):
                if bilhetes_comprados != 0: # Tem que ter comprado ao menos um bilhete
                    # Devolve os bilhetes restantes ao baralho
                    for bilhete in bilhetes:
                        self.baralho_objetivo.append(bilhete)

                    comprando = False

                else:
                    print("Você deve comprar ao menos um bilhete!")
                    msg_popup(display, "Você deve comprar ao menos um bilhete!", 32, (0, 0, 0), 1, (150, 0, 0))
                    

            pygame.display.update()


            # Eventos
            mouse_clicado = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_clicado = True
                
            
    def processa_turno_IA(self, rota, display, mapa):
        """
        Processa a ação decidida pela IA, seja conquistar uma rota ou comprar cartas.
        Exibe pop-ups na tela para informar o jogador sobre a ação da IA.
        """
        jogador_atual = self.jogadores[self.jogador_atual_index]
        pygame.time.wait(500) # Uma pequena pausa para o turno da IA não ser instantâneo

        # CASO 1: A IA decidiu conquistar uma rota
        if rota:
            u, v, key, data = rota
            print(f"IA ({jogador_atual.cor}) tentando conquistar a rota {u}-{v}...")

            # Usa os métodos existentes do jogador para verificar e conquistar
            conquista_possivel = jogador_atual.pode_conquistar(data)
            if conquista_possivel and jogador_atual.conquistar_rota(data, conquista_possivel):
                
                # Atualiza o estado do grafo principal
                self.map_graph.graph[u][v][key]['owned'] = True
                self.map_graph.graph[u][v][key]['owner_color'] = jogador_atual.cor
                
                # pinta rota
                mapa.atualizar_trens(data['train_pos'], jogador_atual.cor)

                # Exibe a mensagem de sucesso por 3 segundos
                mensagem = f"IA ({jogador_atual.cor}) conquistou a rota {u}-{v}!"
                msg_popup(display, mensagem, 32, (255, 255, 255), 3, (0, 100, 0))
                
                # A função conquistar_rota já dá os pontos e remove os trens e cartas.
            else:
                # Se, por algum motivo, a conquista falhar, a IA compra cartas como plano B.
                print(f"IA ({jogador_atual.cor}) falhou em conquistar a rota. Comprando cartas.")
                self.processa_turno_IA(None, display) # Chama a si mesma com a ação de comprar carta
                return # Retorna para não passar o turno duas vezes

        # CASO 2: A IA decidiu comprar cartas (porque 'rota' é None)
        else:
            print(f"IA ({jogador_atual.cor}) vai comprar 2 cartas.")
            
            # Primeira compra de carta
            if self.baralho_trem:
                carta_comprada = self.baralho_trem.pop()
                jogador_atual.cartas.append(carta_comprada)
                # Exibe a mensagem por 3 segundos
                mensagem = f"IA ({jogador_atual.cor}) comprou uma carta."
                msg_popup(display, mensagem, 32, (255, 255, 255), 3, (50, 50, 50))
            else:
                msg_popup(display, "Baralho de trem vazio!", 32, (255, 255, 255), 3, (150, 0, 0))

            # Segunda compra de carta
            if self.baralho_trem:
                carta_comprada = self.baralho_trem.pop()
                jogador_atual.cartas.append(carta_comprada)
                # Exibe a segunda mensagem por 3 segundos
                mensagem = f"IA ({jogador_atual.cor}) comprou outra carta."
                msg_popup(display, mensagem, 32, (255, 255, 255), 3, (50, 50, 50))
            else:
                 msg_popup(display, "Baralho de trem vazio!", 32, (255, 255, 255), 3, (150, 0, 0))
        
        # Ao final da ação da IA (conquistar ou comprar), o turno é passado.
        # A sua função `passar_turno` já lida com a checagem do próximo jogador ser IA.
        self.passar_turno(display, mapa)
    
    def verif_fim_de_jogo(self, display):
        if not self.finalizando_jogo:
            if self.jogadores[self.jogador_atual_index].trens <= 2:
                self.finalizando_jogo = True

                self.jogador_fim = self.jogador_atual_index # Esse é quem decretou o fim do jogo
        else:
            #print(f"Jogador que finalizou: {self.jogador_fim}")
            if self.jogador_atual_index == self.jogador_fim:
                self.game_over(display)

    def calcular_vencedor(self):
        '''
        Passa por todos os jogadores e calcula:
        1 - Cartas de destino concluidas
        2 - Maior caminho
        3 - Pontos gerais

        Constrói um ranking e retorna um dicionário do tipo
        {"jogador": pontos, etc} ja ordenado pelos maiores pontos
        '''

        jogador_maior_cam = []
        tam_maior_cam = 0

        for jogador in self.jogadores:

            # Pontuando cartas de destino concluidas ou não
            for destino in jogador.objetivos:
                if destino.concluido:
                    jogador.pontos += destino.pontos
                else:
                    jogador.pontos -= destino.pontos

            # Pontuando maior caminho
            tam_cam = jogador.mapa_conquistado.calcular_maior_caminho()['peso']

            if tam_cam > tam_maior_cam: # Se foi um que superou
                jogador_maior_cam = [] # Limpa a lista de jogadores a serem pontuados
                tam_maior_cam = tam_cam
                jogador_maior_cam.append(jogador)

            elif tam_cam == tam_maior_cam: # Se foi igual, o jogo permite empate
                tam_maior_cam = tam_cam
                jogador_maior_cam.append(jogador)

        for jogador in jogador_maior_cam: jogador.pontos += 10 # Pontuando os jogadores


        # Construindo o ranking de jogadores
        ranking = {}

        for jogador in self.jogadores:
            ranking[jogador.cor] = jogador.pontos

        return dict(sorted(ranking.items(), key=lambda item: item[1], reverse=True))


    def game_over(self, display):
        fim = True

        ranking = self.calcular_vencedor()

        while fim:
            pygame.display.update()

            message_to_screen(display, "GAME OVER", 40, self.width//2, 100, (255, 0, 0), (0, 0, 0))

            for i, (jogador, pontos) in enumerate(ranking.items()):
                message_to_screen(display, f"Jogador {jogador} => {pontos}", 20, self.width//2, 200 + i*50, (255, 0, 0), (0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


def salvar_jogo(jogo:Jogo):
    root = Tk()
    root.withdraw()
    
    # Copia todos vetores de cartas
    backups = {
        'baralho_objetivo': [],
        'jogadores_objetivos': [[] for _ in jogo.jogadores]
    }

    # Retira os parametros (pygame.surface) que impedem a serialização
    for carta in jogo.baralho_objetivo:
        backups['baralho_objetivo'].append(carta.imagem)
        carta.imagem = None


    for i, jogador in enumerate(jogo.jogadores):
        for carta in jogador.objetivos:
            backups['jogadores_objetivos'][i].append(carta.imagem)
            carta.imagem = None
    
    # Salva
    caminho_arquivo = filedialog.asksaveasfilename(
        title="Salvar jogo",
        defaultextension=".pkl",
        filetypes=[("Arquivos de jogo", "*.pkl")]
    )

    if not caminho_arquivo:
        print("Salvamento cancelado.")
    else:
        with open(caminho_arquivo, 'wb') as f:
            pickle.dump(jogo, f)

    print(f"Jogo salvo em: {caminho_arquivo}")

    # Retorna os vetores de cartas para a situação inicial
    for i, carta in enumerate(jogo.baralho_objetivo):
        carta.imagem = backups['baralho_objetivo'][i]


    for i, jogador in enumerate(jogo.jogadores):
        for j, carta in enumerate(jogador.objetivos):
            carta.imagem = backups['jogadores_objetivos'][i][j]

def carregar_jogo():
    root = Tk()
    root.withdraw()

    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo de jogo salvo",
        filetypes=[("Arquivos de jogo", "*.pkl")]
    )

    if not caminho_arquivo:
        print("Nenhum arquivo selecionado.")
        return None

    with open(caminho_arquivo, 'rb') as f:
        jogo = pickle.load(f)
    
    bo = CartaObjetivo.criar_baralho_objetivo(jogo.width, jogo.height)
    
    #retorna as surfaces
    for carta in bo:    
        for a in jogo.baralho_objetivo:
            if carta.origem == a.origem and carta.destino == a.destino:
                a.imagem = carta.imagem
                
        for player in jogo.jogadores:
            for a in player.objetivos:
                if carta.origem == a.origem and carta.destino == a.destino:
                    a.imagem = carta.imagem
                    
            
    return jogo

