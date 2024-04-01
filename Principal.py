from classes.Experimento import Experimento
import time
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.strategies.EstrategiaGold import EstrategiaGold
from classes.strategies.EstrategiaAllin import EstrategiaAllin

# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
vscode = True
if vscode:
    caminho = './classes'
else:  # PyCharm
    caminho = '.'

experimento = Experimento(caminho)
startTime = time.time()

# Treinar modelo por 10min = 600s
#experimento.treinar_modelo_mcts(600)

# # Testar treino contra outras estratégias
# estrategias = [EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4'), EstrategiaFelipe()]
# estrategias = [EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaFelipe('Felipe 2'), EstrategiaMCTS(caminho)]
# Experimento.testar_estrategias(estrategias, 1000)

estrategias_treino = [EstrategiaFelipe('Felipe 1'), EstrategiaFelipe('Felipe 2'), EstrategiaFelipe('Felipe 3'), EstrategiaFelipe('Felipe 4')]
experimento.treinar_modelo_mcts(estrategias_treino, 1000)

print(f"Tempo da simulação = {(time.time() - startTime):.2f}s")
