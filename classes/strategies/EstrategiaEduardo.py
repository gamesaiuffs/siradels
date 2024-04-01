import time

from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random
from enum import Enum

DEBUG = False
DEBUG_TIME = False

def debugTime():
    if DEBUG_TIME:
        time.sleep(5)


def debug(message: str):
    if (DEBUG):
        print(message)



class Estrategias(Enum):
    Ofensiva = 0   # se alguém estiver à frente
        # foco - distritos de ataque
        # foco - personagens de ataque
            # assassina
            # ladrão
            # senhor da guerra

    Defensiva = 1  # adotar se estiver à frente no jogo
        # foco - reserva de recursos
            # ilusionista - trocar mão de cartas
            #

        # foco - distritos variádos


        # foco - personagens com defesa
            # bispo

    Farming = 3    # adotar no início
        # foco - geração de renda passiva
            # distritos variádos
            # ou
            # focar em um tipo


        # foco - escolher personagem com bonus de renda - feito
            # rei
            # comerciante
            # bispo
            # senhor da guerra

        # distritos estratégicos
            # escola de magia - mantém cartas compradas
            # laboratório - troca 1 carta por 2 ouros
            # pedreira - construír distritos iguais

        # Ordem de preferência de tipos de distritos
            # especial = 4
            # comercial = 3
            # nobre = 2
            # militar(1), religioso(0)


    Religioso = 0
    Militar = 1
    Nobre = 2
    Comercial = 3
    Especial = 4

    BonusFimJogo = 4   # adotar se estiver à frente no jogo
        # foco - distritos variádos
        # foco - distritos com bônus de fim de jogo
        # foco - ações que rendem pontuação extra


# usar o estado para recalcular a estratégia e retorná-la - a função da classe estratégia fica responsável por escolher a ação
def calcularEstrategiaGeral(estado: Estado):
    # estratégia inicial
    debug("---------------------------------------| Escolha de estratégia |-------------------------------- ")
    debug(f"rodada: {estado.rodada}\t\tturno: {estado.turno}")
    debug(f"Ouro: ")
    for jogador in estado.jogadores:
        debug(f"{jogador.nome}\t\t\touro: {jogador.ouro}\tpontos: {jogador.pontuacao}")
    debug("------------------------------------------------------------------------------------------------ ")

    return Estrategias.Farming.value


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
        estrategia = calcularEstrategiaGeral(estado)
        # debug("---------------------------------------| Escolha de personagem |-------------------------------- ")

        # encontra o jogador
        index_jogador = -1
        for index, jog in enumerate(estado.jogadores):
            # print(jog.nome)
            if jog.nome == 'Bot - Eduardo':
                index_jogador = index

        if index_jogador == -1:
            print("ERRO----------------------------------------------------------------------------------------")
            time.sleep(150)



        # estratégia de farming
        if estrategia == Estrategias.Farming.value:

            # verificar distritos construídos
            qtd_distritos_cada_tipo = {
                "0": 0,
                "1": 0,
                "2": 0,
                "3": 0,
                "4": 0
            }

            # mapear quantos distritos de cada tipo foram construídos
            for dist in estado.jogadores[index_jogador].distritos_construidos:
                qtd_distritos_cada_tipo[str(dist.tipo_de_distrito.value)] += 1

            # ordenar dicionário por número de distritos construídos de cada tipo
            qtd_distritos_cada_tipo = dict(sorted(qtd_distritos_cada_tipo.items(), key=lambda item: item[1], reverse=True))

            # criar lista de preferência de escolha de personagem
            lista_preferencia_personagens = []
            for chave, valor in qtd_distritos_cada_tipo.items():
                if chave == '0': lista_preferencia_personagens.append("Bispo")
                elif chave == '1': lista_preferencia_personagens.append("Senhor da Guerra")
                elif chave == '2': lista_preferencia_personagens.append("Rei")
                elif chave == '3': lista_preferencia_personagens.append("Comerciante")

            # Religioso = 0
            # Militar = 1
            # Nobre = 2
            # Comercial = 3
            # Especial = 4

            # escolher o menor indice possível da lista de personagens
            for nome_personagem in lista_preferencia_personagens:
                for posicao, escolha_personagem in enumerate(estado.tabuleiro.baralho_personagens):
                    if escolha_personagem.nome == nome_personagem:
                        debug(f"Personagem escolhido pela preferência: {escolha_personagem.nome}")
                        return posicao


            debug("Estratégia - farming\t\tPersonagem: aleatório")
            return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

        # sem estratégia
        else:
            # print("Estratégia - nenhuma\t\tPersonagem: aleatório")
            return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        index_jogador = -1
        for index, jog in enumerate(estado.jogadores):
            # print(jog.nome)
            if jog.nome == 'Bot - Eduardo':
                index_jogador = index

        if index_jogador == -1:
            print("ERRO----------------------------------------------------------------------------------------")
            time.sleep(150)


        if len(acoes_disponiveis) > 1:

            # decisão de cartas ou ouro
            if len(acoes_disponiveis) == 2 and acoes_disponiveis[0] == TipoAcao.ColetarOuro:
                if len(estado.jogadores[index_jogador].cartas_distrito_mao) < 2:
                    debug("Escolheu cartas...")
                    return 1 # coletar carta
                else:
                    debug("Escolheu ouro...")
                    return 0 # coletar ouro

            for index_acao, acao in enumerate(acoes_disponiveis):

                if acao.value == TipoAcao.ConstruirDistrito:
                    return index_acao # construir distrito


            debug("Ação escolhida: Aleatória.")
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
