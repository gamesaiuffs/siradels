from stable_baselines3 import DQN
import gymnasium as gym
import os
import time 
import matplotlib.pyplot as plt
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


ENV_ID = "Citadels"
ENV_ENTRY_POINT = 'classes.openaigym_env.Citadels_box:Citadels'

gym.register(
    id=ENV_ID,
    entry_point=ENV_ENTRY_POINT
)


# Configurações gerais 
DIR_NAME =              "testes/teste"      # Diretório onde são salvos modelos intermediários e graficos 
TRAIN_STEPS =           50000                 # Steps de treinamento
MODEL_SAVE_FREQ =       10000                   # Frequência de salvamento de modelos 
NOT_ALLOW_REUSE_DIRS =  False                  # impedir que arquivos com modelos salvos sejam sobrescritos
ENV_RENDER_MODE =       None                #modo de renderização

# Configurações da avaliação do treinamento 
EVAL_LOG_FILE =         os.path.join(DIR_NAME, "evaluations.txt")   # arquivo onde são registradas as avaliações dos modelos 
EVAL_FREQUENCY =        MODEL_SAVE_FREQ
NUM_EVAL_EPISODES =     100                     # numero de episodios de cada avaliação
PLOT_FREQUENCY =        10000                   # Frequência de plot do gráfico de evolução (valor deve ser múltiplo de MODEL_SAVE_FREQ)

LEARN_ENV = gym.make(ENV_ID)
TEST_ENV = gym.make(ENV_ID)


class SaveOnTrainStepsNumCallback(BaseCallback):
    def __init__(self, save_freq: int, verbose: int):
        super().__init__(verbose)  # 0 -> verbose
        self.save_freq = save_freq
        self.log_dir = DIR_NAME
        self.num_saves = 1
        self.save_path =  os.path.join(self.log_dir, str(self.num_saves))
        self.historico_vitorias = []    # Historico de vitórias respectivos ao nomero de passos 
        self.pontos_de_ref = []         # Valores de passo em que dados foram coletados para o gráfico
        self.pontos_media = []          # média de pontuação para cada teste

    def plot_performance(self) -> None:
        # if self.save_path is not None:
        #     os.makedirs(self.save_path, exist_ok=True)
        plt.figure(figsize=(10, 6))
        plt.xlabel("Learn steps")
        plt.ylabel("Avarage Score")
        plt.title("Model performance in training")
        plt.grid(True)
        plt.plot(self.pontos_de_ref, self.historico_vitorias, label="Win percentage")
        plt.plot(self.pontos_de_ref, self.pontos_media, label="Average Score")
        plt.ylim(0, 100)  # Fixando o eixo Y no intervalo de 0 a 100
        plt.legend()
        # Salvar a figura no diretório especificado
        save_path = os.path.join(DIR_NAME, f"performance_plot{self.num_saves}.png")
        plt.savefig(save_path)
        print(f"Gráfico salvo em {save_path}")
        

    def _on_step(self) -> bool:
        
        # print(f"steps: {self.n_calls}/{TRAIN_STEPS}", end="\r")
        
        if self.n_calls % self.save_freq == 0:
            print(f"Salvando modelo: {self.save_path}")
            self.model.save(self.save_path)
            
            # Teste do modelo atual
            local_model = DQN.load(self.save_path)
            local_model.exploration_rate = 0.1
            
            file = open(EVAL_LOG_FILE, "a+")
            
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
                
                
            file.write(f"Rodadas: {NUM_EVAL_EPISODES} Steps: {self.n_calls} Vitórias: {vitoria} Média de pontos {pontuacao_media}"+"\n")
            file.close()
            
            if self.n_calls % PLOT_FREQUENCY == 0: 
                self.plot_performance()
                print(f"Grafico de {self.n_calls} steps plotado!")
            
            print("Testes Finalizados")
            
            
            self.num_saves += 1
            self.save_path = os.path.join(self.log_dir, str(self.num_saves))

        return True
    


if __name__ == "__main__":
    if not os.path.isdir(DIR_NAME): 
        os.makedirs(DIR_NAME)
    else: 
        print(f"Diretório '{DIR_NAME}' já existe. Usá-lo pode afetar o conteúdo pré-existente.")
        if NOT_ALLOW_REUSE_DIRS: exit(0)

    gym.register(
        id=ENV_ID,
        entry_point=ENV_ENTRY_POINT
    )
    
    start_time = time.time()
    
    env = Monitor(LEARN_ENV, DIR_NAME)
    
    # Callback de salvamento
    save_callback = SaveOnTrainStepsNumCallback(save_freq=MODEL_SAVE_FREQ, verbose=3)
    
    # model = DQN(
    #         "MlpPolicy",                     # Política de rede neural MLP
    #         env=env,                         # Ambiente de OpenAI Gym
    #         verbose=0,                       # Nível de detalhamento dos logs
    #         # Parâmetros de exploração
    #         exploration_initial_eps=0.9,    
    #         exploration_final_eps=0.5,      
    #         exploration_fraction=0.4,       

    #         # # Parâmetros de treinamento e otimização
    #         learning_rate=0.0005,             
    #         learning_starts=5000,           
    #         gradient_steps=10,            
    #         policy_kwargs=dict(net_arch=[32]),  

    #         # # Parâmetros de desconto e frequência de treinamento
    #         gamma=0.95,                     
    #         train_freq=1000,                   

    #         # # Parâmetros do replay buffer
    #         buffer_size=100000,             
    #         batch_size=128,                 
    #         target_update_interval=3000
    # )
    
        # Nicolas novo 
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
        
    # Treinamento com callbacks
    model.learn(total_timesteps=TRAIN_STEPS, callback=[save_callback])
    
    end_time = time.time()  
    execution_time = end_time - start_time
    print(f"Tempo de execução: {execution_time} segundos")
    
    # plot_performance(save_callback)