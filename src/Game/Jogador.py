import pygame

class Jogador():
    def __init__(self, cor):
        self.cor = cor

        self.pontos = 0

        self.trens = 45

        self.cartas = []

        self.objetivos = []

        self.mapa_conquistado = None

        # Define se é o turno do jogador ou não
        self.ativo = False

    def pode_conquistar(self, rota):
        """
        Faz a contagem das cartas selecionadas e verifica se
        essas são suficientes para conquistar a rota dada

        Retorna a cor a ser usada para a conquista
        """
        contagem_cores = {'vermelho' : 0, 'azul' : 0, 'verde' : 0, 'amarelo' : 0, 'preto' : 0, 'branco' : 0, 'laranja' : 0, 'rosa' : 0}
        coringas = 0
        # Passa por todas as cartas
        for carta in self.cartas:
            # Verifica se a carta está selecionada
            if carta.selecionada:
                if carta.cor == "coringa":
                    coringas += 1
                else:
                    if carta.cor in contagem_cores:
                        contagem_cores[carta.cor] += 1
                    else:
                        contagem_cores[carta.cor] = 1

        # Se for uma rota cinza, basta ter selecionado uma qtd de cartas DE MESMA COR igual ao tamanho da rota
        if rota["color"] == "cinza":
            maior_cor = max(contagem_cores.items(), key=lambda item: item[1]) # Pega a cor que está em maior qtd

            if maior_cor[1] != 0: # Se a maior qtd de cores não for 0 (seria o caso em que o player selecionou só coringas)
                return maior_cor[0]
            
            elif coringas >= rota["length"]: # Significa que o player selecionou só coringas
                return "vermelho" # Retorna alguma coisa, só pra não quebrar
            
        else: # Se for uma rota de outra cor, basta ver a qtd de cores selecionadas + coringas e ver se é maior que o tamanho da rota
            if contagem_cores[rota["color"]] + coringas >= rota["length"]:
                return rota["color"]

        # Não foram selecionadas cartas o suficiente para conqusitar
        return None

    def conquistar_rota(self, rota, conquista_possivel):
        """
        Remove as cartas selecionadas usadas para conquistar a rota

        E dá pontos ao player por conquistar

        1 trem=> 1
        2 trem=> 2
        3 trem=> 4
        4 trem=> 7
        5 trem=> 10
        6 trem=> 15
        """

        # Removendo as cartas de mão %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        # Ideia: passa por todas as cartas de mão e pega N cartas selecionadas da cor da rota onde N é o tamanho da rota.
        # Caso não tenha encontrado cartas da cor da rota suficientes, começa a pegar os coringas

        cartas_usadas = []
        qtd_cartas_necessairas = rota["length"] # Pra garantir que não vão ser usadas mais cartas que o necessário

        # Itera por todas as cartas da cor da rota
        for carta in self.cartas:

            if qtd_cartas_necessairas == 0: # Se já pegou cartas o suficiente sai do loop
                break

            if carta.selecionada: # Se é uma carta selecionada

                # Se for uma rota cinza, garante que o player usará apenas cartas de uma unica cor
                # (definida em pode_conquistar como sendo a cor com maior qtd de cartas selecionadas)
                # Se não for uma rota cinza, apenas verifica se a carta tem a cor da rota
                if (rota["color"] == "cinza" and carta.cor == conquista_possivel) or (rota["color"] != "cinza" and carta.cor == rota["color"]):
                    cartas_usadas.append(carta)
                    qtd_cartas_necessairas -= 1

         # Se ainda não pegou cartas o suficiente, começa a pegar coringas
        if qtd_cartas_necessairas > 0:

            for carta in self.cartas:

                if qtd_cartas_necessairas == 0:
                    break

                if carta.selecionada and carta.cor == "coringa":
                    cartas_usadas.append(carta)
                    qtd_cartas_necessairas -= 1

        # Por fim, remove tais cartas da mão do jogador
        for carta in cartas_usadas:
            self.cartas.remove(carta)

        # Desseleciona todas as cartas da mão
        for carta in self.cartas: carta.selecionada = False

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



        # Concedendo pontos ao player com base no tamanho da rota
        match rota["length"]:
            case 1:
                self.pontos += 1
            case 2:
                self.pontos += 2
            case 3:
                self.pontos += 4
            case 4:
                self.pontos += 7
            case 5:
                self.pontos += 10
            case _:
                self.pontos += 15

        # Removendo a qtd de trens usadas pra conquistar a rota
        self.trens -= rota["length"]

    def comprar_cartas_trem(self):
        pass

    def comprar_cartas_objetivo(self):
        pass