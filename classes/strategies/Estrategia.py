from abc import ABC, abstractmethod

from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
from classes.model.Acao import Acao


class Estrategia(ABC):

    @staticmethod
    @abstractmethod
    def escolher_personagem(jogador: Jogador, estado: Estado) -> int:
        pass

    @staticmethod
    @abstractmethod
    def escolher_acao(jogador: Jogador, estado: Estado, acoes: list[Acao]) -> int:
        pass
