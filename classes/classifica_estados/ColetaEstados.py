from classes.classifica_estados.ClassificaEstados import ClassificaEstados
from classes.Simulacao import Simulacao
from classes.classifica_estados.SimulacaoColeta import SimulacaoColeta
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
import numpy as np
import random


class ColetaEstados:
    @staticmethod
    def simula_estados(qtd_partidas: int):

        X = [np.zeros(48)]
        Y = []

        qtd_simulacao = 0
        while qtd_simulacao < qtd_partidas:
            for qtd_jogadores in range(6, 7):       ## ajustar quantidade de jogadores (original: range(4,7))
                qtd_simulacao += 1
                
                # Inicializa variaveis para nova simulacao do jogo
                estrategias = []
                
                for i in range(qtd_jogadores):          # fixo em 6 players
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
                try:
                    X_coleta, Y_coleta = simulacao.rodar_simulacao()

                except:
                    try:
                        estado = simulacao.rodar_simulacao()
                        jogador_aleatorio_idx = random.randint(0, len(estado.jogadores)-1)
                        jogador_aleatorio = estado.jogadores[jogador_aleatorio_idx]
                        nome_coleta = jogador_aleatorio.nome

                        for jogador in estado.jogadores:
                            if jogador.vencedor:
                                jogador_venceu = jogador.nome

                        if jogador_venceu == nome_coleta:
                            Y_coleta = 1
                        else:
                            Y_coleta = 0
        
                        X_coleta = ClassificaEstados.coleta_estados_treino(estado, estado.rodada, nome_coleta, jogador_venceu, 1)
                    except:
                        continue
                X = np.vstack((X, X_coleta))
                Y.append(Y_coleta)

        X = np.delete(X, 0, axis=0)

        print(X)
        ClassificaEstados.salvar_resultados(X, Y)
        ClassificaEstados.treina_modelo(X, Y)
        #ColetaEstadosFinais.calcula_porcentagem(0)
