import os
import pygame
import pytest
from unittest.mock import MagicMock, patch
from src.Game.Jogo import Jogo

os.environ["SDL_VIDEODRIVER"] = "dummy"

pygame.init()
pygame.display.set_mode((1, 1))


def criar_baralho_trem_mock(*args, **kwargs):
    return [MagicMock(cor="vermelho", rect=None) for _ in range(50)]


def criar_baralho_objetivo_mock(*args, **kwargs):
    mock_carta = MagicMock()
    mock_carta.imagem = pygame.Surface((10, 10))
    return [mock_carta for _ in range(30)]


@pytest.fixture
@patch("src.Game.Jogo.CartaTrem.criar_baralho_trem", side_effect=criar_baralho_trem_mock)
@patch("src.Game.Jogo.CartaObjetivo.criar_baralho_objetivo", side_effect=criar_baralho_objetivo_mock)
def jogo_com_3_jogadores(mock_obj, mock_trem):
    return Jogo(["vermelho", "azul", "verde"], 800, 600)


def test_jogo_inicializa_com_dados_corretos(jogo_com_3_jogadores):
    jogo = jogo_com_3_jogadores
    assert len(jogo.jogadores) == 3
    assert len(jogo.cartas_trem_abertas) == 5
    assert jogo.jogadores[0].ativo is True
    assert all(len(j.cartas) == 4 for j in jogo.jogadores)
    assert all(len(j.objetivos) == 3 for j in jogo.jogadores)


def test_passar_turno_avanca_ciclo(jogo_com_3_jogadores):
    jogo = jogo_com_3_jogadores

    ordem = []
    for _ in range(6):
        ativo = [j.ativo for j in jogo.jogadores]
        ordem.append(ativo)
        jogo.passar_turno()

    ativos_por_turno = [i.index(True) for i in ordem]
    assert ativos_por_turno == [0, 1, 2, 0, 1, 2]


def test_verif_fim_de_jogo_dispara_quando_menos_de_tres_trens(jogo_com_3_jogadores):
    jogo = jogo_com_3_jogadores
    jogador = jogo.jogadores[jogo.jogador_atual_index]
    jogador.trens = 2

    mock_display = MagicMock()
    jogo.verif_fim_de_jogo(mock_display)

    assert jogo.finalizando_jogo is True
    assert jogo.jogador_fim == jogo.jogador_atual_index


def test_calcular_vencedor_ordena_por_pontos(jogo_com_3_jogadores):
    jogo = jogo_com_3_jogadores
    jogo.jogadores[0].pontos = 50
    jogo.jogadores[1].pontos = 30
    jogo.jogadores[2].pontos = 70

    ranking = jogo.calcular_vencedor()

    pontos_ordenados = list(ranking.values())
    assert pontos_ordenados == sorted(pontos_ordenados, reverse=True)


@patch("src.Game.Jogo.CartaTrem.criar_baralho_trem", side_effect=criar_baralho_trem_mock)
@patch("src.Game.Jogo.CartaObjetivo.criar_baralho_objetivo", side_effect=criar_baralho_objetivo_mock)
def test_jogo_estado_inicial(mock_obj, mock_trem):
    jogo = Jogo(["vermelho"], 800, 600)
    assert jogo.jogadores[0].ativo
    assert jogo.cartas_compradas_esse_turno == 0
    assert jogo.cartas_abertas_compradas_nesse_turno == 0
    assert len(jogo.baralho_trem) >= 0
    assert len(jogo.baralho_objetivo) >= 0
