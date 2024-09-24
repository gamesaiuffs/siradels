from classes.classification.ClassificaEstados import ClassificaEstados
from classes.Simulacao import Simulacao
from classes.classification.SimulacaoColeta import SimulacaoColeta
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.strategies.EstrategiaAndrei import EstrategiaAndrei
from classes.strategies.EstrategiaDjonatan import EstrategiaDjonatan
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaLuis import EstrategiaLuisII
import numpy as np
import random
import itertools

estrategias_disponiveis = [EstrategiaDjonatan(), EstrategiaFelipe(), EstrategiaLuisII('luis'), EstrategiaTotalmenteAleatoria('bot-1'), EstrategiaTotalmenteAleatoria('bot-2')]

class ColetaEstados:
    @staticmethod
    def coleta_amostras(qtd_partidas: int, n_features: int, jogos: str, rotulos: str, nome_modelo: str):
        X_inicial = [np.zeros(n_features)]
        X = X_inicial
        Y = []
        qtd_jogadores = 5

        qtd_simulacao = 0

        assert len(estrategias_disponiveis) >= qtd_jogadores, "Estratégias insuficientes para formar combinações."

        combinacoes_estrategias = list(itertools.permutations(estrategias_disponiveis, qtd_jogadores))

        # Verifica se há combinações disponíveis
        if len(combinacoes_estrategias) == 0:
            raise ValueError("Não há combinações de estratégias disponíveis.")


        while qtd_simulacao < qtd_partidas:

            qtd_simulacao += 1
            
            # Inicializa variaveis para nova simulacao do jogo
            estrategias = []
            
            combinacao_atual = combinacoes_estrategias[qtd_simulacao % len(combinacoes_estrategias)]

            for i in range(qtd_jogadores):
                estrategia_classe = combinacao_atual[i]
                estrategias.append(estrategia_classe)
                
            # Cria simulacao
            simulacao = SimulacaoColeta(estrategias)
            # Executa simulacao
            X_coleta, Y_coleta, n_rodada = simulacao.rodar_simulacao(X_inicial, nome_modelo)
            #print(qtd_partidas-qtd_simulacao)
            # Remove primeira linha nula
            X_coleta = np.delete(X_coleta, 0, axis=0)
            # Empilha linhas na matriz
            X = np.vstack((X, X_coleta))
            # Atrubui rótulos de acordo com a quantidade de rodadas
            for i in range(n_rodada):
                Y.append(Y_coleta)
        # Remove primeira linha nula
        X = np.delete(X, 0, axis=0)
        ClassificaEstados.salvar_amostras(X, Y, jogos, rotulos)
        #ClassificaEstados.treinar_modelo(X, Y)
