import gymnasium as gym
import time
from itertools import combinations

from classes.Experimento import Experimento

from classes.strategies.Agente import AgenteTestes
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
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria

start_time = time.time()

print("Início dos testes das estratégias")

exp = 6
print(f"\n\nExperimento {exp}:")

for init in range(1, 11):

    estrategias: list[Estrategia] = [AgenteTestes(exp=exp, model=f"aaa_experimentos_final/{exp}/in_{init}/30.zip"), EstrategiaAndrei(),  EstrategiaDjonatan(), EstrategiaEduardo(), EstrategiaFelipe(), EstrategiaFrequency("Frequency"), EstrategiaGold("Gold"), EstrategiaJean(), EstrategiaLuisII(), EstrategiaTotalmenteAleatoria()]
    # estrategias: list[Estrategia] = [AgenteTestes( model=f"./testes/teste_entradaPadrao_ambienteBox/30.zip"), EstrategiaAndrei(),  EstrategiaDjonatan(), EstrategiaEduardo(), EstrategiaFelipe(), EstrategiaFrequency("Frequency"), EstrategiaGold("Gold"), EstrategiaJean(), EstrategiaLuisII(), EstrategiaTotalmenteAleatoria()]

    comb = list(combinations(estrategias, 5))
    qtd_comb = len(comb)

    qtd_simulacao: int = 10
    resultados_total: dict[str, (int, int, int, int, int, int, int)] = dict()
    for e in estrategias:
        resultados_total[e.nome] = (0, 0, 0, 0, 0, 0, 0)
    for i, p in enumerate(comb):
        resultados = Experimento.testar_estrategias(list(p), qtd_simulacao)
        for jogador, resultado in resultados.items():
            (vitoria, seg, ter, qua, qui, pontuacao) = resultado
            vitoria += resultados_total[jogador][0]
            seg += resultados_total[jogador][1]
            ter += resultados_total[jogador][2]
            qua += resultados_total[jogador][3]
            qui += resultados_total[jogador][4]
            pontuacao += resultados_total[jogador][5]
            resultados_total[jogador] = (vitoria, seg, ter, qua, qui, pontuacao, resultados_total[jogador][6] + qtd_simulacao)
    print(f"Resultados exp {exp} - {init}: ")
    for jogador, resultado in resultados_total.items(): 
        if jogador == "Agente":
            (vitoria, seg, ter, qua, qui, pontuacao, qtd_simulacao_total) = resultado
            pontuacao_media = pontuacao / qtd_simulacao_total
            taxa_vitoria = 100 * vitoria / qtd_simulacao_total
            taxa_seg = 100 * seg / qtd_simulacao_total
            taxa_ter = 100 * ter / qtd_simulacao_total
            taxa_qua = 100 * qua / qtd_simulacao_total
            taxa_qui = 100 * qui / qtd_simulacao_total
            print(
                f'{jogador} - Vitórias: {vitoria} - Taxa de Vitórias: {taxa_vitoria:.2f}% - Pontuação Média: {pontuacao_media:.2f}\n\t'
                f'Primeiro: {taxa_vitoria:5.2f}%\n\tSegundo : {taxa_seg:5.2f}%\n\tTerceiro: {taxa_ter:5.2f}%\n\tQuarto  : {taxa_qua:5.2f}%\n\tQuinto  : {taxa_qui:5.2f}%\n')
            
    
    
    
print("Fim dos testes das estratégias")

# Imprime duração do experimento
s = time.time() - start_time
m = s // 60
h = m // 60
s -= m * 60
m -= h * 60
print(f"Tempo de execução = {h:.0f}h {m:.0f}min {s:.2f}s")