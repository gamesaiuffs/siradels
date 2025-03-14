import time

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

# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
vscode = True
if vscode:
    caminho = './treinos/EstrategiaAndrei'
else:  # PyCharm
    caminho = '.'

# Cria uma instância experimento para gerar estatítisticas e comparar o desempenho dos modelos
# Treinar modelo MCTS RL por 10min = 600s

experimento = Experimento(caminho)
# estrategiasTreino = [EstrategiaAllin(), EstrategiaAllin(), EstrategiaAllin(), EstrategiaAllin()]
# estrategiasTreino = [EstrategiaFelipe(), EstrategiaFelipe(), EstrategiaFelipe(), EstrategiaFelipe()]
estrategiasTreino = [EstrategiaAndrei(), EstrategiaAndrei(), EstrategiaAndrei(), EstrategiaAndrei()]
experimento.treinar_modelo_mcts(540, 1, estrategiasTreino)

# Testar treino contra outras estratégias
# estrategias = [EstrategiaAndrei(), EstrategiaFelipe(), EstrategiaEduardo(), EstrategiaJean(), EstrategiaDjonatan()]
# Experimento.testar_estrategias(estrategias, 10000)

estrategias = [EstrategiaMCTS(caminho), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
Experimento.testar_estrategias(estrategias, 1000)

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
