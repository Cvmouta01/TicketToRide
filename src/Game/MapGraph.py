import networkx as nx
import matplotlib.pyplot as plt

class MapGraph:
    def __init__(self):
        
        self.graph = nx.MultiGraph()
        self.load_cities_from_file('cities.csv')
        self.load_routes_from_file('routes.csv')


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
                    # Ignora linhas em branco
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Divide a linha pelos campos
                    parts = line.split(',')
                    if len(parts) >= 3:
                        city_name = parts[0].strip()
                        try:
                            pos_x = float(parts[1].strip())
                            pos_y = float(parts[2].strip())
                            
                            # Adiciona a cidade ao grafo
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


    def add_route(self, city1, city2, color, length, train_pos):
        """
        Adiciona uma rota entre duas cidades apenas se ambas já existirem no grafo.
        
        Args:
            city1 (str): Nome da primeira cidade
            city2 (str): Nome da segunda cidade
            color (str): Cor da rota
            length (int): Comprimento da rota
            train_pos (dict): Dicionário com a posição de cada trilho da rota
        
        Returns:
            bool: True se a rota foi adicionada com sucesso, False caso contrário
        """
        # Verifica se as cidades existem
        if city1 not in self.graph.nodes:
            print(f"Erro: Cidade '{city1}' não existe no grafo. A rota não foi adicionada.")
            return False
        if city2 not in self.graph.nodes:
            print(f"Erro: Cidade '{city2}' não existe no grafo. A rota não foi adicionada.")
            return False
        
        # Se ambas as cidades existem, adiciona a rota
        self.graph.add_edge(city1, city2, color=color, length=length, train_pos=train_pos, owned=False)
        print(f"Rota adicionada: {city1} - {city2} (cor: {color}, comprimento: {length})")
        return True


    def set_route_owned(self, city1, city2, key=0):
        """
        Define o status de propriedade de uma rota específica.
        
        Args:
            city1 (str): Nome da primeira cidade
            city2 (str): Nome da segunda cidade
            key (int): Identificador da aresta (para múltiplas arestas entre as mesmas cidades)
            owned (bool): Status de propriedade da rota (True para adquirida, False para não adquirida)
        
        Returns:
            bool: True se a operação foi bem sucedida, False caso contrário
        """
        try:
            # Verifica se a aresta existe
            if not self.graph.has_edge(city1, city2):
                print(f"Erro: Não existe rota entre '{city1}' e '{city2}'.")
                return False
            
            # Obtém os dados da aresta
            edge_data = self.graph.get_edge_data(city1, city2)
            
            # Verifica se a chave específica existe
            if key not in edge_data:
                print(f"Erro: Não existe rota com chave {key} entre '{city1}' e '{city2}'.")
                return False
            
            # Atualiza o status de propriedade
            self.graph[city1][city2][key]['owned'] = True
            status = "adquirida" if True else "não adquirida"
            print(f"Rota entre '{city1}' e '{city2}' (chave {key}) agora está {status}.")
            return True
        except Exception as e:
            print(f"Erro ao definir propriedade da rota: {e}")
            return False


    def load_routes_from_file(self, filename):
        """
        Carrega as rotas a partir de um arquivo CSV.
        O arquivo deve ter o formato: cidade_1,cidade_2,cor,comprimento em cada linha.
        
        Args:
            filename (str): Caminho para o arquivo com as informações das rotas
            
        Returns:
            bool: True se o carregamento foi bem sucedido, False caso contrário
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                next(file)  # Ignora a primeira linha do arquivo, que é o header
                routes_added = 0
                routes_failed = 0
                
                for line in file:
                    # Ignora linhas em branco
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Divide a linha pelos campos
                    parts = line.split(';')
                    if len(parts) >= 5:
                        city_1 = parts[0].strip()
                        city_2 = parts[1].strip()
                        color = parts[2].strip()
                        train_pos = parts[4].strip()
                        
                        try:
                            length = int(parts[3].strip())
                            
                            # Adiciona a rota usando o método add_route existente
                            if self.add_route(city_1, city_2, color, length, train_pos):
                                routes_added += 1
                            else:
                                routes_failed += 1
                                
                        except ValueError:
                            print(f"Erro ao converter o comprimento da rota entre {city_1} e {city_2}")
                            routes_failed += 1
                    else:
                        print(f"Formato inválido na linha: {line}")
                        routes_failed += 1
            
            print(f"Carregamento de rotas concluído: {routes_added} rotas adicionadas, {routes_failed} falhas.")
            return True
        except Exception as e:
            print(f"Erro ao carregar o arquivo de rotas: {e}")
            return False

    @staticmethod
    def translate_color(cor_portugues):
        cores = {
            "branco": "white",
            "preto": "black",
            "vermelho": "red",
            "azul": "blue",
            "amarelo": "yellow",
            "verde": "green",
            "laranja": "orange",
            "rosa": "pink",
            "cinza": "grey"
        }

        return cores.get(cor_portugues.lower(), cor_portugues)

    def visualize(self, figsize=(70.16, 46.65), node_size=300, font_size=8):
        """
        Visualiza o grafo do jogo Ticket to Ride.
        
        Args:
            figsize (tuple): Tamanho da figura (largura, altura)
            node_size (int): Tamanho dos nós (cidades)
            font_size (int): Tamanho da fonte para os nomes das cidades
        """
        # Cria a figura e os eixos com a cor de fundo desejada
        fig = plt.figure(figsize=figsize, dpi=100, facecolor='#d3d3d3')  # Cinza claro

        ax = fig.add_subplot(111)
        ax.set_facecolor('#d3d3d3')
        
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

        # Dicionário para rastrear pares de cidades já processados
        processed_pairs = {}
    
        # Desenha as arestas (rotas) com cores diferentes
        for (city1, city2, key, data) in self.graph.edges(data=True, keys=True):
            # Obtém a cor e o comprimento da aresta
            edge_color = self.translate_color(data.get('color', 'grey'))
            edge_width = 5
            edge_length = data.get('length', 1)
            
            # Verifica se a rota é de propriedade do jogador
            is_owned = data.get('owned', False)

            # Ajusta a largura ou estilo da linha com base na propriedade
            if is_owned:
                edge_width = 8  # Rotas de propriedade são mais grossas

            # Cria um par ordenado para identificar a aresta
            edge_pair = tuple(sorted([city1, city2]))
            
            # Verifica se já processou este par de cidades
            if edge_pair in processed_pairs:
                # Esta é a segunda aresta entre estas cidades
                # Desenha com uma curvatura positiva
                curve = 0.3
            else:
                # Esta é a primeira aresta entre estas cidades
                # Desenha com uma curvatura negativa ou reta
                curve = -0.3 if self.graph.number_of_edges(city1, city2) > 1 else 0
                processed_pairs[edge_pair] = True
            
            # Desenha a aresta com a curvatura apropriada
            nx.draw_networkx_edges(self.graph, pos,
                                edgelist=[(city1, city2)],
                                width=edge_width,
                                edge_color=edge_color,
                                connectionstyle=f'arc3, rad={curve}',
                                ax = ax)
            
            # Calcula a posição do rótulo
            edge_x = (pos[city1][0] + pos[city2][0]) / 2
            edge_y = (pos[city1][1] + pos[city2][1]) / 2
            
            # Adiciona um deslocamento baseado na curvatura
            displacement = 0.1 if curve != 0 else 0
            dx = -(pos[city2][1] - pos[city1][1]) * displacement * (1 if curve > 0 else -1)
            dy = (pos[city2][0] - pos[city1][0]) * displacement * (1 if curve > 0 else -1)
            
            # Adiciona o rótulo com o comprimento da rota
            plt.text(edge_x + dx, edge_y + dy, 
                    str(edge_length), 
                    color=edge_color,
                    fontsize=8,
                    fontweight='bold',
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=0.3),
                    horizontalalignment='center', 
                    verticalalignment='center')


            # Verifica se existem as informações de posição dos trilhos
            train_pos_str = data.get('train_pos', None)
            if train_pos_str:
                try:
                    # Converte a string para um dicionário
                    train_pos_dict = eval(train_pos_str)
                    
                    # Para cada trilho no dicionário
                    for train_id, positions in train_pos_dict.items():
                        # Verifica se tem a informação todos os 8 valores (4 pontos)
                        if len(positions) == 8:
                            # Verifica se os pontos são válidos (não são todos zeros)
                            if all(p == 0 for p in positions):
                                # Se todos os pontos são zeros, pula este trilho
                                continue
                            
                            # Extrai as coordenadas dos 4 pontos
                            x1, y1, x2, y2, x3, y3, x4, y4 = positions
                            
                            # Cria os pontos do retângulo
                            rectangle_points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
                            
                            # Cria um retângulo para o trilho
                            rectangle = plt.Polygon(rectangle_points, 
                                                closed=True, 
                                                fill=True,
                                                color=edge_color if not is_owned else 'darkgrey',
                                                alpha=0.7)
                            
                            # Adiciona o retângulo ao gráfico
                            ax.add_patch(rectangle)
                            
                except Exception as e:
                    print(f"Erro ao desenhar trilhos para a rota {city1}-{city2}: {e}")

        plt.title("Ticket to Ride")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def update_arestas(self, surface, mapa):
        # Recebe a superficie e o mapa do jogo
        # Atualiza as coordenadas das arestas do grafo para as novas coordenadas

        for u, v, k, data in self.graph.edges(data=True, keys=True):
            # Avalia a string do dicionário
            posicoes = eval(data['train_pos']) # EVAL (!!!)

            # Aplica a função a cada ponto de cada trem
            for trem in posicoes:
                posicoes[trem] = mapa.ajustar_ponto(surface, posicoes[trem])

            # Atualiza no grafo
            data['train_pos'] = posicoes


if __name__ == "__main__":
    # Cria uma instância do grafo
    grafo = MapGraph()

    grafo.visualize()