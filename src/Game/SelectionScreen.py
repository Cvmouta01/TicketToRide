from Jogo import Jogo
import pygame
import sys
import settings
import Utils
from Jogo import carregar_jogo


def SelectionScreen(height, width):

    # Iniciando parametros do pygame e de controle
    print(height, width)
    pygame.init()
    screen = pygame.display.set_mode((height,width))
    pygame.display.set_caption(settings.WINDOW_TITLE)
    background_image = pygame.image.load(settings.BACKGROUND_IMAGE_PATH).convert()
    background_image = pygame.transform.scale(background_image, (height, width))
    mouse_state = [1,1]
    rodando = True
    cores_disponiveis = ["verde", "azul", "cinza", "roxo", "rosa"]
    slots = {1:"vermelho", 2: "none", 3: "none", 4: "none", 5: "none"}

    while rodando:

        # Parametros para controle
        mouse_state[0] = mouse_state[1]
        mouse_state[1] = pygame.mouse.get_pressed()[0]
        Utils.draw_cropped_background(screen, background_image)

        # Evento para fechar o jogo sem travar
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
        
        # Desenha player 1 obrigatório 
        pygame.draw.rect(screen,settings.cores[slots[1]],(50, 50, 100, 100),border_radius= 25)
        
        # Botão para mudar de cor
        if Utils.button(screen, ">", 20, pygame.Rect(160 ,110 ,40,40), (0,0,0), (255,255,255)) and mouse_state == [0,1]:
            cores_disponiveis.append(slots[1])
            slots[1] = cores_disponiveis[0]
            cores_disponiveis.remove(slots[1])

        # Verifica e carrega na tela a situação dos slots de jogadores
        for i in range(2,6):
            x = [screen.get_width()//2 - 100, screen.get_width()- 250, 100, screen.get_width()-300]
            y = [50,50,300,300]
            if slots[i] == "none":
    
                if Utils.button(screen, "+Player", 20, pygame.Rect(x[i-2] ,y[i-2] ,100,100), (0,150,0), (255,255,255)) and mouse_state == [0,1]:
                    # Atribui uma cor ao player slot
                    slots[i] = cores_disponiveis[0]
                    cores_disponiveis.remove(slots[i])
                if Utils.button(screen, "+AI", 20, pygame.Rect(x[i-2]+100 ,y[i-2] ,100,100), (150,0,0), (255,255,255)) and mouse_state == [0,1]:
                    # por enquanto adiciona Player, mudar quando programar AI
                    # slots[i] = "ai"
                    slots[i] = cores_disponiveis[0]
                    cores_disponiveis.remove(slots[i])
            elif slots != "ai":
                pygame.draw.rect(screen,settings.cores[slots[i]],(x[i-2], y[i-2], 100, 100),border_radius= 25)
                
                # Botão para mudar de cor
                if Utils.button(screen, ">", 20, pygame.Rect(x[i-2] + 110 ,y[i-2] + 60 , 40, 40), (0,0,0), (255,255,255)) and mouse_state == [0,1]:
                    cores_disponiveis.append(slots[i])
                    slots[i] = cores_disponiveis[0]
                    cores_disponiveis.remove(slots[i])
                
                # Botão para deletar jogador
                if Utils.button(screen, "x", 20, pygame.Rect(x[i-2] + 110 ,y[i-2]  , 40, 40), (0,0,0), (255,255,255)) and mouse_state == [0,1]:
                    cores_disponiveis.append(slots[i])
                    slots[i] = "none"
                    

    
            

        # Botão para voltar ao menu principal
        if Utils.button(screen, "Voltar", 20, pygame.Rect(50 ,screen.get_height()-100,200,75), settings.BUTTON_COLOR, settings.BUTTON_ACTIVE_COLOR) and mouse_state == [0,1]:
            # Import feio para não ter import circular
            from Menu import menuPrincipal
            rodando = False
            menuPrincipal(height, width)
        
         # Botão para funcionalidade de carregar jogo anteriormente salvo
        if Utils.button(screen, "Carregar Jogo", 20, pygame.Rect(screen.get_width()//2 - 100 ,screen.get_height()-100,200,75), settings.BUTTON_COLOR, settings.BUTTON_ACTIVE_COLOR) and mouse_state == [0,1]:
            rodando = False
            jogo = carregar_jogo()
            
            # Ajustando dimensões 
            jogo.height = screen.get_height()
            jogo.width = screen.get_width()
            jogo.game_loop()
        
        if Utils.button(screen, "Iniciar Jogo", 20, pygame.Rect(screen.get_width() - 250, screen.get_height()-100, 200, 75), settings.BUTTON_COLOR, settings.BUTTON_ACTIVE_COLOR) and mouse_state == [0,1]:
            cores_selecionadas = []
            for i in range(1,6):
                if slots[i] != "none":
                    cores_selecionadas.append(slots[i])
            if len(cores_selecionadas) < 2:
                print("jogadores insuficientes para iniciar jogo")
            else:
                ticket_to_ride = Jogo(cores_selecionadas, screen.get_width(), screen.get_height())
                rodando = False
                ticket_to_ride.game_loop()

        pygame.display.update()

