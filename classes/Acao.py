# Imports
from abc import abstractmethod
from Estado import Estado
from Jogador import Jogador


class Acao:
    # Construtor
    def __init__(self, descricao: str):
        self.descricao = descricao

    # To String
    def __str__(self):
        return f'descrição do efeito: {self.descricao}'

    @staticmethod
    @abstractmethod
    def ativar_efeito(estado: Estado, jogador: Jogador) -> Estado:
        pass


class ColetarOuro(Acao):
    def __init__(self):
        super().__init__('Colete 2 ouros do banco.')

    @staticmethod
    def ativar_efeito(estado: Estado, jogador_alvo: Jogador):
        estado.jogadores[estado.jogadores.index(jogador_alvo)].ouro += 2

class ColetarCartas(Acao):
    def __init__(self):
        super().__init__('Colete 2 cartas do baralho e escolha uma.')

    @staticmethod
    def ativar_efeito(estado: Estado, jogador_alvo: Jogador):
        escolherCartas = estado.tabuleiro.baralho_distritos[0:2]
        estado.tabuleiro.baralho_distritos.pop()
        estado.tabuleiro.baralho_distritos.pop()

        print(escolherCartas[0])
        print(escolherCartas[1])

        escolha = int(input("Digite 1 para a primeira opção, 2 para a segunda: "))
        if escolha == 1:
            estado.jogadores[estado.jogadores.index(jogador_alvo)].cartas_distrito_mao.append(escolherCartas[0])
            estado.tabuleiro.baralho_distritos.append(escolherCartas[0])
        else:
            estado.jogadores[estado.jogadores.index(jogador_alvo)].cartas_distrito_mao.append(escolherCartas[1])
            estado.tabuleiro.baralho_distritos.append(escolherCartas[0])


class EfeitoAssassino(Acao):
    def __init__(self):
        super().__init__('Anuncie um personagem que você deseja assassinar. O personagem assassinado perde o turno.')

    @staticmethod
    def ativar_efeito(estado: Estado, jogador_alvo: Jogador):
        estado.jogadores[estado.jogadores.index(jogador_alvo)].morto = True
