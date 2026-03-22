#from classes.Experimento import Experimento
import datetime
from classes.classification.dataset.ColetaEstados import ColetaEstados
from classes.classification.ClassificaEstados import ClassificaEstados
from classes.classification.AnaliseResultados import AnaliseResultados
import sys

caminho = './classes'
n_features = 30

data = datetime.date.today()
data = "2026-03-20"

jogos = f"Jogos {n_features}f {data}"
rotulos = f"Rótulos {n_features}f {data}"

jogos_optuna = f"Jogos {n_features}f {data} optuna"
rotulos_optuna = f"Rótulos {n_features}f {data} optuna"

metrics = ["Accuracy", "F1_Score", "Precision", "Recall"]

# -------------------------------------------------------
# BUSCA DE HIPERPARÂMETROS (OPTUNA)
# -------------------------------------------------------

print("\n===== OPTUNA SEARCH =====\n")

res_cart = ClassificaEstados.optuna_CART(jogos_optuna, rotulos_optuna)
res_rf   = ClassificaEstados.optuna_RF(jogos_optuna, rotulos_optuna)
res_xgb  = ClassificaEstados.optuna_XGB(jogos_optuna, rotulos_optuna)
res_mlp  = ClassificaEstados.optuna_MLP(jogos_optuna, rotulos_optuna)

best_cart = res_cart["best_params"]
best_rf   = res_rf["best_params"]
best_xgb  = res_xgb["best_params"]
best_mlp  = res_mlp["best_params"]


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

print("\nResultados CART:", cart_results)
print("\nResultados RF:", rf_results)
print("\nResultados XGB:", xgb_results)
print("\nResultados MLP:", mlp_results)

logreg_results = ClassificaEstados.treinar_regressao_logistica(
    jogos,
    rotulos,
    nome_modelo="LogReg",
    class_weight="balanced"
)

print("\nResultados LogReg:", logreg_results)


# -------------------------------------------------------
# CÓDIGOS DE ANÁLISE / GRÁFICOS (MANTIDOS COMENTADOS)
# -------------------------------------------------------

#ColetaEstados.correlacao()

#AnaliseResultados.plot_performance()

#AnaliseResultados.plot_tree(models[2], model_names[2], feature_names)

#AnaliseResultados.shap_analysis(X_train, X_test, models[3], feature_names, model_names[3])

#AnaliseResultados.plot_importances(info_dict["Feature Importances"], studies_names[i])

#for study in studies:
#    ClassificaEstados.study_best_trials(study)

#ClassificaEstados.model_comparation()