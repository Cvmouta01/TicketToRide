import unittest
import os
import sys
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'Game')))

from src.Game.Jogo import Jogo
from src.Game.CartaTrem import CartaTrem
from src.Game.PlayerGraph import PlayerGraph
import networkx as nx

class TestSistema(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo(['Alice', 'Bob'])
        self.jogador = self.jogo.jogador_atual
        self.map_graph = self.jogo.map_graph

    def test_cumprimento_carta_objetivo(self):
        objetivo = self.jogador.cartas_objetivo[0]
        origem = objetivo.origem
        destino = objetivo.destino

        try:
            caminho = nx.shortest_path(self.map_graph.graph, origem, destino)
        except nx.NetworkXNoPath:
            self.skipTest("Não há caminho disponível no mapa entre origem e destino.")

        color = "vermelho"

        for i in range(len(caminho) - 1):
            cidade1 = caminho[i]
            cidade2 = caminho[i + 1]
            edge_data = self.map_graph.graph.get_edge_data(cidade1, cidade2)
            if not edge_data:
                continue
            length = list(edge_data.values())[0]["length"]
            self.jogador.cartas_trem += [CartaTrem(color)] * length
            self.jogo.tentar_conquistar_rota(cidade1, cidade2, color)

        self.assertTrue(self.jogador.verificar_objetivo_cumprido(objetivo))

    def test_fim_de_jogo_por_falta_de_cartas(self):
        self.jogo.baralho_trem = []
        carta = self.jogo.comprar_carta_trem_do_monte()
        self.assertIsNone(carta)
        self.assertEqual(len(self.jogo.baralho_trem), 0)

    def test_passagem_turno(self):
        jogador_atual = self.jogo.jogador_atual
        self.jogo.proximo_turno()
        novo_jogador = self.jogo.jogador_atual
        self.assertNotEqual(jogador_atual, novo_jogador)
        self.assertIn(novo_jogador.nome, ["Alice", "Bob"])

    def test_gerenciamento_cartas_trem(self):
        jogador = self.jogador
        carta = CartaTrem("azul")
        jogador.cartas_trem.append(carta)
        self.assertIn(carta, jogador.cartas_trem)
        jogador.cartas_trem.remove(carta)
        self.assertNotIn(carta, jogador.cartas_trem)

    def test_objetivo_nao_cumprido(self):
        objetivo = self.jogador.cartas_objetivo[0]
        cumprido = self.jogador.verificar_objetivo_cumprido(objetivo)
        self.assertFalse(cumprido)

if __name__ == '__main__':
    unittest.main()
