import argparse
import gym
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
