from classes.enum.TipoPersonagem import TipoPersonagem


class CartaPersonagem:
    # Construtor
    def __init__(self, nome: str, rank: int, tipo_personagem: TipoPersonagem, descricao_habilidade: str = ''):
        self.nome: str = nome
        self.rank: int = rank
        self.descricao_habilidade: str = descricao_habilidade
        self.tipo_personagem: TipoPersonagem = tipo_personagem

    # To String
    def __str__(self) -> str:
        return f"{self.nome} - Rank({self.rank})"
    
    # Pegar apenas o nome do personagem
    def obter_nome(self):
        return self.nome
