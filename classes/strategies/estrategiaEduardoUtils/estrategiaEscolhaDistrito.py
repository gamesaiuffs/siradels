import os
import time
from classes.strategies.estrategiaEduardoUtils.funcoesDebug.debug import *
from classes.strategies.estrategiaEduardoUtils.funcoesPeso.pesoDistritosParaConstruir import *


from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoDistrito import TipoDistrito
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random
from enum import Enum


def calcularPesoDistritos(distritos_para_construir: list[CartaDistrito]):
    pass

def estrategiaEscolhaDistrito(estado: Estado, distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)], estado_interno: dict):

    tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_covil_ladroes)

    # print("Distritos para construir covil ladrões: ", distritos_para_construir_covil_ladroes, tamanho_maximo)

    index_jogador = -1
    for index, jog in enumerate(estado.jogadores):
        # print(jog.nome)
        if jog.nome == 'Eduardo':
            index_jogador = index

    if index_jogador == -1:
        debug("ERRO----------------------------------------------------------------------------------------")
        if debugTime: 
            print("Debug time - estrategiaEscolhaDistrito - 37")
            time.sleep(150)

    if estado.jogador_atual.nome == estado.jogadores[index_jogador].nome:
        debug(f"Nome jogador: {estado.jogador_atual.nome} Ouros: {estado.jogador_atual.ouro}")
        debug("\ndist para construir ---------------------")
        for distrito in distritos_para_construir:
            debug(
                f"nome: {distrito.nome_do_distrito}\t\ttipo: {distrito.tipo_de_distrito}\t\tvalor: {distrito.valor_do_distrito}\t\tquantidade: {distrito.quantidade}")
        debug("dist na mão ---------------------")
        for distrito in estado.jogador_atual.cartas_distrito_mao:
            debug(
                f"nome: {distrito.nome_do_distrito}\t\ttipo: {distrito.tipo_de_distrito}\t\tvalor: {distrito.valor_do_distrito}\t\tquantidade: {distrito.quantidade}")
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
    # maior = -1
    # for index, dist in enumerate(distritos_para_construir):
    #     if dist.valor_do_distrito > distritos_para_construir[maior].valor_do_distrito:
    #         maior = index
    #
    # # debug(f"\nDistrito construido: {distritos_para_construir[maior].nome_do_distrito}\n")
    # if maior != -1: return maior

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

    escolha = pesosDistritosParaConstruir(estado, distritos_para_construir, distritos_para_construir_covil_ladroes, estado_interno)
    if escolha != -1:
        return escolha

    # estratégia inicial - escolha aleatória ---------------------------------------------------------------------------------------------------------
    return random.randint(0, tamanho_maximo - 1)