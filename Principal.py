from classes.Experimento import Experimento
import time

from classes.openaigym_env.Citadels import Citadels
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria

'''
# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
vscode = False
if vscode:
    caminho = './classes'
else:  # PyCharm
    caminho = '.'

experimento = Experimento(caminho)
startTime = time.time()

# Treinar modelo por 10min = 600s
experimento.treinar_modelo_mcts(60)

# Testar treino contra outras estratégias
estrategias = [EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaMCTS(caminho), EstrategiaTotalmenteAleatoria('Bot 4')]
Experimento.testar_estrategias(estrategias)

print(f"Tempo da simulação = {(time.time() - startTime):.2f}s")
'''

import gymnasium as gym

from stable_baselines3 import A2C

env = Citadels()

model = A2C("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=1000, log_interval=4)
model.save("ppo_citadels")

# remove to demonstrate saving and loading
#del model
#model = PPO.load("ppo_citadels")

#obs = env.reset()
#while True:
#    action, _states = model.predict(obs)
#    obs, rewards, dones, _, _ = env.step(action)
