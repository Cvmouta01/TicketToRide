import pytest
import pygame
from src.Game.Menu import menuPrincipal


@pytest.fixture
def mock_pygame(monkeypatch):
    class DummySurface:
        def convert(self): return self
        def get_width(self): return 800
        def get_height(self): return 600
        def get_size(self): return (800, 600)
        def fill(self, color): pass
        def blit(self, *args): pass

    monkeypatch.setattr(pygame.display, "set_mode", lambda size, *args, **kwargs: DummySurface())
    monkeypatch.setattr(pygame.display, "set_caption", lambda title: None)
    monkeypatch.setattr(pygame.display, "update", lambda: None)
    monkeypatch.setattr(pygame.display, "flip", lambda: None)
    monkeypatch.setattr(pygame.image, "load", lambda path: DummySurface())  # ✅

    pressed = [0, 0, 0]
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda: pressed)
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (0, 0))

    return pressed



def test_menuPrincipal_jogar_called(monkeypatch, mock_pygame):
    def fake_button(screen, text, size, rect, color1, color2):
        return text == "Jogar"

    monkeypatch.setattr("src.Game.Utils.button", fake_button)
    monkeypatch.setattr("src.Game.Utils.draw_cropped_background", lambda screen, bg: None)
    monkeypatch.setattr("src.Game.Utils.message_to_screen", lambda *args, **kwargs: None)
    monkeypatch.setattr("src.Game.settings.BACKGROUND_IMAGE_PATH", "fake_path")

    called = {}
    monkeypatch.setattr("src.Game.SelectionScreen.SelectionScreen", lambda h, w: called.setdefault("called", True))

    events = [
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, {}),
        pygame.event.Event(pygame.QUIT, {}),
    ]
    monkeypatch.setattr(pygame.event, "get", lambda: events)

    with pytest.raises(SystemExit):
        menuPrincipal(800, 600)

    assert called.get("called", False)


def test_menuPrincipal_configurar(monkeypatch, mock_pygame):
    # Simula clique no botão "Configurar"
    def fake_button(screen, text, size, rect, color1, color2):
        return text == "Configurar"

    monkeypatch.setattr("src.Game.Utils.button", fake_button)
    monkeypatch.setattr("src.Game.Utils.draw_cropped_background", lambda screen, bg: None)
    monkeypatch.setattr("src.Game.Utils.message_to_screen", lambda *args, **kwargs: None)
    monkeypatch.setattr("src.Game.settings.BACKGROUND_IMAGE_PATH", "fake_path")

    # Simula retorno da tela de configuração
    monkeypatch.setattr("src.Game.settingsScreen.settingsScreen", lambda screen: (1024, 768))

    events = [
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, {}),
        pygame.event.Event(pygame.QUIT, {}),
    ]
    monkeypatch.setattr(pygame.event, "get", lambda: events)

    with pytest.raises(SystemExit):
        menuPrincipal(800, 600)


def test_menuPrincipal_sair(monkeypatch, mock_pygame):
    def fake_button(screen, text, size, rect, color1, color2):
        return text == "Sair"

    monkeypatch.setattr("src.Game.Utils.button", fake_button)
    monkeypatch.setattr("src.Game.Utils.draw_cropped_background", lambda screen, bg: None)
    monkeypatch.setattr("src.Game.Utils.message_to_screen", lambda *args, **kwargs: None)
    monkeypatch.setattr("src.Game.settings.BACKGROUND_IMAGE_PATH", "fake_path")

    events = [
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, {}),
        pygame.event.Event(pygame.QUIT, {}),
    ]
    monkeypatch.setattr(pygame.event, "get", lambda: events)

    with pytest.raises(SystemExit):
        menuPrincipal(800, 600)


def test_menuPrincipal_mouse_fora_dos_botoes(monkeypatch, mock_pygame):
    def fake_button(screen, text, size, rect, color1, color2):
        return False  # Nenhum botão clicado

    monkeypatch.setattr("src.Game.Utils.button", fake_button)
    monkeypatch.setattr("src.Game.Utils.draw_cropped_background", lambda screen, bg: None)
    monkeypatch.setattr("src.Game.Utils.message_to_screen", lambda *args, **kwargs: None)
    monkeypatch.setattr("src.Game.settings.BACKGROUND_IMAGE_PATH", "fake_path")

    # Evento QUIT para encerrar após um ciclo
    monkeypatch.setattr(pygame.event, "get", lambda: [pygame.event.Event(pygame.QUIT)])

    with pytest.raises(SystemExit):
        menuPrincipal(800, 600)


def test_menuPrincipal_configura_em_fullscreen(monkeypatch, mock_pygame):
    fullscreen = True

    def fake_button(screen, text, size, rect, color1, color2):
        return text == "Configurar"

    monkeypatch.setattr("src.Game.Utils.button", fake_button)
    monkeypatch.setattr("src.Game.Utils.draw_cropped_background", lambda screen, bg: None)
    monkeypatch.setattr("src.Game.Utils.message_to_screen", lambda *args, **kwargs: None)
    monkeypatch.setattr("src.Game.settings.BACKGROUND_IMAGE_PATH", "fake_path")

    monkeypatch.setattr("src.Game.settingsScreen.settingsScreen", lambda screen: (1024, 768))

    monkeypatch.setattr(pygame.display, "set_mode", lambda size, flag=0: mock_pygame)

    # Evento QUIT para encerrar
    monkeypatch.setattr(pygame.event, "get", lambda: [pygame.event.Event(pygame.QUIT)])

    with pytest.raises(SystemExit):
        menuPrincipal(800, 600)
