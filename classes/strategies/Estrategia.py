from abc import ABC, abstractmethod

from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador


class Estrategia(ABC):

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    @abstractmethod
    def escolher_personagem(estado: Estado) -> int:
        pass

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    @abstractmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        pass

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    @abstractmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        pass

    # Estratégia usada na ação de construir distritos
    @staticmethod
    @abstractmethod
    def construir_distrito(estado: Estado,
                           distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_cardeal: list[CartaDistrito],
                           distritos_para_construir_necropole: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[CartaDistrito],
                           distritos_para_construir_estrutura: list[CartaDistrito]) -> int:
        pass

    # Estratégia usada na ação de construir distritos (efeito Cardeal)
    @staticmethod
    @abstractmethod
    def construir_distrito_cardeal(estado: Estado, diferenca: int, i: int) -> int:
        pass

    # Estratégia usada na ação de construir distritos (efeito Covil dos Ladrões)
    @staticmethod
    @abstractmethod
    def construir_distrito_covil_dos_ladroes(estado: Estado, qtd_cartas: int, i: int) -> int:
        pass

    # Estratégia usada na habilidade da Assassina
    @staticmethod
    @abstractmethod
    def habilidade_assassina(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        pass

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    @abstractmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        pass

    # Estratégia usada na habilidade do Mago (escolha do jogador alvo)
    @staticmethod
    @abstractmethod
    def habilidade_mago_jogador(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        pass

    # Estratégia usada na habilidade do Mago (escolha da carta da mão)
    @staticmethod
    @abstractmethod
    def habilidade_mago_carta(estado: Estado, opcoes_cartas: list[CartaDistrito]) -> int:
        pass

    # Estratégia usada na habilidade da Navegadora
    @staticmethod
    @abstractmethod
    def habilidade_navegadora(estado: Estado) -> int:
        pass

    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    @abstractmethod
    def habilidade_senhor_da_guerra(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador, int)]) -> int:
        pass

    # Estratégia usada na ação do Laboratório
    @staticmethod
    @abstractmethod
    def laboratorio(estado: Estado) -> int:
        pass

    # Estratégia usada na ação do Arsenal
    @staticmethod
    @abstractmethod
    def arsenal(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        pass

    # Estratégia usada na ação do Museu
    @staticmethod
    def museu(estado: Estado) -> int:
        pass
