from classes.strategies.estrategiaEduardoUtils.funcoesDebug.debug import *
from enum import Enum
from classes.model.Estado import *

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