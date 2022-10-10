class CartaPersonagem:
    # Construtor
    def __init__(self, nome: str, rank: int):
        self.nome = nome
        self.rank = rank

    # To String
    def __str__(self):
        return f'\nNome: {self.nome}' \
               f'\nRank: {self.rank}'
