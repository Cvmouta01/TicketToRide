import Jogador
import random

class IA(Jogador):
    def __init__(self, cor):
        super().__init__(cor)

        self.identificador = False

    #Metodo para IA escolher qual acao tomar baseado em RNG.
    def escolher_acao(self, rotas_disponiveis):
        
        
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
