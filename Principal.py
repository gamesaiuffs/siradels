#from classes.Experimento import Experimento
from classes.classification.dataset.ColetaEstados import ColetaEstados
from classes.classification.ClassificaEstados import ClassificaEstados, carregar_resultados_optuna, carregar_resultados_avaliacao, carregar_best_params, carregar_resultados_progress
from classes.classification.AnaliseResultados import AnaliseResultados
import sys
import numpy as np 

caminho = './classes'
n_features = 30

data = "2026-03-26"

jogos_base = f"Jogos {n_features}f {data}"
rotulos_base = f"Rótulos {n_features}f {data}"

datasets = [" otimização", " testes", " por_round"]
metrics = ["Accuracy", "F1_Score", "Precision", "Recall"]

jogos = jogos_base + "por_round"
rotulos = rotulos_base + "por_round"

# -------------------------------------------------------
# BUSCA DE HIPERPARÂMETROS (OPTUNA)
# -------------------------------------------------------

""" 
for i in datasets:

    jogos = jogos_base + i
    rotulos = rotulos_base + i  

    ColetaEstados.coleta_amostras(137, jogos, rotulos, '', 25) """


'''
print("\n===== OPTUNA SEARCH =====\n")

res_cart = ClassificaEstados.optuna_CART(jogos, rotulos)
res_rf   = ClassificaEstados.optuna_RF(jogos, rotulos)
res_xgb  = ClassificaEstados.optuna_XGB(jogos, rotulos)
res_mlp  = ClassificaEstados.optuna_MLP(jogos, rotulos)

print("\n===== LOADING BEST PARAMS =====\n")
'''

'''
best_cart = carregar_best_params("CART")
best_rf   = carregar_best_params("RF")
best_xgb  = carregar_best_params("XGB")
best_mlp  = carregar_best_params("MLP")

# -------------------------------------------------------
# TREINAR + TESTAR MODELOS COM OS MELHORES PARÂMETROS
# -------------------------------------------------------

print("\n===== MODEL EVALUATION =====\n")

cart_results = ClassificaEstados.treinar_e_avaliar_CART(
    jogos, rotulos, best_cart
)

rf_results = ClassificaEstados.treinar_e_avaliar_RF(
    jogos, rotulos, best_rf
)

xgb_results = ClassificaEstados.treinar_e_avaliar_XGB(
    jogos, rotulos, best_xgb
)

mlp_results = ClassificaEstados.treinar_e_avaliar_MLP(
    jogos, rotulos, best_mlp
)

logreg_results = ClassificaEstados.treinar_regressao_logistica(
    jogos,
    rotulos,
    nome_modelo="LogReg",
    class_weight="balanced"
)

print("\n===== PROGRESS EVALUATION =====\n")

cart_progress = ClassificaEstados.treinar_e_avaliar_progress_CART(
    jogos, rotulos
)

rf_progress = ClassificaEstados.treinar_e_avaliar_progress_RF(
    jogos, rotulos
)

xgb_progress = ClassificaEstados.treinar_e_avaliar_progress_XGB(
    jogos, rotulos
)

mlp_progress = ClassificaEstados.treinar_e_avaliar_progress_MLP(
    jogos, rotulos
)
'''
# -------------------------------------------------------
# CÓDIGOS DE ANÁLISE / GRÁFICOS (MANTIDOS COMENTADOS)
# -------------------------------------------------------

'''
AnaliseResultados.plot_performance_from_pkls([
    "CART",
    "RF",
    "XGB",
    "MLP"
])

#AnaliseResultados.shap_analysis(X_train, X_test, models[3], feature_names, model_names[3])

'''

#AnaliseResultados.plot_optuna_trials()
#AnaliseResultados.plot_evaluation_comparison()
#AnaliseResultados.print_evaluation_table()
#AnaliseResultados.plot_progress_by_type()