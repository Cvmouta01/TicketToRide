import pygame
from Mapa import Mapa
from Jogador import Jogador

pygame.init()
width, height = 1600, 900

# Classe que segurará os objetos de jogo
class Jogo():
    # Jogadores é um array de cores
    def __init__(self, jogadores):
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Ticket to Ride")

        self.mapa = Mapa(self.display)

        # Criando os objetos jogadores
        self.jogadores = []
        for cor in jogadores:
            self.jogadores.append(Jogador(cor))
            

    def game_loop(self):
        while True:
            # Draw
            self.mapa.draw(self.display, self.jogadores) # Desenha os elementos da UI

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Update
            pygame.display.update()


# Teste de Execução
ticket_to_ride = Jogo(["vermelho", "amarelo", "verde", "azul", "preto"])
ticket_to_ride.game_loop()