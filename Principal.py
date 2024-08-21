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
from stable_baselines3 import DQN

# Marca tempo de início para computar duração do experimento
start_time = time.time()

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

model = DQN(
    policy="MlpPolicy",
    env=env,
    verbose=2,

    # Parâmetros de exploração
    exploration_initial_eps=1.0,
    exploration_final_eps=0.1,
    exploration_fraction=0.9,

    # Parâmetros de treinamento e otimização
    learning_rate=1e-5,
    learning_starts=2000,
    gradient_steps=-1,
    policy_kwargs=dict(net_arch=[256, 256]),

    # Parâmetros de desconto e frequência de treinamento
    gamma=0.7,
    train_freq=10,

    # Parâmetros do replay buffer
    buffer_size=100000,
    batch_size=256,
    target_update_interval=800)
model.learn(total_timesteps=1000)
model.save("citadels_agent")


# Cria uma instância experimento para gerar estatítisticas e comparar o desempenho dos modelos
# Treinar modelo MCTS RL por 10min = 600s
'''
experimento = Experimento(caminho)
experimento.treinar_modelo_mcts(600, 0)
'''

# Testar treino contra outras estratégias

estrategias = [Agente(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
Experimento.testar_estrategias(estrategias, 1000)
'''
estrategias = [EstrategiaMCTS(caminho), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
Experimento.testar_estrategias(estrategias, 1000)

estrategias = [EstrategiaFelipe(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
Experimento.testar_estrategias(estrategias, 1000)

estrategias = [Agente(), EstrategiaMCTS(caminho), EstrategiaFelipe(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2')]
Experimento.testar_estrategias(estrategias, 10000)
'''

# Imprime duração do experimento
s = time.time() - start_time
m = s // 60
h = m // 60
s -= m * 60
m -= h * 60
print(f"Tempo de execução = {h:.0f}h {m:.0f}min {s:.2f}s")
