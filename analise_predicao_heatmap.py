import numpy as np
import random as rd
import gymnasium as gym
import seaborn as sns
import matplotlib.pyplot as plt
from stable_baselines3 import DQN

if __name__ == "__main__":
    ENV_ID = "Citadels"
    ENV_ENTRY_POINT = 'classes.openaigym_env.Citadels_mb:Citadels'
    NUM_EPISODES = 100000
    gym.register(id=ENV_ID, entry_point=ENV_ENTRY_POINT)
    
    VARIABLE_NAME = "e_character_gold"  
    VARIABLE_RANGE = range(0, 3)  # Range de valores para a variável escolhida
    
    EXP_NUM = 4
    MODEL = 30
    
    # INIT_NUM = 2
    
    for INIT_NUM in range(1, 11):
        print(f"\nInit: {INIT_NUM}")
    
        EXP_NAME = f"" 
        NUM_ACTIONS = 8
        MODEL_PATH = f"./aaa_experimentos_final/{EXP_NUM}/in_{INIT_NUM}/{MODEL}.zip"

        model = DQN.load(MODEL_PATH)
        env = gym.make(ENV_ID)
        steps_past = 0

        escolhas = np.zeros((len(VARIABLE_RANGE), NUM_ACTIONS))

        for i, var_value in enumerate(VARIABLE_RANGE):
            for _ in range(NUM_EPISODES // len(VARIABLE_RANGE)):  # Distribuindo episódios
                steps_past += 1
                if _ % 100 == 0: 
                    print(f"Rodando teste para {var_value}: {(steps_past/NUM_EPISODES)*100:.2f}%", end="\r")
                
                # Representação original
                # external_input = np.array([
                #     var_value,   # ouro_personagem (0 a 7)
                #     rd.randint(0, 6),   # cartas_dist_mao (0 a 10)
                #     rd.randint(0, 6),  # carta_mais_cara
                #     rd.randint(0, 6),  # carta_mais_barata
                #     rd.randint(0, 6),  # qtd_dist_const
                #     rd.randint(0, 6),  # qtd_dist_cada_tipo
                #     rd.randint(0, 6),  # ||
                #     rd.randint(0, 6),  # ||
                #     rd.randint(0, 6),  # ||
                #     rd.randint(0, 6),  # ||
                #     rd.randint(0, 7),  # dist_const_jog_mais_const (0, 7)
                #     rd.randint(0, 8), # jog_mais_cartas_mao
                #     rd.randint(0, 8), # ouro_oponentes
                #     rd.randint(0, 8), # ||
                #     rd.randint(0, 8), # ||
                #     rd.randint(0, 8), # ||
                    
                #     rd.randint(0, 1),  # personagem rank 1
                #     rd.randint(0, 1),  # personagem rank 2
                #     rd.randint(0, 1),  # personagem rank 3
                #     rd.randint(0, 1),  # personagem rank 4
                #     rd.randint(0, 1),  # personagem rank 5
                #     rd.randint(0, 1),  # personagem rank 6
                #     rd.randint(0, 1),  # personagem rank 7
                #     rd.randint(0, 1),  # personagem rank 8
                    
                #     0  # Turno jogador
                # ])
               
            #    # Representação classes 
                external_input = np.array([
                    var_value,   # ouro_personagem (0 a 7)
                    rd.randint(0, 2),   # cartas_dist_mao (0 a 20)
                    rd.randint(0, 2),  # carta_mais_cara
                    rd.randint(0, 2),  # carta_mais_barata
                    rd.randint(0, 2),  # qtd_dist_const
                    rd.randint(0, 2),  # qtd_dist_cada_tipo
                    rd.randint(0, 2),  # ||
                    rd.randint(0, 2),  # ||
                    rd.randint(0, 2),  # ||
                    rd.randint(0, 2),  # ||
                    rd.randint(0, 2),  # dist_const_jog_mais_const (0, 7)
                    rd.randint(0, 2), # jog_mais_cartas_mao
                    rd.randint(0, 2), # ouro_oponentes
                    rd.randint(0, 2), # ||
                    rd.randint(0, 2), # ||
                    rd.randint(0, 2), # ||
                    
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
                
                # print(external_input)
                
                action, _states = model.predict(external_input, deterministic=True)
                escolhas[i, action - 1] += 1
        
        escolhas_norm = escolhas / escolhas.sum(axis=1, keepdims=True) 

        plt.figure(figsize=(10, 6))
        # sns.heatmap(escolhas_norm, annot=True, cmap="coolwarm", xticklabels=range(1, 9), yticklabels=VARIABLE_RANGE)
        sns.heatmap(escolhas_norm * 100, annot=True, fmt=".1f", cmap="coolwarm", 
                xticklabels=range(1, 9), yticklabels=VARIABLE_RANGE)
        plt.xlabel("Actions")
        plt.ylabel(f"Values of {VARIABLE_NAME}")
        plt.title(EXP_NAME)
        plt.savefig(f"graficos_atualizado/predicao/{VARIABLE_NAME}/{VARIABLE_NAME}_heatmap_exp={EXP_NUM}_init={INIT_NUM}_model={MODEL}.png")
    # plt.show()
