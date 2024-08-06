import gymnasium as gym
import time

from classes.Experimento import Experimento
from classes.enum.TipoAcaoOpenAI import TipoAcaoOpenAI
from classes.openaigym_env.Citadels import Citadels
from classes.strategies.Agente import Agente
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaManual import EstrategiaManual
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.strategies.EstrategiaGold import EstrategiaGold
from classes.strategies.EstrategiaAllin import EstrategiaAllin
from classes.strategies.EstrategiaEduardo import EstrategiaEduardo


from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO

# Marca tempo de início para computar duração do experimento
startTime = time.time()

# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
vscode = True
if vscode:
    caminho = './classes'
else:  # PyCharm
    caminho = '.'

# Cria instância do ambiente seguindo o modelo da OpeanAI Gym para treinar modelos

gym.register(
    id='Citadels',
    entry_point='classes.openaigym_env.Citadels:Citadels',
    # parâmetros __init__
    # kwargs={'game': None}
)
env = gym.make('Citadels')


# Método que checa se o Ambiente segue os padrões da OpeanAI Gym
'''
check_env(env)
'''

# Cria, treina e salva instância de modelo de RL da biblioteca Stable-Baseline

model = PPO(env=env, policy='MlpPolicy')
model.learn(total_timesteps=100000)
model.save("citadels_agent")


# Cria uma instância experimento para gerar estatítisticas e comparar o desempenho dos modelos
# Treinar modelo MCTS RL por 10min = 600s

experimento = Experimento(caminho)
experimento.treinar_modelo_mcts(600, 0)


<<<<<<< HEAD
# # Testar treino contra outras estratégias
# estrategias = [EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaEduardo(), EstrategiaFelipe()]
estrategias = [EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaEduardo(), EstrategiaFelipe(), EstrategiaMCTS(caminho)]
Experimento.testar_estrategias(estrategias, 1000)

# # estrategias_treino = [EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
# estrategias_treino = [EstrategiaFelipe('Felipe 1'), EstrategiaFelipe('Felipe 2'), EstrategiaFelipe('Felipe 3'), EstrategiaFelipe('Felipe 4')]
# experimento.treinar_modelo_mcts(estrategias_treino, 5000)
=======
# Testar treino contra outras estratégias
>>>>>>> main

estrategias = [Agente(imprimir=False), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
Experimento.testar_estrategias(estrategias, 1000, True)

estrategias = [EstrategiaMCTS(caminho), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
Experimento.testar_estrategias(estrategias, 1000)

estrategias = [EstrategiaFelipe(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
Experimento.testar_estrategias(estrategias, 1000)

estrategias = [Agente(), EstrategiaMCTS(caminho), EstrategiaFelipe(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2')]
Experimento.testar_estrategias(estrategias, 1000)


# Imprime duração do experimento
print(f"Tempo da simulação = {(time.time() - startTime):.2f}s")

'''
Bot 3 - Vitórias: 202 - Porcento Vitorias: 20.20% - Pontuação Média: 14.73
Bot 1 - Vitórias: 218 - Porcento Vitorias: 21.80% - Pontuação Média: 15.109
Bot 4 - Vitórias: 213 - Porcento Vitorias: 21.30% - Pontuação Média: 15.152
Bot 2 - Vitórias: 214 - Porcento Vitorias: 21.40% - Pontuação Média: 14.83
Agente - Vitórias: 153 - Porcento Vitorias: 15.30% - Pontuação Média: 13.126

Bot 2 - Vitórias: 182 - Porcento Vitorias: 18.20% - Pontuação Média: 14.594
Bot 4 - Vitórias: 198 - Porcento Vitorias: 19.80% - Pontuação Média: 14.203
Bot 3 - Vitórias: 193 - Porcento Vitorias: 19.30% - Pontuação Média: 14.271
MCTS - Vitórias: 250 - Porcento Vitorias: 25.00% - Pontuação Média: 15.381
Bot 1 - Vitórias: 177 - Porcento Vitorias: 17.70% - Pontuação Média: 14.044

Felipe. - Vitórias: 720 - Porcento Vitorias: 72.00% - Pontuação Média: 25.169
Bot 3 - Vitórias: 70 - Porcento Vitorias: 7.00% - Pontuação Média: 12.173
Bot 2 - Vitórias: 75 - Porcento Vitorias: 7.50% - Pontuação Média: 12.243
Bot 1 - Vitórias: 68 - Porcento Vitorias: 6.80% - Pontuação Média: 11.94
Bot 4 - Vitórias: 67 - Porcento Vitorias: 6.70% - Pontuação Média: 12.197

Felipe. - Vitórias: 715 - Porcento Vitorias: 71.50% - Pontuação Média: 25.101
MCTS - Vitórias: 98 - Porcento Vitorias: 9.80% - Pontuação Média: 13.775
Bot 2 - Vitórias: 72 - Porcento Vitorias: 7.20% - Pontuação Média: 12.679
Bot 1 - Vitórias: 68 - Porcento Vitorias: 6.80% - Pontuação Média: 12.346
Agente - Vitórias: 47 - Porcento Vitorias: 4.70% - Pontuação Média: 10.83
Tempo da simulação = 1060.15s
'''


