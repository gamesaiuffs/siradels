#from classes.Experimento import Experimento
from classes.classification.ColetaEstados import ColetaEstados
from classes.classification.ClassificaEstados import ClassificaEstados
from classes.classification.AnaliseResultados import AnaliseResultados
import sys
caminho = './classes'
n_features = 30
data = '04-10-2024'
x = f"Jogos {n_features}f {data}"
y = f"Rótulos {n_features}f {data}" 

feature_names = [
    # Board features
    "Round", "Max Districts Built", "Score P5", "Score P4", "Score P3", "Score P2", "Score P1",

    # AP features
    "Gold (AP)", "Cards in Hand (AP)", "Built Districts (AP)", "Built Districts Cost (AP)",
    "Hand Districts Cost (AP)", "Built District Types (AP)", "Hand District Types (AP)",
    "Low-Cost Built Districts (AP)", "High-Cost Built Districts (AP)",
    "Low-Cost Districts in Hand (AP)", "High-Cost Districts in Hand (AP)",
    "Special Districts in Hand (AP)", "Built Special Districts (AP)", "Character Rank (AP)",

    # MVP features
    "Gold (MVP)", "Cards in Hand (MVP)", "Built Districts (MVP)", "Built Districts Cost (MVP)",
    "Built District Types (MVP)", "Low-Cost Built Districts (MVP)", "High-Cost Built Districts (MVP)",
    "Built Special Districts (MVP)", "Character Rank (MVP)",
]
metrics = ["Accuracy", "F1_Score", "Precision"]

'''

ClassificaEstados.optuna_CART(X_train, y_train)
ClassificaEstados.optuna_RF(X_train, y_train)

#ClassificaEstados.analise_study(study_path)
#diretorio_studies = './classes/classification/models/'
    
for i in range(len(metrics)):
    print("\nBest", metrics[i], ":\n")
    study_path = f"./classes/classification/models/CART/CART_Best_{metrics[i]}.pkl"
    ClassificaEstados.optuna_learning_curve(study_path, metrics[i])

    ClassificaEstados.study_best_trials(study_path)
'''

model_base_path = f'./classes/classification/models/'
study_base_path = f'./classes/classification/results/study/'

models = [
    f'{model_base_path}CART/CART_Accuracy_BestModel_0.joblib', 
    f'{model_base_path}CART/CART_F1_Score_BestModel_0.joblib',
    f'{model_base_path}CART/CART_Precision_BestModel_0.joblib',
    f'{model_base_path}RF/RF_Accuracy_BestModel_0.joblib',
    f'{model_base_path}RF/RF_F1_Score_BestModel_0.joblib',
    f'{model_base_path}RF/RF_Precision_BestModel_0.joblib']

model_names = [
    "CART_Accuracy",
    "CART_F1",
    "CART_Precision_0",
    "RF_Accuracy",
    "RF_F1",
    "RF_Precision"
]

studies =[
    f'{study_base_path}CART/CART_Best_Accuracy.pkl',
    f'{study_base_path}CART/CART_Best_F1_Score.pkl',
    f'{study_base_path}CART/CART_Best_Precision.pkl',
    f'{study_base_path}RF/RF_Best_Accuracy.pkl',
    f'{study_base_path}RF/RF_Best_F1_Score.pkl',
    f'{study_base_path}RF/RF_Best_Precision.pkl'
]

studies_names = [
    'CART-A',
    'CART-F1',
    'CART-P',
    'RF-A',
    'RF-F1',
    'RF-P'
]

metrics = [
    "Accuracy",
    "F1",
    "Precision",
    "Accuracy",
    "F1",
    "Precision"
]

ColetaEstados.correlacao()

#for i in range(len(studies)):
#    AnaliseResultados.plot_study_trials(studies[i], metrics[i], studies_names[i])

#print(X_test[0])
#print(y_test[0])
#AnaliseResultados.shap_analysis(X_train, X_test, models[3], feature_names, model_names[3])

#AnaliseResultados.plot_tree(models[2], model_names[2], feature_names)

#AnaliseResultados.plot_performance()

#for i in range(len(models)):
#    info_dict = ClassificaEstados.modelo_info(models[i], feature_names)
#    AnaliseResultados.plot_importances(info_dict["Feature Importances"], studies_names[i])

#ColetaEstados.correlacao()

#ColetaEstados.coleta_amostras(30, x, y, '', 1)

#ClassificaEstados.testa_modelos(models, './classes/classification/samples/sample_by_round')

#ClassificaEstados.plot_performance()

#for study in studies:
    #ClassificaEstados.study_best_trials(study)



'''
ClassificaEstados.model_comparation()

for i in range(len(studies)):

    #ClassificaEstados.study_best_trials(studies[i])
    try:
        ClassificaEstados.plot_study_trials(studies[i], studies_names[i])
    except:
        continue

   
for i in range(len(metrics)):
    study_path = f"./classes/classification/results/CART/CART_Best_{metrics[i]}.pkl"
    model_name = f"CART/CART_{metrics[i]}_BestModel"
    ClassificaEstados.modelo_info(model_name, feature_names)
    #ClassificaEstados.study_best_trials(study_path)

for i in range(len(metrics)):
    study_path = f"./classes/classification/results/RF/RF_Best_{metrics[i]}.pkl"
    model_name = f"RF/RF_{metrics[i]}_BestModel"
    ClassificaEstados.modelo_info(model_name, feature_names)
    #ClassificaEstados.study_best_trials(study_path)
'''
