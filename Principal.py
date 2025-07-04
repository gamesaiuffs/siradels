from classes.Experimento import Experimento
from classes.classification.ColetaEstados import ColetaEstados
from classes.classification.ClassificaEstados import ClassificaEstados
import sys
caminho = './classes'
n_features = 30
data = '04-10-2024'
x = f"Jogos {n_features}f {data}"
y = f"Rótulos {n_features}f {data}" 
feature_names = [
    # Board features
    "Round", "Largest Number of Districts Built", "Score P1", "Score P2", "Score P3", "Score P4", "Score P5", 

    # AP features
    "Gold Amount (AP)", "Number of cards in Hand (AP)", "Number of Builded Districts (AP)", "Cost of citadel (AP)", "Cost of Hand (AP)", "Builded District Types (AP)", "District Types in Hand (AP)", "Low Cost District in Hand (AP)", "High Cost District in Hand (AP)", "Special District in Hand (AP)", "Special District Builded (AP)", "Character Rank (AP)",

    # MVP features
    "Gold Amount (MVP)", "Number of Cards in Hand (MVP)", "Number of Builded Districts (MVP)", "Cost of citadel (MVP)", "Builded District Types (MVP)", "District Types in Hand (MVP)", "Low Cost District in Hand (MVP)", "High Cost District in Hand (MVP)", "Special District in Hand (MVP)", "Special District Builded (MVP)", "Character Rank (MVP)",
]

#jogos, rotulos = ClassificaEstados.ler_amostras(x, y, False)
X_train, X_test, y_train, y_test = ClassificaEstados.ler_amostras(x, y, True)

ClassificaEstados.optuna_CART(X_train, y_train)
ClassificaEstados.optuna_RF(X_train, y_train)

metrics = ["Accuracy", "F1_Score", "Precision"]

#ClassificaEstados.analise_study(study_path)
#diretorio_studies = './classes/classification/models/'

for i in range(5000):
    try:
        for i in range(len(metrics)):
            model_path = f"./classes/classification/models/CART/CART_{metrics[i]}_BestModel_{i}.joblib"
            ClassificaEstados.avaliar_modelo_carregado(model_path, X_test, y_test, "/CART/evaluation.txt")

            model_path = f"./classes/classification/models/RF/RF_{metrics[i]}_BestModel_{i}.joblib"
            ClassificaEstados.avaliar_modelo_carregado(model_path, X_test, y_test, "/RF/evaluation.txt")
    except:
        continue
    
'''
for i in range(len(metrics)):
    print("\nBest", metrics[i], ":\n")
    study_path = f"./classes/classification/models/CART/CART_Best_{metrics[i]}.pkl"
    ClassificaEstados.optuna_learning_curve(study_path, metrics[i])

    ClassificaEstados.study_best_trials(study_path)
'''