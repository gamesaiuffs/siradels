from classes.classification.ClassificaEstados import ClassificaEstados
from classes.Simulacao import Simulacao
from classes.classification.SimulacaoColeta import SimulacaoColeta
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
import numpy as np
import random


class ColetaEstados:
    @staticmethod
    def coleta_amostras(qtd_partidas: int, n_features: int, jogos: str, rotulos: str):
        X_inicial = [np.zeros(n_features)]
        X = X_inicial
        Y = []

        qtd_simulacao = 0
        while qtd_simulacao < qtd_partidas:
            for qtd_jogadores in range(5, 6):       ## ajustar quantidade de jogadores (original: range(4,7))
                qtd_simulacao += 1
                
                # Inicializa variaveis para nova simulacao do jogo
                estrategias = []
                
                for i in range(qtd_jogadores):          # fixo em 5 players
                    estrategias.append(EstrategiaTotalmenteAleatoria(str(i+1)))
                
                # Estrategias fixas e especificas
                '''
                estrategias.append(EstrategiaDjonatan())
                estrategias.append(EstrategiaAndrei())
                estrategias.append(EstrategiaBernardo())
                estrategias.append(EstrategiaFelipe())
                estrategias.append(EstrategiaGustavo())
                estrategias.append(EstrategiaJoao())
                '''
                # Cria simulacao
                simulacao = SimulacaoColeta(estrategias)
                # Executa simulacao
                X_coleta, Y_coleta, n_rodada = simulacao.rodar_simulacao(X_inicial)
                print(n_rodada)
                # Remove primeira linha nula
                X_coleta = np.delete(X_coleta, 0, axis=0)
                # Empilha linhas na matriz
                X = np.vstack((X, X_coleta))
                # Atrubui rótulos de acordo com a quantidade de rodadas
                for i in range(n_rodada):
                    Y.append(Y_coleta)
        # Remove primeira linha nula
        X = np.delete(X, 0, axis=0)
        ClassificaEstados.salvar_resultados(X, Y, jogos, rotulos)
        #ClassificaEstados.treinar_modelo(X, Y)
