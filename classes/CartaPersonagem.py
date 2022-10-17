class CartaPersonagem:
    # Construtor
    def __init__(self, nome: str, rank: int, descricao_habilidade: str = ''):
        self.nome = nome
        self.rank = rank
        self.descrissao_habilidade = descricao_habilidade

    # To String
    def __str__(self) -> str:
        return f'{self.nome}, Rank: {self.rank}' \
               f'\n\tHabilidade: {self.descrissao_habilidade}'
