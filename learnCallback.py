from stable_baselines3 import DQN
import gymnasium as gym
import os
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
ENV_ENTRY_POINT = 'classes.openaigym_env.Citadels:Citadels'

gym.register(
    id=ENV_ID,
    entry_point=ENV_ENTRY_POINT
)


# Configurações gerais 
DIR_NAME =              "treinamento"      # Diretório onde são salvos modelos intermediários e graficos 
TRAIN_STEPS =           300000                 # Steps de treinamento
MODEL_SAVE_FREQ =       20000                   # Frequência de salvamento de modelos 
NOT_ALLOW_REUSE_DIRS =  True                  # impedir que arquivos com modelos salvos sejam sobrescritos
ENV_RENDER_MODE =       None                #modo de renderização

# Configurações da avaliação do treinamento 
EVAL_LOG_FILE =         os.path.join(DIR_NAME, "evaluations.txt")   # arquivo onde são registradas as avaliações dos modelos 
EVAL_FREQUENCY =        MODEL_SAVE_FREQ
NUM_EVAL_EPISODES =     100                     # numero de episodios de cada avaliação
PLOT_FREQUENCY =        20000                   # Frequência de plot do gráfico de evolução (valor deve ser múltiplo de MODEL_SAVE_FREQ)

LEARN_ENV = gym.make(ENV_ID)
TEST_ENV = gym.make(ENV_ID)


class SaveOnTrainStepsNumCallback(BaseCallback):
    def __init__(self, save_freq: int):
        super().__init__(0)  # 0 -> verbose
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
            
            # episodes_reward_list = []
            # episode_steps_num = []

            # for i in range(0, NUM_EVAL_EPISODES):
            #     obs, _ = local_env.reset()
            #     print("Rodada: ", i)
            #     episode_rew = 0
            #     episode_steps = 0
                # while True:
                #     action, _states = local_model.predict(obs, deterministic=True)
                #     obs, reward, done, truncated, _ = local_env.step(action)
                #     # local_env.render()

                #     episode_steps += 1
                #     episode_rew += reward
                #     if done:
                #         break
            estrategias = [Agente(imprimir=False, model=local_model), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
            resposta, pontuacao_media, vitoria = Experimento.testar_estrategias(estrategias, NUM_EVAL_EPISODES, True)

                # episode_steps_num.append(episode_steps)
                # episodes_reward_list.append(episode_rew)
            
            # Média da recompensa por passo
            # mean_reward = sum(episodes_reward_list) / sum(episode_steps_num)
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
    
    env = Monitor(LEARN_ENV, DIR_NAME)
    
    # Callback de salvamento
    save_callback = SaveOnTrainStepsNumCallback(save_freq=MODEL_SAVE_FREQ)

    # Modelo DQN
    # model = DQN(
    #         "MlpPolicy",                     # Política de rede neural MLP
    #         env=env,                         # Ambiente de OpenAI Gym
    #         verbose=0,                       # Nível de detalhamento dos logs

    #         # Parâmetros de exploração
    #         exploration_initial_eps=0.7,     # Taxa inicial de exploração alta
    #         exploration_final_eps=0.3,       # Taxa final de exploração baixa
    #         exploration_fraction=0.3,        # Fração do total de etapas dedicadas à exploração

    #         # Parâmetros de treinamento e otimização
    #         learning_rate=6.3e-4,            # Taxa de aprendizado
    #         learning_starts=5000,            # Número de etapas de aprendizado antes de começar a treinar
    #         gradient_steps=-1,               # Número de passos de gradiente (padrão usa -1, que é automático)
    #         policy_kwargs=dict(net_arch=[32, 32]),  # Arquitetura da rede neural

    #         # Parâmetros de desconto e frequência de treinamento
    #         gamma=0.99,                      # Fator de desconto
    #         train_freq=100,                    # Frequência de treinamento (a cada 4 passos)

    #         # Parâmetros do replay buffer
    #         buffer_size=100000,               # Tamanho do buffer de replay
    #         batch_size=512,                  # Tamanho do lote de amostras para o treinamento
    #         target_update_interval=3000,     # Intervalo de atualização do alvo
    # )

    # treino 6
    # model = DQN(
    #         "MlpPolicy",                     # Política de rede neural MLP
    #         env=env,                         # Ambiente de OpenAI Gym
    #         verbose=0,                       # Nível de detalhamento dos logs
    #         tau=0.75,   
    #         # Parâmetros de exploração
    #         exploration_initial_eps=0.5,     # Taxa inicial de exploração alta
    #         exploration_final_eps=0.1,       # Taxa final de exploração baixa
    #         exploration_fraction=0.5,        # Fração do total de etapas dedicadas à exploração

    #         # Parâmetros de treinamento e otimização
    #         learning_rate= 2e-4,            # Taxa de aprendizado
    #         learning_starts=5000,            # Número de etapas de aprendizado antes de começar a treinar
    #         gradient_steps=-1,               # Número de passos de gradiente (padrão usa -1, que é automático)
    #         policy_kwargs=dict(net_arch=[32, 32]),  # Arquitetura da rede neural

    #         # Parâmetros de desconto e frequência de treinamento
    #         gamma=0.95,                      # Fator de desconto
    #         train_freq=(1, 'episode'),                    # Frequência de treinamento 

    #         # Parâmetros do replay buffer
    #         buffer_size=100000,               # Tamanho do buffer de replay
    #         batch_size=256,                  # Tamanho do lote de amostras para o treinamento
    #         target_update_interval=7500,     # Intervalo de atualização do alvo
    # )
    
    # treino 7 
    # model = DQN(
    #         "MlpPolicy",                     # Política de rede neural MLP
    #         env=env,                         # Ambiente de OpenAI Gym
    #         verbose=0,                       # Nível de detalhamento dos logs
    #         tau=0.75,   
    #         # Parâmetros de exploração
    #         exploration_initial_eps=0.5,     # Taxa inicial de exploração alta
    #         exploration_final_eps=0.1,       # Taxa final de exploração baixa
    #         exploration_fraction=0.5,        # Fração do total de etapas dedicadas à exploração

    #         # Parâmetros de treinamento e otimização
    #         learning_rate= 1e-4,            # Taxa de aprendizado
    #         learning_starts=5000,            # Número de etapas de aprendizado antes de começar a treinar
    #         gradient_steps=-1,               # Número de passos de gradiente (padrão usa -1, que é automático)
    #         policy_kwargs=dict(net_arch=[48, 48]),  # Arquitetura da rede neural

    #         # Parâmetros de desconto e frequência de treinamento
    #         gamma=0.95,                      # Fator de desconto
    #         train_freq=(1, 'episode'),                    # Frequência de treinamento 

    #         # Parâmetros do replay buffer
    #         buffer_size=100000,               # Tamanho do buffer de replay
    #         batch_size=256,                  # Tamanho do lote de amostras para o treinamento
    #         target_update_interval=8000,     # Intervalo de atualização do alvo
    # )
    
    # treino 8
    # model = DQN(
    #         "MlpPolicy",                     # Política de rede neural MLP
    #         env=env,                         # Ambiente de OpenAI Gym
    #         verbose=0,                       # Nível de detalhamento dos logs
    #         tau=0.7,   
    #         # Parâmetros de exploração
    #         exploration_initial_eps=0.5,     # Taxa inicial de exploração alta
    #         exploration_final_eps=0.1,       # Taxa final de exploração baixa
    #         exploration_fraction=0.5,        # Fração do total de etapas dedicadas à exploração

    #         # Parâmetros de treinamento e otimização
    #         learning_rate= 5e-3,            # Taxa de aprendizado
    #         learning_starts=5000,            # Número de etapas de aprendizado antes de começar a treinar
    #         gradient_steps=1,               # Número de passos de gradiente (padrão usa -1, que é automático)
    #         policy_kwargs=dict(net_arch=[48, 48]),  # Arquitetura da rede neural

    #         # Parâmetros de desconto e frequência de treinamento
    #         gamma=0.95,                      # Fator de desconto
    #         train_freq=(1, 'episode'),                    # Frequência de treinamento 

    #         # Parâmetros do replay buffer
    #         buffer_size=100000,               # Tamanho do buffer de replay
    #         batch_size=256,                  # Tamanho do lote de amostras para o treinamento
    #         target_update_interval=8000,     # Intervalo de atualização do alvo
    # )
    
    # Treino 9
    # model = DQN(
    #         "MlpPolicy",                     # Política de rede neural MLP
    #         env=env,                         # Ambiente de OpenAI Gym
    #         verbose=0,                       # Nível de detalhamento dos logs
    #         tau=0.7,   
    #         # Parâmetros de exploração
    #         exploration_initial_eps=0.5,     # Taxa inicial de exploração alta
    #         exploration_final_eps=0.1,       # Taxa final de exploração baixa
    #         exploration_fraction=0.5,        # Fração do total de etapas dedicadas à exploração

    #         # Parâmetros de treinamento e otimização
    #         learning_rate= 1e-4,            # Taxa de aprendizado
    #         learning_starts=5000,            # Número de etapas de aprendizado antes de começar a treinar
    #         gradient_steps=1,               # Número de passos de gradiente (padrão usa -1, que é automático)
    #         policy_kwargs=dict(net_arch=[48, 48]),  # Arquitetura da rede neural

    #         # Parâmetros de desconto e frequência de treinamento
    #         gamma=0.95,                      # Fator de desconto
    #         train_freq=20,                    # Frequência de treinamento 

    #         # Parâmetros do replay buffer
    #         buffer_size=100000,               # Tamanho do buffer de replay
    #         batch_size=256,                  # Tamanho do lote de amostras para o treinamento
    #         target_update_interval=8000,     # Intervalo de atualização do alvo
    # )
    
    # treino 10
    # model = DQN(
    #         "MlpPolicy",                     # Política de rede neural MLP
    #         env=env,                         # Ambiente de OpenAI Gym
    #         verbose=0,                       # Nível de detalhamento dos logs
    #         tau=0.7,   
    #         # Parâmetros de exploração
    #         exploration_initial_eps=0.5,     # Taxa inicial de exploração alta
    #         exploration_final_eps=0.1,       # Taxa final de exploração baixa
    #         exploration_fraction=0.5,        # Fração do total de etapas dedicadas à exploração

    #         # Parâmetros de treinamento e otimização
    #         learning_rate= 1e-4,            # Taxa de aprendizado
    #         learning_starts=5000,            # Número de etapas de aprendizado antes de começar a treinar
    #         gradient_steps=1,               # Número de passos de gradiente (padrão usa -1, que é automático)
    #         policy_kwargs=dict(net_arch=[48]),  # Arquitetura da rede neural

    #         # Parâmetros de desconto e frequência de treinamento
    #         gamma=0.95,                      # Fator de desconto
    #         train_freq=(1, 'episode'),                    # Frequência de treinamento 

    #         # Parâmetros do replay buffer
    #         buffer_size=100000,               # Tamanho do buffer de replay
    #         batch_size=256,                  # Tamanho do lote de amostras para o treinamento
    #         target_update_interval=8000,     # Intervalo de atualização do alvo
    # )
    
    # treino 11
    # model = DQN(
    #         "MlpPolicy",                     # Política de rede neural MLP
    #         env=env,                         # Ambiente de OpenAI Gym
    #         verbose=0,                       # Nível de detalhamento dos logs

    #         # Parâmetros de exploração
    #         exploration_initial_eps=0.7,     # Taxa inicial de exploração alta
    #         exploration_final_eps=0.3,       # Taxa final de exploração baixa
    #         exploration_fraction=0.3,        # Fração do total de etapas dedicadas à exploração

    #         # Parâmetros de treinamento e otimização
    #         learning_rate=6.3e-4,            # Taxa de aprendizado
    #         learning_starts=5000,            # Número de etapas de aprendizado antes de começar a treinar
    #         gradient_steps=-1,               # Número de passos de gradiente (padrão usa -1, que é automático)
    #         policy_kwargs=dict(net_arch=[32]),  # Arquitetura da rede neural

    #         # Parâmetros de desconto e frequência de treinamento
    #         gamma=0.99,                      # Fator de desconto
    #         train_freq=(1, 'episode'),                    # Frequência de treinamento (a cada 4 passos)

    #         # Parâmetros do replay buffer
    #         buffer_size=100000,               # Tamanho do buffer de replay
    #         batch_size=512,                  # Tamanho do lote de amostras para o treinamento
    #         target_update_interval=3000,     # Intervalo de atualização do alvo
    # )
    
    # treino 13 
    # model = DQN(
    #     "MlpPolicy",                     # Política de rede neural MLP
    #     env=env,                         # Ambiente de OpenAI Gym
    #     verbose=0,                       # Nível de detalhamento dos logs
    #     tau=0.7,   
    #     # Parâmetros de exploração
    #     exploration_initial_eps=0.5,     # Taxa inicial de exploração alta
    #     exploration_final_eps=0.1,       # Taxa final de exploração baixa
    #     exploration_fraction=0.4,        # Fração do total de etapas dedicadas à exploração

    #     # Parâmetros de treinamento e otimização
    #     learning_rate= 1e-4,            # Taxa de aprendizado
    #     learning_starts=5000,            # Número de etapas de aprendizado antes de começar a treinar
    #     gradient_steps=1,               # Número de passos de gradiente (padrão usa -1, que é automático)
    #     policy_kwargs=dict(net_arch=[16]),  # Arquitetura da rede neural

    #     # Parâmetros de desconto e frequência de treinamento
    #     gamma=0.95,                      # Fator de desconto
    #     train_freq=1000,                    # Frequência de treinamento 

    #     # Parâmetros do replay buffer
    #     buffer_size=100000,               # Tamanho do buffer de replay
    #     batch_size=256,                  # Tamanho do lote de amostras para o treinamento
    #     target_update_interval=8000,     # Intervalo de atualização do alvo
    # )
    
    
    # treinamento 15
#     model = DQN(
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
#     target_update_interval=800,     
# )
    
    # treinamento 16
    # model = DQN(
    #         "MlpPolicy",                     # Política de rede neural MLP
    #         env=env,                         # Ambiente de OpenAI Gym
    #         verbose=3,                       # Nível de detalhamento dos logs
    #         tau=0.7,   
    #         # Parâmetros de exploração
    #         exploration_initial_eps=0.8,     # Taxa inicial de exploração alta
    #         exploration_final_eps=0.05,       # Taxa final de exploração baixa
    #         exploration_fraction=0.8,        # Fração do total de etapas dedicadas à exploração

    #         # Parâmetros de treinamento e otimização
    #         learning_rate= 1e-4,            # Taxa de aprendizado
    #         learning_starts=5000,            # Número de etapas de aprendizado antes de começar a treinar
    #         gradient_steps=1,               # Número de passos de gradiente (padrão usa -1, que é automático)
    #         policy_kwargs=dict(net_arch=[32]),  # Arquitetura da rede neural

    #         # Parâmetros de desconto e frequência de treinamento
    #         gamma=0.95,                      # Fator de desconto
    #         train_freq=(1, 'episode'),                    # Frequência de treinamento 

    #         # Parâmetros do replay buffer
    #         buffer_size=100000,               # Tamanho do buffer de replay
    #         batch_size=256,                  # Tamanho do lote de amostras para o treinamento
    #         target_update_interval=8000,     # Intervalo de atualização do alvo
    # )
    
    # treinamento 17
    # teste de troca do train_freq de (1, 'episode') para 1000
    model = DQN(
            "MlpPolicy",                     # Política de rede neural MLP
            env=env,                         # Ambiente de OpenAI Gym
            verbose=3,                       # Nível de detalhamento dos logs
            tau=0.7,   
            # Parâmetros de exploração
            exploration_initial_eps=0.8,     # Taxa inicial de exploração alta
            exploration_final_eps=0.05,       # Taxa final de exploração baixa
            exploration_fraction=0.8,        # Fração do total de etapas dedicadas à exploração

            # Parâmetros de treinamento e otimização
            learning_rate= 1e-4,            # Taxa de aprendizado
            learning_starts=5000,            # Número de etapas de aprendizado antes de começar a treinar
            gradient_steps=1,               # Número de passos de gradiente (padrão usa -1, que é automático)
            policy_kwargs=dict(net_arch=[32]),  # Arquitetura da rede neural

            # Parâmetros de desconto e frequência de treinamento
            gamma=0.95,                      # Fator de desconto
            train_freq=1000,                    # Frequência de treinamento 

            # Parâmetros do replay buffer
            buffer_size=100000,               # Tamanho do buffer de replay
            batch_size=256,                  # Tamanho do lote de amostras para o treinamento
            target_update_interval=8000,     # Intervalo de atualização do alvo
    )
    # Treinamento com callbacks
    model.learn(total_timesteps=TRAIN_STEPS, callback=[save_callback])
    
    # plot_performance(save_callback)
