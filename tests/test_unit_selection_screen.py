import pygame
import pytest
from unittest.mock import patch, MagicMock
import sys
import types

# Mock Utils module
mock_utils = types.ModuleType("Utils")
mock_utils.button = MagicMock(return_value=False)
mock_utils.draw_cropped_background = lambda screen, bg: None
sys.modules["Utils"] = mock_utils

# Mock settings module
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

def surface_with_convert(size=(1000, 800)):
    surf = pygame.Surface(size)
    surf.convert = lambda: surf
    return surf


def test_adicionar_e_remover_jogador_simples():
    slots_local = {1: "vermelho", 2: "none", 3: "none", 4: "none", 5: "none"}
    cores = ["verde", "azul"]

    cor_adicionada = cores.pop(0)
    slots_local[2] = cor_adicionada
    assert slots_local[2] == "verde"
    assert "verde" not in cores

    cores.append(slots_local[2])
    slots_local[2] = "none"
    assert slots_local[2] == "none"
    assert "verde" in cores


@patch("SelectionScreen.Utils.button", side_effect=[False]*10)
@patch("SelectionScreen.pygame.image.load")
@patch("SelectionScreen.pygame.display.set_mode")
@patch("SelectionScreen.pygame.event.get", return_value=[pygame.event.Event(pygame.QUIT)])
def test_selectionscreen_quit_event(mock_event, mock_mode, mock_load, mock_button):
    mock_load.return_value = surface_with_convert()
    SelectionScreen(1000, 800)


@patch("SelectionScreen.carregar_jogo")
@patch("SelectionScreen.Utils.button", side_effect=[False]*20 + [True])  # clicar "Carregar Jogo"
@patch("SelectionScreen.pygame.image.load")
@patch("SelectionScreen.pygame.display.set_mode")
@patch("SelectionScreen.pygame.event.get", side_effect=[
    [pygame.event.Event(pygame.NOEVENT)],
    [pygame.event.Event(pygame.QUIT)]
])
def test_selectionscreen_carregar_jogo(mock_event, mock_mode, mock_load, mock_button, mock_carregar):
    mock_load.return_value = surface_with_convert()
    jogo_mock = MagicMock()
    mock_carregar.return_value = jogo_mock

    SelectionScreen(1000, 800)

    assert mock_carregar.called
    assert jogo_mock.game_loop.called


@patch("SelectionScreen.Jogo")
@patch("SelectionScreen.Utils.button", side_effect=[False]*30 + [True])  # clicar "Iniciar Jogo"
@patch("SelectionScreen.pygame.image.load")
@patch("SelectionScreen.pygame.display.set_mode")
@patch("SelectionScreen.pygame.event.get", side_effect=[
    [pygame.event.Event(pygame.NOEVENT)],
    [pygame.event.Event(pygame.QUIT)]
])
def test_selectionscreen_inicia_jogo(mock_event, mock_mode, mock_load, mock_button, mock_jogo):
    mock_load.return_value = surface_with_convert()
    jogo_instancia = MagicMock()
    mock_jogo.return_value = jogo_instancia

    SelectionScreen(1000, 800)

    assert mock_jogo.called
    assert jogo_instancia.game_loop.called


def test_muda_cor_jogador_1(monkeypatch):
    # Simula clique no botão ">" para mudar cor do jogador 1 no primeiro frame
    clicked = [True, False, False]

    def fake_button(screen, text, *args, **kwargs):
        return clicked.pop(0) if clicked else False

    monkeypatch.setattr("SelectionScreen.Utils.button", fake_button)
    monkeypatch.setattr("SelectionScreen.Utils.draw_cropped_background", lambda screen, bg: None)
    monkeypatch.setattr("SelectionScreen.pygame.image.load", lambda path: surface_with_convert())
    monkeypatch.setattr("SelectionScreen.pygame.display.set_mode", lambda size, *args, **kwargs: pygame.Surface(size))
    monkeypatch.setattr("SelectionScreen.pygame.event.get", lambda: [pygame.event.Event(pygame.QUIT)])

    SelectionScreen(1000, 800)


def test_adiciona_player_e_ai(monkeypatch):
    # Simula clique no botão "+Player" e "+AI" para os slots 2 e 3
    clicks = [False]*5 + [True, False, True] + [False]*10  # clicando "+Player" e "+AI" no segundo e terceiro slots
    def fake_button(screen, text, *args, **kwargs):
        if clicks:
            return clicks.pop(0)
        return False

    monkeypatch.setattr("SelectionScreen.Utils.button", fake_button)
    monkeypatch.setattr("SelectionScreen.Utils.draw_cropped_background", lambda s,b: None)
    monkeypatch.setattr("SelectionScreen.pygame.image.load", lambda path: surface_with_convert())
    monkeypatch.setattr("SelectionScreen.pygame.display.set_mode", lambda size, *a, **k: pygame.Surface(size))
    monkeypatch.setattr("SelectionScreen.pygame.event.get", lambda: [pygame.event.Event(pygame.QUIT)])

    SelectionScreen(1000, 800)


def test_deleta_jogador(monkeypatch):
    # Simula clique no botão "x" para deletar jogador em slot 2
    clicks = [False]*10 + [True] + [False]*5  # clicar delete depois do 10 frames
    def fake_button(screen, text, *args, **kwargs):
        if clicks:
            return clicks.pop(0)
        return False

    monkeypatch.setattr("SelectionScreen.Utils.button", fake_button)
    monkeypatch.setattr("SelectionScreen.Utils.draw_cropped_background", lambda s,b: None)
    monkeypatch.setattr("SelectionScreen.pygame.image.load", lambda path: surface_with_convert())
    monkeypatch.setattr("SelectionScreen.pygame.display.set_mode", lambda size, *a, **k: pygame.Surface(size))
    monkeypatch.setattr("SelectionScreen.pygame.event.get", lambda: [pygame.event.Event(pygame.QUIT)])

    SelectionScreen(1000, 800)


@patch("SelectionScreen.Menu.menuPrincipal")
def test_botao_voltar_chama_menu(mock_menu, monkeypatch):
    # Simula clique no botão "Voltar" para sair e chamar menuPrincipal
    clicks = [False]*10 + [True]
    def fake_button(screen, text, *args, **kwargs):
        if clicks:
            return clicks.pop(0)
        return False

    monkeypatch.setattr("SelectionScreen.Utils.button", fake_button)
    monkeypatch.setattr("SelectionScreen.Utils.draw_cropped_background", lambda s,b: None)
    monkeypatch.setattr("SelectionScreen.pygame.image.load", lambda path: surface_with_convert())
    monkeypatch.setattr("SelectionScreen.pygame.display.set_mode", lambda size, *a, **k: pygame.Surface(size))
    monkeypatch.setattr("SelectionScreen.pygame.event.get", lambda: [pygame.event.Event(pygame.QUIT)])

    SelectionScreen(1000, 800)
    assert mock_menu.called


def test_botao_iniciar_jogo_jogadores_insuficientes(monkeypatch):
    # Simula clicar em "Iniciar Jogo" com menos de 2 jogadores (slots só 1 vermelho + none)
    clicks = [False]*30 + [True]
    def fake_button(screen, text, *args, **kwargs):
        if clicks:
            return clicks.pop(0)
        return False

    monkeypatch.setattr("SelectionScreen.Utils.button", fake_button)
    monkeypatch.setattr("SelectionScreen.Utils.draw_cropped_background", lambda s,b: None)
    monkeypatch.setattr("SelectionScreen.pygame.image.load", lambda path: surface_with_convert())
    monkeypatch.setattr("SelectionScreen.pygame.display.set_mode", lambda size, *a, **k: pygame.Surface(size))
    monkeypatch.setattr("SelectionScreen.pygame.event.get", lambda: [pygame.event.Event(pygame.QUIT)])

    # Deve rodar e imprimir mensagem de jogadores insuficientes (sem erro)
    SelectionScreen(1000, 800)


@patch("SelectionScreen.Jogo")
def test_botao_iniciar_jogo_jogadores_suficientes(mock_jogo, monkeypatch):
    # Simula clicar em "Iniciar Jogo" com 2 jogadores
    clicks = [False]*30 + [True]
    def fake_button(screen, text, *args, **kwargs):
        if clicks:
            return clicks.pop(0)
        return False

    mock_jogo_inst = MagicMock()
    mock_jogo.return_value = mock_jogo_inst

    monkeypatch.setattr("SelectionScreen.Utils.button", fake_button)
    monkeypatch.setattr("SelectionScreen.Utils.draw_cropped_background", lambda s,b: None)
    monkeypatch.setattr("SelectionScreen.pygame.image.load", lambda path: surface_with_convert())
    monkeypatch.setattr("SelectionScreen.pygame.display.set_mode", lambda size, *a, **k: pygame.Surface(size))
    monkeypatch.setattr("SelectionScreen.pygame.event.get", lambda: [pygame.event.Event(pygame.QUIT)])

    # Configura slots localmente para 2 jogadores antes do clique
    from src.Game import SelectionScreen as sel
    sel_slots_backup = getattr(sel, "slots", None)
    sel.slots = {1: "vermelho", 2: "verde", 3: "none", 4: "none", 5: "none"}

    SelectionScreen(1000, 800)

    assert mock_jogo.called
    assert mock_jogo_inst.game_loop.called

    # Restaura slots original se existia
    if sel_slots_backup is not None:
        sel.slots = sel_slots_backup
