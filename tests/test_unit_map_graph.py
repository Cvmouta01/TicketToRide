import os
import tempfile
import pytest
from unittest.mock import MagicMock, patch

from src.Game.MapGraph import MapGraph 


@pytest.fixture
def temp_valid_cities_file():
    content = "nome,pos_x,pos_y\n" \
              "CidadeA,10,20\n" \
              "CidadeB,30,40\n"
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def temp_invalid_cities_file():
    content = "nome,pos_x,pos_y\n" \
              "CidadeA,dez,20\n" \
              "CidadeB,30\n" \
              "\n" \
              "CidadeC,40,50\n"
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def temp_valid_routes_file():
    content = "cidade_1;cidade_2;cor;comprimento;train_pos\n" \
              "CidadeA;CidadeB;vermelho;5;{'trem1':[1,2,3,4,5,6,7,8]}\n"
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def temp_invalid_routes_file():
    content = "cidade_1;cidade_2;cor;comprimento;train_pos\n" \
              "CidadeA;CidadeB;vermelho;cinco;{'trem1':[1,2,3,4,5,6,7,8]}\n" \
              "CidadeA;CidadeC\n" \
              "\n"
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)


def test_load_cities_with_invalid_lines(temp_invalid_cities_file):
    mg = MapGraph()
    result = mg.load_cities_from_file(temp_invalid_cities_file)
    assert result is True  # Ainda deve retornar True pois falhas são ignoradas individualmente
    assert "CidadeC" in mg.graph.nodes
    assert "CidadeA" not in mg.graph.nodes or mg.graph.nodes["CidadeA"]["pos_raw"][0] != "dez"  # Conversão falhou
    assert "CidadeB" not in mg.graph.nodes  # Linha inválida


def test_load_routes_with_invalid_lines(temp_valid_cities_file, temp_invalid_routes_file):
    mg = MapGraph()
    mg.load_cities_from_file(temp_valid_cities_file)
    result = mg.load_routes_from_file(temp_invalid_routes_file)
    assert result is True
    # Rota inválida não deve ser adicionada
    assert not mg.graph.has_edge("CidadeA", "CidadeC")
    # A rota com comprimento inválido não deve ser adicionada
    assert not mg.graph.has_edge("CidadeA", "CidadeB")


def test_add_route_with_nonexistent_cities(temp_valid_cities_file):
    mg = MapGraph()
    mg.load_cities_from_file(temp_valid_cities_file)

    # Cidade inexistente
    success = mg.add_route("CidadeA", "CidadeX", "azul", 4, "{}")
    assert success is False

    success = mg.add_route("CidadeX", "CidadeB", "azul", 4, "{}")
    assert success is False


def test_set_route_owned_errors(temp_valid_cities_file):
    mg = MapGraph()
    mg.load_cities_from_file(temp_valid_cities_file)
    # Nenhuma rota ainda adicionada
    success = mg.set_route_owned("CidadeA", "CidadeB", 0)
    assert success is False

    # Adiciona uma rota
    mg.add_route("CidadeA", "CidadeB", "vermelho", 5, "{}")

    # Usa uma chave inválida
    success = mg.set_route_owned("CidadeA", "CidadeB", 99)
    assert success is False


def test_translate_color_defaults():
    # Cor não mapeada retorna igual
    assert MapGraph.translate_color("inexistente") == "inexistente"
    # Maiúsculas/minúsculas
    assert MapGraph.translate_color("VERMELHO") == "red"
    assert MapGraph.translate_color("AzUl") == "blue"


def test_update_arestas_skips_invalid_train_pos():
    mg = MapGraph()
    mg.graph.add_node("A", pos_raw=(0, 0))
    mg.graph.add_node("B", pos_raw=(1, 1))

    # train_pos_raw não string
    mg.graph.add_edge("A", "B", color="azul", length=3, train_pos_raw=None)

    class DummyMapa:
        def ajustar_ponto(self, surface, pontos):
            return pontos

    mg.update_arestas(None, DummyMapa())  


def test_update_vertices_updates_positions():
    mg = MapGraph()
    mg.graph.add_node("A", pos_raw=(1, 2))
    mg.graph.add_node("B", pos_raw=(3, 4))

    class DummyMapa:
        def ajustar_ponto(self, surface, pontos):
            return [(x+10, y+10) for (x, y) in pontos]

    mg.update_vertices(None, DummyMapa())
    assert mg.graph.nodes["A"]["pos"] == (11, 12)
    assert mg.graph.nodes["B"]["pos"] == (13, 14)


@patch("matplotlib.pyplot.show")
def test_visualize_runs_without_error(mock_show, temp_valid_cities_file, temp_valid_routes_file):
    mg = MapGraph()
    mg.load_cities_from_file(temp_valid_cities_file)
    mg.load_routes_from_file(temp_valid_routes_file)

    for node in mg.graph.nodes:
        mg.graph.nodes[node]['pos'] = (10, 10)

    mg.visualize()


if __name__ == "__main__":
    pytest.main()
