import pygame
import sys
import settings
import Utils
from settingsScreen import settingsScreen
from Jogo import Jogo
import random


def menuPrincipal(height, width):
    pygame.init()
    

    screen = pygame.display.set_mode((height, width))
    pygame.display.set_caption(settings.WINDOW_TITLE)
    running = True
    fullscreen = False
    background_image = pygame.image.load(settings.BACKGROUND_IMAGE_PATH).convert()
    menuState = 0
    mouse_state = [1,1]

    rodando = True
    while rodando:

        mouse_state[0] = mouse_state[1]
        mouse_state[1] = pygame.mouse.get_pressed()[0]
        Utils.draw_cropped_background(screen, background_image)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if 250 <= mouse_x <= 550:
                    if 150 <= mouse_y <= 200:
                        #Chamar jogo
                        print("Menu de jogo")
                    elif 250 <= mouse_y <= 300:
                        #Chamar menu de configuracao
                        print("Menu de configuracao")
                    elif 350 <= mouse_y <= 400:
                        rodando = False

        Utils.message_to_screen(screen, "Ticket to Ride", 30, screen.get_width()//2, 50, settings.BUTTON_COLOR)

        # Jogar o jogo
        if Utils.button(screen, "Jogar", 20, pygame.Rect(screen.get_width()//2 - 150, 150, 300, 50), settings.BUTTON_COLOR, settings.BUTTON_ACTIVE_COLOR) and mouse_state == [0,1]:
            rodando = False
            # Import feio para não ter import circular
            from SelectionScreen import SelectionScreen
            print(height, width)
            SelectionScreen(height, width)
            

        if Utils.button(screen, "Configurar", 20, pygame.Rect(screen.get_width()//2 - 150, 250, 300, 50), settings.BUTTON_COLOR, settings.BUTTON_ACTIVE_COLOR) and mouse_state == [0,1]:
            size = settingsScreen(screen)
            height, width = size
            if fullscreen:
                screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode(size)

        if Utils.button(screen, "Sair", 20, pygame.Rect(screen.get_width()//2 - 150, 350, 300, 50), settings.BUTTON_COLOR, settings.BUTTON_ACTIVE_COLOR) and mouse_state == [0,1]:
            pygame.quit()
            quit()

        pygame.display.update()
    
    pygame.quit()
    sys.exit()

