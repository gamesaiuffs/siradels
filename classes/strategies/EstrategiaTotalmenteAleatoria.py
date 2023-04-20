from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
from classes.model.Acao import Acao
import random


class EstrategiaTotalmenteAleatoria(Estrategia):

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(jogador: Jogador, estado: Estado) -> int:
        return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(jogador: Jogador, estado: Estado, acoes: list[Acao]) -> int:
        return random.randint(0, len(acoes) - 1)
