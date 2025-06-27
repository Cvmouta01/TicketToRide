import os
import tempfile
import pytest
from unittest.mock import MagicMock

from src.Game.MapGraph import MapGraph  # Ajuste para o caminho real do seu módulo


@pytest.fixture
def temp_cities_file():
    content = "nome,pos_x,pos_y\n" \
              "CidadeA,10,20\n" \
              "CidadeB,30,40\n"
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def temp_routes_file():
    content = "cidade_1;cidade_2;cor;comprimento;train_pos\n" \
              "CidadeA;CidadeB;vermelho;5;{'trem1':[1,2,3,4,5,6,7,8]}\n"
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)


def test_load_cities(temp_cities_file):
    mg = MapGraph()
    result = mg.load_cities_from_file(temp_cities_file)
    assert result is True
    assert "CidadeA" in mg.graph.nodes
    assert "CidadeB" in mg.graph.nodes
    pos_a = mg.graph.nodes["CidadeA"]["pos"]
    assert pos_a == (10.0, 20.0)


def test_load_routes(temp_cities_file, temp_routes_file):
    mg = MapGraph()
    # Carrega cidades primeiro para garantir que rotas possam ser adicionadas
    mg.load_cities_from_file(temp_cities_file)

    result = mg.load_routes_from_file(temp_routes_file)
    assert result is True

    # Verifica se a rota foi adicionada
    assert mg.graph.has_edge("CidadeA", "CidadeB")
    edge_data = mg.graph.get_edge_data("CidadeA", "CidadeB")
    # Pode ter múltiplas arestas, pega a primeira
    first_key = list(edge_data.keys())[0]
    data = edge_data[first_key]
    assert data['color'] == "vermelho"
    assert data['length'] == 5
    assert data['train_pos'] == "{'trem1':[1,2,3,4,5,6,7,8]}"


def test_add_route_and_set_route_owned(temp_cities_file):
    mg = MapGraph()
    mg.load_cities_from_file(temp_cities_file)

    # Adiciona uma rota válida
    success = mg.add_route("CidadeA", "CidadeB", "azul", 3, "{'trem1':[0,0,0,0,0,0,0,0]}")
    assert success is True
    assert mg.graph.has_edge("CidadeA", "CidadeB")

    # Marca a rota como propriedade
    # Como pode haver múltiplas arestas, pega a chave da primeira aresta
    key = list(mg.graph.get_edge_data("CidadeA", "CidadeB").keys())[0]
    owned_success = mg.set_route_owned("CidadeA", "CidadeB", key)
    assert owned_success is True
    assert mg.graph["CidadeA"]["CidadeB"][key]["owned"] is True


def test_translate_color():
    assert MapGraph.translate_color("vermelho") == "red"
    assert MapGraph.translate_color("AZUL") == "blue"  # Testa case insensitive
    assert MapGraph.translate_color("desconhecida") == "desconhecida"


def test_update_arestas_and_vertices(monkeypatch):
    mg = MapGraph()
    mg.graph.add_node("CidadeA", pos=(10, 20))
    mg.graph.add_node("CidadeB", pos=(30, 40))

    mg.graph.add_edge("CidadeA", "CidadeB", color="vermelho", length=5, train_pos="{'trem1':[0,0,0,0,0,0,0,0]}", owned=False)

    # Mock do objeto mapa com método ajustar_ponto que retorna coordenadas alteradas
    class MockMapa:
        def ajustar_ponto(self, surface, pontos):
            # Apenas soma 1 a cada coordenada para teste
            return [(x+1, y+1) for (x,y) in pontos]

    mock_mapa = MockMapa()
    mock_surface = MagicMock()

    mg.update_arestas(mock_surface, mock_mapa)

    # Verifica se train_pos foi atualizado (com valores aumentados em 1)
    edge_data = mg.graph.get_edge_data("CidadeA", "CidadeB")
    key = list(edge_data.keys())[0]
    train_pos = edge_data[key]['train_pos']
    for coords in train_pos.values():
        for c in coords:
            assert c > 0  # Agora maior que zero pois somou 1


    mg.update_vertices(mock_surface, mock_mapa)
    pos_novo = mg.graph.nodes["CidadeA"]["pos"]
    assert pos_novo == (11, 21)  # Original (10,20) + 1

