import pygame

def message_to_screen(surface, text, size, x, y, color, bckg_color=None, returning=False, alignment="center"):
    """
    Renderiza um texto na tela ou retorna o texto e seu retângulo.

    Parameters:
        surface (pygame.Surface): Superfície onde será desenhado o texto.
        text (str): Texto a ser exibido.
        size (int): Tamanho da fonte.
        x (int): Coordenada X para posicionamento.
        y (int): Coordenada Y para posicionamento.
        color (tuple): Cor do texto (R, G, B).
        bckg_color (tuple, optional): Cor de fundo do texto. Default None.
        returning (bool, optional): Se True, retorna o texto e o retângulo. Default False.
        alignment (str, optional): Alinhamento do texto: 'center', 'bottomleft', 'bottomright'. Default 'center'.

    Returns:
        dict (optional): {'text': Surface, 'text_rect': Rect} se returning=True.
    """
    font = pygame.font.Font("freesansbold.ttf", size)
    text_surf = font.render(text, True, color, bckg_color)
    text_rect = text_surf.get_rect()

    if alignment == "center":
        text_rect.center = (x, y)
    elif alignment == "bottomleft":
        text_rect.bottomleft = (x, y)
    elif alignment == "bottomright":
        text_rect.bottomright = (x, y)

    if returning:
        return {"text": text_surf, "text_rect": text_rect}

    surface.blit(text_surf, text_rect)

def button(surface, text, text_size, rect, color, active_color):
    """
    Desenha um botão e retorna True se clicado.

    Parameters:
        surface (pygame.Surface): Superfície onde será desenhado o botão.
        text (str): Texto do botão.
        text_size (int): Tamanho do texto.
        rect (pygame.Rect): Retângulo do botão (x, y, w, h).
        color (tuple): Cor padrão do botão (R, G, B).
        active_color (tuple): Cor quando o botão está com o mouse sobre.

    Returns:
        bool: True se o botão for clicado, False caso contrário.
    """
    mouse = pygame.mouse.get_pos()
    is_hover = rect.collidepoint(mouse)

    border_color = active_color if is_hover else color
    pygame.draw.rect(surface, border_color, rect, 3)

    message_to_screen(surface, text, text_size, rect.x + rect.w // 2, rect.y + rect.h // 2, color)

    if is_hover and pygame.mouse.get_pressed()[0]:
        return True

    return False

def draw_cropped_background(screen, background_image):
    """
    Desenha a parte central da imagem de fundo cortada para caber na janela.

    Parameters:
        screen (pygame.Surface): Superfície onde desenhar o fundo.
        background_image (pygame.Surface): Imagem completa de fundo.
    """
    screen_width, screen_height = screen.get_size()
    bg_width, bg_height = background_image.get_size()

    crop_x = max((bg_width - screen_width) // 2, 0)
    crop_y = max((bg_height - screen_height) // 2, 0)

    crop_rect = pygame.Rect(crop_x, crop_y, screen_width, screen_height)
    cropped_image = background_image.subsurface(crop_rect)
    screen.blit(cropped_image, (0, 0))

def check_f11(event, fullscreen, window_size, screen):
    """
    Alterna entre o modo de tela cheia e o modo janela ao pressionar a tecla F11.

    Parameters:
        event (pygame.event): Evento do Pygame.
        fullscreen (bool): Flag indicando se a tela está em modo de tela cheia.
        window_size (tuple): Tamanho da janela (largura, altura).
        screen (pygame.Surface): Superfície de tela.

    Returns:
        fullscreen (bool): Novo estado de fullscreen.
        screen (pygame.Surface): Superfície de tela atualizada.
    """
    if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
        fullscreen = not fullscreen
        if fullscreen:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(window_size)
    return fullscreen, screen

def resize_com_escala(imagem, tela_w, tela_h, proporcao_x, porporcao_y):
    """
    Recebe uma imagem e dá resize mantendo as proporções
    imagem -> objeto imagem que sofrerá o resize
    tela_w -> largura da tela
    tela_h -> altura da tela
    proporcao_x -> % da tela que a imagem deve ocupar em x
    proporcao_y -> % da tela que a imagem deve ocupar em y
    """
    w, h = imagem.get_size()
    escala = max(tela_w*proporcao_x / w, tela_h*porporcao_y / h)
    return pygame.transform.scale(imagem, (w*escala, h*escala))