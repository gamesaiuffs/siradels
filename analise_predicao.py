import argparse
import gymnasium as gym
from stable_baselines3 import DQN  # Altere para o algoritmo usado no treinamento
from stable_baselines3.common.env_util import make_vec_env

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
    MODEL_PATH="./aaa_experimentos_final/30/in_1/30.zip"

    gym.register(
        id=ENV_ID,
        entry_point=ENV_ENTRY_POINT
    )
    
    model = DQN.load(MODEL_PATH)
    env = gym.make(ENV_ID)
    
    for _ in range(100):
        external_input = np.array([
            1.0,    # ouro_personagem
            1.0,    # cartas_dist_mao
            1.0,    # carta_mais_cara
            1.0,    # carta_mais_barata
            1.0,    # qtd_dist_const
            1.0,    # qtd_dist_cada_tipo
            1.0,    # ||
            1.0,    # ||
            1.0,    # ||
            1.0,    # ||
            1.0,    # dist_const_jog_mais_const
            1.0,    # jog_mais_cartas_mao
            1.0,    # 
            1.0,    # 
            1.0,    # 
            2, 2, 2, 2, 2, 2, 2, 2, 2])
        
        action, _states = model.predict(external_input, deterministic=True)
        print("Ação prevista:", action, _states)
    
    
    
    
    
    
    