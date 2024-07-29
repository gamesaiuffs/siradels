from classes.enum.TipoPersonagem import TipoPersonagem
from classes.model.IndexMCTS import IndexMCTS


class CartaPersonagem(IndexMCTS):
    # Construtor
    def __init__(self, nome: str, rank: int, tipo_personagem: TipoPersonagem, descricao_habilidade: str = ''):
        super().__init__(rank - 1)
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
