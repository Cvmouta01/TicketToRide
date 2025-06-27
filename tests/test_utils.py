import pygame
import pytest
from unittest.mock import MagicMock
import src.Game.Utils as utils


@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


def test_message_to_screen_returning(monkeypatch):
    surface = MagicMock()

    # Testa retorno com returning=True
    resultado = utils.message_to_screen(surface, "Teste", 20, 100, 50, (255, 0, 0), returning=True)
    assert isinstance(resultado, dict)
    assert "text" in resultado and "text_rect" in resultado


def test_message_to_screen_blit(monkeypatch):
    surface = MagicMock()

    # Mock da classe pygame.font.Font para retornar um objeto com método render válido
    class MockFont:
        def render(self, text, aa, color, bckg=None):
            return pygame.Surface((10, 10))

    monkeypatch.setattr(pygame.font, "Font", lambda *args, **kwargs: MockFont())

    # Chama a função (returning=False) para verificar se surface.blit foi chamado
    utils.message_to_screen(surface, "Olá", 20, 100, 50, (255, 255, 255), returning=False)

    surface.blit.assert_called_once()


def test_button(monkeypatch):
    surface = MagicMock()
    rect = pygame.Rect(0, 0, 100, 50)

    # Mock do mouse: dentro do botão e mouse clicado
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (10, 10))
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda: (1, 0, 0))

    clicked = utils.button(surface, "Click", 20, rect, (255, 255, 255), (0, 255, 0))
    assert clicked is True

    # Mock mouse fora do botão
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (200, 200))
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda: (0, 0, 0))

    clicked = utils.button(surface, "Click", 20, rect, (255, 255, 255), (0, 255, 0))
    assert clicked is False


def test_draw_cropped_background(monkeypatch):
    screen = MagicMock()
    background = MagicMock()

    screen.get_size.return_value = (800, 600)
    background.get_size.return_value = (1000, 1000)

    cropped_mock = MagicMock()
    # Mock subsurface para retornar objeto mockado
    background.subsurface = MagicMock(return_value=cropped_mock)

    utils.draw_cropped_background(screen, background)

    # Verifica se subsurface foi chamado com o retângulo correto
    background.subsurface.assert_called_once()
    screen.blit.assert_called_once_with(cropped_mock, (0, 0))


def test_check_f11(monkeypatch):
    screen = pygame.display.set_mode((640, 480))
    fullscreen = False
    window_size = (640, 480)

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F11)

    fullscreen, new_screen = utils.check_f11(event, fullscreen, window_size, screen)
    assert fullscreen is True
    assert isinstance(new_screen, pygame.Surface)

    # Chamar de novo para voltar ao modo janela
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F11)
    fullscreen, new_screen = utils.check_f11(event, fullscreen, window_size, new_screen)
    assert fullscreen is False


def test_resize_com_escala():
    pygame.init()
    img = pygame.Surface((100, 50))
    tela_w, tela_h = 800, 600

    # Escala para 50% em x e y
    proporcao_x, proporcao_y = 0.5, 0.5
    resized = utils.resize_com_escala(img, tela_w, tela_h, proporcao_x, proporcao_y)
    assert isinstance(resized, pygame.Surface)

    # A largura e altura devem ser proporcionais e >= (tela_w * proporcao_x, tela_h * proporcao_y)
    w, h = resized.get_size()
    assert w >= tela_w * proporcao_x
    assert h >= tela_h * proporcao_y


def test_dentro_poligono():
    polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]

    # Ponto dentro
    assert utils.dentro_poligono((5, 5), polygon) is True
    # Ponto fora
    assert utils.dentro_poligono((15, 5), polygon) is False
    # Ponto na borda (considerado dentro)
    assert utils.dentro_poligono((0, 0), polygon) is True
    # Ponto fora acima
    assert utils.dentro_poligono((5, -1), polygon) is False
