import os
import time
from classes.strategies.estrategiaEduardoUtils.funcoesDebug.debug import *
from classes.strategies.estrategiaEduardoUtils.funcoesPeso.pesoDistritosParaConstruir import *

from classes.strategies.estrategiaEduardoUtils.estrategiaEscolhaEstrategia import Estrategias
from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoDistrito import TipoDistrito
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random
from enum import Enum

def pesosDistritosParaConstruir(estado: Estado, distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)], estado_interno: dict):
    if len(distritos_para_construir) == 0:
        return -1

    posicao_melhor = -1
    peso_melhor = -1

    for pos, dist in enumerate(distritos_para_construir):
        peso = 0

        # FARMING
        if estado_interno["estrategia"] == Estrategias.Farming.value:
            # valor distrito - += valor
            peso += dist.valor_do_distrito

            # ainda n deste tipo - += 3
            if estado_interno["qtd_tipos_distritos"][str(dist.tipo_de_distrito.value)] == 0:
                peso += 3

            # gera renda passiva - += 2
            if dist.tipo_de_distrito.value in [TipoDistrito.Nobre.value, TipoDistrito.Comercial.value, TipoDistrito.Religioso.value, TipoDistrito.Militar.value]:
                peso += 2

            # tipo especial - += 1
            if dist.tipo_de_distrito.value == TipoDistrito.Especial.value:
                peso += 3

            if peso > peso_melhor:
                peso_melhor = peso
                posicao_melhor = pos

    # debug(f"Confirmação escolha distrito: {distritos_para_construir[posicao_melhor].nome_do_distrito}")

    return posicao_melhor

