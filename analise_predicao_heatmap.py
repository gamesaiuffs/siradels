import numpy as np
import random as rd
import gymnasium as gym
import seaborn as sns
import matplotlib.pyplot as plt
from stable_baselines3 import DQN

if __name__ == "__main__":
    ENV_ID = "Citadels"
    ENV_ENTRY_POINT = 'classes.openaigym_env.Citadels_box:Citadels'
    MODEL_PATH = "./aaa_experimentos_final/1/in_1/30.zip"
    NUM_EPISODES = 100000
    
    VARIABLE_NAME = "character_gold"  
    VARIABLE_RANGE = range(0, 7)  
    NUM_ACTIONS = 8  

    EXP_NAME = f"Action choices heatmap in {NUM_EPISODES} episodes - variable: {VARIABLE_NAME}"

    gym.register(id=ENV_ID, entry_point=ENV_ENTRY_POINT)
    model = DQN.load(MODEL_PATH)
    env = gym.make(ENV_ID)

    escolhas = np.zeros((len(VARIABLE_RANGE), NUM_ACTIONS))

    for i, var_value in enumerate(VARIABLE_RANGE):
        for _ in range(NUM_EPISODES // len(VARIABLE_RANGE)):  # Distribuindo episódios
            if _ % 100 == 0: 
                print(f"Rodando teste para {var_value}: {((i+1)*_/NUM_EPISODES)*100:.2f}%", end="\r")
            
            external_input = np.array([
                var_value,   # ouro_personagem (0 a 6)
                rd.randint(0, 10),   # cartas_dist_mao (0 a 10)
                rd.randint(0, 6),  # carta_mais_cara
                rd.randint(0, 6),  # carta_mais_barata
                rd.randint(0, 7),  # qtd_dist_const
                rd.randint(0, 6),  # qtd_dist_cada_tipo
                rd.randint(0, 6),  # ||
                rd.randint(0, 6),  # ||
                rd.randint(0, 6),  # ||
                rd.randint(0, 6),  # ||
                rd.randint(0, 7),  # dist_const_jog_mais_const
                rd.randint(0, 10), # jog_mais_cartas_mao
                rd.randint(0, 10), # ouro_oponentes
                rd.randint(0, 10), # ||
                rd.randint(0, 10), # ||
                rd.randint(0, 10), # ||
                
                rd.randint(0, 1),  # personagem rank 1
                rd.randint(0, 1),  # personagem rank 2
                rd.randint(0, 1),  # personagem rank 3
                rd.randint(0, 1),  # personagem rank 4
                rd.randint(0, 1),  # personagem rank 5
                rd.randint(0, 1),  # personagem rank 6
                rd.randint(0, 1),  # personagem rank 7
                rd.randint(0, 1),  # personagem rank 8
                
                0  # Turno jogador
            ])
            
            action, _states = model.predict(external_input, deterministic=True)
            escolhas[i, action - 1] += 1
    
    escolhas_norm = escolhas / escolhas.sum(axis=1, keepdims=True) # Normalização 

    plt.figure(figsize=(10, 6))
    sns.heatmap(escolhas_norm, annot=True, cmap="coolwarm", xticklabels=range(1, 9), yticklabels=VARIABLE_RANGE)
    plt.xlabel("Ações")
    plt.ylabel(f"Valores de {VARIABLE_NAME}")
    plt.title(EXP_NAME)
    plt.savefig(f"graficos_atualizado/predicao/ouro_personagem/{VARIABLE_NAME}_heatmap.png")
    plt.show()
