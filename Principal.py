from classes.Experimento import Experimento

experimento = Experimento()
# Treinar modelo por 10min
experimento.treinar_modelo_mcts(600)

# Testar treino
# experimento.testar_modelo_mcts(1000, 4)
