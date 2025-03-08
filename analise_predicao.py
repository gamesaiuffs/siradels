import argparse
import gymnasium as gym
from stable_baselines3 import DQN  # Altere para o algoritmo usado no treinamento
from stable_baselines3.common.env_util import make_vec_env
import random as rd
import matplotlib.pyplot as plt

# def load_model(model_path, env_id):
#     """Carrega um modelo treinado e o ambiente correspondente."""
#     env = make_vec_env(env_id, n_envs=1)  # Cria o ambiente vetorizado
#     model = DQN.load(model_path)  # Altere para o algoritmo correto
#     return model, env

# def run_prediction(model, env, episodes=5, render=True):
#     """Executa o modelo por um número de episódios e exibe a ação tomada."""
#     for episode in range(episodes):
#         obs = env.reset()
#         done = False
#         total_reward = 0
#         while not done:
#             action, _states = model.predict(obs, deterministic=True)
#             obs, reward, done, info = env.step(action)
#             total_reward += reward
#             if render:
#                 env.render()

#         print(f"Episode {episode+1}: Total Reward: {total_reward}")

#     env.close()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--model", type=str, required=True, help="Caminho do modelo treinado (.zip)")
#     parser.add_argument("--env", type=str, required=True, help="ID do ambiente Gym (ex: CartPole-v1)")
#     parser.add_argument("--episodes", type=int, default=5, help="Número de episódios para rodar")
#     parser.add_argument("--no-render", action="store_true", help="Desativar renderização do ambiente")

#     args = parser.parse_args()

#     model, env = load_model(args.model, args.env)
#     run_prediction(model, env, episodes=args.episodes, render=not args.no_render)


# Carregar modelo e ambiente 

import numpy as np

if __name__ == "__main__":
    ENV_ID = "Citadels"
    ENV_ENTRY_POINT = 'classes.openaigym_env.Citadels_box:Citadels'
    MODEL_PATH="./aaa_experimentos_final/1/in_1/30.zip"

    gym.register(
        id=ENV_ID,
        entry_point=ENV_ENTRY_POINT
    )
    
    model = DQN.load(MODEL_PATH)
    env = gym.make(ENV_ID)
    escolhas = [0, 0, 0, 0, 0, 0, 0, 0]
    
    for _ in range(100000):
        if _ % 5000 == 0: print(f"Rodando teste: {(_/100000)*100:.2f}%", end="\r")
        
        # Array com tamanho para a representação de estado original 
        external_input = np.array([
            rd.randint(0, 6),    # ouro_personagem
            rd.randint(0, 10),    # cartas_dist_mao
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
    plt.title(f'Action Choices in 100000 Random Tests')
    labels = ["1", "2", "3", "4", "5", "6", "7", "8"]

    plt.bar(labels, escolhas, color="lightgreen")
    for i in range(len(escolhas)):
        plt.text(i, escolhas[i] + 0.5, str(escolhas[i]), ha='center', va='bottom')
    
    plt.savefig(f"graficos_atualizado/teste_escolhas.png")
        
        
# cartas_dist_mao_original 4
# carta_mais_cara_original 5
# carta_mais_barata_original 3
# qtd_dist_const_original 0
# qtd_dist_cada_tipo_original [0, 0, 0, 0, 0]
# dist_const_jog_mais_const_original 1
# jog_mais_cartas_mao_original 4
# ouro_oponentes_original [0, 2, 0, 0]
# disponibilidade_personagens [1, 1, 0, 0, 0, 0, 1, 1]
# turno_agente 0
    
    
    
    
    