from abc import ABC, abstractmethod

from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador


class Estrategia(ABC):
    def __init__(self, nome: str, imprimir: bool = False):
        self.nome: str = nome
        self.imprimir: bool = imprimir

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
    def construir_distrito(estado: Estado, distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)]) -> int:
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

    # Estratégia usada na habilidade da Ilusionista (escolha do jogador alvo)
    @staticmethod
    @abstractmethod
    def habilidade_ilusionista_trocar(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        pass

    # Estratégia usada na habilidade da Ilusionista (escolha de quantas cartas serão descartadas)
    @staticmethod
    @abstractmethod
    def habilidade_ilusionista_descartar_qtd_cartas(estado: Estado, qtd_maxima: int) -> int:
        pass

    # Estratégia usada na habilidade da Ilusionista (escolha de qual carta descartar)
    @staticmethod
    @abstractmethod
    def habilidade_ilusionista_descartar_carta(estado: Estado, qtd_cartas: int, i: int) -> int:
        pass

    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    @abstractmethod
    def habilidade_senhor_da_guerra_destruir(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        pass

    # Estratégia usada na ação do Laboratório
    @staticmethod
    @abstractmethod
    def laboratorio(estado: Estado) -> int:
        pass
