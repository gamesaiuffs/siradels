from classes.Experimento import Experimento
import time
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.strategies.EstrategiaEduardo import EstrategiaEduardo
from classes.strategies.EstrategiaGold import EstrategiaGold
from classes.strategies.EstrategiaManual import EstrategiaManual
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe

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
estrategias_meio_a_meio = [EstrategiaTotalmenteAleatoria('Rand 1'), EstrategiaGold('Gold 1'), EstrategiaTotalmenteAleatoria('Rand 2'), EstrategiaGold('Gold 2'), EstrategiaEduardo()]

estrategias_gold = [EstrategiaGold('Gold 1'), EstrategiaGold('Gold 2'), EstrategiaGold('Gold 3'), EstrategiaGold('Gold 4'), EstrategiaEduardo()]

estrategias_aleatorio = [EstrategiaTotalmenteAleatoria('Rand 1'), EstrategiaTotalmenteAleatoria('Rand 2'), EstrategiaTotalmenteAleatoria('Rand 3'), EstrategiaTotalmenteAleatoria('Rand 4'), EstrategiaEduardo()]


Experimento.testar_estrategias(estrategias_aleatorio)


print(f"Tempo da simulação = {(time.time() - startTime):.2f}s")
