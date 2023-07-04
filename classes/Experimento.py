import time
import numpy as np
from classes.Simulacao import Simulacao
from classes.strategies.EstrategiaBernardo import EstrategiaBernardo
from classes.strategies.EstrategiaDjonatan import EstrategiaDjonatan
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaGustavo import EstrategiaGustavo
from classes.strategies.EstrategiaJoao import EstrategiaJoao
from classes.strategies.EstrategiaAndrei import EstrategiaAndrei
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.enum.TipoTabelaPersonagem import TipoTabelaPersonagem


class Experimento:

    # Cria modelo MCTS (tabelas) preenchidas com um valor inicial
    @staticmethod
    def inicializar_modelo_mcts(qtd_acoes: int, valor_inicial: int = 1) -> list[np.ndarray]:
        modelo = []
        # Tamanho total 12 672 células para 8 ações
        modelo.append(np.ones((7, qtd_acoes*2))*valor_inicial)  # Qtd ouro [0,1,2,3,4,5,>=6] = 112
        modelo.append(np.ones((6, qtd_acoes*2))*valor_inicial)  # Qtd carta mão [0,1,2,3,4,>=5] = 96
        modelo.append(np.ones((7, qtd_acoes*2))*valor_inicial)  # Carta mão mais cara [1 a 6] = 112
        modelo.append(np.ones((7, qtd_acoes*2))*valor_inicial)  # Carta mão mais barata [1 a 6] = 112
        modelo.append(np.ones((7, qtd_acoes*2))*valor_inicial)  # Qtd distritos construido [0 a 6] = 112
        modelo.append(np.ones((4, qtd_acoes*2))*valor_inicial)  # Qtd distrito construido Militar [0,1,2,>=3] = 64
        modelo.append(np.ones((4, qtd_acoes*2))*valor_inicial)  # Qtd distrito construido Religioso [0,1,2,>=3] = 64
        modelo.append(np.ones((4, qtd_acoes*2))*valor_inicial)  # Qtd distrito construido Nobre [0,1,2,>=3] = 64
        modelo.append(np.ones((8, qtd_acoes*2))*valor_inicial)  # Qtd personagens disponíveis [2,3,4,5,6,7] = 128
        modelo.append(np.ones((7, qtd_acoes*2))*valor_inicial)  # Pontuacao [0-3,4-7,8-11,12-15,16-19,20-23,>=24] = 112
        modelo.append(np.ones((7, qtd_acoes*2))*valor_inicial)  # Qtd distrito construido [0 a 6] = 112
        modelo.append(np.ones((7, qtd_acoes*2))*valor_inicial)  # Qtd ouro [0,1,2,3,4,5,>=6] = 112
        modelo.append(np.ones((6, qtd_acoes * 2)) * valor_inicial)  # Qtd carta mão [0,1,2,3,4,>=5] = 96
        modelo.append(np.ones((511, qtd_acoes*2))*valor_inicial)  # Personagem disponivel para escolha [1,2,3,4,5,6,7,8] = 8176
        modelo.append(np.ones((7, qtd_acoes * 2)) * valor_inicial)  # Quantidade de jogadores [4,5,6] = 112
        modelo.append(np.ones((193, qtd_acoes*2))*valor_inicial)  # Personagem visivel descartado [1,2,3,5,6,7,8] = 3088
        return modelo

    # Salva o modelo em arquivos CSV
    @staticmethod
    def salvar_modelo(modelo: list[np.ndarray]):
        for (i, j) in zip(modelo, TipoTabelaPersonagem):
            #np.savetxt('./classes/tabela/' + j.name + '.csv', i, delimiter=',', fmt='%6u')
            np.savetxt('./tabela/' + j.name + '.csv', i, delimiter=',', fmt='%6u')

    # Carrega o modelo a partir dos arquivos CSV
    @staticmethod
    def ler_modelo() -> list[np.ndarray]:
        modelo = []
        for i in TipoTabelaPersonagem:
            #a = np.genfromtxt('./classes/tabela/' + i.name + '.csv', delimiter=',')
            a = np.genfromtxt('./tabela/' + i.name + '.csv', delimiter=',')
            modelo.append(a)
        return modelo

    # Inicializa o treinamento do modelo do zero e treina durante o tempo limite em segundos
    def treinar_modelo_mcts(self, tempo_limite: int):
        inicio = time.time()
        qtd_acoes = 8
        modelo = self.inicializar_modelo_mcts(qtd_acoes)
        qtd_simulacao = 0
        while True:
        # while tempo_limite > time.time() - inicio:
            for qtd_jogadores in range(4, 7):
                for modo in TipoTabelaPersonagem:
                    qtd_simulacao += 1

                    # Faz um teste premiliminar a cada 300.000 (estimado em 1 arquivo por hora) jogos de treino e salva os resultados
                    if qtd_simulacao % 300000 == 0:
                        self.testar_modelo_gravar(10000, 6, qtd_simulacao)

                    # Inicializa variáveis para nova simulação do jogo
                    historico = self.inicializar_modelo_mcts(qtd_acoes, 0)
                    estrategias = [EstrategiaMCTS(modelo, historico, modo)]
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
                                for tabela, tabela_hist in zip(modelo, historico):
                                    tabela += tabela_hist
                            else:
                                metade_tabela = int(modelo[0].shape[1] / 2)
                                for tabela, tabela_hist in zip(modelo, historico):
                                    tabela[:, metade_tabela:] += tabela_hist[:, metade_tabela:]
            self.salvar_modelo(modelo)
            #print(qtd_simulacao)

    # Terminar método
    # Aplica o modelo aprendido durante o número de simulações desejado para coletar o desempenho do modelo
    def testar_modelo_mcts(self, qtd_simulacao_maximo: int, qtd_jogadores: int):
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
        print()
        for jogador, resultado in resultados.items():
            (vitoria, pontuacao) = resultado
            pontuacao_media = pontuacao / qtd_simulacao
            print(
                f'{jogador} - \tVitórias: {vitoria} - Porcento Vitorias: {vitoria / qtd_simulacao * 100:.2f}% - Pontuação Média: {pontuacao_media}')

    # Salva o resultado das simulações em arquivos CSV
    @staticmethod
    def salvar_resultado(resultados: dict[str, (int, int)], qtd_simulacao_treino, qtd_simulacao_teste):
        dados = []
        for jogador, resultado in resultados.items():
            (vitoria, pontuacao) = resultado
            pontuacao_media = pontuacao / qtd_simulacao_teste
            dados.append([jogador, vitoria, vitoria / qtd_simulacao_teste, pontuacao_media])

        #np.savetxt('./classes/simulacoes/' + qtd_simulacao_treino + '.csv', np.array(dados), delimiter=',', fmt='%s')
        np.savetxt('./simulacoes/' + str(qtd_simulacao_treino) + '.csv', np.array(dados), delimiter=',', fmt='%s')

    # Aplica o modelo aprendido durante o número de simulações desejado para coletar o desempenho do modelo e salva os resultados
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

        Experimento.salvar_resultado(resultados, qtd_simulacao_treino, qtd_simulacao)

'''
resultados: dict[str, (int, int)] = dict()
simulacao = Simulacao(estrategias)
estado_final = simulacao.rodar_simulacao()
for jogador in estado_final.jogadores:
    resultados[jogador.nome] = (int(jogador.vencedor), jogador.pontuacao_final)
for _ in range(qtd_simulacao):
    simulacao = Simulacao(estrategias)
    estado_final = simulacao.rodar_simulacao()
    for jogador in estado_final.jogadores:
        (vitoria, pontuacao) = resultados[jogador.nome]
        resultados[jogador.nome] = (int(jogador.vencedor) + vitoria, jogador.pontuacao_final + pontuacao)
print()
for jogador, resultado in resultados.items():
    (vitoria, pontuacao) = resultado
    pontuacao_media = pontuacao / (qtd_simulacao + 1)
    print(
        f'{jogador} - \tVitórias: {vitoria} - Porcento Vitorias: {vitoria / (qtd_simulacao + 1) * 100:.2f}% - Pontuação Média: {pontuacao_media}')
'''
