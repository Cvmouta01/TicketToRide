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

    def _encontrar_caminho_mais_longo_dfs(self, inicio, fim, arestas_usadas, caminho_atual, peso_atual):
        """
        Função auxiliar que usa DFS para encontrar o caminho mais longo entre dois vértices.
        Permite repetir vértices, mas não arestas.
        
        Args:
            inicio: Vértice de início
            fim: Vértice de destino
            arestas_usadas: Set de arestas já usadas no caminho atual
            caminho_atual: Lista com o caminho atual
            peso_atual: Peso acumulado do caminho atual
            
        Returns:
            tuple: (peso_maximo, caminho_maximo)
        """
        if inicio == fim:
            return peso_atual, caminho_atual.copy()
        
        peso_maximo = -1
        caminho_maximo = []
        
        # Explorar todos os vizinhos
        for vizinho in self.grafo.neighbors(inicio):
            # Criar identificador único para a aresta (independente da direção)
            aresta = tuple(sorted([inicio, vizinho]))
            
            # Só continuar se a aresta ainda não foi usada
            if aresta not in arestas_usadas:
                # Obter o peso da aresta
                peso_aresta = self.grafo.edges[inicio, vizinho].get('length', 1)
                
                # Adicionar aresta ao conjunto de usadas
                arestas_usadas.add(aresta)
                caminho_atual.append(vizinho)
                
                # Recursão
                peso, caminho = self._encontrar_caminho_mais_longo_dfs(
                    vizinho, fim, arestas_usadas, caminho_atual, peso_atual + peso_aresta
                )
                
                # Atualizar se encontrou um caminho melhor
                if peso > peso_maximo:
                    peso_maximo = peso
                    caminho_maximo = caminho.copy()
                
                # Backtrack
                arestas_usadas.remove(aresta)
                caminho_atual.pop()
        
        return peso_maximo, caminho_maximo

    def calcular_maior_caminho(self):
        """
        Calcula o maior caminho possível no grafo do jogador.
        Permite repetir vértices, mas não arestas.
        
        Returns:
            dict: Informações sobre o maior caminho encontrado
        """
        if self.grafo.number_of_nodes() == 0:
            return {"peso": 0, "caminho": [], "origem": None, "destino": None}
        
        if self.grafo.number_of_edges() == 0:
            return {"peso": 0, "caminho": [list(self.grafo.nodes())[0]], "origem": list(self.grafo.nodes())[0], "destino": list(self.grafo.nodes())[0]}
        
        peso_global_maximo = -1
        caminho_global_maximo = []
        melhor_origem = None
        melhor_destino = None
        
        vertices = list(self.grafo.nodes())
        
        # Testar todos os pares de vértices
        for i, origem in enumerate(vertices):
            for j, destino in enumerate(vertices):
                if i != j:  # Não considerar caminhos de um vértice para ele mesmo
                    arestas_usadas = set()
                    caminho_atual = [origem]
                    
                    peso, caminho = self._encontrar_caminho_mais_longo_dfs(
                        origem, destino, arestas_usadas, caminho_atual, 0
                    )
                    
                    if peso > peso_global_maximo:
                        peso_global_maximo = peso
                        caminho_global_maximo = caminho.copy()
                        melhor_origem = origem
                        melhor_destino = destino
        
        return {
            "peso": peso_global_maximo,
            "caminho": caminho_global_maximo,
            "origem": melhor_origem,
            "destino": melhor_destino,
            "num_vertices": len(caminho_global_maximo),
            "num_arestas": len(caminho_global_maximo) - 1 if caminho_global_maximo else 0
        }
