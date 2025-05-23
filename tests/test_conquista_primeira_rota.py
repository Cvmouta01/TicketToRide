import pytest
from src.Game.Jogador import Jogador
from collections import namedtuple
import sys
    
def test_primeira_rota_conquista(capsys):
    Rota = namedtuple('Rota', ['color', 'length', 'points'])
    rota = Rota(color='vermelho', length=3, points=3)

    jogador = Jogador('vermelho')
    Card = namedtuple('Card', ['cor'])
    jogador.cartas = [Card(cor='vermelho') for _ in range(3)]

    assert jogador.pode_conquistar(rota) is True
    jogador.conquistar_rota(rota)


    # Feedback
    print(f"Rota conquistada: {rota}")
    print(f"Pontuação do jogador: {jogador.pontos}")
    out = capsys.readouterr().out
    sys.__stdout__.write(out)
    assert "Rota conquistada" in out
    assert str(jogador.pontos) in out