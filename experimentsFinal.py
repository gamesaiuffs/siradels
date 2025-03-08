from stable_baselines3 import DQN
import gymnasium as gym
import os
import shutil
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

# Mudar
ENV_ENTRY_POINT = 'classes.openaigym_env.Citadels_box:Citadels'
EXP_ATUAL = 31
EXP_TITLE='menos:ouro_personagem_original'


gym.register(
    id=ENV_ID,
    entry_point=ENV_ENTRY_POINT
)

# Experimento 1 - salvos nas pastas de 1 a 6 
# Experimento 2 - variável mais importante - pastas de 10 a 19
#   Remoção em ordem - 10 = menos a primeira variável 
#                      19 = menos a ultima variavel 





# Configurações gerais 

NUM_INITS = 10
TRAIN_STEPS = 300000
MODEL_SAVE_FREQ = 10000
NUM_EVAL_EPISODES = 100

DIR_NAME = f"aaa_experimentos_final/{EXP_ATUAL}"
NOT_ALLOW_REUSE_DIRS = True
EVAL_LOG_FILE = os.path.join(DIR_NAME, "evaluations.txt")

LEARN_ENV = gym.make(ENV_ID)
TEST_ENV = gym.make(ENV_ID)


class SaveOnTrainStepsNumCallback(BaseCallback):
    def __init__(self, verbose: int, num_init: int, database: Conexao, idexp: int):
        super().__init__(verbose)  # 0 -> verbose
        self.log_dir = DIR_NAME + "/in_" + str(num_init)
        self.num_saves = 1
        self.num_init = num_init
        self.db = database                   
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
        
        if (num_init == 0): print()

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
            # print("Process", self.num_process, " saving...")

            self.model.save(self.log_dir + "/"+str(self.num_saves))
            
            # Teste do modelo atual
            local_model = DQN.load(self.log_dir + "/"+str(self.num_saves))
            
            self.evaluate_model_policy(local_model)
            
            file = open(os.path.join(self.log_dir, "evaluations.txt"), "a+")
            file.write("-"*30+"\n")
            file.write(self.save_path+"\n")
            
            # Configurar de acordo com o ambiente 
            local_env = TEST_ENV
            local_env.reset()
            
            estrategias = [Agente(imprimir=False, model=local_model), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
            vitoria, pontuacao_media = Experimento.testar_estrategias_graficos(estrategias, NUM_EVAL_EPISODES, True)

            mean_reward, std_reward = evaluate_policy(local_model, local_env, n_eval_episodes=10, deterministic=False)

            self.historico_vitorias.append(vitoria)
            self.pontos_de_ref.append(self.n_calls)
            self.pontos_media.append(pontuacao_media)
                
            file.write(f"Rodadas: {NUM_EVAL_EPISODES} Steps: {self.n_calls} Vitorias: {vitoria} Media de pontos {pontuacao_media}"+"\n")
            file.close()
            
            # cria registro no banco - 
            self.db.executar(f"INSERT INTO sample (id_sample, idin, idexp, avscore, avrew, tsteps, nwins) values ({self.num_saves}, {self.num_init}, {self.idexp}, {pontuacao_media}, {mean_reward}, {self.num_timesteps}, {vitoria})")
            
            # atualiza o valor para o proximo salvamento 
            self.num_saves += 1
            self.save_path = os.path.join(self.log_dir, str(self.num_saves))

        return True
    


if __name__ == "__main__": 
    if not os.path.isdir(DIR_NAME): 
            os.makedirs(DIR_NAME)
    else: 
        print(f"Diretório '{DIR_NAME}' já existe. Usá-lo pode afetar o conteúdo pré-existente.")
        if NOT_ALLOW_REUSE_DIRS: exit(0)
        
    database = Conexao()
    env = gym.make(ENV_ID)
    
    experimento = True
    novo_exp = True
    num_init = 1
    
    
    if novo_exp:
        database.executar(f"insert into experiment(idexp, title, numpt, status) values ({EXP_ATUAL}, '{EXP_TITLE}', {TRAIN_STEPS}, 'pendente');")

    
            
    start_time = time.time()
    while num_init <= NUM_INITS: 
        print(f"Nova inicialização: {num_init}\n\n")
        
        # cria a inicialização no banco 
        database.executar(f"insert into initialize (idexp, idin, status) values ({EXP_ATUAL}, {num_init}, 'pendente');")
        
        model = DQN(
            "MlpPolicy",                     
            env=env,                         
            verbose=0,                       

            # Parâmetros de exploração
            exploration_initial_eps=1.0,    
            exploration_final_eps=0.05,      
            exploration_fraction=0.5,       

            # Parâmetros de treinamento e otimização
            learning_rate=1e-5,             
            learning_starts=2000,           
            gradient_steps=-1,            
            # policy_kwargs=dict(net_arch=[256, 128, 64, 32]),  
            policy_kwargs=dict(net_arch=[256, 256]),  

            # Parâmetros de desconto e frequência de treinamento
            gamma=0.9,                     
            train_freq=10,                   

            # Parâmetros do replay buffer
            buffer_size=100000,             
            batch_size=256,                 
            target_update_interval=300,         
        )


        callback = SaveOnTrainStepsNumCallback(verbose=0, database=database, idexp=EXP_ATUAL, num_init=num_init)  

        model.learn(total_timesteps=TRAIN_STEPS, callback=callback)
        
        # atualiza status da inicialização - completo
        database.executar(f"UPDATE initialize SET status='concluido' WHERE idin='{num_init}' AND idexp='{EXP_ATUAL}';")
        
        num_init += 1


    end_time = time.time()  
    execution_time = end_time - start_time
    print(f"Tempo de execução: {execution_time} segundos")
                