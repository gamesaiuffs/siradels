import Tabuleiro
import Jogador

class Estado:
    def __init__(self, tabuleiro: Tabuleiro, jogadores: Jogador):
        self.board = tabuleiro 
        self.players = jogadores

    def __str__(self):
        return print(f"Tabuleiro:  {self.board} Jogadores:  {self.players}")
