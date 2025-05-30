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
        """
        contagem_cores = {}
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

        # Se for uma rota cinza, basta ter selecionado uma qtd de cartas igual ao tamanho da rota
        if rota["color"] == "cinza":
            return any(qtd + coringas >= rota["length"] for qtd in contagem_cores.values())
        else: # Se for uma rota de outra cor, basta ver a qtd de cores selecionadas + coringas e ver se é maior que o tamanho da rota
            return contagem_cores[rota["color"]] + coringas >= rota["length"]

    def conquistar_rota(self, rota):
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
        # Ta bem simples, apenas remove todas as cartas selecionadas.
        # Não verifica se o player selecionou mais do que deveria
        self.cartas = [carta for carta in self.cartas if not carta.selecionada]

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