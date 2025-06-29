import pygame
import pytest
from unittest.mock import MagicMock
from src.Game import Utils
from src.Game.settingsScreen import settingsScreen as ss_module
import src.Game.settings as settings


@pytest.fixture
def screen():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    yield screen
    pygame.quit()


def test_settings_screen_quit_event(screen, monkeypatch):
    monkeypatch.setattr(Utils, "button", lambda *args, **kwargs: False)
    monkeypatch.setattr(Utils, "check_f11", lambda event, fullscreen, window_Size, screen: (fullscreen, screen))
    monkeypatch.setattr(Utils, "draw_cropped_background", lambda screen, bg: None)
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda: (0, 0, 0))

    window_size = ss_module(screen)
    assert window_size == (800, 600)


def test_settings_screen_voltar_button(screen, monkeypatch):
    def fake_button(screen, text, *args, **kwargs):
        return text == "Voltar"
    monkeypatch.setattr(Utils, "button", fake_button)
    monkeypatch.setattr(Utils, "check_f11", lambda event, fullscreen, window_Size, screen: (False, screen))
    monkeypatch.setattr(Utils, "draw_cropped_background", lambda screen, bg: None)
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda: (0, 0, 0))
    pygame.event.post(pygame.event.Event(pygame.QUIT))

    window_size = ss_module(screen)
    assert window_size == (800, 600)


def test_settings_screen_click_resolution_changes(monkeypatch, screen):
    # Configura botão para retornar True apenas para a resolução do primeiro botão
    clicked_size = settings.window_sizes[0]
    clicked_button_text = f"Resolution: {clicked_size[0]}x{clicked_size[1]}"
    call_count = {"count": 0}

    def fake_button(screen_arg, text, *args, **kwargs):
        # Só retorna True na primeira chamada com o texto esperado e clique no frame certo
        if text == clicked_button_text and call_count["count"] == 0:
            call_count["count"] += 1
            return True
        return False

    monkeypatch.setattr(Utils, "button", fake_button)
    monkeypatch.setattr(Utils, "check_f11", lambda event, fullscreen, window_Size, screen: (False, screen))
    monkeypatch.setattr(Utils, "draw_cropped_background", lambda screen, bg: None)
    # Simula clique do mouse com mouse_state sendo [0, 1] para detectar subida do botão
    mouse_states = [[0, 1]] + [[0, 0]] * 10  # clicou só no primeiro frame, depois não
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda: (1, 0, 0))

    # Posta evento QUIT para sair do loop depois do clique
    pygame.event.post(pygame.event.Event(pygame.QUIT))

    window_size = ss_module(screen)
    assert window_size == clicked_size


def test_settings_screen_fullscreen_toggle(monkeypatch, screen):

    clicked_size = settings.window_sizes[0]
    clicked_button_text = f"Resolution: {clicked_size[0]}x{clicked_size[1]}"
    call_count = {"count": 0}

    def fake_button(screen_arg, text, *args, **kwargs):
        if text == clicked_button_text and call_count["count"] == 0:
            call_count["count"] += 1
            return True
        return False

    monkeypatch.setattr(Utils, "button", fake_button)

    # Simula fullscreen ativo
    def fake_check_f11(event, fullscreen, window_Size, screen):
        return True, screen  # fullscreen ativado

    monkeypatch.setattr(Utils, "check_f11", fake_check_f11)
    monkeypatch.setattr(Utils, "draw_cropped_background", lambda screen, bg: None)
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda: (0, 1, 0))  # simula mouse clicado
    
    # Posta evento QUIT para sair do loop depois do clique
    pygame.event.post(pygame.event.Event(pygame.QUIT))

    window_size = ss_module(screen)
    assert window_size == clicked_size


def test_settings_screen_no_button_click(monkeypatch, screen):
    # Nenhum botão clicado, deve rodar normalmente e terminar no evento QUIT
    monkeypatch.setattr(Utils, "button", lambda *args, **kwargs: False)
    monkeypatch.setattr(Utils, "check_f11", lambda event, fullscreen, window_Size, screen: (False, screen))
    monkeypatch.setattr(Utils, "draw_cropped_background", lambda screen, bg: None)
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda: (0, 0, 0))

    pygame.event.post(pygame.event.Event(pygame.QUIT))

    window_size = ss_module(screen)
    assert window_size == (800, 600)
