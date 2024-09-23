import time
import numpy as np

from classes.Simulacao import Simulacao
from classes.enum.TipoTabela import TipoTabela
from classes.strategies.Estrategia import Estrategia
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria


class Experimento:

    def __init__(self, caminho: str):
        self.caminho: str = caminho

    # Testa estratégias e retorna resultados com dicionário {nome_jogador: (qtd_primeiro, qtd_segundo, qtd_terceiro, qtd_quarto, qtd_quinto, soma_pontuacao)}
    @staticmethod
    def testar_estrategias(estrategias: list[Estrategia], qtd_simulacao_maximo: int = 1000, automatico: bool = True) -> dict[str, (int, int, int, int, int, int)]:
        qtd_simulacao = 1
        resultados: dict[str, (int, int, int, int, int, int)] = dict()
        for jogador in estrategias:
            resultados[jogador.nome] = (0, 0, 0, 0, 0, 0)
        while qtd_simulacao <= qtd_simulacao_maximo:
            # Cria simulação
            simulacao = Simulacao(estrategias, automatico=automatico)
            # Executa simulação
            estado_final = simulacao.rodar_simulacao()
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
            qtd_simulacao += 1
        return resultados

    # Inicializa o treinamento do modelo do zero e treina durante o tempo limite em segundos
    def treinar_modelo_mcts(self, tempo_limite: int, tipo_treino):
        inicio = time.time()
        # Fixado quantidade de jogadores em 5
        qtd_jogadores = 5
        mcts = EstrategiaMCTS(self.caminho, tipo_treino)
        estrategias = [mcts]
        for i in range(qtd_jogadores - 1):
            estrategias.append(EstrategiaTotalmenteAleatoria(str(i + 1)))
        while tempo_limite > time.time() - inicio:
            for tipo_tabela in TipoTabela:
                # Treinamento individual por tipo de tabela
                mcts.tipo_tabela = tipo_tabela
                mcts.iniciar_historico()
                # Cria simulação
                simulacao = Simulacao(estrategias)
                # Executa simulação
                estado_final = simulacao.rodar_simulacao()
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
            mcts.salvar_modelos()

    # Salva o resultado das simulações em arquivos CSV
    # Refatorar
    def salvar_resultado(self, resultados: dict[str, (int, int)], qtd_simulacao_treino, qtd_simulacao_teste):
        dados = []
        for jogador, resultado in resultados.items():
            (vitoria, pontuacao) = resultado
            pontuacao_media = pontuacao / qtd_simulacao_teste
            dados.append([jogador, vitoria, vitoria / qtd_simulacao_teste, pontuacao_media])

        np.savetxt(self.caminho + '/simulacoes/' + str(qtd_simulacao_treino) + '.csv', np.array(dados), delimiter=',', fmt='%s')
