from classes.Experimento import Experimento
import time

from classes.openaigym_env.Citadels import Citadels
from classes.strategies.Agente import Agente
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
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

# Cria instância do ambiente seguindo o modelo da OpeanAI Gym apra treinar modelos
'''
env = Citadels()
'''
# Método que checa se o Ambiente segue os padrões da OpeanAI Gym
'''
check_env(env)
'''

# Cria, treina e salva instância de modelo de RL da biblioteca Stable-Baseline
'''
model = PPO(env=env, policy='MlpPolicy')
model.learn(total_timesteps=100000)
model.save("citadels_agent")
'''

# Cria uma instância experimento para gerar estatítisticas e comparar o desempenho dos modelos
# Treinar modelo MCTS RL por 10min = 600s
'''
experimento = Experimento(caminho)
experimento.treinar_modelo_mcts(600, 0)
'''

# Testar treino contra outras estratégias
estrategias = [Agente(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
Experimento.testar_estrategias(estrategias, 1000)

estrategias = [EstrategiaMCTS(caminho), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
Experimento.testar_estrategias(estrategias, 1000)

estrategias = [EstrategiaFelipe(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
Experimento.testar_estrategias(estrategias, 1000)

estrategias = [Agente(), EstrategiaMCTS(caminho), EstrategiaFelipe(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2')]
Experimento.testar_estrategias(estrategias, 1000)

# Imprime duração do experimento
print(f"Tempo da simulação = {(time.time() - startTime):.2f}s")

'''
C:\Users\felip\PycharmProjects\Scripts\python.exe D:\Git\siradels\Principal.py 

Bot 2 - Vitórias: 262 - Porcento Vitorias: 26.20% - Pontuação Média: 15.716
Bot 1 - Vitórias: 229 - Porcento Vitorias: 22.90% - Pontuação Média: 15.637
Agente - Vitórias: 7 - Porcento Vitorias: 0.70% - Pontuação Média: 5.206
Bot 4 - Vitórias: 247 - Porcento Vitorias: 24.70% - Pontuação Média: 15.745
Bot 3 - Vitórias: 255 - Porcento Vitorias: 25.50% - Pontuação Média: 16.109

MCTS - Vitórias: 257 - Porcento Vitorias: 25.70% - Pontuação Média: 16.308
Bot 2 - Vitórias: 201 - Porcento Vitorias: 20.10% - Pontuação Média: 15.158
Bot 1 - Vitórias: 194 - Porcento Vitorias: 19.40% - Pontuação Média: 14.999
Bot 4 - Vitórias: 187 - Porcento Vitorias: 18.70% - Pontuação Média: 15.056
Bot 3 - Vitórias: 161 - Porcento Vitorias: 16.10% - Pontuação Média: 14.874

Felipe. - Vitórias: 704 - Porcento Vitorias: 70.40% - Pontuação Média: 25.714
Bot 3 - Vitórias: 58 - Porcento Vitorias: 5.80% - Pontuação Média: 12.385
Bot 4 - Vitórias: 65 - Porcento Vitorias: 6.50% - Pontuação Média: 12.732
Bot 2 - Vitórias: 74 - Porcento Vitorias: 7.40% - Pontuação Média: 12.736
Bot 1 - Vitórias: 99 - Porcento Vitorias: 9.90% - Pontuação Média: 12.79

MCTS - Vitórias: 110 - Porcento Vitorias: 11.00% - Pontuação Média: 13.315
Felipe. - Vitórias: 725 - Porcento Vitorias: 72.50% - Pontuação Média: 25.521
Bot 1 - Vitórias: 73 - Porcento Vitorias: 7.30% - Pontuação Média: 12.255
Bot 2 - Vitórias: 89 - Porcento Vitorias: 8.90% - Pontuação Média: 12.725
Agente - Vitórias: 3 - Porcento Vitorias: 0.30% - Pontuação Média: 4.707
Tempo da simulação = 74.73s

Process finished with exit code 0
'''




