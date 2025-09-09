import csv
import os
import sys
from matplotlib import pyplot as plt
import seaborn as sns
from classes.classification.ClassificaEstados import ClassificaEstados
from classes.Simulacao import Simulacao
from classes.classification.SimulacaoColeta import SimulacaoColeta
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.strategies.Estrategia import Estrategia
from classes.strategies.EstrategiaAllin import EstrategiaAllin
from classes.strategies.EstrategiaAndrei import EstrategiaAndrei
from classes.strategies.EstrategiaBuild import EstrategiaBuild
from classes.strategies.EstrategiaDjonatan import EstrategiaDjonatan
from classes.strategies.EstrategiaEduardo import EstrategiaEduardo
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaFrequency import EstrategiaFrequency
from classes.strategies.EstrategiaGold import EstrategiaGold
from classes.strategies.EstrategiaJean import EstrategiaJean
from classes.strategies.EstrategiaLuis import EstrategiaLuisII
from classes.Experimento import Experimento
import pandas as pd
import numpy as np
import random
from itertools import combinations, combinations_with_replacement
from math import comb

estrategias: list[Estrategia] = [EstrategiaAndrei(), EstrategiaDjonatan(), EstrategiaEduardo(),
                                 EstrategiaFelipe(), EstrategiaJean(), EstrategiaLuisII(), 
                                 EstrategiaTotalmenteAleatoria()] #MCTS e Agente off, levar para ColetaEstados e adaptar
# estrategias: list[Estrategia] = [Agente(imprimir=True), EstrategiaTotalmenteAleatoria("B2"), EstrategiaTotalmenteAleatoria("B3"), EstrategiaTotalmenteAleatoria("B4"), EstrategiaTotalmenteAleatoria("B5")]
combinacoes = list(combinations_with_replacement(estrategias, 5))

qtd_comb = len(combinacoes)

pasta = r"C:\Users\djona\Programação\siradels\classes\classification\samples\sample_by_round"
arquivos = [f"X_progress_20.csv", f"X_progress_40.csv", f"X_progress_60.csv", f"X_progress_80.csv", f"X_progress_100.csv",
            f"Y_progress_20.csv", f"Y_progress_40.csv", f"Y_progress_60.csv", f"Y_progress_80.csv", f"Y_progress_100.csv"]

#os.makedirs(pasta, exist_ok=True)

#print("Quantidade de Combinações:", qtd_comb)

class ColetaEstados:
    @staticmethod
    def coleta_amostras(n_features: int, jogos: str, rotulos: str, nome_modelo: str = '', qtd_simulacao: int = 25):
        X_inicial = [np.zeros(n_features)]
        X = X_inicial
        Y = []
        num_simulacao = 0

        # Inicializa dicionários de resultados
        resultados_total: dict[str, (int, int, int, int, int, int, int)] = dict()
        resultados: dict[str, (int, int, int, int, int, int)] = dict()
        for arquivo in arquivos:
            caminho = os.path.join(pasta, arquivo)
            with open(caminho, 'w', newline='') as f:
                pass  # só cria/trunca o arquivo, limpa o conteúdo

        # Inicializa resultados para cada estratégia
        for i, jogador in enumerate(estrategias):
            chave = f"{jogador.nome}"
            resultados[chave] = (0, 0, 0, 0, 0, 0)
            resultados_total[chave] = (0, 0, 0, 0, 0, 0, 0)  # Para o total

        while num_simulacao < qtd_simulacao:
            print(f"Simulação {num_simulacao+1}/{qtd_simulacao}")

            """ for i, p in enumerate(combinacoes):
                # Executa simulação com a combinação de estratégias
                simulacao = SimulacaoColeta(list(p))
                estado_final, X_coleta, Y_coleta, n_rodada = simulacao.rodar_simulacao(X_inicial, nome_modelo)
                # Remove a primeira linha nula e empilha as amostras
                X_coleta = np.delete(X_coleta, 0, axis=0)
                X = np.vstack((X, X_coleta))

                # Armazena rótulos
                Y.extend(Y_coleta for _ in range(n_rodada)) """
                
            for i, p in enumerate(combinacoes):
                Y = []
                simulacao = SimulacaoColeta(list(p))
                estado_final, X_coleta, Y_coleta, n_rodada = simulacao.rodar_simulacao(X_inicial, nome_modelo)

                X_coleta = np.delete(X_coleta, 0, axis=0)
                Y.extend(Y_coleta for _ in range(n_rodada))

                for r in range(n_rodada):

                    divisao = (n_rodada+1) / 5
                    if r < divisao:
                        nome_arquivo = "progress_20.csv"
                    elif r < 2 * divisao:
                        nome_arquivo = "progress_40.csv"
                    elif r < 3 * divisao:
                        nome_arquivo = "progress_60.csv"
                    elif r < 4 * divisao:
                        nome_arquivo = "progress_80.csv"
                    else:
                        nome_arquivo = "progress_100.csv"

                    arq_X = os.path.join(pasta, f"X_{nome_arquivo}")
                    arq_Y = os.path.join(pasta, f"Y_{nome_arquivo}")

                    #print(n_rodada, r, X_coleta[r], Y)

                    with open(arq_X, 'a', newline='') as fx:
                        csv.writer(fx).writerow(X_coleta[r])

                    with open(arq_Y, 'a', newline='') as fy:
                        csv.writer(fy).writerow([Y[r]]) 
                    #print(f"Rodada {r+1} de {n_rodada} gravando em {nome_arquivo}")

                    #assert len(X_coleta) == len(Y), f"Tamanhos diferentes: {len(X_coleta)} vs {len(Y)}"

                # Atualiza os resultados da simulação
                for jogador in estado_final.jogadores:
                    chave = f"{jogador.nome}"
                    (vitoria, seg, ter, qua, qui, pontuacao) = resultados[chave]
                    
                    # Atualiza as posições e pontuações de acordo com o estado final da simulação
                    if jogador == estado_final.jogadores[1]:
                        seg += 1
                    elif jogador == estado_final.jogadores[2]:
                        ter += 1
                    elif jogador == estado_final.jogadores[3]:
                        qua += 1
                    elif jogador == estado_final.jogadores[4]:
                        qui += 1

                    resultados[chave] = (int(jogador.vencedor) + vitoria, seg, ter, qua, qui, jogador.pontuacao_final + pontuacao)
            
            # Conta quantas vezes uma estratégia apareceu em uma lista para a combinação
            # Conta participações reais por jogador nas combinações
            participacoes_simulacao = {estrategia.nome: 0 for estrategia in estrategias}
            for combinacao in combinacoes:
                for jogador in combinacao:
                    participacoes_simulacao[jogador.nome] += 1

            num_simulacao += 1

            # Acumula os resultados de todas as simulações
            for jogador, resultado in resultados.items():
                (vitoria, seg, ter, qua, qui, pontuacao) = resultado
                vitoria += resultados_total[jogador][0]
                seg += resultados_total[jogador][1]
                ter += resultados_total[jogador][2]
                qua += resultados_total[jogador][3]
                qui += resultados_total[jogador][4]
                pontuacao += resultados_total[jogador][5]
                participacoes = resultados_total[jogador][6] + participacoes_simulacao[jogador]

                resultados_total[jogador] = (vitoria, seg, ter, qua, qui, pontuacao, participacoes)

        # Calcula estatísticas finais para cada jogador
        resultados_jogadores = {}
        for jogador, resultado in resultados_total.items():
            (vitoria, seg, ter, qua, qui, pontuacao, qtd_simulacao_total) = resultado
            pontuacao_media = pontuacao / qtd_simulacao_total
            taxa_vitoria = 100 * vitoria / qtd_simulacao_total
            taxa_seg = 100 * seg / qtd_simulacao_total
            taxa_ter = 100 * ter / qtd_simulacao_total
            taxa_qua = 100 * qua / qtd_simulacao_total
            taxa_qui = 100 * qui / qtd_simulacao_total
            resultados_jogadores[jogador] = {
                'Victories': vitoria,
                'Win Rate': taxa_vitoria,
                'Avg Ponctuation': pontuacao_media,
                'First Rate': taxa_vitoria,
                'Second Rate': taxa_seg,
                'Third Rate': taxa_ter,
                'Fourth Rate': taxa_qua,
                'Fifth Rate': taxa_qui
            }
            print(
                f'\n{jogador} - Vitórias: {vitoria} - Taxa de Vitórias: {taxa_vitoria:.2f}% - Pontuação Média: {pontuacao_media:.2f}\n\t'
                f'Primeiro: {taxa_vitoria:5.2f}%\n\tSegundo : {taxa_seg:5.2f}%\n\tTerceiro: {taxa_ter:5.2f}%\n\tQuarto  : {taxa_qua:5.2f}%\n\tQuinto  : {taxa_qui:5.2f}%'
            )
        print("Fim dos testes das estratégias")

        # Remove primeira linha nula
        X = np.delete(X, 0, axis=0)
        ClassificaEstados.salva_testes(resultados_jogadores,"./classes/classification/results/Resultado da Coleta")
        #ClassificaEstados.salvar_amostras(X, Y, jogos, rotulos)
        #ClassificaEstados.treinar_modelo(X, Y)

    @staticmethod
    def correlacao():
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd

        # Ler dados
        dados = pd.read_csv('./classes/classification/samples/Jogos 30f 04-10-2024.csv', header=None)
        rotulos = pd.read_csv('./classes/classification/samples/Rótulos 30f 04-10-2024.csv', header=None, names=['label'])

        dados['label'] = rotulos['label']

        # Selecionar apenas as features (colunas 0 a 29)
        features = dados.iloc[:, 0:30]
        features.columns = range(1, 31)  # renomear colunas 1-30

        # Correlação das features com o label
        correlacoes = dados.corr()['label'].drop('label')
        correlacoes.index = range(1, 31)

        # Matriz de correlação entre features
        matriz_corr = features.corr()

        # Salvar CSV
        with open('./classes/classification/samples/correlation/correlação.csv', 'w') as f:
            correlacoes.to_csv(f)
            f.write('\n')
            matriz_corr.to_csv(f)

        # Configuração da paleta Nature-friendly e dpi
        sns.heatmap(matriz_corr, cmap='plasma_r', center=0, annot=True)

        # Heatmap da matriz de correlação
        plt.figure(figsize=(12,10), dpi=300)
        sns.heatmap(matriz_corr, cmap='plasma_r', center=0, annot=False)
        plt.title('Feature Correlation Heatmap')
        plt.tight_layout()
        plt.savefig('./classes/classification/samples/correlation/heatmap_correlacao.png', dpi=300)
        plt.close()

        # Heatmap da correlação com o label
        plt.figure(figsize=(12,10), dpi=300)
        sns.heatmap(pd.DataFrame(correlacoes), cmap='plasma_r', center=0, annot=True, cbar=True)
        plt.title('Feature-Label Correlation')
        plt.tight_layout()
        plt.savefig('./classes/classification/samples/correlation/heatmap_correlacao_label.png', dpi=300)
        plt.close()