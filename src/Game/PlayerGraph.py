import networkx as nx
import pandas as pd
import os

class PlayerGraph:
    def __init__(self):
        # obter o caminho correto para o arquivo cities.csv
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        cities_path = os.path.join(BASE_DIR, 'cities.csv')
        self.grafo = self.criar_grafo_cidades(cities_path)

    def criar_grafo_cidades(self, arquivo_csv):
        
        df = pd.read_csv(arquivo_csv)
        
        # cria grafo vazio
        G = nx.Graph()
        
        # adicionar cada cidade como um vértice
        for _, row in df.iterrows():
            cidade = row['city']
            G.add_node(cidade)
        
        return G

    def adicionar_rota(self, cidade1, cidade2, length):
        self.grafo.add_edge(cidade1, cidade2, length=length)
