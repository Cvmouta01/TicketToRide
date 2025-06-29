import os
import sys
import tempfile
import pygame
import pytest

# Adiciona o caminho correto ao sys.path para encontrar os módulos em src/Game
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'Game')))

from src.Game.MapGraph import MapGraph
from src.Game.CartaObjetivo import CartaObjetivo

@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    # Inicializa o pygame antes dos testes
    pygame.init()
    yield
    pygame.quit()

def test_integra_objetivo_e_mapa(tmp_path):

    # Cria arquivos temporários de cidades e rotas
    cities_path = tmp_path / "cities.csv"
    cities_path.write_text("nome,pos_x,pos_y\nCidadeX,10,20\nCidadeY,30,40\n")

    routes_path = tmp_path / "routes.csv"
    routes_path.write_text("cidade_1;cidade_2;cor;comprimento;train_pos\nCidadeX;CidadeY;vermelho;5;{'trem1':[1,2,3,4,5,6,7,8]}\n")

    # Sobrescreve o caminho do BASE_DIR dentro do MapGraph manualmente
    mg = MapGraph()
    assert mg.load_cities_from_file(str(cities_path))
    assert mg.load_routes_from_file(str(routes_path))

    # Simula uma carta objetivo entre as duas cidades
    surface = pygame.Surface((800, 600))  # dummy surface para teste
    carta = CartaObjetivo(origem="CidadeX", destino="CidadeY", pontos=7, imagem_surface=surface)

    # Verifica se as cidades da carta estão presentes no grafo
    assert carta.origem in mg.graph.nodes
    assert carta.destino in mg.graph.nodes

    # Verifica se há pelo menos uma rota entre as cidades
    assert mg.graph.has_edge(carta.origem, carta.destino)
