import gymnasium as gym
import time
import json
from itertools import combinations

from classes.Experimento import Experimento
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

from classes.logger.LossLoggerCallback import LossLoggerCallback
from stable_baselines3.common.logger import configure

# Flag que modifica caminhos para salvar/ler arquivos dependendo da IDE utilizada
vscode = True
if vscode:
    caminho = './classes'
else:  # PyCharm
    caminho = '.'

# Cria instância do ambiente seguindo o modelo da OpeanAI Gym para treinar modelos

gym.register(
    id='Citadels',
    entry_point='classes.openaigym_env.Citadels:Citadels',
    # parâmetros __init__
    # kwargs={'game': None}
)
env = gym.make('Citadels')


# Método que checa se o Ambiente segue os padrões da OpeanAI Gym
'''
check_env(env)
'''

parameters = [
    {
        "exploration_initial_eps": 1.0,
        "exploration_final_eps": 0.05,
        "exploration_fraction": 0.3,
        "learning_rate": 1e-4,
        "learning_starts": 2000,
        "gradient_steps": -1,
        "net_arch": [256, 128, 64, 32],
        "gamma": 0.9,
        "train_freq": 10,
        "buffer_size": 100000,
        "batch_size": 256,
        "target_update_interval": 300
    },
    {
        "exploration_initial_eps": 1.0,
        "exploration_final_eps": 0.05,
        "exploration_fraction": 0.3,
        "learning_rate": 1e-4,
        "learning_starts": 2000,
        "gradient_steps": -1,
        "net_arch": [256, 128, 64, 32],
        "gamma": 0.9,
        "train_freq": 10,
        "buffer_size": 100000,
        "batch_size": 256,
        "target_update_interval": 300
    },
    {
        "exploration_initial_eps": 1.0,
        "exploration_final_eps": 0.05,
        "exploration_fraction": 0.7,
        "learning_rate": 1e-4,
        "learning_starts": 2000,
        "gradient_steps": -1,
        "net_arch": [256, 128, 64, 32],
        "gamma": 0.9,
        "train_freq": 10,
        "buffer_size": 100000,
        "batch_size": 256,
        "target_update_interval": 300
    },
    {
        "exploration_initial_eps": 1.0,
        "exploration_final_eps": 0.05,
        "exploration_fraction": 0.9,
        "learning_rate": 1e-4,
        "learning_starts": 2000,
        "gradient_steps": -1,
        "net_arch": [256, 128],
        "gamma": 0.9,
        "train_freq": 10,
        "buffer_size": 100000,
        "batch_size": 256,
        "target_update_interval": 300
    },
    {
        "exploration_initial_eps": 1.0,
        "exploration_final_eps": 0.05,
        "exploration_fraction": 0.5,
        "learning_rate": 1e-5,
        "learning_starts": 2000,
        "gradient_steps": -1,
        "net_arch": [256, 256],
        "gamma": 0.9,
        "train_freq": 10,
        "buffer_size": 100000,
        "batch_size": 256,
        "target_update_interval": 300
    },
    {
        "exploration_initial_eps": 1.0,
        "exploration_final_eps": 0.05,
        "exploration_fraction": 0.5,
        "learning_rate": 1e-5,
        "learning_starts": 2000,
        "gradient_steps": -1,
        "net_arch": [256, 256],
        "gamma": 0.5,
        "train_freq": 10,
        "buffer_size": 100000,
        "batch_size": 256,
        "target_update_interval": 300
    },
    {
        "exploration_initial_eps": 1.0,
        "exploration_final_eps": 0.05,
        "exploration_fraction": 0.5,
        "learning_rate": 1e-5,
        "learning_starts": 2000,
        "gradient_steps": -1,
        "net_arch": [64, 32],
        "gamma": 0.9,
        "train_freq": 10,
        "buffer_size": 100000,
        "batch_size": 256,
        "target_update_interval": 300
    },
    {
        "exploration_initial_eps": 1.0,
        "exploration_final_eps": 0.05,
        "exploration_fraction": 0.5,
        "learning_rate": 1e-5,
        "learning_starts": 2000,
        "gradient_steps": -1,
        "net_arch": [256, 256],
        "gamma": 0.5,
        "train_freq": 10,
        "buffer_size": 100000,
        "batch_size": 256,
        "target_update_interval": 800
    },
    {
        "exploration_initial_eps": 1.0,
        "exploration_final_eps": 0.05,
        "exploration_fraction": 0.75,
        "learning_rate": 5e-5,
        "learning_starts": 2000,
        "gradient_steps": -1,
        "net_arch": [256, 128, 64, 32],
        "gamma": 0.9,
        "train_freq": 10,
        "buffer_size": 100000,
        "batch_size": 256,
        "target_update_interval": 800
    }
]

for i, parameter in enumerate(parameters):
    
    base_path = f"./logs/config_{i}/"
    for j in range(10):
        # Marca tempo de início para computar duração do experimento
        start_time = time.time()
        loggpath = base_path + f"ex_{j}/"
        new_logger = configure(loggpath, ["stdout", "csv" ,"log", "json"])

        #Cria, treina e salva instância de modelo de RL da biblioteca Stable-Baseline
        with open(loggpath+"output.txt", 'a') as f:
            # Registra os parâmetros no log em formato JSON
            f.write("Parâmetros do experimento:\n")
            json.dump(parameter, f, indent=4)  # Salva os parâmetros como JSON formatado
            f.write("\n\nInício do treino do modelo de IA\n")
        
        print("Início do treino do modelo de IA")
        model = DQN(
            policy="MlpPolicy",
            env=env,
            verbose=2,

            # Parâmetros de exploração
            exploration_initial_eps=parameter.get('exploration_initial_eps'),
            exploration_final_eps=parameter.get('exploration_final_eps'),
            exploration_fraction=parameter.get('exploration_fraction'),

            # Parâmetros de treinamento e otimização
            learning_rate=parameter.get('learning_rate'),
            learning_starts=parameter.get('learning_starts'),
            gradient_steps=parameter.get('gradient_steps'),
            policy_kwargs=dict(
                net_arch=parameter.get('net_arch')
            ),

            # Parâmetros de desconto e frequência de treinamento
            gamma=parameter.get('gamma'),
            train_freq=parameter.get('train_freq'),

            # Parâmetros do replay buffer
            buffer_size=parameter.get('buffer_size'),
            batch_size=parameter.get('batch_size'),
            target_update_interval=parameter.get('target_update_interval'),
        )
        model.set_logger(new_logger)
        model.learn(total_timesteps=500000, log_interval=1000, progress_bar=True)
        model.save("citadels_agent")
        with open(loggpath+"output.txt", 'a') as f:
            f.write("Fim do treino do modelo de IA\n")
        
        print("Fim do treino do modelo de IA")


        # print("Início do treino MCTS")
        # experimento = Experimento(caminho)
        # experimento.treinar_modelo_mcts(600, 0) # Treinar modelo MCTS RL por 10min = 600s
        # print("Fim do treino MCTS")

        with open(loggpath+"output.txt", 'a') as f:
            f.write("Fim do treino do modelo de IA\n")
        print("Início dos testes das estratégias")

        estrategias: list[Estrategia] = [Agente(), EstrategiaAllin("Allin"), EstrategiaAndrei(), EstrategiaBuild("Build"), EstrategiaDjonatan(), EstrategiaEduardo(),
                                        EstrategiaFelipe(), EstrategiaFrequency("Frequency"), EstrategiaGold("Gold"), EstrategiaJean(), EstrategiaLuisII(),
                                        EstrategiaMCTS(caminho), EstrategiaTotalmenteAleatoria()]
        # estrategias: list[Estrategia] = [Agente(imprimir=True), EstrategiaTotalmenteAleatoria("B2"), EstrategiaTotalmenteAleatoria("B3"), EstrategiaTotalmenteAleatoria("B4"), EstrategiaTotalmenteAleatoria("B5")]
        comb = list(combinations(estrategias, 5))
        qtd_comb = len(comb)
        with open(loggpath+"output.txt", 'a') as f:
            f.write(f"Quantidade de Combinações: {qtd_comb}\n")
        print(f"Quantidade de Combinações: {qtd_comb}")

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
            with open(loggpath+"output.txt", 'a') as f:
                f.write(f'\n{jogador} - Vitórias: {vitoria} - Taxa de Vitórias: {taxa_vitoria:.2f}% - Pontuação Média: {pontuacao_media:.2f}\n\t'
                        f'Primeiro: {taxa_vitoria:5.2f}%\n\tSegundo : {taxa_seg:5.2f}%\n\tTerceiro: {taxa_ter:5.2f}%\n\tQuarto  : {taxa_qua:5.2f}%\n\tQuinto  : {taxa_qui:5.2f}%\n')
            print(
                f'\n{jogador} - Vitórias: {vitoria} - Taxa de Vitórias: {taxa_vitoria:.2f}% - Pontuação Média: {pontuacao_media:.2f}\n\t'
                f'Primeiro: {taxa_vitoria:5.2f}%\n\tSegundo : {taxa_seg:5.2f}%\n\tTerceiro: {taxa_ter:5.2f}%\n\tQuarto  : {taxa_qua:5.2f}%\n\tQuinto  : {taxa_qui:5.2f}%')
        
        with open(loggpath+"output.txt", 'a') as f:
            f.write("Fim dos testes das estratégias\n")
        print("Fim dos testes das estratégias")

        # Imprime duração do experimento
        s = time.time() - start_time
        m = s // 60
        h = m // 60
        s -= m * 60
        m -= h * 60
        with open(loggpath+"output.txt", 'a') as f:
            f.write(f"Tempo de execução = {h:.0f}h {m:.0f}min {s:.2f}s\n")
        print(f"Tempo de execução = {h:.0f}h {m:.0f}min {s:.2f}s")
