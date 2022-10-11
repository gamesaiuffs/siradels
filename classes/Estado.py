# Imports
from more_itertools import sort_together
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

    def ordenar_jogadores_rei(self):
        ordenados, index_rei = [], 0
        for i, jogador in enumerate(self.jogadores):
            if jogador.rei:
                index_rei = i
                ordenados.insert(0, jogador)
        
        for i in range(index_rei + 1, len(self.jogadores)):
            ordenados.append(self.jogadores[i])
        for i in range(index_rei):
            ordenados.append(self.jogadores[i])

        self.jogadores = ordenados

    # Reorganiza a lista de jogadores de acordo com seus personagens
    def ordenar_jogadores(self):
        ordem = [jogador.personagem[0].rank for jogador in self.jogadores]
        self.jogadores = sort_together([ordem, self.jogadores])[1]
