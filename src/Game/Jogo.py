import random
import pygame
from Mapa import Mapa
from Jogador import Jogador
from CartaTrem import CartaTrem
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
        
        # Embaralhar
        random.shuffle(self.baralho_trem)
        random.shuffle(self.baralho_objetivo)

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

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                #Avançar o turno apertando ESPAÇO (provisório)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.jogadores[self.jogador_atual_index].ativo = False
                        self.jogador_atual_index = (self.jogador_atual_index + 1) % len(self.jogadores)
                        self.jogadores[self.jogador_atual_index].ativo = True

            # Update
            pygame.display.update()



num_jogadores = max(2, min(5, 4))  # Garante que o número fique entre 2 e 5
cores_disponiveis = ["vermelho", "amarelo", "verde", "azul", "preto"]
cores_escolhidas = random.sample(cores_disponiveis, num_jogadores)

ticket_to_ride = Jogo(cores_escolhidas)
ticket_to_ride.game_loop()
