from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random
from enum import Enum

class Estrategias(Enum):
    Ofensiva = 0,   # se alguém estiver à frente
        # foco - distritos de ataque
        # foco - personagens de ataque
            # assassina
            # ladrão
            # senhor da guerra

    Defensiva = 1,  # adotar se estiver à frente no jogo
        # foco - reserva de recursos
            # ilusionista - trocar mão de cartas
            #

        # foco - distritos variádos


        # foco - personagens com defesa
            # bispo

    Farming = 3,    # adotar no início
        # foco - geração de renda passiva
            # distritos variádos


        # foco - escolher personagem com bonus de renda
            # rei
            # comerciante
            # bispo
            # senhor da guerra

        # distritos estratégicos
            # escola de magia - mantém cartas compradas
            # laboratório - troca 1 carta por 2 ouros
            # pedreira - construír distritos iguais

    BonusFimJogo = 4,   # adotar se estiver à frente no jogo
        # foco - distritos variádos
        # foco - distritos com bônus de fim de jogo
        # foco - ações que rendem pontuação extra


# usar o estado para recalcular a estratégia e retorná-la - a função da classe estratégia fica responsável por escolher a ação
def calcularEstrategiaGeral(estado: Estado):
    # estratégia inicial
    if estado.rodada == 0:
        return Estrategias.Farming.value[0]


    # estratégia geral
    else:
        return Estrategias.BonusFimJogo.value[0]



class EstrategiaEduardo(Estrategia):
    def __init__(self, nome: str = 'Eduardo'):
        super().__init__(nome)
        # self.estrategia = str(Estrategias.Farming.value[0])
        #
        # self.estrategias = {
        #     str(Estrategias.Farming.value[0]): {
        #         "preferencia_personagem": ["Comerciante", "Rei", "Bispo", "Senhor da Guerra"],
        #     }
        # }

        # print(self.estrategias[self.estrategia])

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(estado: Estado) -> int:
        # return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)
        preferencia_farming = ["Comerciante", "Rei", "Bispo", "Senhor da Guerra"]


    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        if len(acoes_disponiveis) > 1:
            return random.randint(1, len(acoes_disponiveis) - 1)
        return 0

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        return random.randint(0, qtd_cartas - 1)

    # Estratégia usada na ação de construir distritos
        # ordená-los de acordo com a ordem de preferência ditada em cada estratégia
        # especiais primeiro
        # por valor -
    @staticmethod
    def construir_distrito(estado: Estado, distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)]) -> int:
        tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_covil_ladroes)
        return random.randint(0, tamanho_maximo - 1)

    # Estratégia usada na ação de construir distritos (efeito Covil dos Ladrões)
    @staticmethod
    def construir_distrito_covil_dos_ladroes(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade da Assassina
    @staticmethod
    def habilidade_assassina(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade da Ilusionista (escolha do jogador alvo)
    @staticmethod
    def habilidade_ilusionista_trocar(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        return random.randint(0, len(opcoes_jogadores) - 1)

    # Estratégia usada na habilidade da Ilusionista (escolha de quantas cartas serão descartadas)
    @staticmethod
    def habilidade_ilusionista_descartar_qtd_cartas(estado: Estado, qtd_maxima: int) -> int:
        return random.randint(1, qtd_maxima)

    # Estratégia usada na habilidade da Ilusionista (escolha de qual carta descartar)
    @staticmethod
    def habilidade_ilusionista_descartar_carta(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    def habilidade_senhor_da_guerra_destruir(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        return random.randint(0, len(distritos_para_destruir))

    # Estratégia usada na ação do Laboratório
    @staticmethod
    def laboratorio(estado: Estado) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)


EstrategiaEduardo()