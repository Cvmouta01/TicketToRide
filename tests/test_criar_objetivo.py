import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'Game')))
import pytest
import pygame
import src.Game.CartaObjetivo as co_module
from src.Game.CartaObjetivo import CartaObjetivo

# Dummy Surface para substituir o carregamento real
class DummySurface:
    def convert_alpha(self):
        return self

@pytest.fixture(autouse=True)
def dummy_pygame(monkeypatch):
    # faz pygame.image.load(...) retornar uma DummySurface com convert_alpha()
    monkeypatch.setattr(pygame.image, 'load', lambda path: DummySurface())

def test_criar_baralho_objetivo(tmp_path, monkeypatch):
    fake_mod = tmp_path / "CartaObjetivo.py"
    fake_mod.write_text("# módulo fake")
    monkeypatch.setattr(co_module, "__file__", str(fake_mod))

    cards_dir = tmp_path / "src" / "Game" / "Images" / "Objetivos"
    cards_dir.mkdir(parents=True)

    nomes = [
        "CityA_CityB_5.png",   # válido
        "Foo_Bar_10.png",      # válido
        "badname.png",         # inválido
        "X_Y_Z_W.png",         # inválido
        "ignore.txt"           # inválido
    ]
    for n in nomes:
        (cards_dir / n).write_bytes(b"")

    # 4) Executa o método
    baralho = CartaObjetivo.criar_baralho_objetivo()

    # 5) Verifica resultados
    assert len(baralho) == 2
    esperado = {("CityA", "CityB", 5), ("Foo", "Bar", 10)}
    atual = {(c.origem, c.destino, c.pontos) for c in baralho}
    assert atual == esperado

    for carta in baralho:
        assert isinstance(carta.imagem, DummySurface)