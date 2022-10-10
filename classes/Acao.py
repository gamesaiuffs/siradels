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


class EfeitoAssassino(Acao):
    def __init__(self):
        super().__init__('Anuncie um personagem que você deseja assassinar. O personagem assassinado perde o turno.')

    @staticmethod
    def ativar_efeito(estado: Estado, jogador_alvo: Jogador):
        estado.jogadores[estado.jogadores.index(jogador_alvo)].morto = True
