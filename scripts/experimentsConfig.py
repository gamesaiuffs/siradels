import os
from stable_baselines3 import DQN, PPO, A2C
from scripts.represents import *
import gymnasium as gym

# CONSTANTES 
ENV_ID = "Citadels"
ENVS = {
    "original": 'classes.openaigym_env.Citadels_original:Citadels',
    "multibinario": 'classes.openaigym_env.Citadels_mb:Citadels',
    "multidiscreto": 'classes.openaigym_env.Citadels_md:Citadels',
    "box": 'classes.openaigym_env.Citadels_box:Citadels',
}



# Obs: Para alterar o tipo de representação: 
# 1 - alterar o tipo de ambiente do gym na variável abaixo ENV_ENTRY_POINT 
#       - alterar apenas o nome dentro de ENVS
#       - Ambientes disponíveis ficam em ENVS
# 
# 2 - Alterar o valor numerico em EXP_ATUAL -
#       - É um valor arbitrário e pode ser qualquer um (só não pode repetir entre experimentos)
# 
# 3 - Verificar se o diretório listado em DIR_NAME existe
#       - O diretório do experimento o script cria, mas o raiz (atualmente: aaa_experimentos_final) é bom deixar criado 
#
# 4 - No arquivo represents.py, colocar na constante REPRESENT a lista de variáveis correspondente à 
# forma de abstração sendo testada. As opções são listadas abaixo.
#
#    representação               ambiente              Nome da lista de variáveis (valor a colocar em represents.py -> REPRESENT)
#    originais                   box                   variaveis_original
#    original limitado           multidiscreto         variaveis_padrao
#    proporções                  box                   proporcoes
#    3 classes                   multidiscreto         variaveis_classes
#    2 classes (binario)         binario               variaveis_classes_bin
#
# Obs:  originais = sem alteração nenhuma 
#       original limitado = forma implementada originalmente no jogo
#
# 5 - Atualmente, o modelo configurado para treinamento é o A2C. Para trocar, basca comentar 
# comentar o bloco do A2C no final deste arquivo e descomentar o bloco do modelo correspondente. 
# Os hiperparâmetros configurados são os do TCC do Jean. 

ENV_ENTRY_POINT = ENVS["box"]


gym.register(
    id=ENV_ID,
    entry_point=ENV_ENTRY_POINT
)

ENV = gym.make(ENV_ID)


# CONFIGURAÇÃO DO AMBIENTE DE TREINAMENTO
EXP_ATUAL = 50
EXP_TITLE='A2C original'

if len(EXP_TITLE) > 40: 
    print("Titulo muito grande: ", EXP_TITLE)
    exit(1)


NUM_INITS = 10
TRAIN_STEPS = 300000
MODEL_SAVE_FREQ = 10000
NUM_EVAL_EPISODES = 100

DIR_NAME = f"aaa_experimentos_final/{EXP_ATUAL}"
NOT_ALLOW_REUSE_DIRS = True
EVAL_LOG_FILE = os.path.join(DIR_NAME, "evaluations.txt")


print(f"Experimento: {EXP_ATUAL} - {EXP_TITLE}\n")

# CONFIGURAÇÕES DO MODELO TREINANDO 

# LOCAL_MODEL = DQN 
# def getModel(): 
#     return LOCAL_MODEL(
#     "MlpPolicy",                     
#     env=ENV,                         
#     verbose=0,                       

#     # Parâmetros de exploração
#     exploration_initial_eps=1.0,    
#     exploration_final_eps=0.05,      
#     exploration_fraction=0.5,       

#     # Parâmetros de treinamento e otimização
#     learning_rate=1e-5,             
#     learning_starts=2000,           
#     gradient_steps=-1,            
#     # policy_kwargs=dict(net_arch=[256, 128, 64, 32]),  
#     policy_kwargs=dict(net_arch=[256, 256]),  

#     # Parâmetros de desconto e frequência de treinamento
#     gamma=0.9,                     
#     train_freq=10,                   

#     # Parâmetros do replay buffer
#     buffer_size=100000,             
#     batch_size=256,                 
#     target_update_interval=300,         
# )



# LOCAL_MODEL = PPO

# def getModel():
#     return LOCAL_MODEL (
#     policy = "MlpPolicy",
#     env = ENV,
#     learning_rate = 3e-4,
#     n_steps = 2048,
#     batch_size= 64,
#     n_epochs= 10,
#     gamma = 0.99,
#     gae_lambda = 0.95,
#     clip_range = 0.2,
#     clip_range_vf = None,
#     normalize_advantage = True,
#     ent_coef = 0.0,
#     vf_coef = 0.5,
#     max_grad_norm = 0.5,
#     use_sde = False,
#     sde_sample_freq= -1,
#     rollout_buffer_class = None,
#     rollout_buffer_kwargs = None,
#     target_kl = None,
#     stats_window_size= 100,
#     tensorboard_log = None,
#     policy_kwargs = dict(net_arch=[256,256]),
#     verbose= 0,
#     seed = None,
#     device = "auto",
#     _init_setup_model = True,
# )


LOCAL_MODEL = A2C

def getModel():
    return LOCAL_MODEL(
        policy="MlpPolicy",
        env=ENV,
        learning_rate=7e-4,
        n_steps=5,
        gamma=0.99,
        gae_lambda=1.0,
        ent_coef=0.0,
        vf_coef=0.5,
        max_grad_norm=0.5,
        rms_prop_eps=1e-5,
        use_rms_prop=True,
        use_sde=False,
        sde_sample_freq=-1,
        rollout_buffer_class=None,
        rollout_buffer_kwargs=None,
        normalize_advantage=False,
        stats_window_size=100,
        tensorboard_log=None,
        policy_kwargs=dict(net_arch=[256, 256]),
        verbose=0,
        seed=None,
        device="auto",
        _init_setup_model=True,
    )