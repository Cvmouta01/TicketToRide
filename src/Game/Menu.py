import pygame
import sys
import settings
import Utils

pygame.init()

window_Size = settings.window_sizes[0]
screen = pygame.display.set_mode(window_Size)
pygame.display.set_caption(settings.WINDOW_TITLE)
running = True
fullscreen = False
background_image = pygame.image.load(settings.BACKGROUND_IMAGE_PATH).convert()
menuState = 0


def menuPrincipal():
    rodando = True
    while rodando:
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

        Utils.message_to_screen(screen, "Ticket to Ride", 30, 400, 50, settings.BUTTON_COLOR)
        Utils.button(screen, "Jogar", 20, pygame.Rect(250, 150, 300, 50), settings.BUTTON_COLOR, settings. BUTTON_ACTIVE_COLOR)
        Utils.button(screen, "Configurar", 20, pygame.Rect(250, 250, 300, 50), settings.BUTTON_COLOR, settings. BUTTON_ACTIVE_COLOR)
        Utils.button(screen, "Sair", 20, pygame.Rect(250, 350, 300, 50), settings.BUTTON_COLOR, settings. BUTTON_ACTIVE_COLOR)

        pygame.display.update()
    
    pygame.quit()
    sys.exit()

menuPrincipal()
