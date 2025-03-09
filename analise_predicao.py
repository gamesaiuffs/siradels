import gymnasium as gym
from stable_baselines3 import DQN  # Altere para o algoritmo usado no treinamento
import random as rd
import matplotlib.pyplot as plt

import numpy as np

if __name__ == "__main__":
    ENV_ID = "Citadels"
    ENV_ENTRY_POINT = 'classes.openaigym_env.Citadels_box:Citadels'
    MODEL_PATH="./aaa_experimentos_final/1/in_1/30.zip"
    NUM_EPISODES = 10000
    
    VARIABLE_NAME = "gold_and_character_cards"
    VARIABLE_VALUE = 5

    EXP_NAME=f"Action choices in {NUM_EPISODES} timesteps - variable: {VARIABLE_NAME} - Value: {VARIABLE_VALUE}"
    
    
    gym.register(
        id=ENV_ID,
        entry_point=ENV_ENTRY_POINT
    )
    
    model = DQN.load(MODEL_PATH)
    env = gym.make(ENV_ID)
    escolhas = [0, 0, 0, 0, 0, 0, 0, 0]
    
    for _ in range(NUM_EPISODES):
        if _ % 100 == 0: print(f"Rodando teste: {(_/NUM_EPISODES)*100:.2f}%", end="\r")
        
        # Array com tamanho para a representação de estado original 
        external_input = np.array([
            VARIABLE_VALUE,    # ouro_personagem (0 a 6)
            VARIABLE_VALUE,    # cartas_dist_mao (0 a 10)
            rd.randint(0, 6),    # carta_mais_cara
            rd.randint(0, 6),    # carta_mais_barata
            rd.randint(0, 7),    # qtd_dist_const
            rd.randint(0, 6),    # qtd_dist_cada_tipo
            rd.randint(0, 6),    # ||
            rd.randint(0, 6),    # ||
            rd.randint(0, 6),    # ||
            rd.randint(0, 6),    # ||
            rd.randint(0, 7),    # dist_const_jog_mais_const
            rd.randint(0, 10),    # jog_mais_cartas_mao
            rd.randint(0, 10),    # ouro_oponentes
            rd.randint(0, 10),    # ||
            rd.randint(0, 10),    # ||
            rd.randint(0, 10),    # ||
            
            rd.randint(0, 1),     # personagem rank 1
            rd.randint(0, 1),     # personagem rank 2
            rd.randint(0, 1),     # personagem rank 3
            rd.randint(0, 1),     # personagem rank 4
            rd.randint(0, 1),     # personagem rank 5
            rd.randint(0, 1),     # personagem rank 6
            rd.randint(0, 1),     # personagem rank 7
            rd.randint(0, 1),      # personagem rank 8
            
            # Turno jogador 
            0
            ])
        
        action, _states = model.predict(external_input, deterministic=True)
        escolhas[action - 1] += 1
        # print(external_input[0], action)
        
    plt.figure(figsize=(10, 6))
    plt.xlabel('Possibles Actions')
    plt.ylabel('Number of Choices')
    plt.title(EXP_NAME)
    labels = ["1", "2", "3", "4", "5", "6", "7", "8"]

    plt.bar(labels, escolhas, color="lightgray", ec="black")
    for i in range(len(escolhas)):
        plt.text(i, escolhas[i] + 0.5, f"{((escolhas[i] / NUM_EPISODES) * 100):.2f}%", ha='center', va='bottom')
    
    plt.savefig(f"graficos_atualizado/predicao/ouro_e_carta/{VARIABLE_NAME}_var={VARIABLE_VALUE}.png")
        
        
# cartas_dist_mao_original 4
# carta_mais_cara_original 5 Tempo de execução: 16118.937582015991 segundos
# carta_mais_barata_original 3 
# qtd_dist_const_original 0     
# qtd_dist_cada_tipo_original [0, 0, 0, 0, 0]
# dist_const_jog_mais_const_original 1
# jog_mais_cartas_mao_original 4
# ouro_oponentes_original [0, 2, 0, 0]
# disponibilidade_personagens [1, 1, 0, 0, 0, 0, 1, 1]
# turno_agente 0
    
    
    
    
    