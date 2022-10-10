import string


class CartaPersonagem:
    # Construtor
    def __init__(self, nome: str, rank: int, descricao_habilidade:string = ''):
        self.nome = nome
        self.rank = rank
        self.descrissao_habilidade = descricao_habilidade

    # To String
    def __str__(self):
        return f'\nNome: {self.nome}' \
               f'\nRank: {self.rank}' \
               f'\nHabilidade: {self.descrissao_habilidade}'
