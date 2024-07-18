import gymnasium as gym
import time
import numpy as np

from classes.Experimento import Experimento
from classes.enum.TipoAcaoOpenAI import TipoAcaoOpenAI
from classes.openaigym_env.Citadels import Citadels
from classes.strategies.Agente import Agente
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaManual import EstrategiaManual
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria

from stable_baselines3 import DQN

# Marca tempo de início para computar duração do experimento
startTime = time.time()

# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
vscode = False
if vscode:
    caminho = './classes'
else:  # PyCharm
    caminho = '.'

# Cria instância do ambiente seguindo o modelo da OpenAI Gym para treinar modelos
gym.register(
    id='Citadels',
    entry_point='classes.openaigym_env.Citadels:Citadels',
)

env = gym.make('Citadels')

# Verifica se o ambiente está conforme os padrões da OpenAI Gym
# check_env(env)

# Cria e treina um novo modelo
model = DQN(
    "MlpPolicy",                     # Política de rede neural MLP
    env=env,                         # Ambiente de OpenAI Gym
    verbose=0,                       # Nível de detalhamento dos logs

    # Parâmetros de exploração
    exploration_initial_eps=1.0,     # Taxa inicial de exploração alta
    exploration_final_eps=0.1,       # Taxa final de exploração baixa
    exploration_fraction=0.3,        # Fração do total de etapas dedicadas à exploração

    # Parâmetros de treinamento e otimização
    learning_rate=6.3e-4,            # Taxa de aprendizado
    learning_starts=1000,            # Número de etapas de aprendizado antes de começar a treinar
    gradient_steps=-1,               # Número de passos de gradiente (padrão usa -1, que é automático)
    policy_kwargs=dict(net_arch=[256, 256]),  # Arquitetura da rede neural

    # Parâmetros de desconto e frequência de treinamento
    gamma=0.99,                      # Fator de desconto
    train_freq=4,                    # Frequência de treinamento (a cada 4 passos)

    # Parâmetros do replay buffer
    buffer_size=50000,               # Tamanho do buffer de replay
    batch_size=128,                  # Tamanho do lote de amostras para o treinamento
    target_update_interval=1000,     # Intervalo de atualização do alvo
)

total_timesteps = 1000
checkpoint_interval = 100

print("Treinando...")

for i in range(0, total_timesteps, checkpoint_interval):
    # Treina o modelo por checkpoint_interval passos
    model.learn(total_timesteps=checkpoint_interval)

    # Salva o modelo após cada intervalo
    ref = (i + checkpoint_interval) // checkpoint_interval
    model.save("treino/" + str(ref))

    print()
    print(f"Rodada de teste após {i + checkpoint_interval} passos de treinamento...")
    print()
    # Carrega o modelo e configura para testes
    test_model = DQN.load("treino/" + str(ref), env)
    test_model.exploration_rate = 0.1

    # Executa 100 rodadas de teste
    estrategias = [
        Agente(model=test_model),
        EstrategiaTotalmenteAleatoria('Bot 0'),
        EstrategiaTotalmenteAleatoria('Bot 1'),
        EstrategiaTotalmenteAleatoria('Bot 2'),
        EstrategiaTotalmenteAleatoria('Bot 3')
    ]
    Experimento.testar_estrategias(estrategias, 100)

print(f"Tempo total da simulação = {(time.time() - startTime):.2f}s")