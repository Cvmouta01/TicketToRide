import Jogador
import random
from collections import Counter

class IA(Jogador):
    def __init__(self, cor):
        super().__init__(cor)

        self.identificador = False

    #Metodo para IA escolher qual acao tomar.
    def escolher_acao(self, grafo):
        
        #Checa se possui cartas, se a lista estiver vazia realiza a compra
        if self.cartas.empty:
            return None
        
        #Se tiver cartas, conta e tenta conquistar uma rota
        else:
            
            #Contagem de cores como em Jogador, mas contando o total inves das selecionadas
            contagem_cores = {'vermelho' : 0, 'azul' : 0, 'verde' : 0, 'amarelo' : 0, 'preto' : 0, 'branco' : 0, 'laranja' : 0, 'rosa' : 0}
            coringas = 0
            
            # Passa por todas as cartas
            for carta in self.cartas:
                if carta.cor == "coringa":
                    coringas += 1
                else:
                    if carta.cor in contagem_cores:
                        contagem_cores[carta.cor] += 1
                    else:
                        contagem_cores[carta.cor] = 1

            #Checa qual a cor em maior quantidade
            maior_cor = max(contagem_cores.values())
            
            #Cria uma lista com todas as cores que possi valor igual a maior_cor, caso houver mais do que uma
            #Para cada tupla em contagem_cores, adiciona na lista todas com o valor igual maior_cor
            cores_mais_repetidas = [
                cor for cor, contagem in contagem_cores.items()
                if contagem == maior_cor
            ]

            #Cria uma lista de possiveis rotas, itera sobre as aresta do grafo e adiciona na lista as rotas possiveis
            rotas_possiveis = []

            for u, v, data in grafo.edges(data=True):
                if (data.get('color') in cores_mais_repetidas or data.get('color') == 'cinza') and data.get('length', 0) <= maior_cor and data.get('owned' is False):
                    rotas_possiveis.append((u, v, data))


            #Se a lista de rotas possiveis não esta vazia, escolhe um elemento aleatoriamente e tenta conquiastar
            if rotas_possiveis:
                
                rng = random.randint(0, len(rotas_possiveis)-1)
                rota_escolhida = rotas_possiveis[rng]
                
                #Seleciona as cartas necessaria para conquistar a rota. Contador é indice para selecionar a qtd certa de cartas
                contador = 0
                for carta in self.cartas:                    
                    if contador < rota_escolhida[2]['length']:

                        #Se a rota não for cinza, compara a cor da carta na mão com a cor da rota escolhida
                        if (rota_escolhida[2]['color'] != 'cinza' and carta.cor == rota_escolhida[2]['color']):
                            carta.selecionada = True
                            contador += 1
                        
                        #Se a rota for cinza, compara a cor da carta na mão com a cor na lista de mais repetidas
                        elif(rota_escolhida[2]['color'] == 'cinza' and carta.cor == cores_mais_repetidas[0]):
                            carta.selecionada = True
                            contador += 1
                
                #Retorna a rota escolhida para o Jogo gerenciar as mudanças no grafo
                return rota_escolhida
            
            #Se lista estiver vazia, compra carta
            else:
                return None
        
        #Cada valor representa um do metodos da classe Jogador: 1 = conquistar_rota
        #2 = comprar_carta_trem
        #3 = comprar_carta_objetivo
        
        escolha = random.randint(1, 3) 

        if escolha == 1:
            pass

        elif escolha == 2:
            pass

        elif escolha == 3:
            pass
