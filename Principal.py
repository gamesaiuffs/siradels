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


def inicializar_modelo_mcts(valor_inicial: int = 1) -> list[np.array]:
    modelo = []

    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(7)]))  # Qtd ouro [0,1,2,3,4,5,>=6] = 56
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(6)]))  # Qtd carta mão [0,1,2,3,4,>=5] = 48
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(7)]))  # Carta mão mais cara [1 a 6] = 48
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(7)]))  # Carta mão mais barata [1 a 6] = 48
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(7)]))  # Qtd distritos construido [0 a 6] = 56
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(4)]))  # Qtd distrito construido Militar [0,1,2,>=3] = 32
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(4)]))  # Qtd distrito construido Religioso [0,1,2,>=3] = 32
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(4)]))  # Qtd distrito construido Nobre [0,1,2,>=3] = 32
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(8)]))  # Qtd personagens disponíveis [2,3,4,5,6,7] = 48
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(7)]))  # Pontuacao [0-3,4-7,8-11,12-15,16-19,20-23,>=24] = 56
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(7)]))  # Qtd distrito construido [0 a 6] = 56
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(7)]))  # Qtd ouro [0,1,2,3,4,5,>=6] = 56
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(7)]))  # Quantidade de jogadores [4,5,6] = 24
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(511)]))  # Personagem disponivel para escolha [1,2,3,4,5,6,7,8] = 64
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(6)]))  # Qtd carta mão [0,1,2,3,4,>=5] = 48
    modelo.append(np.array([[valor_inicial for _ in range(16)] for _ in range(193)]))  # Personagem visivel descartado [1,2,3,5,6,7,8] = 56

    return modelo


def salvar_modelo(modelo: list[np.array]):
    for (i, j) in zip(modelo, TipoTabelaPersonagem):
        np.savetxt('./Tabela/' + j.name + '.csv', i, delimiter=',', fmt='%6u')


def ler_modelo() -> list[np.array]:
    modelo = []
    for i in TipoTabelaPersonagem:
        a = np.genfromtxt('./Tabela/' + i.name + '.csv', delimiter=',')
        modelo.append(a)
    return modelo


#salvar_modelo(inicializar_modelo_mcts())
qtd_simulacao = 10
modelo_aprendido = ler_modelo()
historico = inicializar_modelo_mcts(0)
estrategias = [
    EstrategiaMCTS(modelo_aprendido, historico, TipoTabelaPersonagem.JaCartaCara),
    EstrategiaTotalmenteAleatoria('1'),
    EstrategiaTotalmenteAleatoria('2'),
    EstrategiaTotalmenteAleatoria('3'),
    EstrategiaTotalmenteAleatoria('4'),
    EstrategiaTotalmenteAleatoria('5'),
]
resultados: dict[str, (int, int)] = dict()
simulacao = Simulacao(estrategias)
estado_final = simulacao.rodar_simulacao()
for jogador in estado_final.jogadores:
    resultados[jogador.nome] = (int(jogador.vencedor), jogador.pontuacao_final)

# Atualizar modelo com vitórias e ações escolhidas
for jogador in estado_final.jogadores:
    if jogador.nome == 'Bot - MCTS':
        if jogador.vencedor:
            for tabela, tabela_hist in zip(modelo_aprendido, historico):
                tabela += tabela_hist
        else:
            metade_tabela = int(modelo_aprendido[0].shape[1]/2)
            for tabela, tabela_hist in zip(modelo_aprendido, historico):
                tabela[:, metade_tabela:] += tabela_hist[:, metade_tabela:]

salvar_modelo(modelo_aprendido)

'''
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