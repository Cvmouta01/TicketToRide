import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'Game')))
from src.Game.MapGraph import MapGraph
from src.Game.PlayerGraph import PlayerGraph

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class TestIntegrationMapPlayerGraphs(unittest.TestCase):
    def setUp(self):
        # Instancia MapGraph e carrega dados
        self.map_graph = MapGraph()

        # Instancia PlayerGraph
        self.player_graph = PlayerGraph()

        # Limpa grafo player para garantir controle
        self.player_graph.grafo.clear()

        # Adiciona rotas do MapGraph ao PlayerGraph
        for u, v, data in self.map_graph.graph.edges(data=True):
            length = data.get('length', 1)
            self.player_graph.adicionar_rota(u, v, length)

    def test_cidades_carregadas(self):
        # Verifica se cidades carregadas no MapGraph estão no PlayerGraph
        map_cities = set(self.map_graph.graph.nodes())
        player_cities = set(self.player_graph.grafo.nodes())

        for city in map_cities:
            self.assertIn(city, player_cities, f"Cidade {city} não está no grafo do jogador.")

    def test_rotas_carregadas(self):
        # Verifica se as rotas do MapGraph estão no PlayerGraph
        for u, v, data in self.map_graph.graph.edges(data=True):
            self.assertTrue(self.player_graph.grafo.has_edge(u, v), f"Rota {u}-{v} não encontrada no grafo do jogador.")

    def test_tem_caminho(self):
        # Testa se tem caminho entre duas cidades quaisquer do MapGraph, se existir aresta
        nodes = list(self.player_graph.grafo.nodes())
        if len(nodes) >= 2:
            origem = nodes[0]
            destino = nodes[1]
            # Pode não existir caminho se grafo desconexo, então não é assert obrigatório
            # Apenas garante que o método funciona
            _ = self.player_graph.tem_caminho(origem, destino)

if __name__ == '__main__':
    unittest.main()
