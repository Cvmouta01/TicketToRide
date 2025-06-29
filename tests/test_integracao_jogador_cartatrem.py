import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'Game')))
from src.Game.Jogador import Jogador
from src.Game.CartaTrem import CartaTrem


def test_jogador_conquista_rota_com_cartas_corretas():
    jogador = Jogador(cor="vermelho")

    # Cria cartas vermelhas e coringas
    cartas = [CartaTrem("vermelho") for _ in range(2)]
    coringas = [CartaTrem("coringa")]

    # Seleciona todas
    for carta in cartas + coringas:
        carta.selecionada = True

    jogador.cartas = cartas + coringas
    rota = {
        "color": "vermelho",
        "length": 3
    }

    conquista = jogador.pode_conquistar(rota)
    assert conquista == "vermelho"

    sucesso = jogador.conquistar_rota(rota, conquista)
    assert sucesso is True
    assert jogador.pontos == 4  # 3 trens = 4 pontos
    assert jogador.trens == 42  # começou com 45
    assert len(jogador.cartas) == 0  # todas usadas

def test_jogador_falha_sem_cartas_suficientes():
    jogador = Jogador(cor="azul")
    jogador.cartas = [CartaTrem("azul")]  # só 1 carta azul
    jogador.cartas[0].selecionada = True

    rota = {
        "color": "azul",
        "length": 2
    }

    conquista = jogador.pode_conquistar(rota)
    assert conquista is None  # não tem cartas suficientes

    sucesso = jogador.conquistar_rota(rota, conquista)
    assert sucesso is False  # falhou
    assert jogador.trens == 45
    assert jogador.pontos == 0
