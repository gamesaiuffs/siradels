from classes.Experimento import Experimento
from classes.classifica_estados.ClassificaEstados import ClassificaEstados
from classes.classifica_estados.ColetaEstados import ColetaEstados
from classes.Simulacao import Simulacao
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
import time
vscode = True

estrategias = []

for i in range(6):          # fixo em 6 players
    estrategias.append(EstrategiaTotalmenteAleatoria(str(i+1)))

# Estrategias fixas e especificas
'''
estrategias.append(EstrategiaDjonatan())
estrategias.append(EstrategiaAndrei())
estrategias.append(EstrategiaBernardo())
estrategias.append(EstrategiaFelipe())
estrategias.append(EstrategiaGustavo())
estrategias.append(EstrategiaJoao())
'''

# Cria simulacao
simulacao = Simulacao(estrategias)

#ColetaEstados.simula_estados(10000)

X, Y = ClassificaEstados.ler_resultados()

ClassificaEstados.treinar_modelo(X, Y)

ClassificaEstados.modelo_info()

simulacao.rodar_simulacao()

'''
# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
experimento = Experimento(vscode)
startTime = time.time()

# Testar com jogadores manuais
#experimento.testar_simulacao(True, 1, 5)

# Testar com jogadores totalmente aleatórios
#experimento.testar_simulacao(False, 10000, 5)

# Treinar modelo por 10min
experimento.treinar_modelo_mcts(600)

# Testar treino contra jogadores totalmente aleatórios
experimento.testar_modelo_mcts(10000, 5)

print(f"Tempo da simulação = {(time.time() - startTime):.2f}s")
'''