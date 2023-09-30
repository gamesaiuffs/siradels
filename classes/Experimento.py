import time
import numpy as np
from classes.Simulacao import Simulacao
from classes.strategies.EstrategiaManual import EstrategiaManual
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.enum.TipoTabela import TipoTabela
from classes.enum.TipoModeloAcao import TipoModeloAcao


class Experimento:

    def __init__(self, vscode: bool):
        if vscode:
            self.caminho = './classes'
        else:
            self.caminho = '.'

    # Cria modelo MCTS (tabelas) preenchidas com um valor inicial
    @staticmethod
    def inicializar_modelo_mcts(qtd_acoes: int, valor_inicial: int = 1) -> list[np.ndarray]:
        modelo = []
        for tabela in TipoTabela:
            modelo.append(np.ones((tabela.tamanho, qtd_acoes*2)) * valor_inicial)
        return modelo

    # Salva os modelos em arquivos CSV
    def salvar_modelos(self, modelos_mcts: list[list[np.ndarray]]):
        for (modelo, tipo_modelo) in zip(modelos_mcts, TipoModeloAcao):
            for (i, tipo_tabela) in zip(modelo, TipoTabela):
                np.savetxt(self.caminho + '/modelos_mcts/' + tipo_modelo.name + '/' + tipo_tabela.name + '.csv', i, delimiter=',', fmt='%6u')

    # Carrega os modelos a partir dos arquivos CSV
    def ler_modelos(self) -> list[list[np.ndarray]]:
        modelos_mcts = []
        for tipo_modelo in TipoModeloAcao:
            modelo = []
            for tipo_tabela in TipoTabela:
                a = np.genfromtxt(self.caminho + '/modelos_mcts/' + tipo_modelo.name + '/' + tipo_tabela.name + '.csv', delimiter=',')
                modelo.append(a)
            modelos_mcts.append(modelo)
        return modelos_mcts

    # Inicializa o treinamento do modelo do zero e treina durante o tempo limite em segundos
    def treinar_modelo_mcts(self, tempo_limite: int):
        inicio = time.time()
        modelos_mcts = []
        for tipo_modelo in TipoModeloAcao:
            modelos_mcts.append(self.inicializar_modelo_mcts(tipo_modelo.tamanho))
        # qtd_simulacao = 0
        # Fixado quantidade de jogadores em 5
        qtd_jogadores = 5
        while tempo_limite > time.time() - inicio:
            for modo in TipoTabela:
                # Faz um teste premiliminar a cada 300.000 (estimado em 1 arquivo por hora) jogos de treino e salva os resultados
                # if qtd_simulacao % 1000 == 0:
                #    self.testar_modelo_gravar(5000, 6, qtd_simulacao)

                # Inicializa variáveis para nova simulação do jogo
                # qtd_simulacao += 1
                modelos_historico = []
                for tipo_modelo in TipoModeloAcao:
                    modelos_historico.append(self.inicializar_modelo_mcts(tipo_modelo.tamanho, 0))
                estrategias = [EstrategiaMCTS(modelos_mcts, modelos_historico, modo)]
                for i in range(qtd_jogadores - 1):
                    estrategias.append(EstrategiaTotalmenteAleatoria(str(i+1)))
                # Cria simulação
                simulacao = Simulacao(estrategias)
                # Executa simulação
                estado_final = simulacao.rodar_simulacao()
                # Atualizar modelo com vitórias e ações escolhidas
                for jogador in estado_final.jogadores:
                    if jogador.nome == 'Bot - MCTS':
                        if jogador.vencedor:
                            for modelo, historico in zip(modelos_mcts, modelos_historico):
                                for tabela, tabela_hist in zip(modelo, historico):
                                    tabela += tabela_hist
                        else:
                            for modelo, historico in zip(modelos_mcts, modelos_historico):
                                metade_tabela = int(modelo[0].shape[1] / 2)
                                for tabela, tabela_hist in zip(modelo, historico):
                                    tabela[:, metade_tabela:] += tabela_hist[:, metade_tabela:]
            self.salvar_modelos(modelos_mcts)

    # Aplica o modelo aprendido durante o número de simulações desejado para coletar o desempenho do modelo
    def testar_modelo_mcts(self, qtd_simulacao_maximo: int, qtd_jogadores: int = 5):
        modelos_mcts = self.ler_modelos()
        qtd_simulacao = 1
        resultados: dict[str, (int, int)] = dict()
        # Inicializa variáveis para simulações do jogo
        estrategias = [EstrategiaMCTS(modelos_mcts, None, None, False)]
        for i in range(qtd_jogadores - 1):
            estrategias.append(EstrategiaTotalmenteAleatoria(str(i + 1)))
        # Cria simulação
        simulacao = Simulacao(estrategias)
        # Executa simulação
        estado_final = simulacao.rodar_simulacao()
        for jogador in estado_final.jogadores:
            resultados[jogador.nome] = (int(jogador.vencedor), jogador.pontuacao_final)
        while qtd_simulacao < qtd_simulacao_maximo:
            qtd_simulacao += 1
            # Cria simulação
            simulacao = Simulacao(estrategias)
            # Executa simulação
            estado_final = simulacao.rodar_simulacao()
            for jogador in estado_final.jogadores:
                (vitoria, pontuacao) = resultados[jogador.nome]
                resultados[jogador.nome] = (int(jogador.vencedor) + vitoria, jogador.pontuacao_final + pontuacao)
        print()
        for jogador, resultado in resultados.items():
            (vitoria, pontuacao) = resultado
            pontuacao_media = pontuacao / qtd_simulacao
            print(
                f'{jogador} - \tVitórias: {vitoria} - Porcento Vitorias: {vitoria / qtd_simulacao * 100:.2f}% - Pontuação Média: {pontuacao_media}')

    # Testa a simulaçào do jogo apenas com a estratégia aleatória
    @staticmethod
    def testar_simulacao(manual: bool = False, qtd_simulacao_maximo: int = 1000, qtd_jogadores: int = 5):
        qtd_simulacao = 1
        resultados: dict[str, (int, int)] = dict()
        # Inicializa variáveis para simulações do jogo
        estrategias = []
        if not manual:
            for i in range(qtd_jogadores):
                estrategias.append(EstrategiaTotalmenteAleatoria(str(i + 1)))
            simulacao = Simulacao(estrategias)
        else:
            for i in range(qtd_jogadores):
                estrategias.append(EstrategiaManual())
            simulacao = Simulacao(estrategias, 8, False)
        # Executa simulação
        estado_final = simulacao.rodar_simulacao()
        for jogador in estado_final.jogadores:
            resultados[jogador.nome] = (int(jogador.vencedor), jogador.pontuacao_final)
        while qtd_simulacao < qtd_simulacao_maximo:
            qtd_simulacao += 1
            # Cria simulação
            simulacao = Simulacao(estrategias)
            # Executa simulação
            estado_final = simulacao.rodar_simulacao()
            for jogador in estado_final.jogadores:
                (vitoria, pontuacao) = resultados[jogador.nome]
                resultados[jogador.nome] = (int(jogador.vencedor) + vitoria, jogador.pontuacao_final + pontuacao)
        print()
        for jogador, resultado in resultados.items():
            (vitoria, pontuacao) = resultado
            pontuacao_media = pontuacao / qtd_simulacao
            print(
                f'{jogador} - Vitórias: {vitoria} - Porcento Vitorias: {vitoria / qtd_simulacao * 100:.2f}% - Pontuação Média: {pontuacao_media}')

    # Salva o resultado das simulações em arquivos CSV
    # Refatorar
    def salvar_resultado(self, resultados: dict[str, (int, int)], qtd_simulacao_treino, qtd_simulacao_teste):
        dados = []
        for jogador, resultado in resultados.items():
            (vitoria, pontuacao) = resultado
            pontuacao_media = pontuacao / qtd_simulacao_teste
            dados.append([jogador, vitoria, vitoria / qtd_simulacao_teste, pontuacao_media])

        np.savetxt(self.caminho + '/simulacoes/' + str(qtd_simulacao_treino) + '.csv', np.array(dados), delimiter=',', fmt='%s')

    # Aplica o modelo aprendido durante o número de simulações desejado para coletar o desempenho do modelo e salva os resultados
    # Refatorar
    def testar_modelo_gravar(self, qtd_simulacao_maximo: int, qtd_jogadores: int, qtd_simulacao_treino):
        modelo = self.ler_modelo()
        qtd_simulacao = 1
        resultados: dict[str, (int, int)] = dict()
        # Inicializa variáveis para simulações do jogo
        estrategias = [EstrategiaMCTS(modelo, None, None, False)]
        for i in range(qtd_jogadores - 1):
            estrategias.append(EstrategiaTotalmenteAleatoria(str(i + 1)))
        # Cria simulação
        simulacao = Simulacao(estrategias)
        # Executa simulação
        estado_final = simulacao.rodar_simulacao()
        for jogador in estado_final.jogadores:
            resultados[jogador.nome] = (int(jogador.vencedor), jogador.pontuacao_final)
        while qtd_simulacao < qtd_simulacao_maximo:
            qtd_simulacao += 1
            # Cria simulação
            simulacao = Simulacao(estrategias)
            # Executa simulação
            estado_final = simulacao.rodar_simulacao()
            for jogador in estado_final.jogadores:
                (vitoria, pontuacao) = resultados[jogador.nome]
                resultados[jogador.nome] = (int(jogador.vencedor) + vitoria, jogador.pontuacao_final + pontuacao)

        self.salvar_resultado(resultados, qtd_simulacao_treino, qtd_simulacao)
