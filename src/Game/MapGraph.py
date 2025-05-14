import networkx as nx
import matplotlib.pyplot as plt

class MapGraph:
    def __init__(self):
        
        self.graph = nx.MultiGraph()
        self.load_cities_from_file('cities.csv')

    def load_cities_from_file(self, filename):
        """
        Carrega as informações das cidades a partir de um arquivo.
        O arquivo deve ter o formato: nome_cidade,pos_x,pos_y em cada linha.
        
        Args:
            filename (str): Caminho para o arquivo com as informações das cidades
        
        Returns:
            bool: True se o carregamento foi bem sucedido, False caso contrário
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                next(file)  # Ignora a primeira linha do arquivo, que é o header
                for line in file:
                    # Ignoramos linhas em branco
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Dividimos a linha pelos campos
                    parts = line.split(',')
                    if len(parts) >= 3:
                        city_name = parts[0].strip()
                        try:
                            pos_x = float(parts[1].strip())
                            pos_y = float(parts[2].strip())
                            
                            # Adicionamos a cidade ao grafo
                            self.graph.add_node(city_name, pos=(pos_x, pos_y))
                            print(f"Cidade adicionada ao grafo: {city_name} ({pos_x}, {pos_y})")
                        except ValueError:
                            print(f"Erro ao converter coordenadas para a cidade {city_name}")
                    else:
                        print(f"Formato inválido na linha: {line}")
            
            return True
        except Exception as e:
            print(f"Erro ao carregar o arquivo de cidades: {e}")
            return False

    def visualize(self, figsize=(12, 10), node_size=300, font_size=8):
        """
        Visualiza o grafo do jogo Ticket to Ride.
        
        Args:
            figsize (tuple): Tamanho da figura (largura, altura)
            node_size (int): Tamanho dos nós (cidades)
            font_size (int): Tamanho da fonte para os nomes das cidades
        """
        plt.figure(figsize=figsize)
        
        # Obtém as posições dos nós a partir dos atributos
        pos = {}
        for node, attrs in self.graph.nodes(data=True):
            pos[node] = attrs['pos']
        
        # Desenha os nós (cidades)
        nx.draw_networkx_nodes(self.graph, pos, 
                              node_color='lightblue', 
                              node_size=node_size)
        
        # Desenha os rótulos das cidades
        nx.draw_networkx_labels(self.graph, pos, 
                               font_size=font_size, 
                               font_weight='bold')
        
        plt.title("Ticket to Ride")
        plt.axis('off')
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # Criamos uma instância do grafo
    grafo = MapGraph()

    grafo.visualize()