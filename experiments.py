from stable_baselines3 import DQN
import gymnasium as gym
import os
import matplotlib.pyplot as plt
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback

from classes.strategies.Agente import Agente
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.Experimento import Experimento
from stable_baselines3.common.evaluation import evaluate_policy

import time
import ray

from database.Postgres import Conexao

ENV_ID = "Citadels"
ENV_ENTRY_POINT = 'classes.openaigym_env.Citadels:Citadels'

gym.register(
    id=ENV_ID,
    entry_point=ENV_ENTRY_POINT
)

# Configurações gerais 
DIR_NAME = "experimentos/teste_experimentos"
TRAIN_STEPS = 1000000
MODEL_SAVE_FREQ = 25000
NOT_ALLOW_REUSE_DIRS = False

EVAL_LOG_FILE = os.path.join(DIR_NAME, "evaluations.txt")
NUM_EVAL_EPISODES = 100
NUM_INITS = 10

LEARN_ENV = gym.make(ENV_ID)
TEST_ENV = gym.make(ENV_ID)


class SaveOnTrainStepsNumCallback(BaseCallback):
    def __init__(self, verbose: int, num_init: int, database: Conexao, idexp: int):
        super().__init__(verbose)  # 0 -> verbose
        self.log_dir = DIR_NAME + "/in_" + str(num_init)     # gera um nome para a inicialização
        self.num_saves = 1
        self.num_process = num_init
        self.db = database                      # conexão com o banco
        self.idexp = idexp
        
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
            
        # self.cria_inicializacao()    
        
        print("Process ", num_init, " started")
        
        if (num_init == 0): print()

    # def plot_performance(self) -> None:
    #     plt.figure(figsize=(10, 6))
    #     plt.xlabel("Learn steps")
    #     plt.ylabel("Average Score")
    #     plt.title("Model performance in training")
    #     plt.grid(True)
    #     plt.plot(self.pontos_de_ref, self.historico_vitorias, label="Win percentage")
    #     plt.plot(self.pontos_de_ref, self.pontos_media, label="Average Score")
    #     plt.ylim(0, 100)
    #     plt.legend()
    #     save_path = os.path.join(self.log_dir, f"performance_plot{self.num_saves}.png")
    #     plt.savefig(save_path)
        
    # def plot_av_reward(self):
    #     if len(self.eva_rew_moments) == len(self.mean_rewards) and len(self.mean_rewards) > 0:
    #         plt.figure(figsize=(10, 6))
    #         plt.title("Average Reward")
    #         plt.xlabel("Step")
    #         plt.ylabel("Reward")
    #         plt.grid(True)
    #         plt.plot(self.eva_rew_moments, self.mean_rewards, label="Mean Reward")
    #         plt.legend()
    #         save_path = os.path.join(self.log_dir, f"av_reward{self.num_saves}.png")
    #         plt.savefig(save_path)
    #     else:
    #         print("Tamanhos diferentes entre 'eva_rew_moments' e 'mean_rewards' ou lista vazia. Gráfico não gerado.")

    def cria_inicializacao(self): 
        self.db = Conexao()

    def evaluate_model_policy(self, model): 
        local_env = TEST_ENV
        local_env.reset()
        
        mean_reward, std_reward = evaluate_policy(model, local_env, n_eval_episodes=10, deterministic=False)
        self.mean_rewards.append(mean_reward)
        self.eva_rew_moments.append(self.n_calls)


    def _on_step(self) -> bool:
        print(f"Step: {self.n_calls}", end="\r")
        if self.n_calls % MODEL_SAVE_FREQ == 0:
            print("Process", self.num_process, " saving...")

            self.model.save(self.log_dir + "/"+str(self.num_saves))
            
            # Teste do modelo atual
            local_model = DQN.load(self.log_dir + "/"+str(self.num_saves))
            
            self.evaluate_model_policy(local_model) 
            
            # self.plot_av_reward()
            
            
            file = open(os.path.join(self.log_dir, "evaluations.txt"), "a+")
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
            
            # if self.n_calls % PLOT_FREQUENCY == 0: 
            #     self.plot_performance()
            
            # atualiza o valor para o proximo salvamento 
            self.num_saves += 1
            self.save_path = os.path.join(self.log_dir, str(self.num_saves))

        return True
    

# env = Monitor(LEARN_ENV, DIR_NAME)
# test = 0

env = gym.make(ENV_ID)

# envs = [gym.make(ENV_ID) for _ in range(NUM_PROCESSES)]

database = Conexao()
idexp = 1
num_init = 1

experimento = True

if __name__ == "__main__": 
    if not os.path.isdir(DIR_NAME): 
            os.makedirs(DIR_NAME)
    else: 
        print(f"Diretório '{DIR_NAME}' já existe. Usá-lo pode afetar o conteúdo pré-existente.")
        if NOT_ALLOW_REUSE_DIRS: exit(0)

    start_time = time.time()
    
    while experimento: 
        
        # Cria experimento no banco
        database.executar(f"insert into experiment (idexp, title, numpt, status) values ({idexp}, 'titulo', {NUM_EVAL_EPISODES}, 1)")
        
        while num_init <= NUM_INITS: 
            try: 
                
                # cria a inicialização no banco 
                
                database.executar(f"insert into initialize (status, idexp) values ('{idexp}', {NUM_EVAL_EPISODES}, 1)")
                
                model = DQN(
                    "MlpPolicy",                     
                    env=env,                         
                    verbose=0,                       

                    # Parâmetros de exploração
                    exploration_initial_eps=1.0,    
                    exploration_final_eps=0.05,      
                    exploration_fraction=0.5,       

                    # Parâmetros de treinamento e otimização
                    learning_rate=1e-4,             
                    learning_starts=2000,           
                    gradient_steps=-1,            
                    policy_kwargs=dict(net_arch=[256, 128, 64, 32]),  

                    # Parâmetros de desconto e frequência de treinamento
                    gamma=0.9,                     
                    train_freq=10,                   

                    # Parâmetros do replay buffer
                    buffer_size=100000,             
                    batch_size=256,                 
                    target_update_interval=300,         
                )
    
    
                callback = SaveOnTrainStepsNumCallback(verbose=0, database=database, idexp=idexp, num_init=num_init)  
        
                model.learn(total_timesteps=TRAIN_STEPS, callback=callback)
                
                # atualiza status da inicialização
                
                
                num_init += 1

                
            except KeyboardInterrupt: 
                experimento = False
                # remove a inicialização correspondente do banco 
                
                
                break
            
            # except: 
            #     print("Erro no experimento ...")
                
            #     # remove a inicialização correspondente do banco para iniciar outra
                
            #     continue
        
        # atualiza status do experimento
        
        
        
        
    
    end_time = time.time()  
    execution_time = end_time - start_time
    print(f"Tempo de execução: {execution_time} segundos")
                