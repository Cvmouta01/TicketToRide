class CartaObjetivo():
    def __init__(self, origem, destino, pontos):
        
        self.origem = origem
        
        self.destino = destino
        
        self.pontos = pontos

    @staticmethod
    def criar_baralho_objetivo():
        destinos = [
            ("x", "x1", 5),
            ("x2", "x3", 7),
            ("x4", "x5", 10),
            ("x6", "x7", 8),
            ("x8", "x9", 12),
            ("x10", "x11", 6),
            ("x12", "x13", 9),
            ("x14", "x15", 4),
            ("x16", "x17", 11),
            ("x18", "x19", 7),
            ("x20", "x21", 8),
            ("x22", "x23", 10),
            ("x24", "x25", 9),
            ("x26", "x27", 6),
            ("x28", "x29", 5)]
        baralho = [CartaObjetivo(origem, destino, pontos) for origem, destino, pontos in destinos]
        return baralho