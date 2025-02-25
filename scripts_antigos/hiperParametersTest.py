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


ENV_ID = "Citadels"
ENV_ENTRY_POINT = 'classes.openaigym_env.Citadels:Citadels'

gym.register(
    id=ENV_ID,
    entry_point=ENV_ENTRY_POINT
)


# Configurações gerais 
DIR_NAME = "aa_experimentos_agr_vai_2"
TRAIN_STEPS = 300000
MODEL_SAVE_FREQ = 20000
NOT_ALLOW_REUSE_DIRS = True
ENV_RENDER_MODE = None

EVAL_LOG_FILE = os.path.join(DIR_NAME, "evaluations.txt")
BASE_EVAL_LOG_FILE = "exp_"
SAVE_FILE = ""
EVAL_FREQUENCY = MODEL_SAVE_FREQ
NUM_EVAL_EPISODES = 100
PLOT_FREQUENCY = 100000

LEARN_ENV = gym.make(ENV_ID)
TEST_ENV = gym.make(ENV_ID)


class SaveOnTrainStepsNumCallback(BaseCallback):
    def __init__(self, save_freq: int, verbose: int):
        super().__init__(verbose)  # 0 -> verbose
        self.save_freq = save_freq
        self.log_dir = DIR_NAME
        self.num_saves = 1
        
        self.episode_rewards = []
        self.episode_lengths = []
        self.eva_rew_moments = []
        self.mean_rewards = []
        self.mean_lengths = []
        
        self.save_path =  os.path.join(self.log_dir, str(self.num_saves))
        self.historico_vitorias = []    # Historico de vitórias respectivos ao nomero de passos 
        self.pontos_de_ref = []         # Valores de passo em que dados foram coletados para o gráfico
        self.pontos_media = []          # média de pontuação para cada teste

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
        save_path = os.path.join(SAVE_FILE, f"performance_plot{self.num_saves}.png")
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
            save_path = os.path.join(SAVE_FILE, f"av_reward{self.num_saves}.png")
            plt.savefig(save_path)
            # print(f"Gráfico salvo em {save_path}")
        else:
            print("Tamanhos diferentes entre 'eva_rew_moments' e 'mean_rewards' ou lista vazia. Gráfico não gerado.")

    def evaluate_model_policy(self, model): 
        local_env = TEST_ENV
        local_env.reset()
        
        mean_reward, std_reward = evaluate_policy(model, local_env, n_eval_episodes=10, deterministic=False)
        print(mean_reward)
        self.mean_rewards.append(mean_reward)
        self.eva_rew_moments.append(self.n_calls)
        # input("Pausa para analise das recompensas retornadas")


    def _on_step(self) -> bool:
        print(f"steps: {self.n_calls}/{TRAIN_STEPS}", end="\r")

        if self.n_calls % self.save_freq == 0:
            # self.plot_av_reward()
            print(f"Salvando modelo: {self.save_path}")
            self.model.save(SAVE_FILE + "/"+str(self.num_saves))
            
            # Teste do modelo atual
            local_model = DQN.load(SAVE_FILE + "/"+str(self.num_saves))
            local_model.exploration_rate = 0.1
            
            self.evaluate_model_policy(local_model)
            
            file = open(os.path.join(SAVE_FILE, "evaluations.txt"), "a+")
            print(f"rodada de testes... {self.save_path}")
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
                self.plot_av_reward()
                print(f"Graficos de {self.n_calls} steps plotados!")
            
            # print("Testes Finalizados")
            
            self.num_saves += 1
            self.save_path = os.path.join(self.log_dir, str(self.num_saves))

        return True
    

hyperparam_space = {
    'tau': [0.5, 0.7, 0.9],
    'exploration_initial_eps': [0.99, 0.9, 0.8, 0.7],
    'exploration_final_eps': [0.5, 0.4, 0.3, 0.1, 0.2],
    'exploration_fraction': [0.5, 0.6, 0.4, 0.3, 0.2],
    'learning_rate': [1e-4, 1e-3, 5e-4, 5e-3, ],
    'learning_starts': [1000, 3000, 5000],
    'gradient_steps': [1, 10, -1],
    'policy_net_arch': [[16], [32], [64], [16, 16], [32, 32], [48, 48], [64, 64], [128, 128]],
    'gamma': [0.95, 0.99, 0.75, 0.8],
    'train_freq': [1000, 500, 2000, 2500, 3000],
    'buffer_size': [25000, 50000, 100000],
    'batch_size': [64, 128, 256, 512],
    'target_update_interval': [100, 150, 300, 500, 1000]
}


def sample_hyperparams():
    return {key: random.choice(values) for key, values in hyperparam_space.items()}


def log_hyperparams(file_path, hyperparams, experiment_num):
    # with open(file_path, "a+") as file:
    #     file.write(f"======= Experimento {experiment_num} =======\n")
    #     for param, value in hyperparams.items():
    #         file.write(f"{param}: {value}\n")
    #     file.write("=============================================\n\n")

    file = open(file_path, "+a")
    file.write(f"======= Experimento {experiment_num} =======\n")
    for param, value in hyperparams.items():
        file.write(f"{param}: {value}\n")
    file.write("=============================================\n\n")
    file.close()

env = Monitor(LEARN_ENV, DIR_NAME)
test = 0

if __name__ == "__main__":
    
    if not os.path.isdir(DIR_NAME): 
            os.makedirs(DIR_NAME)
    else: 
        print(f"Diretório '{DIR_NAME}' já existe. Usá-lo pode afetar o conteúdo pré-existente.")
        if NOT_ALLOW_REUSE_DIRS: exit(0)

    
    while True: 
        hyperparams = sample_hyperparams()
        SAVE_FILE = os.path.join(DIR_NAME, f"{BASE_EVAL_LOG_FILE}{test}")
        callback = SaveOnTrainStepsNumCallback(MODEL_SAVE_FREQ, verbose=0)
        
        if not os.path.isdir(SAVE_FILE): 
            os.makedirs(SAVE_FILE)
        
        model = DQN(
            "MlpPolicy",
            env=env,
            tau=hyperparams['tau'],
            exploration_initial_eps=hyperparams['exploration_initial_eps'],
            exploration_final_eps=hyperparams['exploration_final_eps'],
            exploration_fraction=hyperparams['exploration_fraction'],
            learning_rate=hyperparams['learning_rate'],
            learning_starts=hyperparams['learning_starts'],
            gradient_steps=hyperparams['gradient_steps'],
            policy_kwargs=dict(net_arch=hyperparams['policy_net_arch']),
            gamma=hyperparams['gamma'],
            train_freq=hyperparams['train_freq'],
            buffer_size=hyperparams['buffer_size'],
            batch_size=hyperparams['batch_size'],
            target_update_interval=hyperparams['target_update_interval'],
            verbose=0
        )
        
        log_hyperparams(os.path.join(SAVE_FILE, "evaluations.txt"), hyperparams, test)
        
        try: 
            model.learn(total_timesteps=TRAIN_STEPS, callback=callback)
        except Exception as e: 
            print("ERRO:", e)
        
        test += 1





# Calcular média por episódio 
# def plot_av_reward(self):
#     if len(self.eva_rew_moments) == len(self.mean_rewards) and len(self.mean_rewards) > 0:
#         plt.figure(figsize=(10, 6))
#         plt.title("Average Reward")
#         plt.xlabel("Step")
#         plt.ylabel("Reward")
#         plt.grid(True)
#         plt.plot(self.eva_rew_moments, self.mean_rewards, label="Mean Reward")
#         plt.legend()
#         save_path = os.path.join(SAVE_FILE, f"av_reward{self.num_saves}.png")
#         plt.savefig(save_path)
#         print(f"Gráfico salvo em {save_path}")
#     else:
#         print("Tamanhos diferentes entre 'eva_rew_moments' e 'mean_rewards' ou lista vazia. Gráfico não gerado.")

# def _on_step(self) -> bool:
#     print(f"steps: {self.n_calls}/{TRAIN_STEPS}", end="\r")

#     infos = self.locals.get('infos', [])
#     if infos and 'episode' in infos[0]:
#         episode_reward = infos[0]['episode']['r']
#         episode_length = infos[0]['episode']['l']
#         self.episode_rewards.append(episode_reward)
#         self.episode_lengths.append(episode_length)

#         # Recompensa média acumulada até o momento (sobre todos os episódios)
#         mean_reward = np.mean(self.episode_rewards)
#         self.mean_rewards.append(mean_reward)

#         self.eva_rew_moments.append(self.n_calls)  # Adiciona o momento atual

#     if self.n_calls % self.save_freq == 0:
#         self.plot_av_reward()
#         # Continue salvando o modelo e testando...
#         # ...
