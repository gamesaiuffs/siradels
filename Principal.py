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

print(f"{best_cart}\n")
print(f"{best_rf}\n")
print(f"{best_xgb}\n")
print(f"{best_mlp}\n")

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

logreg_progress = ClassificaEstados.treinar_e_avaliar_progress_LogReg(
    jogos, rotulos
)
'''

# -------------------------------------------------------
# CÓDIGOS DE ANÁLISE / GRÁFICOS
# -------------------------------------------------------

MODEL_KEY = "XGB"
MODEL_NAME = "XGB_final"
MODEL_PATH = "./classes/classification/results/modelos/XGB_final.pkl"

TOTAL_PARTIDAS = 1000

FEATURE_NAMES = (
    # ===== global =====
    ["round"] +
    [f"turn_order_p{i}" for i in range(1, 6)] +

    # ===== players =====
    [
        f"{feat}_p{i}"
        for i in range(1, 6)
        for feat in [
            "gold",
            "gold_diff_max",
            "hand_size",
            "hand_diff_max",
            "built_districts",
            "built_diff_max",
            "military_districts",
            "religious_districts",
            "commercial_districts",
            "noble_districts",
            "special_districts",
            "district_cost_max",
            "district_cost_min",
            "district_cost_avg",
            "city_cost_total",
            "city_cost_diff_max",
            "times_killed",
            "times_robbed",
            "role_rank_1",
            "role_rank_2",
            "role_rank_3",
            "role_rank_4",
            "role_rank_5",
            "role_rank_6",
            "role_rank_7",
            "role_rank_8",
        ]
    ]
)

#print(len(FEATURE_NAMES))

# -------------------------------------------------------
# TREINO FINAL (XGB GRANDE)
# -------------------------------------------------------

'''
print("\n===== TREINO FINAL XGB =====\n")
best_xgb = carregar_best_params("XGB")

model = ClassificaEstados.treinar_modelo_final_XGB_grande(
    jogos=jogos,
    rotulos=rotulos,
    best_params=best_xgb,
    total_partidas=TOTAL_PARTIDAS,
    save_name=f"{MODEL_NAME}.pkl"
)
# -------------------------------------------------------
# DATA PARA SHAP (simples)
# -------------------------------------------------------

X_train, X_test, y_train, y_test = ClassificaEstados.ler_amostras(
    jogos,
    rotulos,
    div=True
)

AnaliseResultados.shap_full_analysis(
    X_train=X_train,
    X_test=X_test,
    model_path=MODEL_PATH,
    feature_names=FEATURE_NAMES,
    model_name=MODEL_NAME,
    dataset_name=jogos
)
'''


# -------------------------------------------------------
# (mantido) ANÁLISES OPCIONAIS
# -------------------------------------------------------

#AnaliseResultados.plot_optuna_trials()
#AnaliseResultados.plot_evaluation_comparison()
#AnaliseResultados.print_evaluation_table()
#AnaliseResultados.plot_progress_by_type()

#model_keys = ["CART", "MLP", "RF", "XGB", "LOGREG"]

#for i in model_keys:
    #try:
        #print(f"Modelo {i}")
        #print("Optuna")
        #print(carregar_best_params(i))
        #results = carregar_resultados_optuna(i)
        #for t in results['history']:
        #    print(f"trial={t['trial']} | acc={t['accuracy']:.4f}")
        #print("Avaliação")
        #print(carregar_resultados_avaliacao(i))    
        #print("Progress")
        #progress = carregar_resultados_progress(i)
        #for fase, metrics in progress.items():
        #    means = {
        #        m: v["mean"]
        #        for m, v in metrics.items()
        #        if m != "raw"
        #    }
        #    print(f"{fase} -> {means}")
    #except:
    #    continue

import pandas as pd

df = pd.read_csv("./classes/classification/results/shap/XGB_final/importance_per_class.csv")

col_sum = df.sum()

print(col_sum)