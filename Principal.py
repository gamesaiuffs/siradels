from classes.Experimento import Experimento
from classes.classification.ClassificaEstados import ClassificaEstados
from classes.classification.ColetaEstados import ColetaEstados
from classes.Simulacao import Simulacao
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from sklearn.model_selection import train_test_split
import time
vscode = True

estrategias = []

# Estrategias fixas e especificas
'''
estrategias.append(EstrategiaDjonatan())
estrategias.append(EstrategiaAndrei())
estrategias.append(EstrategiaBernardo())
estrategias.append(EstrategiaFelipe())
estrategias.append(EstrategiaGustavo())
estrategias.append(EstrategiaJoao())
'''
'''
for i in range(5):          # fixo em 5 players
   estrategias.append(EstrategiaTotalmenteAleatoria(str(i+1)))
# Cria simulacao
simulacao = Simulacao(estrategias, 8, True)
'''

#(qtd_pts, n_features, nome_jogos, nome_rotulos)
#ColetaEstados.coleta_amostras(50000, 11, "Jogos 2", "Rótulos 2")

#(jogos, rotulos, nome_modelo, criterion, profundidade)
#ClassificaEstados.treinar_modelo("Jogos", "Rótulos", "Gini Model", "gini", 10)

#(jogos, rotulos, nome_modelo)
ClassificaEstados.modelo_info("Jogos", "Rótulos", "Log Model")

#(jogos_entrada, rotulos_entrada, jogos_saida, rotulos_saida)
#ClassificaEstados.undersampling("Jogos 2", "Rótulos 2", "Jogos 2 Balanceados", "Rotulos 2 Balanceados")

#simulacao.rodar_simulacao()

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