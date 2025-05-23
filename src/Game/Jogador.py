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
        """Retorna True se o jogador tem cartas suficientes (cor+locomotivas)."""
        qtd_cor = sum(1 for c in self.cartas if c.cor == rota.color)
        qtd_loco = sum(1 for c in self.cartas if c.cor == "coringa")
        return (qtd_cor + qtd_loco) >= rota.length

    def conquistar_rota(self, rota):
        """Remove as cartas usadas e soma os pontos da rota."""
        need = rota.length
        for _ in range(min(need, sum(1 for c in self.cartas if c.cor == rota.color))):
            for c in self.cartas:
                if c.cor == rota.color:
                    self.cartas.remove(c)
                    need -= 1
                    break

        while need > 0:
            for c in self.cartas:
                if c.cor == "coringa":
                    self.cartas.remove(c)
                    need -= 1
                    break
        self.pontos += rota.points