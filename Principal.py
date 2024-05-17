from classes.Experimento import Experimento
import time

from classes.openaigym_env.Citadels import Citadels
from classes.strategies.Agente import Agente
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria


from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO

env = Citadels()
#check_env(env)

model = PPO(env = env,
  policy= 'MlpPolicy',
  batch_size= 64,
  n_steps= 32,
  gamma= 0.999,
  learning_rate= 0.000222425,
  ent_coef= 1.37976e-07,
  clip_range= 0.4,
  n_epochs= 5,
  gae_lambda= 0.9,
  max_grad_norm= 0.3,
  vf_coef= 0.19816)
#model.learn(total_timesteps=100000)
#model.save("ppo_citadels")


# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
vscode = False
if vscode:
    caminho = './classes'
else:  # PyCharm
    caminho = '.'

experimento = Experimento(caminho)
startTime = time.time()

# Treinar modelo por 10min = 600s
#experimento.treinar_modelo_mcts(60)

# Testar treino contra outras estratégias
estrategias = [Agente(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
Experimento.testar_estrategias(estrategias)

print(f"Tempo da simulação = {(time.time() - startTime):.2f}s")




