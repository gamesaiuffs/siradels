from classes.Experimento import Experimento
from classes.classification.ClassificaEstados import ClassificaEstados
from classes.classification.ColetaEstados import ColetaEstados
from classes.classification.SimulacaoColeta import SimulacaoColeta 
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from sklearn.model_selection import train_test_split
vscode = True

n_features = 29

profundidade = 30
n_amostras = 10000
min_samp = 200
win_weigth = {0: 1, 1: 3}
criterion = "log_loss"


jogos = f"Jogos {n_amostras} {n_features}f"
rotulos = f"Rótulos {n_amostras} {n_features}f" 
modelo = f"Model 10k d{profundidade} {n_features}f"

modelo = "log_loss 351ms 3mw 29f"


#(qtd_pts, n_features, nome_jogos, nome_rotulos, nome_modelo)
#ColetaEstados.coleta_amostras(n_amostras, n_features, jogos, rotulos, modelo)

#(jogos, rotulos, nome_modelo, criterion, profundidade)
#ClassificaEstados.treinar_modelo(False, jogos, rotulos, modelo, criterion, min_samp, win_weigth, profundidade)

#(jogos, rotulos, n_features)
#ClassificaEstados.circuito_treino_teste(jogos, rotulos, n_features)
ClassificaEstados.avalia_testes()

#(jogos, rotulos, nome_modelo)
#ClassificaEstados.modelo_info(modelo)
#print(ClassificaEstados.testar_modelo(jogos, rotulos, modelo, False))

#ClassificaEstados.plot_tree(modelo)
#ClassificaEstados.plot_learning_curve(jogos, rotulos, modelo)

#(jogos_entrada, rotulos_entrada, jogos_saida, rotulos_saida)
#ClassificaEstados.undersampling("Jogos 2", "Rótulos 2", "Jogos 2 Balanceados", "Rotulos 2 Balanceados")
#simulacao.rodar_simulacao(X=0, model="Log Model")

'''
estrategias = []

# Estrategias fixas e especificas
estrategias.append(EstrategiaDjonatan())
estrategias.append(EstrategiaAndrei())
estrategias.append(EstrategiaBernardo())
estrategias.append(EstrategiaFelipe())
estrategias.append(EstrategiaGustavo())
estrategias.append(EstrategiaJoao())

for i in range(5):          # fixo em 5 players
   estrategias.append(EstrategiaTotalmenteAleatoria(str(i+1)))
simulacao = Simulacao(estrategias, 8, True)

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