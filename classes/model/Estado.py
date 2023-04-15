# Imports
from more_itertools import sort_together
from classes.model.Tabuleiro import Tabuleiro
from classes.model.Jogador import Jogador


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
            jogadores_print_str += "\n"
        return f"\nRODADA {self.rodada}\nTURNO {self.turno}\n\n" \
               f"Tabuleiro: {self.tabuleiro}\nJogadores: {jogadores_print_str}"

    # A nova rodada é iniciada pelo jogador que possui a coroa e segue em sentido horário
    # Fase de escolha de personagens
    def ordenar_jogadores_rei(self):
        index_rei = 0
        for i, jogador in enumerate(self.jogadores):
            if jogador.rei:
                index_rei = i
                break
        ordenados = []
        ordenados.extend(self.jogadores[index_rei:])
        ordenados.extend(self.jogadores[:index_rei])
        self.jogadores = ordenados

    # Reorganiza a lista de jogadores conforme o rank dos seus personagens
    # Fase de ações
    def ordenar_jogadores(self):
        ordem = [jogador.personagem.rank for jogador in self.jogadores]
        self.jogadores = sort_together([ordem, self.jogadores])[1]

    # Retorna o jogador atual/corrente do turno
    def jogador_atual(self) -> Jogador:
        return self.jogadores[self.turno - 1]
