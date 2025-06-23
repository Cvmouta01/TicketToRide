import os
import random
import pygame
from Utils import resize_com_escala

class CartaObjetivo():
    def __init__(self, origem, destino, pontos, imagem_surface):
        self.origem = origem
        self.destino = destino
        self.pontos = pontos
        self.imagem = imagem_surface
        self.concluido = False

    @staticmethod
    def criar_baralho_objetivo(sur_width, sur_height):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # corrige caminho para apontar à pasta Images/Objetivos dentro de src/Game
        pasta = os.path.join(base_dir, 'assets', 'Images', 'Objetivos')
        baralho = []

        for fname in os.listdir(pasta):
            if not fname.lower().endswith('.png'):
                continue

            nome, _ = os.path.splitext(fname)
            partes = nome.split('_')
            if len(partes) != 3:
                continue

            origem, destino, pts_str = partes
            try:
                pontos = int(pts_str)
            except ValueError:
                continue

            caminho_imagem = os.path.join(pasta, fname)
            imagem_surf = pygame.image.load(caminho_imagem).convert_alpha()
            imagem_surf = resize_com_escala(imagem_surf, sur_width, sur_height, 0.1, 0.1)
            baralho.append(CartaObjetivo(origem, destino, pontos, imagem_surf))

        random.shuffle(baralho)
        return baralho
