from Jogador import Jogador
import random
from collections import Counter

class IA(Jogador):
    def __init__(self, cor):
        super().__init__(cor)

        self.identificador = False

    #Metodo para IA escolher qual acao tomar.
    def escolher_acao(self, grafo):
        """
        Analisa o estado do jogo e decide a melhor ação a ser tomada.
        Retorna uma tupla com dados da rota se decidir conquistar, ou None se decidir comprar cartas.
        """
        # CORREÇÃO 1: A lógica foi invertida. Se não tiver cartas, deve comprar.
        if not self.cartas:
            return None
        
        # Se tiver cartas, tenta encontrar uma rota para conquistar
        contagem_cores = Counter(carta.cor for carta in self.cartas if carta.cor != "coringa")
        coringas = sum(1 for carta in self.cartas if carta.cor == "coringa")

        # Se não tiver cartas coloridas, só coringas
        if not contagem_cores:
            maior_cor_nome = "coringa"
            maior_cor_qtd = coringas
        else:
            maior_cor_nome = contagem_cores.most_common(1)[0][0]
            maior_cor_qtd = contagem_cores.most_common(1)[0][1]

        # Cria uma lista de possiveis rotas
        rotas_possiveis = []
        for u, v, key, data in grafo.edges(data=True, keys=True):
            # CORREÇÃO 2: A verificação de 'owned' estava sintaticamente incorreta.
            if not data.get('owned'):
                # Verifica se a IA pode conquistar a rota com a cor que ela mais tem + coringas
                if (data.get('color') == maior_cor_nome or data.get('color') == 'cinza') and data.get('length', 0) <= (maior_cor_qtd + coringas):
                    rotas_possiveis.append((u, v, key, data))

        # Se a lista de rotas possiveis não esta vazia, escolhe um elemento aleatoriamente
        if rotas_possiveis:
            rota_escolhida = random.choice(rotas_possiveis)
            
            # Seleciona as cartas necessárias para a conquista
            cor_a_usar = maior_cor_nome if rota_escolhida[3]['color'] == 'cinza' else rota_escolhida[3]['color']
            
            cartas_necessarias = rota_escolhida[3]['length']
            
            # Marca cartas da cor principal
            for carta in self.cartas:
                if cartas_necessarias > 0 and carta.cor == cor_a_usar:
                    carta.selecionada = True
                    cartas_necessarias -= 1
            
            # Se ainda faltar, marca coringas
            if cartas_necessarias > 0:
                for carta in self.cartas:
                    if cartas_necessarias > 0 and carta.cor == 'coringa':
                        carta.selecionada = True
                        cartas_necessarias -= 1

            # Retorna a rota escolhida para o Jogo gerenciar as mudanças no grafo
            return rota_escolhida
        
        # Se a lista de rotas estiver vazia, decide comprar cartas
        else:
            return None