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
DEBUG = True
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


            # debug("---------------------------------| Status Partida |--------------------------------------")
            # # for posicao, personagem in enumerate(estado.tabuleiro.baralho_personagens):
            # #     if personagem.nome in preferencia_personagem:
            # #         print(f"Estratégia: Farming\t\tPersonagem: {personagem.nome}")
            # #         return posicao
            # debug(f"rodada: {estado_final.rodada}\t\tturno: {estado_final.turno}")
            # debug(f"Ouro: ")
            # for jogador in estado_final.jogadores:
            #     debug(
            #         f"{jogador.nome}\t\t\touro: {jogador.ouro}\tpontos: {jogador.pontuacao} distritos_na_mão: {len(jogador.cartas_distrito_mao)}")
            #     for dist in jogador.distritos_construidos:
            #         debug(
            #             f"\t\tDistrito: {dist.nome_do_distrito}\t\t\tValor:{dist.valor_do_distrito}")
            # debug("------------------------------------------------------------------------------------------------ ")


            for jogador in estado_final.jogadores:
                (vitoria, pontuacao) = resultados[jogador.nome]
                resultados[jogador.nome] = (int(jogador.vencedor) + vitoria, jogador.pontuacao_final + pontuacao)
        print()
        print("Resultados |------------------------------------------------------------------------------------------------")
        print(f"Num de partidas: {qtd_simulacao_maximo}")
        for jogador, resultado in resultados.items():
            (vitoria, pontuacao) = resultado
            pontuacao_media = pontuacao / qtd_simulacao

            print(
                f'{jogador} - \tVitórias: {vitoria} - Porcento Vitorias: {vitoria / qtd_simulacao * 100:.2f}% - Pontuação Média: {pontuacao_media}')

    # Inicializa o treinamento do modelo do zero e treina durante o tempo limite em segundos
    # def treinar_modelo_mcts(self, tempo_limite: int):
    #     inicio = time.time()
    #     # Fixado quantidade de jogadores em 5
    #     qtd_jogadores = 5
    #     mcts = EstrategiaMCTS(self.caminho, 0)
    #     estrategias = [mcts]
    #     for i in range(qtd_jogadores - 1):
    #         estrategias.append(EstrategiaTotalmenteAleatoria(str(i + 1)))
    #     while tempo_limite > time.time() - inicio:
    #         for tipo_tabela in TipoTabela:
    #             # Treinamento individual por tipo de tabela
    #             mcts.tipo_tabela = tipo_tabela
    #             mcts.iniciar_historico()
    #             # Cria simulação
    #             simulacao = Simulacao(estrategias)
    #             # Executa simulação
    #             estado_final = simulacao.rodar_simulacao()
    #             # Atualizar modelo com vitórias e ações escolhidas
    #             for jogador in estado_final.jogadores:
    #                 if jogador.nome == 'Bot - MCTS':
    #                     if jogador.vencedor:
    #                         for modelo, historico in zip(mcts.modelos_mcts, mcts.modelos_historico):
    #                             for tabela, tabela_hist in zip(modelo, historico):
    #                                 tabela += tabela_hist
    #                     else:
    #                         for modelo, historico in zip(mcts.modelos_mcts, mcts.modelos_historico):
    #                             metade_tabela = int(modelo[0].shape[1] / 2)
    #                             for tabela, tabela_hist in zip(modelo, historico):
    #                                 tabela[:, metade_tabela:] += tabela_hist[:, metade_tabela:]
    #         mcts.salvar_modelos()
    #
    # # Salva o resultado das simulações em arquivos CSV
    # # Refatorar
    # def salvar_resultado(self, resultados: dict[str, (int, int)], qtd_simulacao_treino, qtd_simulacao_teste):
    #     dados = []
    #     for jogador, resultado in resultados.items():
    #         (vitoria, pontuacao) = resultado
    #         pontuacao_media = pontuacao / qtd_simulacao_teste
    #         dados.append([jogador, vitoria, vitoria / qtd_simulacao_teste, pontuacao_media])
    #
    #     np.savetxt(self.caminho + '/simulacoes/' + str(qtd_simulacao_treino) + '.csv', np.array(dados), delimiter=',', fmt='%s')
