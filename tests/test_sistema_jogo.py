import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'Game')))

from src.Game.Jogo import Jogo
from src.Game.Jogador import Jogador
from src.Game.CartaTrem import CartaTrem
from src.Game.MapGraph import MapGraph
from src.Game.PlayerGraph import PlayerGraph

class TestSistemaJogo(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo(["Alice", "Bob"], modo_debug=True)
        self.jogador = self.jogo.jogador_atual
        self.map_graph = self.jogo.mapa.grafo
        self.player_graph = self.jogador.grafo_jogador

    def test_fluxo_simples_de_jogo(self):
        # Verifica que o jogo começou com 2 jogadores
        self.assertEqual(len(self.jogo.jogadores), 2)

        # Compra uma carta de trem
        carta_comprada = self.jogo.comprar_carta_trem_do_monte()
        self.assertIsInstance(carta_comprada, CartaTrem)
        self.assertIn(carta_comprada, self.jogador.cartas_trem)

        # Marca uma rota como adquirida
        rotas = list(self.map_graph.graph.edges(data=True))
        if rotas:
            city1, city2, data = rotas[0]
            length = data['length']
            
            # Dá cartas suficientes para simular conquista
            self.jogador.cartas_trem += [CartaTrem(data['color'])] * length

            sucesso = self.jogo.tentar_conquistar_rota(city1, city2, data['color'])
            self.assertTrue(sucesso, f"Não foi possível conquistar a rota {city1} - {city2}")

            # Verifica se a rota foi adicionada ao grafo do jogador
            self.assertTrue(self.player_graph.grafo.has_edge(city1, city2))

        else:
            self.skipTest("Sem rotas disponíveis para testar")

        # Verifica se ainda há jogadores ativos
        self.assertTrue(any(j.esta_ativo for j in self.jogo.jogadores))

if __name__ == '__main__':
    unittest.main()
