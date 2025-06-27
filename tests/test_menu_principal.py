import pytest
import pygame
from src.Game.Menu import menuPrincipal 

@pytest.fixture
def mock_pygame(monkeypatch):
    # Mockar pygame.display.set_mode para retornar um objeto com get_width e get_height
    class DummyScreen:
        def get_width(self): return 800
        def get_height(self): return 600
        def get_size(self): return (800, 600)
        def fill(self, color): pass
        def blit(self, *args): pass
    
    monkeypatch.setattr(pygame.display, "set_mode", lambda size, *args, **kwargs: DummyScreen())
    monkeypatch.setattr(pygame.display, "set_caption", lambda title: None)
    monkeypatch.setattr(pygame.display, "update", lambda: None)
    
    # Mock mouse.get_pressed para simular mouse sendo clicado e solto
    pressed = [0, 0, 0]
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda: pressed)

    # Mock mouse.get_pos para simular posição do mouse
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (300, 160))  

    events = [
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, {}),
        pygame.event.Event(pygame.QUIT, {}),
    ]
    def event_generator():
        for e in events:
            yield e
        while True:
            yield pygame.event.Event(pygame.NOEVENT, {})

    gen = event_generator()
    monkeypatch.setattr(pygame.event, "get", lambda: [next(gen)])

    return pressed

def test_menuPrincipal_jogar_called(monkeypatch, mock_pygame):
    # Mock Utils.button para só retornar True se texto == "Jogar"
    def fake_button(screen, text, size, rect, color1, color2):
        return text == "Jogar"

    monkeypatch.setattr("Utils.button", fake_button)
    monkeypatch.setattr("Utils.draw_cropped_background", lambda screen, bg: None)
    monkeypatch.setattr("Utils.message_to_screen", lambda *args, **kwargs: None)

    # Mock SelectionScreen para marcar que foi chamada
    called = {}
    def fake_SelectionScreen(h, w):
        called["called"] = True
    monkeypatch.setattr("SelectionScreen.SelectionScreen", fake_SelectionScreen)

    # Executa menuPrincipal (deve chamar fake_SelectionScreen e depois sair no QUIT)
    with pytest.raises(SystemExit):
        menuPrincipal(800, 600)
        
    assert called.get("called", False) == True
