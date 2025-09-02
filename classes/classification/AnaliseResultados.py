# -*- coding: utf-8 -*-
import ast
import os
import pickle
import traceback
from more_itertools import sort_together
import pandas as pd
import numpy as np
import json
import optuna
import shap
from sklearn.base import clone
from sklearn.discriminant_analysis import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from classes.strategies.EstrategiaDjonatan import EstrategiaDjonatan
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaAndrei import EstrategiaAndrei
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.enum.TipoDistrito import TipoDistrito
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, make_scorer, accuracy_score, confusion_matrix, log_loss, ConfusionMatrixDisplay
from sklearn.model_selection import learning_curve
from sklearn.decomposition import PCA
from sklearn.model_selection import StratifiedGroupKFold
import matplotlib.pyplot as plt
import joblib
from classes.classification.ClassificaEstados import ClassificaEstados

class AnaliseResultados:

    @staticmethod
    def avaliar_modelo_carregado(caminho_modelo, X_teste, y_teste, nome_saida):
        modelo = joblib.load(caminho_modelo)
        y_pred = modelo.predict(X_teste)

        resultados = {
            'accuracy': accuracy_score(y_teste, y_pred),
            'precision': precision_score(y_teste, y_pred, zero_division=0),
            'recall': recall_score(y_teste, y_pred, zero_division=0),
            'f1_score': f1_score(y_teste, y_pred, zero_division=0)
        }

        with open(f"./classes/classification/results/{nome_saida}", 'a') as f:
            f.write(f"\nModelo: {caminho_modelo}\n")
            for metrica, valor in resultados.items():
                f.write(f"  {metrica}: {valor:.4f}\n")

        return resultados

    @staticmethod
    def avaliar_melhores_modelos(jogos, rotulos, caminho_hiperparametros_txt, caminho_saida_resultados, modelo='MLP'):
        import ast

        with open(caminho_hiperparametros_txt, 'r') as f:
            conteudo = f.read()

        blocos = conteudo.strip().split('----------------------------------------\n')

        with open(caminho_saida_resultados, 'w') as out:
            for bloco in blocos:
                if not bloco.strip():
                    continue

                linhas = bloco.strip().split('\n')
                nome_modelo = linhas[0].split(': ')[1]
                hiperparametros_str = linhas[2].split(': ', 1)[1]
                hiperparametros = ast.literal_eval(hiperparametros_str)

                if modelo == 'MLP':
                    resultado = ClassificaEstados.treinar_e_avaliar_MLP(jogos, rotulos, hiperparametros)
                elif modelo == "GB":
                    resultado = ClassificaEstados.treinar_e_avaliar_GB(jogos, rotulos, hiperparametros)
                elif modelo == "CART":
                    resultado = ClassificaEstados.treinar_e_avaliar_CART(jogos, rotulos, hiperparametros)
                elif modelo == "RF":
                    resultado = ClassificaEstados.treinar_e_avaliar_RF(jogos, rotulos, hiperparametros)

                out.write(f"Modelo: {nome_modelo}\n")
                for metrica, valor in resultado.items():
                    if metrica != 'confusion_matrix':
                        out.write(f"{metrica}: {valor:.4f}\n")
                    else:
                        out.write("Matriz de Confusão:\n")
                        out.write(str(valor) + "\n")
                out.write("-" * 40 + "\n")

    @staticmethod
    def gerar_relatorio_melhores_models(diretorio_studies, caminho_saida_txt, modelo_desejado):
        melhores_modelos = {
            'Accuracy': {},
            'Precision': {},
            'F1': {}
        }

        for arquivo in os.listdir(diretorio_studies):
            caminho_study = os.path.join(diretorio_studies, arquivo)
            if os.path.isdir(caminho_study):
                continue

            # Filtra os arquivos do modelo correto
            if modelo_desejado not in arquivo:
                continue

            try:
                study = joblib.load(caminho_study)
            except Exception as e:
                print(f"Falha ao carregar {arquivo}: {e}")
                continue

            if 'F1' in arquivo:
                metrica = 'F1'
            elif 'Precision' in arquivo:
                metrica = 'Precision'
            elif 'Accuracy' in arquivo:
                metrica = 'Accuracy'
            else:
                continue

            for trial in study.trials:
                score = trial.value
                params = trial.params

                if score not in melhores_modelos[metrica]:
                    melhores_modelos[metrica][score] = []

                melhores_modelos[metrica][score].append({
                    'modelo': modelo_desejado,
                    'params': params
                })

        with open(caminho_saida_txt, 'w') as f:
            for metrica, modelos_dict in melhores_modelos.items():
                if not modelos_dict:
                    continue

                melhor_score = max(modelos_dict.keys())
                modelos = modelos_dict[melhor_score]

                prefixo = {'Accuracy': 'A', 'Precision': 'P', 'F1': 'F'}[metrica]

                for idx, modelo_dict in enumerate(modelos, start=1):
                    nome_modelo = f"{modelo_dict['modelo']}-{prefixo}{idx}"
                    f.write(f"Modelo: {nome_modelo}\n")
                    f.write(f"Score {metrica}: {melhor_score:.4f}\n")
                    f.write(f"Hiperparâmetros: {modelo_dict['params']}\n")
                    f.write("-" * 40 + "\n")

    @staticmethod
    def analise_study(study_path):

        study = joblib.load(study_path)
        # Print geral
        print(f"\nStudy: {study.study_name}")
        print(f"Directions: {study.directions}")
        print(f"N trials: {len(study.trials)}")
        print(f"Best value: {study.best_value}")
        print(f"Best params: {study.best_params}\n")
        
        # Print de todos os trials
        for trial in study.trials:
            print(f"Trial #{trial.number}")
            print(f"  State: {trial.state}")
            print(f"  Value: {trial.value}")
            print(f"  Params: {trial.params}")
            print(f"  Duration: {trial.duration}")
            print(f"  User attrs: {trial.user_attrs}")
            print(f"  System attrs: {trial.system_attrs}")
            print()

            print("-" * 40)
            
        return
    
    @staticmethod
    def study_best_trials(study_path):

        study = joblib.load(study_path)
        
        # Pega o maior valor
        best_value = study.best_value

        # Filtra os trials com esse valor
        melhores_trials = [t for t in study.trials if t.value == best_value]

        # Printa todos
        for trial in melhores_trials:
            print(study_path, ":\n")
            print(len(study.trials), "trials")
            print(f"Trial #{trial.number}")
            print(f"  State: {trial.state}")
            print(f"  Value: {trial.value}")
            #print(f"  Params: {trial.params}")
            print(f"  Duration: {trial.duration}")
            print(f"  User attrs: {trial.user_attrs}")
            print(f"  System attrs: {trial.system_attrs}")
            print("-" * 40)
            for k, v in trial.params.items():
                print(f"  {k}: {v}")
            print()
            print("_" * 40)
   
        return

    @staticmethod
    def plot_study_trials(study_path, metric):
        study = joblib.load(study_path)

        # Extract data
        x = [t.number for t in study.trials if t.value is not None]
        y = [t.value for t in study.trials if t.value is not None]

        # Plot
        plt.figure(figsize=(10, 5))
        plt.plot(x, y, marker='o', linestyle='-', color='blue', label='Score per trial')
        plt.title("Score Evolution per Trial")
        plt.xlabel("Trial #")
        plt.ylabel(f"{metric} Score")
        plt.yscale("log")          # Logarithmic scale
        plt.ylim(1e-3, 0.8)       # Set Y range; avoid 0 for log scale
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"./classes/classification/results/study/trials/{metric}_trial.png")
        # plt.show()
    
    def plot_trials_and_best_value(models_info, metric_name, filename):
        """
        Plots a horizontal bar chart comparing number of trials and best value for each model.

        Exemple:
        models_info = {
            'CART': (50, 0.72),
            'RF': (100, 0.78),
            'XGB': (75, 0.81)
        }
        plot_trials_and_best_value(models_info, metric_name="Accuracy", filename="./trials_best_value.png")

        Args:
            models_info (dict): Dictionary where keys are model abbreviations (str) and values are
                                tuples (num_trials, best_value).
                                Example: {'CART': (50, 0.72), 'RF': (100, 0.78)}
            metric_name (str): Name of the metric (for labels/title)
            filename (str): Path to save the figure
        """
        models = list(models_info.keys())
        num_trials = [info[0] for info in models_info.values()]
        best_values = [info[1] for info in models_info.values()]
        
        y_pos = range(len(models))

        fig, ax1 = plt.subplots(figsize=(10, 6))

        # First axis: number of trials
        ax1.barh(y_pos, num_trials, color='skyblue', height=0.4, label='Number of Trials')
        ax1.set_xlabel("Number of Trials")
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(models)
        ax1.invert_yaxis()  # Highest on top

        # Second axis: best value
        ax2 = ax1.twiny()  # Share the same y-axis
        ax2.barh([y + 0.4 for y in y_pos], best_values, color='salmon', height=0.4, label=f"Final {metric_name} Value")
        ax2.set_xlabel(f"Final {metric_name} Value")
        
        # Legends
        ax1.legend(loc='lower right')
        ax2.legend(loc='upper right')

        plt.title(f"Number of Trials and Final {metric_name} Value per Model")
        plt.tight_layout()
        plt.savefig(filename)
        # plt.show()

    @staticmethod
    def plot_importances(importances: dict, model_name: str):
        
        filtered = {k: v for k, v in importances.items() if v > 0.02}
        #filtered = {k: v for k, v in importances.items()}

        # Ordena por importância decrescente
        sorted_importances = dict(sorted(filtered.items(), key=lambda x: x[1], reverse=True))
        print(sorted_importances)
        # Plot
        plt.figure(figsize=(10, 5))
        plt.barh(list(sorted_importances.keys()), list(sorted_importances.values()))
        plt.xlabel("Importance")
        plt.title(f"{model_name} Feature importances > 0.02")
        plt.gca().invert_yaxis()

        plt.xlim(0, 0.4) # Define o limite do eixo x de 0 a 0.4

        plt.tight_layout()
        #salva imagem no diretório de resultados
        plt.savefig(f"./classes/classification/results/feature_importances/all_features/{model_name}_importances.png")

        #plt.show()

    # Compara os modelos CART e RF treinados
    @staticmethod
    def model_comparation():

        # Métricas
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1', 'F1-Macro']

        # Valores extraídos da tabela
        CART_Acc = [0.7648, 0.7284, 0.6243, 0.6724, 0.7445]
        CART_Precision = [0.7578, 0.7520, 0.5573, 0.6402, 0.7289]
        CART_F1  = [0.7329, 0.6176, 0.8114, 0.7013, 0.7298]
        RF_Acc   = [0.7760, 0.7579, 0.6179, 0.6808, 0.7541]
        RF_Precision = [0.6949, 0.8383, 0.2609, 0.3980, 0.5968]
        RF_F1    = [0.7564, 0.6518, 0.7943, 0.7160, 0.7514]

        # Configuração
        bar_width = 0.12
        x = np.arange(len(metrics))

        # Offsets simétricos
        offsets = np.array([-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]) * bar_width

        # Valores, labels e paleta (tab10)
        values = [CART_Acc, CART_Precision, CART_F1, RF_Acc, RF_Precision, RF_F1]
        labels = ['CART Acc', 'CART Prec', 'CART F1', 'RF Acc', 'RF Prec', 'RF F1']
        colors = plt.get_cmap('tab10')(np.arange(6))

        # Plot
        plt.figure(figsize=(12, 6))
        for off, vals, lbl, col in zip(offsets, values, labels, colors):
            plt.bar(x + off, vals, width=bar_width, label=lbl, color=col)

        plt.xticks(x, metrics)
        plt.ylabel('Score')
        plt.legend(ncol=2, frameon=False)
        plt.tight_layout()

        #salva imagem no diretório de resultados
        plt.savefig("./classes/classification/results/feature_importances/model_comparation/comparation.png")
        #plt.show()

    @staticmethod
    def plot_performance():
        # Dados simulados como nos exemplos anteriores
        data = {
            "Phase": ["0%-20%", "20%-40%", "40%-60%", "60%-80%", "80%-100%"] * 6,
            "Model": (
                ["CART_Best_Accuracy"] * 5 +
                ["CART_Best_F1_score"] * 5 +
                ["CART_Best_Precision"] * 5 +
                ["RF_Best_Accuracy"] * 5 +
                ["RF_Best_F1_score"] * 5 +
                ["RF_Best_Precision"] * 5
            ),
            "Accuracy": [
                0.6631, 0.7248, 0.7819, 0.8560, 0.9091,
                0.6186, 0.6930, 0.7473, 0.8337, 0.9146,
                0.6605, 0.7070, 0.7775, 0.8555, 0.9142,
                0.6794, 0.7342, 0.7924, 0.8651, 0.9384,
                0.6403, 0.7246, 0.7740, 0.8461, 0.9205,
                0.6307, 0.6709, 0.7243, 0.7575, 0.7840
            ],
            "Precision": [
                0.5797, 0.6567, 0.7221, 0.7984, 0.8446,
                0.4975, 0.5691, 0.6268, 0.7289, 0.8488,
                0.5804, 0.6930, 0.7420, 0.8245, 0.8587,
                0.6128, 0.6826, 0.7577, 0.8338, 0.8913,
                0.5185, 0.6113, 0.6671, 0.7472, 0.8436,
                0.7269, 0.7755, 0.8192, 0.8561, 0.8930
            ],
            "Recall": [
                0.4020, 0.5737, 0.6888, 0.8295, 0.9328,
                0.7026, 0.7822, 0.8213, 0.8936, 0.9436,
                0.3740, 0.4072, 0.6319, 0.7860, 0.9268,
                0.4170, 0.5583, 0.6635, 0.8045, 0.9544,
                0.7052, 0.7500, 0.8040, 0.8976, 0.9712,
                0.0400, 0.1853, 0.3483, 0.4330, 0.4910
            ],
            "F1": [
                0.4747, 0.6124, 0.7050, 0.8137, 0.8865,
                0.5825, 0.6588, 0.7110, 0.8029, 0.8937,
                0.4549, 0.5130, 0.6825, 0.8048, 0.8915,
                0.4963, 0.6142, 0.7075, 0.8189, 0.9217,
                0.5976, 0.6736, 0.7292, 0.8155, 0.9029,
                0.0758, 0.2992, 0.4888, 0.5751, 0.6336
            ]
        }

        df = pd.DataFrame(data)

        # Plot comparando acurácia dos modelos ao longo das fases
        plt.figure(figsize=(10, 6))
        for model in df['Model'].unique():
            subset = df[df['Model'] == model]
            plt.plot(subset['Phase'], subset['Accuracy'], marker='o', label=f"{model}")
            
        # Linha de referência para chance aleatória (1 em 5 jogadores)
        plt.axhline(y=0.2, linestyle='--', color='red', label='Random baseline')

        plt.title("Accuracy of Models Across Game Progress Phases")
        plt.xlabel("Game Progress Phase")
        plt.ylabel("Accuracy")
        plt.ylim(0, 1)  # padroniza escala do eixo y
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig("./classes/classification/results/performance_tests/accuracy_across_phases.png")
        plt.close()

        # Plot comparando F1 score dos modelos ao longo das fases
        plt.figure(figsize=(10, 6))
        for model in df['Model'].unique():
            subset = df[df['Model'] == model]
            plt.plot(subset['Phase'], subset['F1'], marker='o', label=f"{model}")

        # Linha de referência para chance aleatória (1 em 5 jogadores)
        plt.axhline(y=0.2, linestyle='--', color='red', label='Random baseline')

        plt.title("F1 Score of Models Across Game Progress Phases")
        plt.xlabel("Game Progress Phase")
        plt.ylabel("F1 Score")
        plt.ylim(0, 1)  # padroniza escala do eixo y
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig("./classes/classification/results/performance_tests/f1_across_phases.png")
        plt.close()

        # Plot comparando Precision dos modelos ao longo das fases
        plt.figure(figsize=(10, 6))
        for model in df['Model'].unique():
            subset = df[df['Model'] == model]
            plt.plot(subset['Phase'], subset['Precision'], marker='o', label=f"{model}")

        # Linha de referência para chance aleatória (1 em 5 jogadores)
        plt.axhline(y=0.2, linestyle='--', color='red', label='Random baseline')

        plt.title("Precision of Models Across Game Progress Phases")
        plt.xlabel("Game Progress Phase")
        plt.ylabel("Precision")
        plt.ylim(0, 1)  # padroniza escala do eixo y
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig("./classes/classification/results/performance_tests/precision_across_phases.png")
        plt.close()

        # Plot comparando Recall dos modelos ao longo das fases
        plt.figure(figsize=(10, 6))
        for model in df['Model'].unique():
            subset = df[df['Model'] == model]
            plt.plot(subset['Phase'], subset['Recall'], marker='o', label=f"{model}")

        # Linha de referência para chance aleatória (1 em 5 jogadores)
        plt.axhline(y=0.2, linestyle='--', color='red', label='Random baseline')    

        plt.title("Recall of Models Across Game Progress Phases")
        plt.xlabel("Game Progress Phase")
        plt.ylabel("Recall")
        plt.ylim(0, 1)  # padroniza escala do eixo y
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig("./classes/classification/results/performance_tests/recall_across_phases.png")
        plt.close()     
        return

    @staticmethod
    def shap_analysis(X_train, X_test, model_path, feature_names, model_name):

        modelo = joblib.load(model_path)

        if hasattr(modelo, "steps"):  
            if len(modelo.steps) > 1:
                preprocessor = modelo[:-1]
                model_final = modelo.steps[-1][1]
                X_train_t = preprocessor.transform(X_train)
                X_test_t = preprocessor.transform(X_test)
            else:
                model_final = modelo.steps[0][1]
                X_train_t = X_train
                X_test_t = X_test
        else:
            model_final = modelo
            X_train_t = X_train
            X_test_t = X_test

        expl = shap.Explainer(model_final, X_train_t, feature_names=feature_names, model_output="probability")
        sv = expl(X_test_t[:1])  # primeira amostra

        # gera gráficos para cada classe (funciona mesmo em versões antigas do shap)
        for class_idx in range(sv.values.shape[-1]):
            sv_single = shap.Explanation(
                values=sv.values[0, :, class_idx],
                base_values=sv.base_values[0, class_idx],
                data=sv.data[0],
                feature_names=sv.feature_names
            )
            shap.waterfall_plot(sv_single)
            plt.savefig(f"./results/shap_{model_name}_class{class_idx}.png", dpi=300, bbox_inches='tight')
            plt.close()

    # Plota árvore
    @staticmethod
    def plot_tree(model_path: str, model_name, nomes_caracteristicas):

        modelo = joblib.load(model_path)

        # Pega o último passo do pipeline (o modelo de fato)
        if hasattr(modelo, "steps"):
            modelo_final = modelo.steps[-1][1]  # último elemento
        else:
            modelo_final = modelo  # já é um modelo direto

        # exporta texto
        tree_rules = export_text(modelo_final, feature_names=nomes_caracteristicas)
        print("Estrutura final da árvore: ")
        print(tree_rules)

        plt.figure(figsize=(40, 20))
        plot_tree(
            modelo_final,
            feature_names=nomes_caracteristicas,
            class_names=["Lose", "Win"],
            filled=True,
            fontsize=12  # aumenta o tamanho do texto
        )

        plt.savefig(f"./classes/classification/results/tree_fig/{model_name}.png", dpi=300)
        plt.close()
        #plt.show()   
        return

    # Plota curva de aprendizado
    @staticmethod
    def plot_learning_curve(jogos: str, rotulos: str, model_name: str):

        model = joblib.load(f'./classes/classification/models/{model_name}')

        X, Y = ClassificaEstados.ler_amostras(jogos, rotulos, False)

        f1_macro_scorer = make_scorer(f1_score, average='macro')
        precision_scorer = make_scorer(precision_score)
        recall_scorer = make_scorer(recall_score)

                                                                        # StratifiedKFold c/ K = 10                 # All processors
        train_sizes_f1, train_scores_f1, test_scores_f1 = learning_curve(model, X, Y, cv=10, scoring=f1_macro_scorer, n_jobs=-1)
        train_sizes_p, train_scores_p, test_scores_p = learning_curve(model, X, Y, cv=10, scoring=precision_scorer, n_jobs=-1)
        train_sizes_r, train_scores_r, test_scores_r = learning_curve(model, X, Y, cv=10, scoring=recall_scorer, n_jobs=-1)

        # Calculando as médias e desvios padrão das pontuações
        f1_train_scores_mean = np.mean(train_scores_f1, axis=1)
        f1_train_scores_std = np.std(train_scores_f1, axis=1)
        f1_test_scores_mean = np.mean(test_scores_f1, axis=1)
        f1_test_scores_std = np.std(test_scores_f1, axis=1)
        p_test_scores_mean = np.mean(test_scores_p, axis=1)
        p_test_scores_std = np.std(test_scores_p, axis=1)
        r_test_scores_mean = np.mean(test_scores_r, axis=1)
        r_test_scores_std = np.std(test_scores_r, axis=1)

        # Plotando a curva de aprendizado
        plt.figure(figsize=(10, 7))

        # Desvio padrão f1_train e f1_test
        plt.fill_between(train_sizes_f1, f1_train_scores_mean - f1_train_scores_std, f1_train_scores_mean + f1_train_scores_std, alpha=0.1, color="orange")
        plt.fill_between(train_sizes_f1, f1_test_scores_mean - f1_test_scores_std, f1_test_scores_mean + f1_test_scores_std, alpha=0.1, color="blue")

        # Média f1_train e f1_test
        plt.plot(train_sizes_f1, f1_train_scores_mean, 'o-', color="orange", label="F1 Train")
        plt.plot(train_sizes_f1, f1_test_scores_mean, 'o-', color="blue", label="F1 Test")

        # Desvio padrão precision e recall
        plt.fill_between(train_sizes_p, p_test_scores_mean - p_test_scores_std, p_test_scores_mean + p_test_scores_std, alpha=0.1, color="red")
        plt.fill_between(train_sizes_r, r_test_scores_mean - r_test_scores_std, r_test_scores_mean + r_test_scores_std, alpha=0.1, color="yellow")

        # Média precision e recall
        plt.plot(train_sizes_f1, p_test_scores_mean, 'o-', color="red", label="Precision Test")
        plt.plot(train_sizes_f1, r_test_scores_mean, 'o-', color="yellow", label="Recall Test")

        plt.title("Curva de Aprendizado da Árvore de Decisão")
        plt.xlabel("Tamanho do Conjunto de Treinamento")
        plt.ylabel("Scores")
        plt.legend(loc="best")
        plt.show()
        
        return