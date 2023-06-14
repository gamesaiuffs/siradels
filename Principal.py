import numpy as np
from classes.Simulacao import Simulacao
from classes.strategies.EstrategiaBernardo import EstrategiaBernardo
from classes.strategies.EstrategiaDjonatan import EstrategiaDjonatan
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaGustavo import EstrategiaGustavo
from classes.strategies.EstrategiaJoao import EstrategiaJoao
from classes.strategies.EstrategiaAndrei import EstrategiaAndrei
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.enum.TipoTabelaPersonagem import TipoTabelaPersonagem

'''
qtd_simulacao = 1000
estrategias = [
EstrategiaFelipe(),
EstrategiaDjonatan(),
EstrategiaBernardo(),
EstrategiaJoao(),
EstrategiaGustavo(),
EstrategiaAndrei()
]
resultados: dict[str, (int, int)] = dict()
simulacao = Simulacao(estrategias)
estado_final = simulacao.rodar_simulacao()
for jogador in estado_final.jogadores:
    resultados[jogador.nome] = (int(jogador.vencedor), jogador.pontuacao_final)
for i in range(qtd_simulacao):
    simulacao = Simulacao(estrategias)
    estado_final = simulacao.rodar_simulacao()
    for jogador in estado_final.jogadores:
        (vitoria, pontuacao) = resultados[jogador.nome]
        resultados[jogador.nome] = (int(jogador.vencedor) + vitoria, jogador.pontuacao_final + pontuacao)
print()
for jogador, resultado in resultados.items():
    (vitoria, pontuacao) = resultado
    pontuacao_media = pontuacao/qtd_simulacao
    print(f'{jogador} - \tVitórias: {vitoria} - Porcento Vitorias: {vitoria/qtd_simulacao*100:.2f}% - Pontuação Média: {pontuacao_media}')
'''


def inicializar_modelo_mcts() -> list[list]:
    modelo = []

    modelo.append([[0 for _ in range(17)] for _ in range(7)])# Qtd ouro [0,1,2,3,4,5,>=6] = 56
    modelo.append([[0 for _ in range(17)] for _ in range(6)])# Qtd carta mão [0,1,2,3,4,>=5] = 48
    modelo.append([[0 for _ in range(17)] for _ in range(7)])# Carta mão mais cara [1 a 6] = 48
    modelo.append([[0 for _ in range(17)] for _ in range(7)])# Carta mão mais barata [1 a 6] = 48
    modelo.append([[0 for _ in range(17)] for _ in range(7)])# Qtd distritos construido [0 a 6] = 56
    modelo.append([[0 for _ in range(17)] for _ in range(4)])# Qtd distrito construido Militar [0,1,2,>=3] = 32
    modelo.append([[0 for _ in range(17)] for _ in range(4)])# Qtd distrito construido Religioso [0,1,2,>=3] = 32
    modelo.append([[0 for _ in range(17)] for _ in range(4)])# Qtd distrito construido Nobre [0,1,2,>=3] = 32
    modelo.append([[0 for _ in range(17)] for _ in range(8)])# Qtd personagens disponíveis [2,3,4,5,6,7] = 48
    modelo.append([[0 for _ in range(17)] for _ in range(7)])# Pontuacao [0-3,4-7,8-11,12-15,16-19,20-23,>=24] = 56
    modelo.append([[0 for _ in range(17)] for _ in range(7)])# Qtd distrito construido [0 a 6] = 56
    modelo.append([[0 for _ in range(17)] for _ in range(7)])# Qtd ouro [0,1,2,3,4,5,>=6] = 56
    modelo.append([[0 for _ in range(17)] for _ in range(7)])# Quantidade de jogadores [4,5,6] = 24
    modelo.append([[0 for _ in range(17)] for _ in range(511)])# Personagem disponivel para escolha [1,2,3,4,5,6,7,8] = 64
    modelo.append([[0 for _ in range(17)] for _ in range(6)])# Qtd carta mão [0,1,2,3,4,>=5] = 48
    modelo.append([[0 for _ in range(17)] for _ in range(193)])# Personagem visivel descartado [1,2,3,5,6,7,8] = 56

    return modelo


def salvar_modelo(modelo: list[list]):
    for (i, j) in zip(modelo, TipoTabelaPersonagem):
        np.savetxt('./Tabela/'+j.name+'.csv', np.array(i), delimiter=',')


def ler_modelo() -> list[np.array]:
    modelo = []
    for i in TipoTabelaPersonagem:
        a = np.genfromtxt('./Tabela/'+i.name+'.csv', delimiter=',')
        modelo.append(a)
    return modelo


salvar_modelo(inicializar_modelo_mcts())
print(ler_modelo()[0])
