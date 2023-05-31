from abc import ABC, abstractmethod

from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador


class Estrategia(ABC):
    def __init__(self, descricao: str):
        self.descricao: str = descricao

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    @abstractmethod
    def escolher_personagem(estado: Estado) -> int:
        # JAtual
            # Qtd ouro [0,1,2,3,4,5,>=6] = 56
            # Qtd carta mão [0,1,2,3,4,>=5] = 48
            # Carta mão mais cara [1 a 6] = 48
            # Carta mão mais barata [1 a 6] = 48
            # Qtd distritos construido [0 a 6] = 56
            # Qtd distrito construido Militar [0,1,2,>=3] = 32
            # Qtd distrito construido Religioso [0,1,2,>=3] = 32
            # Qtd distrito construido Nobre [0,1,2,>=3] = 32
            # Qtd personagens disponíveis [2,3,4,5,6,7] = 48
            # Pontuacao [0-3,4-7,8-11,12-15,16-19,20-23,>=24] = 56
        # JMais
            # Qtd distrito construido [0 a 6] = 56
            # Qtd ouro [0,1,2,3,4,5,>=6] = 56
            # Qtd carta mão [0,1,2,3,4,>=5] = 48
        # Personagem visivel descartado [1,2,3,5,6,7,8] = 56
        # Personagem disponivel para escolha [1,2,3,4,5,6,7,8] = 64
        # Quantidade de jogadores [4,5,6] = 24
        # Total = 24 + 3*32 + 5*48 + ... = 760
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
                           distritos_para_construir_cardeal: list[(CartaDistrito, Jogador)],
                           distritos_para_construir_necropole: list[(CartaDistrito, CartaDistrito)],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)],
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
