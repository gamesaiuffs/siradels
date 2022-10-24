class CartaPersonagem:
    # Construtor
    def __init__(self, nome: str, rank: int, descricao_habilidade: str = ''):
        self.nome = nome
        self.rank = rank
        self.descricao_habilidade = descricao_habilidade

    # To String
    def __str__(self) -> str:
        if self.rank == 0:
            return f'{self.nome}'
        if self.descricao_habilidade == '':
            return f'{self.nome}, Rank: {self.rank}'
        return f'{self.nome}, Rank: {self.rank}' \
               f'\n\tHabilidade: {self.descricao_habilidade}'
    
    # Pegar apenas o nome do personagem
    def obter_nome(self):
        return self.nome
