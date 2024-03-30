import time

from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random
from enum import Enum

DEBUG = True
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


        # foco - escolher personagem com bonus de renda
            # rei
            # comerciante
            # bispo
            # senhor da guerra

        # distritos estratégicos
            # escola de magia - mantém cartas compradas
            # laboratório - troca 1 carta por 2 ouros
            # pedreira - construír distritos iguais

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
    

    # if estado.rodada == 1:
    #     return Estrategias.Farming.value[0]
    #
    # # se: vários distritos comerciais na conta -> farming
    #
    #
    # # estratégia geral
    # else:
    #     return Estrategias.BonusFimJogo.value[0]
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
                # - rel, mil, nob, com, (-esp)
            # qtd_distritos_cada_tipo = [0, 0, 0, 0, 0]
            # print("---------------------------- debug calculo distritos ----------------------------------")
            # print(f"Distritos construídos: {estado.jogadores[index_jogador].distritos_construidos}")
            qtd_distritos_cada_tipo = {
                "0": 0,
                "1": 0,
                "2": 0,
                "3": 0,
                "4": 0
            }

            # print("Dict inicial: ", qtd_distritos_cada_tipo)

            # mapear quantos distritos de cada tipo foram construídos
            for dist in estado.jogadores[index_jogador].distritos_construidos:
                # print("dist add: ", dist.nome_do_distrito)
                qtd_distritos_cada_tipo[str(dist.tipo_de_distrito.value)] += 1

            # print("Dict mapeado: ", qtd_distritos_cada_tipo)

            qtd_distritos_cada_tipo = dict(sorted(qtd_distritos_cada_tipo.items(), key=lambda item: item[1], reverse=True))
            # print("Dict mapeado ordenado: ", qtd_distritos_cada_tipo)
            #
            # print("---------------------------- /debug calculo distritos ----------------------------------")

            # print("Essa linha aqui: ", qtd_distritos_cada_tipo)
            # time.sleep(3)

            # criar lista de preferência de escolha de personagem
            lista_preferencia_personagens = []
            for chave, valor in qtd_distritos_cada_tipo.items():
                if chave == '0': lista_preferencia_personagens.append("Bispo")
                elif chave == '1': lista_preferencia_personagens.append("Senhor da Guerra")
                elif chave == '2': lista_preferencia_personagens.append("Rei")
                elif chave == '3': lista_preferencia_personagens.append("Comerciante")

            # print("Lista de preferências: ", lista_preferencia_personagens)


            # Religioso = 0
            # Militar = 1
            # Nobre = 2
            # Comercial = 3
            # Especial = 4

            # escolher o menor indice possível da lista de personagens

            # print("------------------------- Escolha de personagem ---------------------------------------------")
            for nome_personagem in lista_preferencia_personagens:
                for posicao, escolha_personagem in enumerate(estado.tabuleiro.baralho_personagens):
                    # print(posicao, escolha_personagem.nome, nome_personagem)
                    if escolha_personagem.nome == nome_personagem:
                        debug(f"Personagem escolhido pela preferência: {escolha_personagem.nome}")
                        # time.sleep(3)
                        return posicao
            # print("------------------------- Fim Escolha de personagem ---------------------------------------------")


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

            # if TipoAcao.ColetarOuro in acoes_disponiveis:
            #     if random.randint(0, 9) == 0:
            #         return 1
            #     else:
            #         return 0



            # for index_acao, acao in enumerate(acoes_disponiveis):
            #     # #codigo de coleta de ouro / carta antigo (90% vitória)
            #     # if acao.value == TipoAcao.ColetarOuro.value and estado.jogadores[index_jogador].ouro <= 2:
            #     #     debug("Ação escolhida: Coletar ouro")
            #     #     return index_acao # coletar ouro
            #     # if acao.value == TipoAcao.ColetarCartas.value and len(estado.jogadores[index_jogador].cartas_distrito_mao) < 2:
            #     #     debug("Ação escolhida: Coletar cartas")
            #     #     return index_acao # comprar carta
            #
            #     # codigo de coleta de ouro / carta novo
            #     if acao.value == TipoAcao.ColetarCartas.value and len(estado.jogadores[index_jogador].cartas_distrito_mao) < 4:
            #         debug("Ação escolhida: Coletar cartas")
            #         return TipoAcao.ColetarCartas.value  # comprar carta
            #     else:
            #         debug("Ação escolhida: Coletar ouro")
            #         return TipoAcao.ColetarOuro.value  # coletar ouro

            if len(acoes_disponiveis) == 2 and acoes_disponiveis[0] == TipoAcao.ColetarOuro:
                if len(estado.jogadores[index_jogador].cartas_distrito_mao) < 2:
                    debug("Escolheu cartas...")
                    return 1 # coletar carta
                else:
                    debug("Escolheu ouro...")
                    return 0 # coletar ouro

                # < 3 - valor testado - pg 3 documento de notas
                # if acao.value == 1 and estado.jogadores[index_jogador].ouro < 3:
                #     return 0 # coletar ouro
                #
                # else:
                #     return 1   # coletar carta

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
