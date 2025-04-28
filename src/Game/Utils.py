import pygame

# Escreve algo na tela.
# surface -> superfície onde será escrita
# text -> texto a ser escrito (str)
# size -> tamanho do texto (int)
# x -> posição x do texto
# y -> posição y do texto
# color -> tupla contendo valores RGB
# bckg_color -> tupla contendo a cor de fundo do texto (default None)
# returning -> diz se a função deve retornar o objeto texto e seu rect ou desenhar direto
# alignment -> diz a forma de alinhar o texto (center, bottomleft, bottomright) (default center)
def message_to_screen(surface, text, size, x, y, color, bckg_color=None, returning=False, alignment="center"):
    font = pygame.font.Font("freesansbold.ttf", size) # Pode mudar pra uma fonte customizada
    text = font.render(text, True, color, bckg_color)

    textRect = text.get_rect()

    if alignment == "center":
        textRect.center = (x, y)
    elif alignment == "bottomleft":
        textRect.bottomleft = (x, y)
    elif alignment == "bottomright":
        textRect.bottomright = (x, y)

    if returning:
        return {"text": text, "text_rect": textRect}

    surface.blit(text, textRect)

# Desenha um botão na tela
# surface -> superfície onde será escrita
# text -> texto a ser escrito (str)
# text_size -> tamanho do texto (int)
# rect -> contém as dimensões do botão (x, y, w, h)
# color -> cor do botão
# active_color -> cor do botão ativo (on hover)
def button(surface, text, text_size, rect, color, active_color):
    pygame.draw.rect(surface, color, rect, 3)
    message_to_screen(surface, text, text_size, rect.x + rect.w//2, rect.y + rect.h//2, color)
    
    # checking if the mouse is over the button
    mouse = pygame.mouse.get_pos()
    if rect.x < mouse[0] < rect.x + rect.w:
        if rect.y < mouse[1] < rect.y + rect.h:
            pygame.draw.rect(surface, active_color, rect, 3)
            if pygame.mouse.get_pressed()[0]:
                return 1

    return 0