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

print("Quantidade de Combinações:", qtd_comb)

class ColetaEstados:
    @staticmethod
    def coleta_amostras(n_features: int, jogos: str, rotulos: str, nome_modelo: str = '', qtd_simulacao: int = 100):
        X_inicial = [np.zeros(n_features)]
        X = X_inicial
        Y = []
        num_simulacao = 0

        # Inicializa dicionários de resultados
        resultados_total: dict[str, (int, int, int, int, int, int, int)] = dict()
        resultados: dict[str, (int, int, int, int, int, int)] = dict()

        # Inicializa resultados para cada estratégia
        for i, jogador in enumerate(estrategias):
            chave = f"{jogador.nome}"
            resultados[chave] = (0, 0, 0, 0, 0, 0)
            resultados_total[chave] = (0, 0, 0, 0, 0, 0, 0)  # Para o total

        while num_simulacao < qtd_simulacao:
            print(f"Simulação {num_simulacao+1}/{qtd_simulacao}")

            for i, p in enumerate(combinacoes):
                # Executa simulação com a combinação de estratégias
                simulacao = SimulacaoColeta(list(p))
                estado_final, X_coleta, Y_coleta, n_rodada = simulacao.rodar_simulacao(X_inicial, nome_modelo)
                # Remove a primeira linha nula e empilha as amostras
                X_coleta = np.delete(X_coleta, 0, axis=0)
                X = np.vstack((X, X_coleta))

                # Armazena rótulos
                Y.extend(Y_coleta for _ in range(n_rodada))

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
            count = 0
            num_simulacao += 1
            for i in combinacoes:
                for j in i:
                    if j.nome == estrategias[0].nome:
                        count += 1
                        break

            # Acumula os resultados de todas as simulações
            for jogador, resultado in resultados.items():
                (vitoria, seg, ter, qua, qui, pontuacao) = resultado
                vitoria += resultados_total[jogador][0]
                seg += resultados_total[jogador][1]
                ter += resultados_total[jogador][2]
                qua += resultados_total[jogador][3]
                qui += resultados_total[jogador][4]
                pontuacao += resultados_total[jogador][5]
                resultados_total[jogador] = (vitoria, seg, ter, qua, qui, pontuacao, resultados_total[jogador][6] + count)

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
        ClassificaEstados.salvar_amostras(X, Y, jogos, rotulos)
        #ClassificaEstados.treinar_modelo(X, Y)
