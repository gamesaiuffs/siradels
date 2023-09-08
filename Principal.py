from classes.Experimento import Experimento
import time

# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
vscode = False
experimento = Experimento(vscode)
startTime = time.time()

# Testar com jogadores manuais
#experimento.testar_simulacao(True, 1, 5)

# Testar com jogadores totalmente aleatórios
#experimento.testar_simulacao(False, 10000, 5)

# Treinar modelo por 10min
#experimento.treinar_modelo_mcts(600)

# Testar treino
#experimento.testar_modelo_mcts(5000, 5)

print(f"Tempo da simulação = {(time.time() - startTime):.2f}s")
