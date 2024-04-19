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
    if len(distritos_para_construir) + len(distritos_para_construir_covil_ladroes) == 0:
        return False
    else:
        return True