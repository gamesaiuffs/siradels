class CartaPersonagem:
    # Construtor
    def __init__(self, nome: str, rank: int, descricao_habilidade: str = ''):
        self.nome = nome
        self.rank = rank
        self.descricao_habilidade = descricao_habilidade

    # To String
    def __str__(self) -> str:
        return f"{self.nome} - {self.rank}"
    
    # Pegar apenas o nome do personagem
    def obter_nome(self):
        return self.nome
