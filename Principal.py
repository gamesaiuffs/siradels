from classes.Experimento import Experimento
import time

startTime = time.time()
experimento = Experimento()
# Treinar modelo por 10min
# experimento.treinar_modelo_mcts(600)

# Testar treino
experimento.testar_modelo_mcts(10000, 6)
print(time.time() - startTime)
