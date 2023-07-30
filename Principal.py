from classes.Experimento import Experimento
import time

vscode = False
startTime = time.time()
experimento = Experimento(vscode)
# Treinar modelo por 10min
# experimento.treinar_modelo_mcts(600)

# Testar treino
experimento.testar_modelo_mcts(1000, 4)
print(time.time() - startTime)
