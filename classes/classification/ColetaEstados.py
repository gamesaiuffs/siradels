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
import itertools

estrategias: list[Estrategia] = [EstrategiaAndrei(), EstrategiaDjonatan(), EstrategiaEduardo(),
                                 EstrategiaFelipe(), EstrategiaJean(), EstrategiaLuisII(),
                                 EstrategiaTotalmenteAleatoria()] #MCTS e Agente off, levar para ColetaEstados e adaptar
# estrategias: list[Estrategia] = [Agente(imprimir=True), EstrategiaTotalmenteAleatoria("B2"), EstrategiaTotalmenteAleatoria("B3"), EstrategiaTotalmenteAleatoria("B4"), EstrategiaTotalmenteAleatoria("B5")]
comb = list(combinations_with_replacement(estrategias, 5))

qtd_comb = len(comb)

#print("Quantidade de Combinações:", qtd_comb)

class ColetaEstados:
    @staticmethod
    def coleta_amostras(n_features: int, jogos: str, rotulos: str, nome_modelo: str = '', qtd_simulacao: int = 100,):
        X_inicial = [np.zeros(n_features)]
        X = X_inicial
        Y = []
        num_simulacao = 0
        resultados: dict[str, (int, int, int, int, int, int)] = dict()
        resultados_total: dict[str, (int, int, int, int, int, int, int)] = dict()
        
        while num_simulacao <= qtd_simulacao-1:
            print(f"{num_simulacao+1}/{qtd_simulacao}")

            for e in estrategias:
                resultados_total[e.nome] = (0, 0, 0, 0, 0, 0, 0)
            for i, p in enumerate(comb):
                #if (i+1) % 100 == 0 or i+1 == qtd_comb:
                #    print(f"{i+1}/{qtd_comb} - {((i+1)*100/qtd_comb):.2f}%")

            #resultados = Experimento.testar_estrategias(list(p), qtd_simulacao)
                # Cria simulacao
                simulacao = SimulacaoColeta(list(p))
                # Executa simulacao
                estado_final, X_coleta, Y_coleta, n_rodada = simulacao.rodar_simulacao(X_inicial, nome_modelo)
                # Remove primeira linha nula
                X_coleta = np.delete(X_coleta, 0, axis=0)
                # Empilha linhas na matriz
                X = np.vstack((X, X_coleta))
                # Atrubui rótulos de acordo com a quantidade de rodadas
                for i in range(n_rodada):
                    Y.append(Y_coleta)
                '''
                for jogador in estado_final.jogadores:
                    (vitoria, seg, ter, qua, qui, pontuacao) = resultados[jogador.nome]
                    if jogador == estado_final.jogadores[1]:
                        seg += 1
                    if jogador == estado_final.jogadores[2]:
                        ter += 1
                    if jogador == estado_final.jogadores[3]:
                        qua += 1
                    if jogador == estado_final.jogadores[4]:
                        qui += 1
                    resultados[jogador.nome] = (int(jogador.vencedor) + vitoria, seg, ter, qua, qui, jogador.pontuacao_final + pontuacao)
                '''
            num_simulacao += 1
        '''
        for jogador, resultado in resultados.items():
            (vitoria, seg, ter, qua, qui, pontuacao) = resultado
            vitoria += resultados_total[jogador][0]
            seg += resultados_total[jogador][1]
            ter += resultados_total[jogador][2]
            qua += resultados_total[jogador][3]
            qui += resultados_total[jogador][4]
            pontuacao += resultados_total[jogador][5]
            resultados_total[jogador] = (vitoria, seg, ter, qua, qui, pontuacao, resultados_total[jogador][6] + qtd_simulacao)
        '''
        '''    
        for jogador, resultado in resultados_total.items():
            (vitoria, seg, ter, qua, qui, pontuacao, qtd_simulacao_total) = resultado
            pontuacao_media = pontuacao / qtd_simulacao_total
            taxa_vitoria = 100 * vitoria / qtd_simulacao_total
            taxa_seg = 100 * seg / qtd_simulacao_total
            taxa_ter = 100 * ter / qtd_simulacao_total
            taxa_qua = 100 * qua / qtd_simulacao_total
            taxa_qui = 100 * qui / qtd_simulacao_total
        print(
        f'\n{jogador} - Vitórias: {vitoria} - Taxa de Vitórias: {taxa_vitoria:.2f}% - Pontuação Média: {pontuacao_media:.2f}\n\t'
        f'Primeiro: {taxa_vitoria:5.2f}%\n\tSegundo : {taxa_seg:5.2f}%\n\tTerceiro: {taxa_ter:5.2f}%\n\tQuarto  : {taxa_qua:5.2f}%\n\tQuinto  : {taxa_qui:5.2f}%')
        print("Fim dos testes das estratégias")
        '''
           
        # Remove primeira linha nula
        X = np.delete(X, 0, axis=0)
        ClassificaEstados.salvar_amostras(X, Y, jogos, rotulos)
        #ClassificaEstados.treinar_modelo(X, Y)
