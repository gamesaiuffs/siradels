from classes.Experimento import Experimento
from classes.classification.ClassificaEstados import ClassificaEstados
from classes.classification.ColetaEstados import ColetaEstados
from classes.classification.SimulacaoColeta import SimulacaoColeta 
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from sklearn.model_selection import train_test_split
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

n_features = 28
#n_features = 23

profundidade = 30 
n_amostras = 15000

jogos = f"Jogos {n_amostras} {n_features}f"
rotulos = f"Rótulos {n_amostras} {n_features}f" 
modelo = f"Model 15k d{profundidade} {n_features}f"

'''for i in range(5):          # fixo em 5 players
   estrategias.append(EstrategiaTotalmenteAleatoria(str(i+1)))
simulacao = Simulacao(estrategias, 8, True)
'''

#(qtd_pts, n_features, nome_jogos, nome_rotulos, nome_modelo)
#ColetaEstados.coleta_amostras(n_amostras, n_features, jogos, rotulos, modelo)

#(jogos, rotulos, nome_modelo, criterion, profundidade)
#ClassificaEstados.treinar_modelo(jogos, rotulos, modelo, "log_loss", profundidade)

#(jogos, rotulos, nome_modelo)
#ClassificaEstados.modelo_info(modelo)
#print(ClassificaEstados.testar_modelo(jogos, rotulos, modelo))

#ClassificaEstados.plot_tree(modelo)
#ClassificaEstados.plot_learning_curve(jogos, rotulos, modelo)

#(jogos_entrada, rotulos_entrada, jogos_saida, rotulos_saida)
#ClassificaEstados.undersampling("Jogos 2", "Rótulos 2", "Jogos 2 Balanceados", "Rotulos 2 Balanceados")
#simulacao.rodar_simulacao(X=0, model="Log Model")

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