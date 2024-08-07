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

path = "modelo4/3"


# Método que checa se o Ambiente segue os padrões da OpeanAI Gym
'''
check_env(env)
'''

# Cria, treina e salva instância de modelo de RL da biblioteca Stable-Baseline

# model = DQN(
#             "MlpPolicy",                     # Política de rede neural MLP
#             env=env,                         # Ambiente de OpenAI Gym
#             verbose=0,                       # Nível de detalhamento dos logs

#             # Parâmetros de exploração
#             exploration_initial_eps=0.7,     # Taxa inicial de exploração alta
#             exploration_final_eps=0.7,       # Taxa final de exploração baixa
#             exploration_fraction=0.3,        # Fração do total de etapas dedicadas à exploração

#             # Parâmetros de treinamento e otimização
#             learning_rate=6.3e-4,            # Taxa de aprendizado
#             learning_starts=1000,            # Número de etapas de aprendizado antes de começar a treinar
#             gradient_steps=-1,               # Número de passos de gradiente (padrão usa -1, que é automático)
#             policy_kwargs=dict(net_arch=[256, 256]),  # Arquitetura da rede neural

#             # Parâmetros de desconto e frequência de treinamento
#             gamma=0.99,                      # Fator de desconto
#             train_freq=4,                    # Frequência de treinamento (a cada 4 passos)

#             # Parâmetros do replay buffer
#             buffer_size=50000,               # Tamanho do buffer de replay
#             batch_size=128,                  # Tamanho do lote de amostras para o treinamento
#             target_update_interval=1000,     # Intervalo de atualização do alvo
#         )


# Melhor até agora +- 40% de vitória contra aleatórios 
# model = DQN(
#     "MlpPolicy",                     
#     env=env,                         
#     verbose=0,                       

#     # Parâmetros de exploração
#     exploration_initial_eps=0.5,
#     exploration_final_eps=0.2,      
#     exploration_fraction=0.3,       

#     # Parâmetros de treinamento e otimização
#     learning_rate=1e-5,             
#     learning_starts=2000,           
#     gradient_steps=-1,            
#     policy_kwargs=dict(net_arch=[256, 256]),  

#     # Parâmetros de desconto e frequência de treinamento
#     gamma=0.7,                     
#     train_freq=10,                   

#     # Parâmetros do replay buffer
#     buffer_size=100000,             
#     batch_size=256,                 
#     target_update_interval=800
# )
# print()



# modelo 3 
    # exploração inicial 0.5 -> 0.8
    # exploração final 0.3 -> 0.1
    # piorou - 8% de vitória
    
    # exploração inicial 0.8 -> 0.7
    # exploração final 0.1 -> 0.2
    # melhorou - 34% de vitória - salvo - modelo4/2
    
    # exploração inicial 0.7 -> 0.6
    # piorou - 2% e 30% - 10000 steps
        # 29% - 30000 steps
    
    # exploração inicial 0.6 -> 0.7
    # exploração final 0.2 -> 0.3
        # piorou - 3% 
        
        
        
    
# modelo 4 -
    # learning rate - 1e-4
        # 43% - 0% - 
        
    
# (venv) D:\github\siradels>python Principal.py
# step:  10000
# ptds:  99
# Bot 3 - Vitórias: 16 - Porcento Vitorias: 16.00% - Pontuação Média: 13.94
# Bot 4 - Vitórias: 20 - Porcento Vitorias: 20.00% - Pontuação Média: 14.84
# Bot 2 - Vitórias: 9 - Porcento Vitorias: 9.00% - Pontuação Média: 13.1
# Bot 1 - Vitórias: 17 - Porcento Vitorias: 17.00% - Pontuação Média: 14.11
# Agente - Vitórias: 38 - Porcento Vitorias: 38.00% - Pontuação Média: 18.47
# Tempo da simulação = 114.73s
    
model = DQN(
            "MlpPolicy",                     # Política de rede neural MLP
            env=env,                         # Ambiente de OpenAI Gym
            verbose=0,                       # Nível de detalhamento dos logs

            # Parâmetros de exploração
            exploration_initial_eps=0.7,     # Taxa inicial de exploração alta
            exploration_final_eps=0.3,       # Taxa final de exploração baixa
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

model.learn(total_timesteps=10000)
model.save(path)
print()

# Cria uma instância experimento para gerar estatítisticas e comparar o desempenho dos modelos
# Treinar modelo MCTS RL por 10min = 600s

# experimento = Experimento(caminho)
# experimento.treinar_modelo_mcts(600, 0)


# Testar treino contra outras estratégias
model = DQN.load(path, env=env)

# model.exploration_rate = 0.1



estrategias = [Agente(imprimir=False, model=model), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
Experimento.testar_estrategias(estrategias, 100, True)

# estrategias = [EstrategiaMCTS(caminho), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
# Experimento.testar_estrategias(estrategias, 1000)

# estrategias = [EstrategiaFelipe(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
# Experimento.testar_estrategias(estrategias, 1000)

# estrategias = [Agente(), EstrategiaMCTS(caminho), EstrategiaFelipe(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2')]
# Experimento.testar_estrategias(estrategias, 1000)


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


