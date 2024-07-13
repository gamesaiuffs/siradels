import subprocess
import time
import numpy as np

from classes.Simulacao import Simulacao
from classes.enum.TipoTabela import TipoTabela
from classes.strategies.Estrategia import Estrategia
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from subprocess import run
import os

QTD_SIMULACOES = 10000
DEBUG = False
DEBUG_TIME = False

PORCENTAGEM = True
COMANDO_CLEAR = "cls"

import time
import os

def debugTime():
    if DEBUG_TIME:
        time.sleep(5)


def debug(message: str):
    if (DEBUG):
        print(message)
class Experimento:

    def __init__(self, caminho: str):
        self.caminho = caminho

    @staticmethod
    def testar_estrategias(estrategias: list[Estrategia], qtd_simulacao_maximo: int = QTD_SIMULACOES):
        qtd_simulacao = 1
        resultados: dict[str, (int, int)] = dict()
        # Cria simulação
        simulacao = Simulacao(estrategias)
        # Executa simulação
        estado_final = simulacao.rodar_simulacao()
        for jogador in estado_final.jogadores:
            resultados[jogador.nome] = (int(jogador.vencedor), jogador.pontuacao_final)
        if PORCENTAGEM:
            os.system(COMANDO_CLEAR)
            print(f"Rodando simulações: [{QTD_SIMULACOES} rodadas]")
        while qtd_simulacao < qtd_simulacao_maximo:
            qtd_simulacao += 1
            # limpar_console()

            # run("cls", shell=True)

            # print("Rodando simulações... ")
            if PORCENTAGEM: print(f"Progresso: {str(100 * qtd_simulacao // qtd_simulacao_maximo)}%", end="\r")

            # Cria simulação
            simulacao = Simulacao(estrategias)
            # Executa simulação
            estado_final = simulacao.rodar_simulacao()

            for jogador in estado_final.jogadores:
                (vitoria, pontuacao) = resultados[jogador.nome]
                resultados[jogador.nome] = (int(jogador.vencedor) + vitoria, jogador.pontuacao_final + pontuacao)
        print()
        os.system("pause")
        print("Resultados |------------------------------------------------------------------------------------------------")
        print(f"Num de partidas: {qtd_simulacao_maximo}")
        for jogador, resultado in resultados.items():
            (vitoria, pontuacao) = resultado
            pontuacao_media = pontuacao / qtd_simulacao

            print(
                f'{jogador} - \tVitórias: {vitoria} - Porcento Vitorias: {vitoria / qtd_simulacao * 100:.2f}% - Pontuação Média: {pontuacao_media}')

