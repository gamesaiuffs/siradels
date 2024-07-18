# import gymnasium as gym
# import time

# from classes.Experimento import Experimento
# from classes.enum.TipoAcaoOpenAI import TipoAcaoOpenAI
# from classes.openaigym_env.Citadels import Citadels
# from classes.strategies.Agente import Agente
# from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
# from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
# from classes.strategies.EstrategiaManual import EstrategiaManual
# from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria


# from stable_baselines3.common.env_checker import check_env
# from stable_baselines3 import DQN

# # Marca tempo de início para computar duração do experimento
# startTime = time.time()

# # Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
# vscode = False
# if vscode:
#     caminho = './classes'
# else:  # PyCharm
#     caminho = '.'

# # Cria instância do ambiente seguindo o modelo da OpeanAI Gym para treinar modelos

# gym.register(
#     id='Citadels',
#     entry_point='classes.openaigym_env.Citadels:Citadels',
#     # parâmetros __init__
#     # kwargs={'game': None}
# )
# env = gym.make('Citadels')


# # Método que checa se o Ambiente segue os padrões da OpeanAI Gym
# '''
# check_env(env)
# '''

# # Cria, treina e salva instância de modelo de RL da biblioteca Stable-Baseline

# # model = DQN(env=env, policy='MlpPolicy')
# # print("treinando...")

# # model = DQN (
# #     "MlpPolicy",
# #     env=env,
# #     verbose=2,
# #     # exploration_initial_eps=1.0,  # Aumenta a exploração inicial
# #     exploration_final_eps=0.1,  # Aumenta a exploração final
# #     target_update_interval=250,
# #     learning_rate = 6.3e-4,
# #     learning_starts=0, 
# #     gradient_steps=-1,
# #     exploration_fraction=0.12,
# #     policy_kwargs= dict(net_arch=[256, 256]),
# #     gamma= 0.99,
# #     train_freq=4,
# #     buffer_size=50000,  # Ajusta o tamanho do buffer de replay
# #     batch_size=128,  # Ajusta o tamanho do batch
# # )

# # model = DQN(
# #     "MlpPolicy",  # Política de rede neural MLP
# #     env=env,
# #     verbose=2,  # Nível de detalhamento dos logs

# #     # Parâmetros de exploração
# #     exploration_final_eps=0.1,  # Valor final da taxa de exploração

# #     # Parâmetros de treinamento e otimização
# #     target_update_interval=250,  # Intervalo de atualização do alvo
# #     learning_rate=6.3e-4,  # Taxa de aprendizado
# #     learning_starts=0,  # Número de etapas de aprendizado antes de começar a treinar
# #     gradient_steps=-1,  # Número de passos de gradiente (padrão usa -1, que é automático)
# #     exploration_fraction=0.12,  # Fração do total de etapas dedicadas à exploração
# #     policy_kwargs=dict(net_arch=[256, 256]),  # Arquitetura da rede neural

# #     # Parâmetros de desconto e frequência de treinamento
# #     gamma=0.99,  # Fator de desconto
# #     train_freq=4,  # Frequência de treinamento (a cada 4 passos)

# #     # Parâmetros do replay buffer
# #     buffer_size=50000,  # Tamanho do buffer de replay
# #     batch_size=128,  # Tamanho do lote de amostras para o treinamento
# # )

# ref = 0

# while (True):
#     print("\n\n Rodada: ", ref)
#     model = DQN.load("reforco/"+str(ref))
#     model.set_env(env=env)

#     model.learn(total_timesteps=100)
#     ref = ref + 1
#     model.save("reforco/"+str(ref))
#     print()
#     model = DQN.load("reforco/"+str(ref))
#     model.set_env(env=env)
#     model.exploration_rate = 0.0
#     # model.policy.exploration_rate = 0.0
    
    
#     print("jogando")

#     estrategias = [Agente(model=model), EstrategiaTotalmenteAleatoria('Bot 0'), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3')]
#     Experimento.testar_estrategias(estrategias, 1)

# print()
# # Cria uma instância experimento para gerar estatítisticas e comparar o desempenho dos modelos
# # Treinar modelo MCTS RL por 10min = 600s

# # experimento = Experimento(caminho)
# # experimento.treinar_modelo_mcts(600, 0)


# # Testar treino contra outras estratégias

# # estrategias = [Agente(imprimir=False), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
# # Experimento.testar_estrategias(estrategias, 1000, True)

# # estrategias = [EstrategiaMCTS(caminho), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
# # Experimento.testar_estrategias(estrategias, 1000)

# # estrategias = [EstrategiaFelipe(), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
# # Experimento.testar_estrategias(estrategias, 1000)

# print("jogando")

# estrategias = [Agente(), EstrategiaTotalmenteAleatoria('Bot 0'), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3')]
# Experimento.testar_estrategias(estrategias, 100)


# # Imprime duração do experimento
# print(f"Tempo da simulação = {(time.time() - startTime):.2f}s")


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

ref = 0

while True:
    print("\n\nRodada:", ref)
    if ref == 0:
        # Cria e treina um novo modelo
        # model = DQN(
        #     "MlpPolicy",
        #     env=env,
        #     verbose=0,
        #     exploration_final_eps=0.1,
        #     target_update_interval=250,
        #     learning_rate=6.3e-4,
        #     learning_starts=0,
        #     gradient_steps=-1,
        #     exploration_fraction=0.12,
        #     policy_kwargs=dict(net_arch=[256, 256]),
        #     gamma=0.99,
        #     train_freq=4,
        #     buffer_size=50000,
        #     batch_size=128,
        # )
        
        # model = DQN(
        #     "MlpPolicy",                     # Política de rede neural MLP
        #     env=env,                         # Ambiente de OpenAI Gym
        #     verbose=0,                       # Nível de detalhamento dos logs

        #     # Parâmetros de exploração
        #     exploration_initial_eps=0.7,     # Taxa inicial de exploração alta
        #     exploration_final_eps=0.1,       # Taxa final de exploração baixa
        #     exploration_fraction=0.4,        # Fração do total de etapas dedicadas à exploração

        #     # Parâmetros de treinamento e otimização
        #     learning_rate=6.3e-4,            # Taxa de aprendizado
        #     learning_starts=1000,            # Número de etapas de aprendizado antes de começar a treinar
        #     gradient_steps=-1,               # Número de passos de gradiente (padrão usa -1, que é automático)
        #     policy_kwargs=dict(net_arch=[256, 256]),  # Arquitetura da rede neural

        #     # Parâmetros de desconto e frequência de treinamento
        #     gamma=0.99,                      # Fator de desconto
        #     train_freq=4,                    # Frequência de treinamento (a cada 4 passos)

        #     # Parâmetros do replay buffer
        #     buffer_size=50000,               # Tamanho do buffer de replay
        #     batch_size=128,                  # Tamanho do lote de amostras para o treinamento
        #     target_update_interval=1000,     # Intervalo de atualização do alvo
        # )
        
        model = DQN(
            "MlpPolicy",                     
            env=env,                         
            verbose=0,                       

            # Parâmetros de exploração
            exploration_initial_eps=0.5,    
            exploration_final_eps=0.2,      
            exploration_fraction=0.3,       

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
            target_update_interval=800,     
        )
        
        # proximas modificações 
            # reduzir gamma (menos peso para recompensas futuras)
                # pode ajudar ao modelo aprender a não escolher ação errada 
            
            # learning rate
                # Alta: Pode fazer o modelo aprender mais rapidamente, mas também pode levar a um comportamento instável e saltos excessivos.
                # Baixa: Pode resultar em aprendizado mais lento, mas mais estável e com convergência mais suave.
                
            # train freq: 
                # quantos passos para atualizar a rede 
                
            # buffer size : grande = bom 
            
            # batch size: grande = melhor
            
            # target_update_interval    
                # curto = melhor
            
    else:
        # Carrega o modelo treinado
            model = DQN.load("reforco3/" + str(ref))
        

    # model.learn(total_timesteps=10000)

    print("Treinando...")
    fail = True
    while fail:
        try:
            model.set_env(env=env)
            # model.exploration_initial_eps = 0.5
            # model.exploration_final_eps = 0.1
            # model.exploration_rate = 0.7    
            model.learn(total_timesteps=10000)
            fail = False
        except KeyboardInterrupt: 
            exit(0)
        except: 
            print("Erro...")
            model = DQN.load("reforco3/" + str(ref))
            model.set_env(env=env)
            continue
        
    print()
    
    ref += 1
    model.save("reforco3/" + str(ref))
    
    

    print("Jogando...")
    # model = DQN.load("reforco")
    # model.set_env(env)
    
    # Definindo exploração para zero durante o teste
    

    fail = True
    while fail:
        try:
            model = DQN.load("reforco3/" + str(ref), env)
            model.exploration_rate = 0.1
            estrategias = [Agente(model=model), EstrategiaTotalmenteAleatoria('Bot 0'), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3')]
            Experimento.testar_estrategias(estrategias, 100)
            break
        except KeyboardInterrupt: 
            exit(0)
        except: 
            print("Erro...")
            continue

    print()
    print(f"Tempo da simulação = {(time.time() - startTime):.2f}s")
