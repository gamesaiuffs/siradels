# Importar classe na tipagem habilidade e efeito
import Efeito


class CartaPersonagem:
    def __init__(self, nome: str, efeito: Efeito, rank: int, habilidade: str):
        self.nome = nome
        self.efeito = efeito
        self.rank = rank
        self.habilidade = habilidade

    def __str__(self):
        return f'nome: {self.nome} efeito: {self.efeito} rank: {self.rank} skill: {self.habilidade}'
