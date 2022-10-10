# Imports
from Tabuleiro import Tabuleiro
from Jogador import Jogador


class Estado:
    # Construtor
    def __init__(self, tabuleiro: Tabuleiro, jogadores: list[Jogador]):
        self.tabuleiro = tabuleiro
        self.jogadores = jogadores
        self.turno = 1
        self.rodada = 1

    # To String
    def __str__(self):
        return f"Tabuleiro:  {self.tabuleiro} Jogadores:  {self.jogadores}"

    # Reorganiza a lista de jogadores de acordo com seus personagens
    def ordenar_jogadores(self):
        # WIP
        pass
