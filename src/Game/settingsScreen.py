import pygame
import settings
import Utils

def settingsScreen(screen):
    running = True
    fullscreen = False

    window_Size = (screen.get_width(), screen.get_height())

    background_image = pygame.image.load(settings.BACKGROUND_IMAGE_PATH).convert()

    while running:
        Utils.draw_cropped_background(screen, background_image)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            fullscreen, screen = Utils.check_f11(event, fullscreen, window_Size, screen)

        total_height = len(settings.window_sizes) * settings.BUTTON_HEIGHT + (len(settings.window_sizes) - 1) * settings.BUTTON_SPACING
        screen_width, screen_height = screen.get_size()

        start_y = (screen_height - total_height) // 2
        start_x = (screen_width - settings.BUTTON_WIDTH) // 2

        for i, size in enumerate(settings.window_sizes):
            rect = pygame.Rect(
                start_x,
                start_y + i * (settings.BUTTON_HEIGHT + settings.BUTTON_SPACING),
                settings.BUTTON_WIDTH,
                settings.BUTTON_HEIGHT
            )
            if Utils.button(screen, f"Resolution: {size[0]}x{size[1]}", 20, rect, settings.BUTTON_COLOR, settings.BUTTON_ACTIVE_COLOR):
                window_Size = size
                if fullscreen:
                    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(size)

        if Utils.button(screen, "Voltar", 20, pygame.Rect(screen.get_width()//2 - 150, screen.get_height()-100, 300, 50), settings.BUTTON_COLOR, settings.BUTTON_ACTIVE_COLOR):
            running = False

        pygame.display.flip()

    return window_Size
