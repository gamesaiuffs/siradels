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
        jogadores_print_str = ""
        for jogador in self.jogadores:
            jogadores_print_str += jogador.__str__()
            jogadores_print_str += "\n\n"
        return f"\nRODADA {self.rodada}\nTURNO {self.turno}\n\nTabuleiro:  {self.tabuleiro}\n\nJogadores:  {jogadores_print_str}"

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
        ordem = [jogador.personagem.rank for jogador in self.jogadores]
        self.jogadores = sort_together([ordem, self.jogadores])[1]

    # Retorna o jogador atual/corrente do turno
    def jogador_atual(self) -> Jogador:
        return self.jogadores[self.turno - 1]