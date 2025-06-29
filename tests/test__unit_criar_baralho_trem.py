import pytest
from src.Game.CartaTrem import CartaTrem

def test_construtor_carta_trem():
    cor = 'vermelho'
    carta = CartaTrem(cor)
    assert carta.cor == cor
    assert carta.selecionada is False
    assert carta.rect is None

def test_criar_baralho_trem():
    baralho = CartaTrem.criar_baralho_trem()

    # Total esperado
    assert len(baralho) == 110

    # Verifica tipos
    assert all(isinstance(carta, CartaTrem) for carta in baralho)

    # Verifica cores e quantidades
    from collections import Counter
    cores_contadas = Counter(carta.cor for carta in baralho)

    assert cores_contadas['coringa'] == 14
    for cor in ['vermelho', 'azul', 'verde', 'amarelo', 'preto', 'branco', 'laranja', 'rosa']:
        assert cores_contadas[cor] == 12
