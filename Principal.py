from classes.classification.ClassificaEstados import ClassificaEstados
from classes.classification.ColetaEstados import ColetaEstados

'''
import gymnasium as gym
from classes.enum.TipoAcaoOpenAI import TipoAcaoOpenAI
from classes.openaigym_env.Citadels import Citadels

from classes.strategies.Agente import Agente
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
'''

import time
vscode = True

feature_names = [
    # Board features
        "Round", "Largest Number of Districts Built", "Score P1", "Score P2", "Score P3", "Score P4", "Score P5", 

        # AP features
        "Gold Amount (AP)", "Number of cards in Hand (AP)", "Number of Builded Districts (AP)", "Cost of citadel (AP)", "Cost of Hand (AP)", "Builded District Types (AP)", "District Types in Hand (AP)", "Low Cost District in Hand (AP)", "High Cost District in Hand (AP)", "Special District in Hand (AP)", "Special District Builded (AP)", "Character Rank (AP)",

        # MVP features
        "Gold Amount (MVP)", "Number of Cards in Hand (MVP)", "Number of Builded Districts (MVP)", "Cost of citadel (MVP)", "Builded District Types (MVP)", "District Types in Hand (MVP)", "Low Cost District in Hand (MVP)", "High Cost District in Hand (MVP)", "Special District in Hand (MVP)", "Special District Builded (MVP)", "Character Rank (MVP)",
]

n_features = 30

data = '04-10-2024'
#ww = 3

x = f"Jogos {n_features}f {data}"
y = f"Rótulos {n_features}f {data}" 
#modelo = f"{criterion} {min_samp}ms {ww}mw {n_features}f"


inicio = time.time()

#(qtd_pts, n_features, nome_jogos, nome_rotulos, nome_modelo)
#ColetaEstados.coleta_amostras(n_features, x, y)

#fim_coleta = time.time() # 76 segundos = 1 minuto

#print(f"Tempo para coletar amostras: {fim_coleta - inicio}")

jogos, rotulos = ClassificaEstados.ler_amostras(x, y, False)
#{'Name': 'gini 151ms 3mw 30f', 'F1 Macro': np.float64(0.75), 'Win Precision': np.float64(0.73), 'Win Recall': np.float64(0.64), 'Accuracy': 0.77, 'Macro Precision': np.float64(0.76), 'Macro Recall': np.float64(0.74)}
ClassificaEstados.grid_cart(jogos, rotulos)

fim_cart = time.time() 

print(f"Tempo para treinar e testar CART: {fim_cart - inicio}")

ClassificaEstados.grid_rf(jogos, rotulos)

fim_rf = time.time() 

print(f"Tempo para treinar e testar Random Forest: {fim_rf - fim_cart}")

ClassificaEstados.grid_gb(jogos, rotulos)

fim_gb = time.time()

print(f"Tempo para treinar e testar Random Forest: {fim_gb - inicio}")

print(f"Tempo total de execução: {fim_gb - inicio}")

#(jogos, rotulos, nome_modelo, criterion, profundidade)
#ClassificaEstados.treinar_modelo(False, jogos, rotulos, modelo, criterion, min_samp, win_weigth, profundidade)
#ClassificaEstados.treinar_floresta(False, jogos, rotulos, "Forest1", 100, criterion, min_samp, win_weigth, profundidade)
#ClassificaEstados.treinar_gradiente(False, jogos, rotulos, "Gradient1", 100, 'friedman_mse', min_samp, 'log_loss', 0.1, profundidade)

#(jogos, rotulos, n_features)
#ClassificaEstados.circuito_treino_teste(jogos, rotulos, n_features)
#ClassificaEstados.avalia_testes(feature_names)

#(jogos, rotulos, nome_modelo)
#ClassificaEstados.modelo_info(modelo)
#print(ClassificaEstados.testar_modelo(jogos, rotulos, modelo, False))
#print(ClassificaEstados.testar_modelo(jogos, rotulos, '', False))

#ClassificaEstados.plot_tree(modelo)
#ClassificaEstados.plot_learning_curve(jogos, rotulos, modelo)

#(jogos_entrada, rotulos_entrada, jogos_saida, rotulos_saida)
#ClassificaEstados.undersampling("Jogos 2", "Rótulos 2", "Jogos 2 Balanceados", "Rotulos 2 Balanceados")
#simulacao.rodar_simulacao(X=0, model="Log Model")

# Cria instância do ambiente seguindo o modelo da OpeanAI Gym para treinar modelos

# Marca tempo de início para computar duração do experimento
#startTime = time.time()

# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
vscode = True
if vscode:
    caminho = './classes'
else:  # PyCharm
    caminho = '.'

'''
gym.register(
    id='Citadels',
    entry_point='classes.openaigym_env.Citadels:Citadels',
    # parâmetros __init__
    # kwargs={'game': None}
)
env = gym.make('Citadels')

# Método que checa se o Ambiente segue os padrões da OpeanAI Gym
check_env(env)
'''

# Cria, treina e salva instância de modelo de RL da biblioteca Stable-Baseline
# print("Início do treino do modelo de IA")
# model = DQN(
#     policy="MlpPolicy",
#     env=env,
#     verbose=2,
#
#     # Parâmetros de exploração
#     exploration_initial_eps=1.0,
#     exploration_final_eps=0.05,
#     exploration_fraction=0.9,
#
#     # Parâmetros de treinamento e otimização
#     learning_rate=1e-5,
#     learning_starts=2000,
#     gradient_steps=-1,
#     policy_kwargs=dict(net_arch=[256, 256]),
#
#     # Parâmetros de desconto e frequência de treinamento
#     gamma=0.7,
#     train_freq=10,
#
#     # Parâmetros do replay buffer
#     buffer_size=100000,
#     batch_size=256,
#     target_update_interval=800)
# model.learn(total_timesteps=500000, log_interval=10000)
# model.save("citadels_agent")
# print("Fim do treino do modelo de IA")

# print("Início do treino MCTS")
# experimento = Experimento(caminho)
# experimento.treinar_modelo_mcts(600, 0) # Treinar modelo MCTS RL por 10min = 600s
# print("Fim do treino MCTS")
'''
print("Início dos testes das estratégias")
estrategias: list[Estrategia] = [EstrategiaAndrei(), EstrategiaDjonatan(), EstrategiaEduardo(),
                                 EstrategiaFelipe(), EstrategiaJean(), EstrategiaLuisII(),
                                 EstrategiaTotalmenteAleatoria()] #MCTS e Agente off, levar para ColetaEstados e adaptar
# estrategias: list[Estrategia] = [Agente(imprimir=True), EstrategiaTotalmenteAleatoria("B2"), EstrategiaTotalmenteAleatoria("B3"), EstrategiaTotalmenteAleatoria("B4"), EstrategiaTotalmenteAleatoria("B5")]
comb = list(combinations_with_replacement(estrategias, 5))
qtd_comb = len(comb)
print("Quantidade de Combinações:", qtd_comb)

qtd_simulacao: int = 10
resultados_total: dict[str, (int, int, int, int, int, int, int)] = dict()
for e in estrategias:
    resultados_total[e.nome] = (0, 0, 0, 0, 0, 0, 0)
for i, p in enumerate(comb):
    if (i+1) % 100 == 0 or i+1 == qtd_comb:
        print(f"{i+1}/{qtd_comb} - {((i+1)*100/qtd_comb):.2f}%")
    resultados = Experimento.testar_estrategias(list(p), qtd_simulacao)
    for jogador, resultado in resultados.items():
        (vitoria, seg, ter, qua, qui, pontuacao) = resultado
        vitoria += resultados_total[jogador][0]
        seg += resultados_total[jogador][1]
        ter += resultados_total[jogador][2]
        qua += resultados_total[jogador][3]
        qui += resultados_total[jogador][4]
        pontuacao += resultados_total[jogador][5]
        resultados_total[jogador] = (vitoria, seg, ter, qua, qui, pontuacao, resultados_total[jogador][6] + qtd_simulacao)
for jogador, resultado in resultados_total.items():
    (vitoria, seg, ter, qua, qui, pontuacao, qtd_simulacao_total) = resultado
    pontuacao_media = pontuacao / qtd_simulacao_total
    taxa_vitoria = 100 * vitoria / qtd_simulacao_total
    taxa_seg = 100 * seg / qtd_simulacao_total
    taxa_ter = 100 * ter / qtd_simulacao_total
    taxa_qua = 100 * qua / qtd_simulacao_total
    taxa_qui = 100 * qui / qtd_simulacao_total
    print(
        f'\n{jogador} - Vitórias: {vitoria} - Taxa de Vitórias: {taxa_vitoria:.2f}% - Pontuação Média: {pontuacao_media:.2f}\n\t'
        f'Primeiro: {taxa_vitoria:5.2f}%\n\tSegundo : {taxa_seg:5.2f}%\n\tTerceiro: {taxa_ter:5.2f}%\n\tQuarto  : {taxa_qua:5.2f}%\n\tQuinto  : {taxa_qui:5.2f}%')
print("Fim dos testes das estratégias")
'''
# Imprime duração do experimento
#print(f"Tempo da simulação = {(time.time() - startTime):.2f}s")
