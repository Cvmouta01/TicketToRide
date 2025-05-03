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