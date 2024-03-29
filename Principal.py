from classes.Experimento import Experimento
import time
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.strategies.EstrategiaEduardo import EstrategiaEduardo
from classes.strategies.EstrategiaGold import EstrategiaGold
from classes.strategies.EstrategiaManual import EstrategiaManual

# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
vscode = False
if vscode:
    caminho = './classes'
else:  # PyCharm
    caminho = '.'

experimento = Experimento(caminho)
startTime = time.time()

# Treinar modelo por 10min = 600s
#experimento.treinar_modelo_mcts(600)

# Testar treino contra outras estratégias
estrategias_gold = [EstrategiaGold('Bot 1'), EstrategiaGold('Bot 2'), EstrategiaGold('Bot 3'), EstrategiaGold('Bot 4'), EstrategiaEduardo()]

estrategias_aleatorio = [EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4'), EstrategiaEduardo()]
Experimento.testar_estrategias(estrategias_gold)


print(f"Tempo da simulação = {(time.time() - startTime):.2f}s")
