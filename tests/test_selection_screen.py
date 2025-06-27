import pygame
import pytest
from unittest.mock import patch, MagicMock
import sys
import types

# Mock Utils
mock_utils = types.ModuleType("Utils")
mock_utils.button = MagicMock(return_value=False)
mock_utils.draw_cropped_background = lambda screen, bg: None
sys.modules["Utils"] = mock_utils

# Mock settings
mock_settings = types.ModuleType("settings")
mock_settings.WINDOW_TITLE = "Ticket to Ride"
mock_settings.BACKGROUND_IMAGE_PATH = "dummy/path.jpg"
mock_settings.BUTTON_COLOR = (0, 0, 0)
mock_settings.BUTTON_ACTIVE_COLOR = (255, 255, 255)
mock_settings.cores = {
    "vermelho": (255, 0, 0),
    "verde": (0, 255, 0),
    "azul": (0, 0, 255),
    "cinza": (100, 100, 100),
    "roxo": (128, 0, 128),
    "rosa": (255, 105, 180)
}
sys.modules["settings"] = mock_settings

from src.Game.SelectionScreen import SelectionScreen

@pytest.fixture(scope="module", autouse=True)
def pygame_setup_teardown():
    pygame.init()
    yield
    pygame.quit()


def test_adicionar_e_remover_jogador_simples():
    from src.Game.SelectionScreen import slots
    slots_local = {1: "vermelho", 2: "none", 3: "none", 4: "none", 5: "none"}
    cores = ["verde", "azul"]

    # Simula adicionar jogador
    cor_adicionada = cores.pop(0)
    slots_local[2] = cor_adicionada
    assert slots_local[2] == "verde"
    assert "verde" not in cores

    # Simula remover jogador
    cores.append(slots_local[2])
    slots_local[2] = "none"
    assert slots_local[2] == "none"
    assert "verde" in cores

@patch("SelectionScreen.Utils.button", side_effect=[False]*10)
@patch("SelectionScreen.pygame.image.load", return_value=pygame.Surface((1000, 800)))
@patch("SelectionScreen.pygame.display.set_mode")
@patch("SelectionScreen.pygame.event.get", return_value=[pygame.event.Event(pygame.QUIT)])
def test_selectionscreen_quit_event(mock_event, mock_mode, mock_load, mock_button):
    SelectionScreen(1000, 800)
    # Espera-se que apenas saia sem erro


@patch("SelectionScreen.carregar_jogo")
@patch("SelectionScreen.Utils.button", side_effect=[False]*20 + [True])  # simula clique no botão "Carregar Jogo"
@patch("SelectionScreen.pygame.image.load", return_value=pygame.Surface((1000, 800)))
@patch("SelectionScreen.pygame.display.set_mode")
@patch("SelectionScreen.pygame.event.get", side_effect=[  
    [pygame.event.Event(pygame.NOEVENT)],
    [pygame.event.Event(pygame.QUIT)]
])
def test_selectionscreen_carregar_jogo(mock_event, mock_mode, mock_load, mock_button, mock_carregar):
    jogo_mock = MagicMock()
    mock_carregar.return_value = jogo_mock

    SelectionScreen(1000, 800)

    assert mock_carregar.called
    assert jogo_mock.game_loop.called


@patch("SelectionScreen.Jogo")
@patch("SelectionScreen.Utils.button", side_effect=[False]*30 + [True])  # botão "Iniciar Jogo"
@patch("SelectionScreen.pygame.image.load", return_value=pygame.Surface((1000, 800)))
@patch("SelectionScreen.pygame.display.set_mode")
@patch("SelectionScreen.pygame.event.get", side_effect=[
    [pygame.event.Event(pygame.NOEVENT)],
    [pygame.event.Event(pygame.QUIT)]
])
def test_selectionscreen_inicia_jogo(mock_event, mock_mode, mock_load, mock_button, mock_jogo):
    jogo_instancia = MagicMock()
    mock_jogo.return_value = jogo_instancia

    SelectionScreen(1000, 800)

    assert mock_jogo.called
    assert jogo_instancia.game_loop.called
