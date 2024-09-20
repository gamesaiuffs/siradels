import gymnasium as gym
import time
from itertools import permutations

from classes.Experimento import Experimento
from classes.enum.TipoAcaoOpenAI import TipoAcaoOpenAI
from classes.openaigym_env.Citadels import Citadels

from classes.strategies.Agente import Agente
from classes.strategies.Estrategia import Estrategia
from classes.strategies.EstrategiaAllin import EstrategiaAllin
from classes.strategies.EstrategiaAndrei import EstrategiaAndrei
from classes.strategies.EstrategiaBuild import EstrategiaBuild
from classes.strategies.EstrategiaDjonatan import EstrategiaDjonatan
from classes.strategies.EstrategiaEduardo import EstrategiaEduardo
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaFrequency import EstrategiaFrequency
from classes.strategies.EstrategiaGold import EstrategiaGold
from classes.strategies.EstrategiaJean import EstrategiaJean
from classes.strategies.EstrategiaLuis import EstrategiaLuisII
from classes.strategies.EstrategiaManual import EstrategiaManual
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import DQN

# Marca tempo de início para computar duração do experimento
start_time = time.time()

# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
vscode = True
if vscode:
    caminho = './classes'
else:  # PyCharm
    caminho = '.'

# Cria instância do ambiente seguindo o modelo da OpeanAI Gym para treinar modelos

# gym.register(
#     id='Citadels',
#     entry_point='classes.openaigym_env.Citadels:Citadels',
#     # parâmetros __init__
#     # kwargs={'game': None}
# )
# env = gym.make('Citadels')


# Método que checa se o Ambiente segue os padrões da OpeanAI Gym
'''
check_env(env)
'''

# Cria, treina e salva instância de modelo de RL da biblioteca Stable-Baseline

# model = DQN(
#     policy="MlpPolicy",
#     env=env,
#     verbose=2,

#     # Parâmetros de exploração
#     exploration_initial_eps=1.0,
#     exploration_final_eps=0.1,
#     exploration_fraction=0.9,

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
#     target_update_interval=800)
# model.learn(total_timesteps=1000)
# model.save("citadels_agent")

# print("Início do treino MCTS")
# experimento = Experimento(caminho)
# experimento.treinar_modelo_mcts(600, 0) # Treinar modelo MCTS RL por 10min = 600s
# print("Fim do treino MCTS")

print("Início dos testes das estratégias")
# Sem o Agente()
estrategias: list[Estrategia] = [EstrategiaAllin("Allin"), EstrategiaAndrei(), EstrategiaBuild("Build"), EstrategiaDjonatan(), EstrategiaEduardo(),
                                 EstrategiaFelipe(), EstrategiaFrequency("Frequency"), EstrategiaGold("Gold"), EstrategiaJean(), EstrategiaLuisII(),
                                 EstrategiaMCTS(caminho), EstrategiaTotalmenteAleatoria()]
perm = list(permutations(estrategias, 5))
qtd_perm = len(perm)
print("Quantidade de Permutações:", qtd_perm)
qtd_simulacao: int = 2
resultados_total: dict[str, (int, int)] = dict()
for e in estrategias:
    resultados_total[e.nome] = (0, 0, 0)
for i, p in enumerate(perm):
    if i % 1000 == 0:
        print(f"{i}/{qtd_perm} - {(i*100/qtd_perm):.2f}%")
    resultados = Experimento.testar_estrategias(list(p), qtd_simulacao)
    for jogador, resultado in resultados.items():
        (vitoria, pontuacao) = resultado
        resultados_total[jogador] = (resultados_total[jogador][0] + vitoria, resultados_total[jogador][1] + pontuacao, resultados_total[jogador][2] + qtd_simulacao)
for jogador, resultado in resultados_total.items():
    (vitoria, pontuacao, qtd_simulacao_total) = resultado
    pontuacao_media = pontuacao / qtd_simulacao_total
    taxa_vitoria = 100 * vitoria / qtd_simulacao_total
    print(
        f'{jogador} - Vitórias: {vitoria} - Taxa de Vitórias: {taxa_vitoria:.2f}% - Pontuação Média: {pontuacao_media:.2f}')
print("Fim dos testes das estratégias")

# Imprime duração do experimento
s = time.time() - start_time
m = s // 60
h = m // 60
s -= m * 60
m -= h * 60
print(f"Tempo de execução = {h:.0f}h {m:.0f}min {s:.2f}s")
