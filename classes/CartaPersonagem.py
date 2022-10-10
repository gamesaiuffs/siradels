class CartaPersonagem:
    def __init__(self, nome: str, rank: int):
        self.nome = nome
        self.rank = rank

    def __str__(self):
        return f'nome: {self.nome} rank: {self.rank}'
