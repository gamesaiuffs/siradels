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


from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO

# Marca tempo de início para computar duração do experimento
startTime = time.time()

# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
vscode = False
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


# Testar treino contra outras estratégias

estrategias = [Agente(imprimir=True), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
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
Bot 4 - Vitórias: 274 - Porcento Vitorias: 27.40% - Pontuação Média: 16.425
Bot 1 - Vitórias: 218 - Porcento Vitorias: 21.80% - Pontuação Média: 15.458
Bot 2 - Vitórias: 240 - Porcento Vitorias: 24.00% - Pontuação Média: 15.731
Agente - Vitórias: 11 - Porcento Vitorias: 1.10% - Pontuação Média: 5.571
Bot 3 - Vitórias: 257 - Porcento Vitorias: 25.70% - Pontuação Média: 16.096

Bot 2 - Vitórias: 172 - Porcento Vitorias: 17.20% - Pontuação Média: 14.684
MCTS - Vitórias: 266 - Porcento Vitorias: 26.60% - Pontuação Média: 16.472
Bot 1 - Vitórias: 180 - Porcento Vitorias: 18.00% - Pontuação Média: 14.782
Bot 4 - Vitórias: 204 - Porcento Vitorias: 20.40% - Pontuação Média: 15.22
Bot 3 - Vitórias: 178 - Porcento Vitorias: 17.80% - Pontuação Média: 14.76

Felipe. - Vitórias: 731 - Porcento Vitorias: 73.10% - Pontuação Média: 26.117
Bot 3 - Vitórias: 83 - Porcento Vitorias: 8.30% - Pontuação Média: 12.574
Bot 2 - Vitórias: 58 - Porcento Vitorias: 5.80% - Pontuação Média: 12.264
Bot 4 - Vitórias: 71 - Porcento Vitorias: 7.10% - Pontuação Média: 12.622
Bot 1 - Vitórias: 57 - Porcento Vitorias: 5.70% - Pontuação Média: 12.226

Felipe. - Vitórias: 739 - Porcento Vitorias: 73.90% - Pontuação Média: 25.693
Bot 2 - Vitórias: 83 - Porcento Vitorias: 8.30% - Pontuação Média: 12.549
Bot 1 - Vitórias: 73 - Porcento Vitorias: 7.30% - Pontuação Média: 12.457
MCTS - Vitórias: 101 - Porcento Vitorias: 10.10% - Pontuação Média: 13.371
Agente - Vitórias: 4 - Porcento Vitorias: 0.40% - Pontuação Média: 4.585
Tempo da simulação = 191.60s
'''


