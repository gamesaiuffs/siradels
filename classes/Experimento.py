import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

from classes.Simulacao import Simulacao
from classes.enum.TipoTabela import TipoTabela
from classes.strategies.Estrategia import Estrategia
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria

from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaAndrei import EstrategiaAndrei
from classes.strategies.EstrategiaEduardo import EstrategiaEduardo
from classes.strategies.EstrategiaJean import EstrategiaJean
from classes.strategies.EstrategiaDjonatan import EstrategiaDjonatan

class Experimento:

    def __init__(self, caminho: str):
        self.caminho: str = caminho

    @staticmethod
    def testar_estrategias(caminho, estrategias: list[Estrategia], qtd_simulacao_maximo: int = 1000, automatico: bool = True):
        qtd_simulacao = 1
        resultados: dict[str, (int, int)] = dict()
        # Cria simulação
        simulacao = Simulacao(estrategias, automatico=automatico)
        # Executa simulação
        estado_final = simulacao.rodar_simulacao()
        for jogador in estado_final.jogadores:
            resultados[jogador.nome] = (int(jogador.vencedor), jogador.pontuacao_final)
        while qtd_simulacao < qtd_simulacao_maximo:
            qtd_simulacao += 1
            # Cria simulação
            simulacao = Simulacao(estrategias, automatico=automatico)
            # Executa simulação
            estado_final = simulacao.rodar_simulacao()
            for jogador in estado_final.jogadores:
                (vitoria, pontuacao) = resultados[jogador.nome]
                resultados[jogador.nome] = (int(jogador.vencedor) + vitoria, jogador.pontuacao_final + pontuacao)
        
        dados = []
        for jogador, resultado in resultados.items():
            (vitoria, pontuacao) = resultado
            pontuacao_media = pontuacao / qtd_simulacao
            dados.append([jogador, vitoria, vitoria / qtd_simulacao, pontuacao_media])
            # print(
            #     f'{jogador} - Vitórias: {vitoria} - Porcento Vitorias: {vitoria / qtd_simulacao * 100:.2f}% - Pontuação Média: {pontuacao_media}')
        
        # Salva o resultado do treino em arquivo
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        nome_arquivo = f"{caminho}/resultados_estrategias_{estrategias[0].__class__.__name__}_{timestamp}.csv"
        with open(nome_arquivo, 'w') as f:
            f.write(f"Estrategias: {[estrategia.__class__.__name__ for estrategia in estrategias]}\n")
            f.write(f"Quantidade de simulacoes: {qtd_simulacao_maximo}\n")
            np.savetxt(f, np.array(dados), delimiter=',', fmt='%s')
            

    # Inicializa o treinamento do modelo do zero e treina durante a quantidade definida de simulacoes
    def treinar_modelo_mcts(self, qt_simulacao: int, tipo_treino, estrategias: list[Estrategia] = []):
        # Fixado quantidade de jogadores em 5
        qtd_jogadores = 5
        # Limita a quantidade de estratégias a quantidade de jogadores - 1
        if len(estrategias) >= qtd_jogadores:
            estrategias = estrategias[:qtd_jogadores - 1]
        # Adiciona a estratégia MCTS
        mcts = EstrategiaMCTS(self.caminho, tipo_treino)
        estrategias.append(mcts)
        # Preenche os espaços restantes com estratégias aleatórias
        if len(estrategias) < 5:
            for i in range(qtd_jogadores - len(estrategias)):
                estrategias.append(EstrategiaTotalmenteAleatoria(str(i + 1)))

        contador_simulacoes = 0
        inicio = time.time()
        while qt_simulacao > contador_simulacoes:
            for tipo_tabela in TipoTabela:
                # Treinamento individual por tipo de tabela
                mcts.tipo_tabela = tipo_tabela
                mcts.iniciar_historico()
                # Cria simulação
                simulacao = Simulacao(estrategias)
                # Executa simulação
                estado_final = simulacao.rodar_simulacao()
                
                contador_simulacoes += 1
                # Adiciona prints de depuração
                tempo_decorrido = time.time() - inicio
                print(f'\rTempo decorrido: {tempo_decorrido:.2f} segundos, Simulações realizadas: {contador_simulacoes} / {qt_simulacao}', end='', flush=True)
                
                # Atualizar modelo com vitórias e ações escolhidas
                for jogador in estado_final.jogadores:
                    if jogador.nome == 'MCTS':
                        if jogador.vencedor:
                            for modelo, historico in zip(mcts.modelos_mcts, mcts.modelos_historico):
                                for tabela, tabela_hist in zip(modelo, historico):
                                    tabela += tabela_hist
                        else:
                            for modelo, historico in zip(mcts.modelos_mcts, mcts.modelos_historico):
                                metade_tabela = int(modelo[0].shape[1] / 2)
                                for tabela, tabela_hist in zip(modelo, historico):
                                    tabela[:, metade_tabela:] += tabela_hist[:, metade_tabela:]
            # Salva a cada 250 simulações para reduzir o acesso ao disco
            if contador_simulacoes % 250 == 0:
                mcts.salvar_modelos()
        mcts.salvar_modelos()
        # Salvar o tempo de execução e quantidade de simulações em um arquivo dentro da pasta de treinos dada pela variável caminho
        tempo_total = time.time() - inicio
        with open(self.caminho + '/tempo_execucao.txt', 'w') as f:
            f.write(f'Tempo total de execucao: {tempo_total:.2f} segundos\n')
            f.write(f'Quantidade de simulacoes: {contador_simulacoes}\n')

    # # Inicializa o treinamento do modelo do zero e treina durante a quantidade definida de simulações
    # def treinar_modelo_mcts(self, qt_simulacao: int, tipo_treino, estrategias: list[Estrategia] = []):
    #     # Fixado quantidade de jogadores em 5
    #     qtd_jogadores = 5
    #     # Limita a quantidade de estratégias a quantidade de jogadores - 1
    #     if len(estrategias) >= qtd_jogadores:
    #         estrategias = estrategias[:qtd_jogadores - 1]
    #     # Adiciona a estratégia MCTS
    #     mcts = EstrategiaMCTS(self.caminho, tipo_treino)
    #     estrategias.append(mcts)
    #     # Preenche os espaços restantes com estratégias aleatórias
    #     if len(estrategias) < 5:
    #         for i in range(qtd_jogadores - len(estrategias)):
    #             estrategias.append(EstrategiaTotalmenteAleatoria(str(i + 1)))

    #     contador_simulacoes = 0
    #     inicio = time.time()

    #     def treinar_tipo_tabela(tipo_tabela):
    #         mcts.tipo_tabela = tipo_tabela
    #         mcts.iniciar_historico()
    #         simulacao = Simulacao(estrategias)
    #         estado_final = simulacao.rodar_simulacao()

    #         # Atualizar modelo com vitórias e ações escolhidas
    #         for jogador in estado_final.jogadores:
    #             if jogador.nome == 'MCTS':
    #                 if jogador.vencedor:
    #                     for modelo, historico in zip(mcts.modelos_mcts, mcts.modelos_historico):
    #                         for tabela, tabela_hist in zip(modelo, historico):
    #                             tabela += tabela_hist
    #                 else:
    #                     for modelo, historico in zip(mcts.modelos_mcts, mcts.modelos_historico):
    #                         metade_tabela = int(modelo[0].shape[1] / 2)
    #                         for tabela, tabela_hist in zip(modelo, historico):
    #                             tabela[:, metade_tabela:] += tabela_hist[:, metade_tabela:]

    #     while qt_simulacao > contador_simulacoes:
    #         with ThreadPoolExecutor() as executor:
    #             futures = [executor.submit(treinar_tipo_tabela, tipo_tabela) for tipo_tabela in TipoTabela]

    #             for future in as_completed(futures):
    #                 contador_simulacoes += 1
    #                 tempo_decorrido = time.time() - inicio
    #                 print(f'\rTempo decorrido: {tempo_decorrido:.2f} segundos, Simulações realizadas: {contador_simulacoes} / {qt_simulacao}', end='')

    #         # Salva apenas após o conjunto completo de simulações para reduzir o acesso ao disco
    #     mcts.salvar_modelos()

    # Salva o resultado das simulações em arquivos CSV
    # Refatorar
    def salvar_resultado(self, resultados: dict[str, (int, int)], qtd_simulacao_treino, qtd_simulacao_teste):
        dados = []
        for jogador, resultado in resultados.items():
            (vitoria, pontuacao) = resultado
            pontuacao_media = pontuacao / qtd_simulacao_teste
            dados.append([jogador, vitoria, vitoria / qtd_simulacao_teste, pontuacao_media])

        np.savetxt(self.caminho + '/simulacoes/' + str(qtd_simulacao_treino) + '.csv', np.array(dados), delimiter=',', fmt='%s')
