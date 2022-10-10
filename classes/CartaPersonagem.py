# Imports
import Efeito


class CartaPersonagem:
    # Construtor
    def __init__(self, nome: str, efeito: Efeito, rank: int, habilidade: str):
        self.nome = nome
        self.efeito = efeito
        self.rank = rank
        self.habilidade = habilidade

    # To String
    def __str__(self):
        return f'\nNome: {self.nome}' \
               f'\nEfeito: {self.efeito}' \
               f'\nRank: {self.rank}' \
               f'\nHabilidade: {self.habilidade}'
