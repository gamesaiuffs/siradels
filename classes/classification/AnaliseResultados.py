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
import matplotlib.cm as cm
from matplotlib.ticker import ScalarFormatter, MaxNLocator
import joblib
from classes.classification.ClassificaEstados import ClassificaEstados

class AnaliseResultados:

    @staticmethod
    def carregar_resultados_progress(model_key, base_dir="./classes/classification/results/progress"):
        path = os.path.join(base_dir, f"{model_key}_progress_evaluation.pkl")

        with open(path, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def resultados_to_df(results_dict, model_name):
        rows = []

        for phase, metrics in results_dict.items():
            rows.append({
                "Phase": phase,
                "Model": model_name,
                "Accuracy": metrics["accuracy"]["mean"],
                "Precision": metrics["precision_macro"]["mean"],
                "Recall": metrics["recall_macro"]["mean"],
                "F1": metrics["f1_macro"]["mean"]
            })

        return pd.DataFrame(rows)


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
    def plot_optuna_trials(base_dir="./classes/classification/results/optuna"):
        import os
        import pickle
        import matplotlib.pyplot as plt

        for file in os.listdir(base_dir):
            if not file.endswith(".pkl"):
                continue

            path = os.path.join(base_dir, file)

            with open(path, "rb") as f:
                data = pickle.load(f)

            history = data.get("history", [])
            if not history:
                continue

            trials = [h["trial"] for h in history]
            scores = [h["accuracy"] for h in history]

            best_idx = int(np.argmax(scores))
            model_name = file.replace("_optuna.pkl", "")

            plt.figure(figsize=(10, 6))

            # linha principal
            plt.plot(trials, scores, marker='o')

            # highlight best
            plt.scatter(
                trials[best_idx],
                scores[best_idx],
                s=120,
                marker='X'
            )

            plt.xlabel("Trial")
            plt.ylabel("Accuracy")
            plt.ylim(0, 1)
            plt.xlim(0, 300)
            plt.grid(True, linestyle="--", alpha=0.5)

            plt.tight_layout()
            plt.savefig(f"./classes/classification/estatisticas_resultados/optuna/{model_name}_trials.png")
            plt.close()

    @staticmethod
    def plot_evaluation_comparison(base_dir="./classes/classification/results/evaluation"):
        import os
        import pickle
        import matplotlib.pyplot as plt

        models = []
        means = []
        errors = []

        for file in os.listdir(base_dir):
            if not file.endswith(".pkl"):
                continue

            path = os.path.join(base_dir, file)

            with open(path, "rb") as f:
                data = pickle.load(f)

            model_name = file.replace(".pkl", "").replace("_evaluation", "")
            
            acc = data["accuracy"]
            mean = acc["mean"]
            ci_low, ci_high = acc["ci95"]

            models.append(model_name)
            means.append(mean)
            errors.append([mean - ci_low, ci_high - mean])

        order = np.argsort(means)

        models = np.array(models)[order]
        means = np.array(means)[order]
        errors = np.array(errors)[order]    

        errors = np.array(errors).T

        x = np.arange(len(models))

        plt.figure(figsize=(10, 6))

        # barras
        plt.bar(x, means, zorder=1)

        # intervalo de confiança 
        plt.errorbar(
            x, means,
            yerr=errors,
            fmt='none',
            ecolor='red',      
            elinewidth=2,      
            capsize=6,
            zorder=3           
        )

        plt.xticks(x, models)
        plt.ylabel("Accuracy")
        plt.xlabel("Model")
        plt.ylim(0, 1)
        plt.grid(True, linestyle="--", alpha=0.5, zorder=0)

        plt.tight_layout()
        plt.savefig("./classes/classification/estatisticas_resultados/general_performance/eval_comparison.png")
        plt.close()

    @staticmethod
    def print_evaluation_table(base_dir="./classes/classification/results/evaluation"):
        import os
        import pickle

        rows = []

        for file in os.listdir(base_dir):
            if not file.endswith(".pkl"):
                continue

            path = os.path.join(base_dir, file)

            with open(path, "rb") as f:
                data = pickle.load(f)

            model_name = file.replace("_evaluation.pkl", "")

            rows.append({
                "Model": model_name,
                "Accuracy": data["accuracy"]["mean"],
                "Precision": data["precision_macro"]["mean"],
                "Recall": data["recall_macro"]["mean"],
                "F1": data["f1_macro"]["mean"]
            })

        df = pd.DataFrame(rows)
        df = df.sort_values("Accuracy", ascending=False)

        print("\n=== MODEL EVALUATION ===\n")
        print(df.to_string(index=False, float_format="%.4f"))

    @staticmethod
    def plot_progress_by_type(base_dir="./classes/classification/results/progress"):
        import os
        import pickle
        import matplotlib.pyplot as plt
        from collections import defaultdict

        model_groups = defaultdict(list)

        for file in os.listdir(base_dir):
            if not file.endswith(".pkl"):
                continue

            model_type = file.split("_")[0]  
            path = os.path.join(base_dir, file)

            with open(path, "rb") as f:
                data = pickle.load(f)

            model_groups[model_type].append(data)

        metrics = ["accuracy", "precision_macro", "recall_macro", "f1_macro"]

        for metric in metrics:
            plt.figure(figsize=(10, 6))

            for model_type, runs in model_groups.items():

                phases = list(runs[0].keys())
                values = []

                for phase in phases:
                    vals = [r[phase][metric]["mean"] for r in runs]
                    values.append(np.mean(vals))

                plt.plot(phases, values, marker='o', label=model_type)

            plt.xlabel("Game Phase")
            plt.ylabel(metric)
            plt.ylim(0, 1)
            plt.grid(True, linestyle="--", alpha=0.5)
            plt.legend()

            plt.tight_layout()
            plt.savefig(f"./classes/classification/estatisticas_resultados/progress_performance/{metric}_progress.png")
            plt.close()

    @staticmethod
    def shap_analysis(X_train, X_test, model_path, feature_names, model_name):
        import os
        import shap
        import joblib
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from matplotlib.ticker import ScalarFormatter

        base_dir = f"./classes/classification/results/shap/{model_name}/"
        os.makedirs(base_dir, exist_ok=True)

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

        expl = shap.TreeExplainer(model_final, X_train_t, feature_names=feature_names, model_output="probability")

        array_path = os.path.join(base_dir, "X_array.npy")
        sv_path = os.path.join(base_dir, "sv_subset.pkl")

        if os.path.exists(array_path) and os.path.exists(sv_path):
            print("Carregando X_array e sv_subset salvos...")
            X_array = np.load(array_path)
            with open(sv_path, "rb") as f:
                sv_subset = joblib.load(f)
        else:
            print("Gerando novo X_array e sv_subset...")
            subset = X_test_t.iloc[:1000] if hasattr(X_test_t, "iloc") else X_test_t[:1000]
            sv_subset = expl(subset)
            X_array = subset.values if hasattr(subset, "values") else np.array(subset)

            np.save(array_path, X_array)
            pd.DataFrame(X_array, columns=feature_names).to_csv(os.path.join(base_dir, "X_array.csv"), index=False)
            with open(sv_path, "wb") as f:
                joblib.dump(sv_subset, f)

        output_dir = os.path.join(base_dir, "Dependence")
        os.makedirs(output_dir, exist_ok=True)

        for i, feat in enumerate(feature_names):
            for class_idx in range(sv_subset.values.shape[-1]):
                shap.dependence_plot(
                    feat,
                    sv_subset.values[:, :, class_idx],
                    X_array,
                    feature_names=feature_names,
                    show=False
                )

                plt.ylabel("SHAP value")

                fig = plt.gcf()
                for ax in fig.axes:
                    for im in ax.get_images():
                        if hasattr(im, "colorbar") and im.colorbar is not None:
                            cbar = im.colorbar
                            cbar.locator = MaxNLocator(integer=True)
                            cbar.update_ticks()

                plt.tight_layout()
                plt.savefig(
                    os.path.join(output_dir, f"dependence_{feat}_class{class_idx}.png"),
                    dpi=300,
                    bbox_inches="tight"
                )
                plt.close()

    @staticmethod
    def shap_beeswarm(X_train, X_test, model_path, feature_names, model_name, dataset_name, vitoria_class_idx=1):

        # Diretório de saída
        base_dir = f"./classes/classification/results/shap/{model_name}/"
        os.makedirs(base_dir, exist_ok=True)
        os.makedirs(os.path.join(base_dir, "Beeswarm"), exist_ok=True)

        # Carrega o modelo
        modelo = joblib.load(model_path)

        # Verifica se é pipeline
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

        # Cria TreeExplainer
        expl = shap.TreeExplainer(model_final, X_train_t, feature_names=feature_names, model_output="probability")

        # Subset para não pesar
        subset_len = 500
        subset = X_test_t.iloc[:subset_len] if hasattr(X_test_t, "iloc") else X_test_t[:subset_len]
        sv_subset = expl(subset)
        X_array = subset.values if hasattr(subset, "values") else np.array(subset)

        # Beeswarm apenas para a classe "vitória"
        plt.figure(figsize=(12, 8))
        shap.summary_plot(
            sv_subset.values[:, :, vitoria_class_idx], 
            X_array, 
            feature_names=feature_names,
            plot_type="dot",  
            max_display=len(feature_names),
            show=False
        )

        # Nome do arquivo com dataset
        file_path = os.path.join(base_dir, f"Beeswarm/beeswarm_vitoria_{dataset_name}.png")
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()

        print(f"Beeswarm salvo em: {file_path}")
        