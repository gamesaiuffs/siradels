import os
import time

from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoDistrito import TipoDistrito
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

def verificar_possibilidade_construir_distritos(estado: Estado) -> bool:
    # Identifica distritos que podem ser construídos
    distritos_para_construir: list[CartaDistrito] = []
    # Identifica opções especiais para construir o covil dos ladrões (divisão do custo em ouro e cartas da mão)
    distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)] = []
    # Identifica se o jogador construiu a Fábrica (afeta custo dos distritos especiais)
    fabrica = estado.jogador_atual.construiu_distrito('Fábrica')
    # Identifica se o jogador construiu a Pedreira (adiciona opções de construção repetida)
    pedreira = estado.jogador_atual.construiu_distrito('Pedreira')
    # Enumera opções de construção
    for carta in estado.jogador_atual.cartas_distrito_mao:
        # Distritos repetidos não podem ser construídos (a não ser que tenha construído a Pedreira)
        repetido = estado.jogador_atual.construiu_distrito(carta.nome_do_distrito)
        if repetido and not pedreira:
            continue
        # Deve possuir ouro suficiente para construir o distrito (Fábrica dá desconto para distritos especiais)
        if carta.valor_do_distrito <= estado.jogador_atual.ouro or \
                (fabrica and carta.tipo_de_distrito == TipoDistrito.Especial and carta.valor_do_distrito - 1 <= estado.jogador_atual.ouro):
            distritos_para_construir.append(carta)
        # O covil dos ladrões pode ser construído com um custo misto de ouro e cartas da mão
        if carta.nome_do_distrito == 'Covil dos Ladrões':
            qtd_cartas = len(estado.jogador_atual.cartas_distrito_mao) - 1
            # Não é necessário ter mais que 6 cartas no pagamento, pois o custo do distrito é 6 (5 com fábrica)
            if qtd_cartas > 6:
                qtd_cartas = 6
            if fabrica and qtd_cartas > 5:
                qtd_cartas = 5
            qtd_ouro = carta.valor_do_distrito - 1
            # Fábrica concede 1 de desconto para distritos especiais
            if fabrica:
                qtd_ouro -= 1
            while qtd_ouro + qtd_cartas >= carta.valor_do_distrito:
                if qtd_ouro > estado.jogador_atual.ouro:
                    qtd_ouro -= 1
                    continue
                distritos_para_construir_covil_ladroes.append((carta, qtd_ouro, carta.valor_do_distrito - qtd_ouro))
                if qtd_ouro > 0:
                    qtd_ouro -= 1
                else:
                    qtd_cartas -= 1
    # Verifica se é possível construir ao menos 1 distrito da mão
    # print("Lens: ", len(distritos_para_construir), len(distritos_para_construir_covil_ladroes))
    if len(distritos_para_construir) + len(distritos_para_construir_covil_ladroes) == 0:
        return False
    else:
        return True

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

            # criar estratégia para decidir se deve construir ou juntar mais ouro


    # Religioso = 0
    # Militar = 1
    # Nobre = 2
    # Comercial = 3
    # Especial = 4

    BonusFimJogo = 4   # adotar se estiver à frente no jogo
        # foco - distritos variádos
        # foco - distritos com bônus de fim de jogo
        # foco - ações que rendem pontuação extra


# usar o estado para recalcular a estratégia e retorná-la - a função da classe estratégia fica responsável por escolher a ação
def calcularEstrategiaGeral(estado: Estado):
    # estratégia inicial
    debug("\n---------------------------------------| Escolha de estratégia |-------------------------------- ")
    debug(f"rodada: {estado.rodada}\t\tturno: {estado.turno}")
    debug(f"Ouro: ")
    for jogador in estado.jogadores:
        debug(f"{jogador.nome}\t\t\touro: {jogador.ouro}\tpontos: {jogador.pontuacao}")
    debug("------------------------------------------------------------------------------------------------ \n")

    return Estrategias.Farming.value


class EstrategiaEduardo(Estrategia):
    def __init__(self, nome: str = 'Eduardo'):
        super().__init__(nome)

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
            # Preferência para personagens com bônus de ouro
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
                        debug(f"\nFarming - Personagem escolhido pela preferência: {escolha_personagem.nome}")
                        return posicao


            debug("\nFarming\t\tPersonagem: aleatório")
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

        # for acao in acoes_disponiveis:
        #     print(acao.name, end=" ")
        # print()

        # decisão de cartas ou ouro
        if len(acoes_disponiveis) == 2 and acoes_disponiveis[0] == TipoAcao.ColetarOuro:
            if len(estado.jogadores[index_jogador].cartas_distrito_mao) < 2:
                debug("\nEscolheu cartas...")
                return 1 # coletar carta
            else:
                debug("\nEscolheu ouro...")
                return 0 # coletar ouro


        for index_acao, acao in enumerate(acoes_disponiveis):

            # Usar habilidade ladrão --------------------------------------------------------------
            if acao.value == TipoAcao.HabilidadeLadrao.value:
                pass

            # Usar habilidades ilusionista  --------------------------------------------------------------
            elif acao.value == TipoAcao.HabilidadeIlusionistaTrocar.value:
                pass

            elif acao.value == TipoAcao.HabilidadeIlusionistaDescartar.value:
                pass

            # Usar habilidade rei --------------------------------------------------------------
            elif acao.value == TipoAcao.HabilidadeRei.value:
                debug("Ação escolhida: Coletar ouro rei")
                return index_acao

            # Usar habilidade Bispo --------------------------------------------------------------
            elif acao.value == TipoAcao.HabilidadeBispo.value:
                debug("Ação escolhida: Coletar ouro bispo")
                return index_acao

            # Usar habilidade comerciante --------------------------------------------------------------
            elif acao.value == TipoAcao.HabilidadeComerciante.value:
                debug("Ação escolhida: Coletar ouro comerciante")
                return index_acao

            # Usar habilidade senhor da guerra  --------------------------------------------------------------
            elif acao.value == TipoAcao.HabilidadeSenhorDaGuerraColetar.value:
                debug("Ação escolhida: Coletar ouro sr guerra")
                return index_acao

            # contruir distrito ou não --------------------------------------------------------------
            elif acao.value == TipoAcao.ConstruirDistrito.value:
                # estratégia de escolha - valor médio maior do que numero de ouros ---------------------------
                valor_dist, contador, dists_para_construir= 0, 0, 0
                for distrito in estado.jogador_atual.cartas_distrito_mao:
                    valor_dist += distrito.valor_do_distrito
                    contador += 1

                # debug(f"AQUI: Valor tot: {valor_dist} qtd: {contador} Resultado: {valor_dist // contador} qtd_ouro: {estado.jogador_atual.ouro}")
                if contador != 0:
                    if (valor_dist // contador) < estado.jogador_atual.ouro:
                        debug("Ação escolhida: Construir distrito")
                        # print("index", index_acao, acao.name)
                        return index_acao

            elif acao.value == TipoAcao.HabilidadeSenhorDaGuerraDestruir.value:
                pass

            # Usar habilidade comerciante --------------------------------------------------------------
            elif acao.value == TipoAcao.Laboratorio.value:
                pass

            # Usar habilidade comerciante --------------------------------------------------------------
            elif acao.value == TipoAcao.Forja.value:
                pass

        # debug("\nAção escolhida: Passar turno\nHabilidades restantes: ")
        # for acao_restante in acoes_disponiveis:
        #     debug(f"\t{acao_restante.name}")
        # debug("----------------------------------------------------------------------------------------\n")
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

        # print("Distritos para construir covil ladrões: ", distritos_para_construir_covil_ladroes, tamanho_maximo)

        index_jogador = -1
        for index, jog in enumerate(estado.jogadores):
            # print(jog.nome)
            if jog.nome == 'Bot - Eduardo':
                index_jogador = index

        if index_jogador == -1:
            debug("ERRO----------------------------------------------------------------------------------------")
            time.sleep(150)

        if estado.jogador_atual.nome == estado.jogadores[index_jogador].nome:
            debug(f"Nome jogador: {estado.jogador_atual.nome} Ouros: {estado.jogador_atual.ouro}")
            debug("\ndist para construir ---------------------")
            for distrito in distritos_para_construir:
                debug(f"nome: {distrito.nome_do_distrito}\t\ttipo: {distrito.tipo_de_distrito}\t\tvalor: {distrito.valor_do_distrito}\t\tquantidade: {distrito.quantidade}")
            debug("dist na mão ---------------------")
            for distrito in estado.jogador_atual.cartas_distrito_mao:
                debug(f"nome: {distrito.nome_do_distrito}\t\ttipo: {distrito.tipo_de_distrito}\t\tvalor: {distrito.valor_do_distrito}\t\tquantidade: {distrito.quantidade}")
            debug("\n")
        # escolher distrito na seguinte ordem de preferência - Farming:
        # especial, comercial, nobre, militar, religioso
        # preferencia_escolha_dist_construir_farming = [
        #                                         TipoDistrito.Comercial.value,
        #                                         TipoDistrito.Especial.value,
        #                                         TipoDistrito.Nobre.value,
        #                                         TipoDistrito.Militar.value,
        #                                         TipoDistrito.Religioso.value
        #                                     ]

        # escolher construir distrito mais caro disponível ---------------------------------------------------------------------------------------------
        maior = -1
        for index, dist in enumerate(distritos_para_construir):
            if dist.valor_do_distrito > distritos_para_construir[maior].valor_do_distrito:
                maior = index

        # debug(f"\nDistrito construido: {distritos_para_construir[maior].nome_do_distrito}\n")
        if maior != -1: return maior

        # preferencia_escolha_dist_construir_por_valor =

        # escolha inicial - pega o primeiro que dá pra construir na ordem de preferência ----------------------------------------------------------------
            # criar estratégia para decidir se deve construir ou juntar mais ouro
        # for preferencia in preferencia_escolha_dist_construir_farming:
        #     for pos, distrito in enumerate(distritos_para_construir):
        #             # print("construído: -------------------------------")
        #         if distrito.tipo_de_distrito.value == preferencia:
        #             # print(f"preferência: {preferencia}\t\tdistrito: {distrito.nome_do_distrito}\t\tTipo: {distrito.tipo_de_distrito}")
        #             # os.system("pause")
        #             return pos


        # estratégia inicial - escolha aleatória ---------------------------------------------------------------------------------------------------------
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
