from stable_baselines3 import DQN
import gymnasium as gym
import os
import random
import matplotlib.pyplot as plt
import numpy as np
from stable_baselines3.common import results_plotter
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import load_results, ts2xy
from stable_baselines3.common.callbacks import BaseCallback, EvalCallback
from stable_baselines3.common.env_util import make_vec_env

from classes.strategies.Agente import Agente
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaManual import EstrategiaManual
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.Experimento import Experimento
from stable_baselines3.common.results_plotter import load_results, ts2xy, plot_results
from stable_baselines3.common.evaluation import evaluate_policy

from multiprocessing import Process
import time
import ray

ENV_ID = "Citadels"
ENV_ENTRY_POINT = 'classes.openaigym_env.Citadels:Citadels'

gym.register(
    id=ENV_ID,
    entry_point=ENV_ENTRY_POINT
)


# Configurações gerais 
DIR_NAME = "experimentos/teste10cors"
TRAIN_STEPS = 100000
MODEL_SAVE_FREQ = 10000
NOT_ALLOW_REUSE_DIRS = False
ENV_RENDER_MODE = None

EVAL_LOG_FILE = os.path.join(DIR_NAME, "evaluations.txt")
# BASE_EVAL_LOG_FILE = "exp_"
SAVE_FILE = ""
EVAL_FREQUENCY = MODEL_SAVE_FREQ
NUM_EVAL_EPISODES = 100
PLOT_FREQUENCY = 10000
NUM_PROCESSES = 10

LEARN_ENV = gym.make(ENV_ID)
TEST_ENV = gym.make(ENV_ID)


class SaveOnTrainStepsNumCallback(BaseCallback):
    def __init__(self, save_freq: int, verbose: int, num_process: int):
        super().__init__(verbose)  # 0 -> verbose
        self.save_freq = save_freq
        self.log_dir = DIR_NAME + "/in_" + str(num_process)
        self.num_saves = 1
        self.num_process = num_process
        
        self.episode_rewards = []
        self.episode_lengths = []
        self.eva_rew_moments = []
        self.mean_rewards = []
        self.mean_lengths = []
        
        self.save_path =  os.path.join(self.log_dir, str(self.num_saves))
        self.historico_vitorias = []    # Historico de vitórias respectivos ao nomero de passos 
        self.pontos_de_ref = []         # Valores de passo em que dados foram coletados para o gráfico
        self.pontos_media = []          # média de pontuação para cada teste
        
        if not os.path.isdir(self.log_dir): 
            os.makedirs(self.log_dir)
            
        print("Process ", num_process, " started")
        
        if (num_process == 0): print()

    def plot_performance(self) -> None:
        plt.figure(figsize=(10, 6))
        plt.xlabel("Learn steps")
        plt.ylabel("Average Score")
        plt.title("Model performance in training")
        plt.grid(True)
        plt.plot(self.pontos_de_ref, self.historico_vitorias, label="Win percentage")
        plt.plot(self.pontos_de_ref, self.pontos_media, label="Average Score")
        plt.ylim(0, 100)
        plt.legend()
        save_path = os.path.join(self.log_dir, f"performance_plot{self.num_saves}.png")
        plt.savefig(save_path)
        # print(f"Gráfico salvo em {save_path}")
        
    def plot_av_reward(self):
        if len(self.eva_rew_moments) == len(self.mean_rewards) and len(self.mean_rewards) > 0:
            plt.figure(figsize=(10, 6))
            plt.title("Average Reward")
            plt.xlabel("Step")
            plt.ylabel("Reward")
            plt.grid(True)
            plt.plot(self.eva_rew_moments, self.mean_rewards, label="Mean Reward")
            plt.legend()
            save_path = os.path.join(self.log_dir, f"av_reward{self.num_saves}.png")
            plt.savefig(save_path)
            # print(f"Gráfico salvo em {save_path}")
        else:
            print("Tamanhos diferentes entre 'eva_rew_moments' e 'mean_rewards' ou lista vazia. Gráfico não gerado.")


    def evaluate_model_policy(self, model): 
        local_env = TEST_ENV
        local_env.reset()
        
        mean_reward, std_reward = evaluate_policy(model, local_env, n_eval_episodes=10, deterministic=False)
        # print(mean_reward)
        self.mean_rewards.append(mean_reward)
        self.eva_rew_moments.append(self.n_calls)
        # input("Pausa para analise das recompensas retornadas")


    def _on_step(self) -> bool:
        # print(f"steps: {self.n_calls}/{TRAIN_STEPS}", end="\r")
        
        if self.n_calls % self.save_freq == 0:
            print("Process", self.num_process, " saving...")

            # print(f"Salvando modelo: {self.save_path}")
            self.model.save(self.log_dir + "/"+str(self.num_saves))
            
            # Teste do modelo atual
            local_model = DQN.load(self.log_dir + "/"+str(self.num_saves))
            # local_model.exploration_rate = 0.1
            
            self.evaluate_model_policy(local_model) 
            
            self.plot_av_reward()
            
            
            file = open(os.path.join(self.log_dir, "evaluations.txt"), "a+")
            # print(f"rodada de testes... {self.save_path}")
            file.write("-"*30+"\n")
            file.write(self.save_path+"\n")
            
            # Configurar de acordo com o ambiente 
            local_env = TEST_ENV
            local_env.reset()
            
            estrategias = [Agente(imprimir=False, model=local_model), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
            vitoria, pontuacao_media = Experimento.testar_estrategias_graficos(estrategias, NUM_EVAL_EPISODES, True)

            self.historico_vitorias.append(vitoria)
            self.pontos_de_ref.append(self.n_calls)
            self.pontos_media.append(pontuacao_media)
                
            file.write(f"Rodadas: {NUM_EVAL_EPISODES} Steps: {self.n_calls} Vitorias: {vitoria} Media de pontos {pontuacao_media}"+"\n")
            file.close()
            
            if self.n_calls % PLOT_FREQUENCY == 0: 
                self.plot_performance()
                # print(f"Grafico de {self.n_calls} steps plotado!")
            
            # print("Testes Finalizados")
            
            self.num_saves += 1
            self.save_path = os.path.join(self.log_dir, str(self.num_saves))

        return True
    

env = Monitor(LEARN_ENV, DIR_NAME)
test = 0

# if __name__ == "__main__":
    
#     if not os.path.isdir(DIR_NAME): 
#             os.makedirs(DIR_NAME)
#     else: 
        # print(f"Diretório '{DIR_NAME}' já existe. Usá-lo pode afetar o conteúdo pré-existente.")
#         if NOT_ALLOW_REUSE_DIRS: exit(0)


#     SAVE_FILE = os.path.join(DIR_NAME, f"{BASE_EVAL_LOG_FILE}{test}")
#     callback = SaveOnTrainStepsNumCallback(MODEL_SAVE_FREQ, verbose=0)
    

    
#     # Teste 4 - modelo com ajuste mais amortecido 
#     # model = DQN(
#     #     policy="MlpPolicy",
#     #     env=env,
#     #     verbose=0,

#     #     tau=0.2,

#     #     # Parâmetros de exploração
#     #     exploration_initial_eps=1.0,
#     #     exploration_final_eps=0.2,
#     #     exploration_fraction=0.8,

#     #     # Parâmetros de treinamento e otimização
#     #     learning_rate=0.0001,
#     #     learning_starts=2000,
#     #     gradient_steps=-1,
#     #     policy_kwargs=dict(net_arch=[64, 64]),

#     #     # Parâmetros de desconto e frequência de treinamento
#     #     gamma=0.9,
#     #     train_freq=1500,

#     #     # Parâmetros do replay buffer
#     #     buffer_size=100000,
#     #     batch_size=512,
#     #     target_update_interval=2000
#     # )
#     model = DQN("MlpPolicy",  env=env)
    
    
#     try: 
#         model.learn(total_timesteps=TRAIN_STEPS, callback=callback)
#     except Exception as e: 
#         print("ERRO:", e)
    
#     test += 1

env = gym.make(ENV_ID)

envs = [gym.make(ENV_ID) for _ in range(NUM_PROCESSES)]

@ray.remote
def model_train(num_process: int):
    # model = DQN(
    #     policy="MlpPolicy",
    #     env=env,
    #     verbose=0,

    #     tau=0.2,

    #     # Parâmetros de exploração
    #     exploration_initial_eps=1.0,
    #     exploration_final_eps=0.2,
    #     exploration_fraction=0.8,

    #     # Parâmetros de treinamento e otimização
    #     learning_rate=0.0001,
    #     learning_starts=2000,
    #     gradient_steps=-1,
    #     policy_kwargs=dict(net_arch=[64, 64]),

    #     # Parâmetros de desconto e frequência de treinamento
    #     gamma=0.9,
    #     train_freq=1500,

    #     # Parâmetros do replay buffer
    #     buffer_size=100000,
    #     batch_size=512,
    #     target_update_interval=2000
    # )
    model = DQN("MlpPolicy",  env=envs[num_process])
  
  
    callback = SaveOnTrainStepsNumCallback(MODEL_SAVE_FREQ, verbose=0, num_process=num_process)  
    
    model.learn(total_timesteps=TRAIN_STEPS, callback=callback)

    

# if __name__ == "__main__": 
#     if not os.path.isdir(DIR_NAME): 
#             os.makedirs(DIR_NAME)
#     else: 
#         print(f"Diretório '{DIR_NAME}' já existe. Usá-lo pode afetar o conteúdo pré-existente.")
#         if NOT_ALLOW_REUSE_DIRS: exit(0)

#     start_time = time.time()

#     processes = [Process(target=model_train, args=(idx_proc,)) for idx_proc in range(NUM_PROCESSES)]
    
#     for proc in processes: proc.start()
#     for proc in processes: proc.join()

#     end_time = time.time()
    
#     execution_time = end_time - start_time
#     print(f"Tempo de execução: {execution_time} segundos")

if __name__ == "__main__": 
    if not os.path.isdir(DIR_NAME): 
            os.makedirs(DIR_NAME)
    else: 
        print(f"Diretório '{DIR_NAME}' já existe. Usá-lo pode afetar o conteúdo pré-existente.")
        if NOT_ALLOW_REUSE_DIRS: exit(0)

    start_time = time.time()

    # processes = [Process(target=model_train, args=(idx_proc,)) for idx_proc in range(NUM_PROCESSES)]
    
    # for proc in processes: proc.start()
    # for proc in processes: proc.join()
    
    ray.init(num_cpus=10)
    
    processes = [model_train.remote(idx_proc) for idx_proc in range(NUM_PROCESSES)]
    ray.get(processes)
    
    ray.shutdown()

    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"Tempo de execução: {execution_time} segundos")
