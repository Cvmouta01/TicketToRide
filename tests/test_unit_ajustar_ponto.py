import sys
import types
import pytest
import pygame
from unittest.mock import patch, MagicMock

# Mock para Utils
mock_utils = types.ModuleType("Utils")
mock_utils.resize_com_escala = lambda img, w, h, sx, sy: img
mock_utils.dentro_poligono = lambda pos, poly: True
mock_utils.message_to_screen = lambda *args, **kwargs: {"text": pygame.Surface((10,10)), "text_rect": (0,0,10,10)}

sys.modules["Utils"] = mock_utils

# Mock para settings
mock_settings = types.ModuleType("settings")
mock_settings.cores = {
    "vermelho": (255, 0, 0),
    "azul": (0, 0, 255),
    "amarelo": (255, 255, 0),
}

sys.modules["settings"] = mock_settings

from src.Game.Mapa import Mapa

@pytest.fixture(scope="module", autouse=True)
def pygame_init_and_quit():
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def surface_mock():
    surf = pygame.Surface((1000, 800))
    return surf

def test_init_loads_images_and_resizes(surface_mock):
    with patch('pygame.image.load', return_value=pygame.Surface((500, 400))) as mock_load:
        mapa = Mapa(surface_mock)

        assert mock_load.call_count > 0
        assert isinstance(mapa.img_cartas_trem_horizontal, dict)
        assert isinstance(mapa.img_cartas_trem_vertical, dict)
        assert len(mapa.img_cartas_trem_horizontal) == len(mapa.img_cartas_trem_vertical)

def test_ajustar_ponto(surface_mock):
    mapa = Mapa(surface_mock)
    mapa.original_width = 500
    mapa.original_height = 400
    mapa.new_width = 800
    mapa.new_height = 600

    ponto = [(250, 200)]
    resultado = mapa.ajustar_ponto(surface_mock, ponto)

    expected_x = 250 * (800 / 500) + (surface_mock.get_width() // 2 - 800 // 2)
    expected_y = 200 * (600 / 400)

    assert resultado[0][0] == expected_x
    assert resultado[0][1] == expected_y

def test_atualizar_trens_adiciona_trilhos(surface_mock):
    mapa = Mapa(surface_mock)

    trilhos = {
        1: [ (1,2), (2,3), (3,4), (4,5) ],
        2: [ (5,6), (6,7), (7,8), (8,9) ]
    }
    cor = "vermelho"

    mapa.atualizar_trens(trilhos, cor)

    assert len(mapa.trilhos_conquistados) == 2
    # Cada elemento da lista tem a cor adicionada no final
    for track in mapa.trilhos_conquistados:
        assert track[-1] == cor

@patch('src.Game.Mapa.dentro_poligono', return_value=True)
def test_desenhar_mao_jogador_marks_rect_and_changes_selection(mock_dentro_poligono, surface_mock):
    mapa = Mapa(surface_mock)

    class Carta:
        def __init__(self, cor):
            self.cor = cor
            self.selecionada = False
            self.rect = None

    cartas = [Carta("vermelho") for _ in range(3)]

    mouse_info = [(10, 10), True]  # posição e botão clicado

    with patch.object(surface_mock, 'blit') as mock_blit, \
         patch('pygame.transform.smoothscale', side_effect=lambda img, size: img), \
         patch('pygame.transform.rotate', side_effect=lambda img, angle: img):

        mapa.desenhar_mao_jogador(surface_mock, cartas, mouse_info)

        # Verifica que o rect foi definido para as cartas
        for carta in cartas:
            assert carta.rect is not None

        # Como mouse clicado e dentro poligono retorna True, seleção deve ter mudado
        assert all(carta.selecionada for carta in cartas)

@patch('src.Game.Mapa.message_to_screen', return_value={"text": pygame.Surface((10,10)), "text_rect": (0,0,10,10)})
def test_criar_card_jogador_calls_draw_and_blit(mock_message_to_screen, surface_mock):
    mapa = Mapa(surface_mock)

    jogador_mock = MagicMock()
    jogador_mock.cor = "vermelho"
    jogador_mock.pontos = 5
    jogador_mock.trens = 10
    jogador_mock.ativo = True

    with patch('pygame.draw.rect') as mock_draw_rect, \
         patch.object(surface_mock, 'blit') as mock_blit:

        rect = (10, 10, 100, 50)
        mapa.criar_card_jogador(surface_mock, jogador_mock, rect)

        # Deve chamar draw.rect pelo menos uma vez
        assert mock_draw_rect.call_count >= 1
        # Deve chamar blit para desenhar avatar, pontos, trens e texto
        assert mock_blit.call_count >= 1

@patch('src.Game.Mapa.dentro_poligono', return_value=False)
@patch('src.Game.Mapa.message_to_screen', return_value={"text": pygame.Surface((10,10)), "text_rect": (0,0,10,10)})
def test_draw_calls_methods_and_blits(mock_message_to_screen, mock_dentro_poligono, surface_mock):
    mapa = Mapa(surface_mock)

    # Criar mock de jogador
    jogador_mock = MagicMock()
    jogador_mock.ativo = True
    jogador_mock.cartas = []
    jogador_mock.objetivos = []

    # Criar lista de jogadores
    jogadores = [jogador_mock]

    cartas_trem_abertas = []
    mouse_info = [(0,0), False]

    grafo_mock = MagicMock()
    grafo_mock.graph.nodes = {}

    with patch.object(mapa, 'desenhar_cartas_laterais') as mock_des_cartas_laterais, \
         patch.object(mapa, 'desenhar_mao_jogador') as mock_des_mao_jogador, \
         patch.object(mapa, 'criar_card_jogador') as mock_criar_card_jogador, \
         patch.object(surface_mock, 'blit') as mock_blit, \
         patch('pygame.draw.polygon') as mock_draw_poly:

        mapa.draw(surface_mock, jogadores, cartas_trem_abertas, mouse_info, grafo_mock)

        mock_des_cartas_laterais.assert_called_once()
        mock_des_mao_jogador.assert_called_once()
        mock_criar_card_jogador.assert_called_once()
        mock_blit.assert_called()
        mock_draw_poly.assert_called()

