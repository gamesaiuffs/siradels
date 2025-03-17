import time
import os

from classes.Experimento import Experimento
from classes.enum.TipoAcaoOpenAI import TipoAcaoOpenAI
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaManual import EstrategiaManual
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.strategies.EstrategiaGold import EstrategiaGold
from classes.strategies.EstrategiaAllin import EstrategiaAllin
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaAndrei import EstrategiaAndrei
from classes.strategies.EstrategiaEduardo import EstrategiaEduardo
from classes.strategies.EstrategiaJean import EstrategiaJean
from classes.strategies.EstrategiaDjonatan import EstrategiaDjonatan

# Marca tempo de início para computar duração do experimento
start_time = time.time()

base_path = './treinos'


# Cria uma instância experimento para gerar estatítisticas e comparar o desempenho dos modelos
# experimento = Experimento(caminho)

def treinar_modelo_mcts(caminho, estrategias, num_treinos=10):
    for i in range(num_treinos):
        treino_path = os.path.join(caminho, str(i))
        os.makedirs(treino_path, exist_ok=True)
        experimento = Experimento(treino_path)
        experimento.treinar_modelo_mcts(50000, 0, estrategias)
        testar_varias_estrategias(treino_path, 1000)

def testar_varias_estrategias(caminho_estrategia, num_testes=1000):
    estrategias_teste = [
        EstrategiaTotalmenteAleatoria,
        EstrategiaFelipe,
        EstrategiaAndrei,
        EstrategiaEduardo,
        EstrategiaJean,
        EstrategiaDjonatan
    ]

    for estrategia in estrategias_teste:
        estrategias = [EstrategiaMCTS(caminho_estrategia), estrategia('Bot 1'), estrategia('Bot 2'), estrategia('Bot 3'), estrategia('Bot 4')]
        experimento = Experimento(caminho_estrategia)
        experimento.testar_estrategias(caminho=caminho_estrategia, estrategias=estrategias, qtd_simulacao_maximo=num_testes)

def main():
    estrategias_oponentes = [
        EstrategiaTotalmenteAleatoria,
        EstrategiaFelipe,
        EstrategiaAndrei,
        EstrategiaEduardo,
        EstrategiaJean,
        EstrategiaDjonatan
    ]

    for Estrategia in estrategias_oponentes:
        nome_estrategia = Estrategia.__name__
        caminho_estrategia = os.path.join(base_path, nome_estrategia)
        oponentes = [Estrategia(), Estrategia(), Estrategia(), Estrategia()]
        treinar_modelo_mcts(caminho_estrategia, oponentes)

    # Imprime duração do experimento
    s = time.time() - start_time
    m = s // 60
    h = m // 60
    s -= m * 60
    m -= h * 60
    print(f"Tempo de execução = {h:.0f}h {m:.0f}min {s:.2f}s")

if __name__ == "__main__":
    main()


# estrategiasTreino = [EstrategiaAllin(), EstrategiaAllin(), EstrategiaAllin(), EstrategiaAllin()]
# estrategiasTreino = [EstrategiaFelipe(), EstrategiaFelipe(), EstrategiaFelipe(), EstrategiaFelipe()]
# estrategiasTreino = [EstrategiaAndrei(), EstrategiaAndrei(), EstrategiaAndrei(), EstrategiaAndrei()]
# experimento.treinar_modelo_mcts(5000, 0)

# Testar treino contra outras estratégias
# estrategias = [EstrategiaAndrei(), EstrategiaFelipe(), EstrategiaEduardo(), EstrategiaJean(), EstrategiaDjonatan()]
# Experimento.testar_estrategias(estrategias, 10000)

# estrategias = [EstrategiaMCTS(caminho), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
# experimento.testar_estrategias(caminho, estrategias, 1000)

# estrategias = [EstrategiaMCTS(caminho), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
# Experimento.testar_estrategias(estrategias, 1000)

# estrategias = [EstrategiaFelipe(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
# Experimento.testar_estrategias(estrategias, 1000)

# estrategias = [Agente(), EstrategiaMCTS(caminho), EstrategiaFelipe(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2')]
# Experimento.testar_estrategias(estrategias, 10000)

# Imprime duração do experimento
s = time.time() - start_time
m = s // 60
h = m // 60
s -= m * 60
m -= h * 60
print(f"Tempo de execução = {h:.0f}h {m:.0f}min {s:.2f}s")
