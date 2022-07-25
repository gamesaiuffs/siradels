from Tabuleiro import Tabuleiro
from Jogadores import Jogadores


class Estado:
    def __init__(self, tabuleiro: Tabuleiro, jogadores: Jogadores):
        self.board = tabuleiro 
        self.players = jogadores

    def __str__(self):
        return print(f"Tabuleiro:  {self.board} Jogadores:  {self.players}")
