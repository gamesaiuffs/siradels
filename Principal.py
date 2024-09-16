from classes.Experimento import Experimento
import numpy as np
import json
from classes.classification.ClassificaEstados import ClassificaEstados
from classes.classification.ColetaEstados import ColetaEstados
from classes.classification.SimulacaoColeta import SimulacaoColeta 
from sklearn.model_selection import train_test_split
from classes.enum.TipoDistrito import TipoDistrito
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, make_scorer, accuracy_score, confusion_matrix, log_loss, ConfusionMatrixDisplay
from sklearn.model_selection import learning_curve
from sklearn.decomposition import PCA
from sklearn.model_selection import StratifiedGroupKFold
import matplotlib.pyplot as plt
'''
import gymnasium as gym
from classes.enum.TipoAcaoOpenAI import TipoAcaoOpenAI
from classes.openaigym_env.Citadels import Citadels
from classes.strategies.Agente import Agente
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
import joblib
'''
from classes.Experimento import Experimento
from classes.Simulacao import Simulacao
from classes.strategies.EstrategiaDjonatan import EstrategiaDjonatan
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
import time
vscode = True

n_features = 29

profundidade = 15
n_amostras = 10
min_samp = 351
win_weigth = {0: 1, 1: 3}
criterion = "gini"
ww = 3

jogos = f"Jogos {n_amostras} {n_features}f"
rotulos = f"Rótulos {n_amostras} {n_features}f" 
modelo = f"{criterion} {min_samp}ms {ww}mw {n_features}f"

#(qtd_pts, n_features, nome_jogos, nome_rotulos, nome_modelo)
#ColetaEstados.coleta_amostras(n_amostras, n_features, jogos, rotulos, modelo)

#(jogos, rotulos, nome_modelo, criterion, profundidade)
#ClassificaEstados.treinar_modelo(False, jogos, rotulos, modelo, criterion, min_samp, win_weigth, profundidade)
#ClassificaEstados.treinar_floresta(False, jogos, rotulos, "Forest1", 100, criterion, min_samp, win_weigth, profundidade)
#ClassificaEstados.treinar_gradiente(False, jogos, rotulos, "Gradient1", 100, 'friedman_mse', min_samp, 'log_loss', 0.1, profundidade)

#(jogos, rotulos, n_features)
#ClassificaEstados.circuito_treino_teste(jogos, rotulos, n_features)
#ClassificaEstados.avalia_testes()

#(jogos, rotulos, nome_modelo)
#ClassificaEstados.modelo_info(modelo)
#print(ClassificaEstados.testar_modelo(jogos, rotulos, modelo, False))
#print(ClassificaEstados.testar_modelo(jogos, rotulos, 'Gradient1', False))

#ClassificaEstados.plot_tree(modelo)
#ClassificaEstados.plot_learning_curve(jogos, rotulos, modelo)

#(jogos_entrada, rotulos_entrada, jogos_saida, rotulos_saida)
#ClassificaEstados.undersampling("Jogos 2", "Rótulos 2", "Jogos 2 Balanceados", "Rotulos 2 Balanceados")
#simulacao.rodar_simulacao(X=0, model="Log Model")

# Cria instância do ambiente seguindo o modelo da OpeanAI Gym para treinar modelos

# Marca tempo de início para computar duração do experimento
#startTime = time.time()

# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
vscode = False
if vscode:
    caminho = './classes'
else:  # PyCharm
    caminho = '.'

'''
gym.register(
    id='Citadels',
    entry_point='classes.openaigym_env.Citadels:Citadels',
    # parâmetros __init__
    # kwargs={'game': None}
)
env = gym.make('Citadels')

# Método que checa se o Ambiente segue os padrões da OpeanAI Gym
check_env(env)
'''

# Cria, treina e salva instância de modelo de RL da biblioteca Stable-Baseline

#model = PPO(env=env, policy='MlpPolicy')
#model.learn(total_timesteps=100000)
#model.save("citadels_agent")

# Cria uma instância experimento para gerar estatítisticas e comparar o desempenho dos modelos
# Treinar modelo MCTS RL por 10min = 600s

#experimento = Experimento(caminho)
#experimento.treinar_modelo_mcts(600, 0)

# Testar treino contra outras estratégias

#estrategias = [Agente(imprimir=True), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
#Experimento.testar_estrategias(estrategias, 1000, True)

#estrategias = [EstrategiaDjonatan(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
#Experimento.testar_estrategias(estrategias, 1000)

#estrategias = [EstrategiaFelipe(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
#Experimento.testar_estrategias(estrategias, 1000)

#estrategias = [EstrategiaDjonatan(), EstrategiaFelipe(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3')]
#Experimento.testar_estrategias(estrategias, 1000)


# Imprime duração do experimento
#print(f"Tempo da simulação = {(time.time() - startTime):.2f}s")
