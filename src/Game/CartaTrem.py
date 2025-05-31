class CartaTrem():
    def __init__(self, cor):
        self.selecionada = False
        self.cor = cor
        self.rect = None
    @staticmethod
    def criar_baralho_trem():
        cores = ['vermelho', 'azul', 'verde', 'amarelo', 'preto', 'branco', 'laranja', 'roxo', 'coringa']
        baralho = []
        for cor in cores:
            for _ in range(12 if cor != 'coringa' else 14):
                baralho.append(CartaTrem(cor))
        return baralho