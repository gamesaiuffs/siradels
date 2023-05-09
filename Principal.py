from classes.Simulacao import Simulacao
from classes.strategies.EstrategiaBernardo import EstrategiaBernardo
from classes.strategies.EstrategiaDjonatan import EstrategiaDjonatan
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaGustavo import EstrategiaGustavo
from classes.strategies.EstrategiaJoao import EstrategiaJoao
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria

qtd_simulacao = 1000
estrategias = (EstrategiaTotalmenteAleatoria(),
               EstrategiaFelipe(),
               EstrategiaDjonatan(),
               EstrategiaBernardo(),
               EstrategiaJoao(),
               EstrategiaGustavo())
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
    print(f'{jogador} - \tVitórias: {vitoria} - Pontuação Média: {pontuacao_media}')
