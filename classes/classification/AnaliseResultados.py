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

            model_type = file.replace("_progress_evaluation.pkl", "")
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
    
    # Compara pares de modelos/baselines usando os mesmos 10 folds (seed=42 fixa em
    # _prepare_balanced_folds, então o fold i é composto pelas mesmas partidas em todas as
    # avaliações rodadas com o mesmo total_partidas). Isso permite teste pareado real em vez de
    # comparar apenas médias e ICs que se sobrepõem (Comentário 5 / Reviewer 2).
    # model_keys: nomes de arquivo sem o sufixo "_evaluation.pkl", ex: "XGB", "LOGREG", "RANDOM".
    @staticmethod
    def testes_pareados(model_keys, base_dir="./classes/classification/results/modelos",
                         baseline_dir="./classes/classification/results/evaluation",
                         metric="accuracy", alpha=0.05, filenames=None):
        from scipy import stats

        filenames = filenames or {}

        def load_raw(key):
            fname = filenames.get(key, f"{key}_evaluation.pkl")
            for d in (base_dir, baseline_dir):
                path = os.path.join(d, fname)
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        data = pickle.load(f)
                    return np.asarray(data["raw"][metric], dtype=float)
            raise FileNotFoundError(f"Evaluation não encontrada para {key} ({fname}) em {base_dir} nem {baseline_dir}")

        raws = {k: load_raw(k) for k in model_keys}

        n_folds_set = {len(v) for v in raws.values()}
        if len(n_folds_set) > 1:
            raise ValueError(f"Modelos com número de folds diferente, comparação pareada inválida: {n_folds_set}")

        rows = []
        for i in range(len(model_keys)):
            for j in range(i + 1, len(model_keys)):
                a, b = model_keys[i], model_keys[j]
                va, vb = raws[a], raws[b]

                t_stat, t_p = stats.ttest_rel(va, vb)
                try:
                    w_stat, w_p = stats.wilcoxon(va, vb)
                except ValueError:
                    w_stat, w_p = np.nan, np.nan

                rows.append({
                    "Model A": a,
                    "Model B": b,
                    "Mean A": va.mean(),
                    "Mean B": vb.mean(),
                    "Mean diff (A-B)": (va - vb).mean(),
                    "t_stat": t_stat,
                    "t_pvalue": t_p,
                    "wilcoxon_stat": w_stat,
                    "wilcoxon_pvalue": w_p,
                    "significant_ttest": bool(t_p < alpha),
                    "significant_wilcoxon": bool(w_p < alpha) if not np.isnan(w_p) else None,
                })

        df = pd.DataFrame(rows)

        save_dir = "./classes/classification/results/statistical_tests"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"paired_tests_{metric}.csv")
        df.to_csv(save_path, index=False)

        print(f"\n=== TESTES PAREADOS ({metric}, alpha={alpha}) ===\n")
        print(df.to_string(index=False, float_format="%.4f"))
        print(f"\nSalvo em {save_path}")

        return df

    @staticmethod
    def shap_full_analysis(X_train, X_test, model_path, feature_names, model_name, dataset_name):
        import os
        import shap
        import joblib
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import pickle

        # =========================
        # DIRS
        # =========================
        base_raw = f"./classes/classification/results/shap/{model_name}/"
        base_plot = f"./classes/classification/estatisticas_resultados/shap/{model_name}/"

        os.makedirs(base_raw, exist_ok=True)
        os.makedirs(base_plot, exist_ok=True)
        os.makedirs(os.path.join(base_plot, "Beeswarm"), exist_ok=True)

        # =========================
        # REMOVE ID
        # =========================
        if hasattr(X_train, "iloc"):
            X_train = X_train.iloc[:, 1:]
            X_test = X_test.iloc[:, 1:]
        else:
            X_train = X_train[:, 1:]
            X_test = X_test[:, 1:]

        assert X_train.shape[1] == len(feature_names)

        # =========================
        # LOAD MODEL
        # =========================
        with open(model_path, "rb") as f:
            modelo = pickle.load(f)

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

        # =========================
        # CACHE SHAP
        # =========================
        sv_path = os.path.join(base_raw, "sv.pkl")
        X_path = os.path.join(base_raw, "X.npy")

        if os.path.exists(sv_path) and os.path.exists(X_path):
            print("Carregando SHAP cache...")
            sv = joblib.load(sv_path)
            X_array = np.load(X_path)
        else:
            print("Gerando SHAP...")

            expl = shap.Explainer(model_final.predict_proba, X_train_t[:1000])

            subset = X_test_t[:1000]
            X_array = subset.values if hasattr(subset, "values") else np.array(subset)

            sv = expl(subset)

            joblib.dump(sv, sv_path)
            np.save(X_path, X_array)

        shap_vals = sv.values  # (samples, features, classes)
        n_classes = shap_vals.shape[2]

        # =====================================================
        # GLOBAL IMPORTANCE
        # =====================================================
        global_importance = np.mean(np.abs(shap_vals), axis=(0, 2))

        df_global = pd.DataFrame({
            "feature": feature_names,
            "importance": global_importance
        }).sort_values("importance", ascending=False)

        df_global.to_csv(os.path.join(base_raw, "global_importance.csv"), index=False)

        # ---- top 20
        top20 = df_global.head(20)

        plt.figure(figsize=(10, 6))
        plt.barh(top20["feature"][::-1], top20["importance"][::-1])
        plt.title("Top 20 Global Features")
        plt.tight_layout()
        plt.savefig(os.path.join(base_plot, "top20_global.png"), dpi=300)
        plt.close()

        # =====================================================
        # IMPORTANCE POR CLASSE
        # =====================================================
        class_importance = np.mean(np.abs(shap_vals), axis=0)

        df_class = pd.DataFrame(
            class_importance,
            index=feature_names,
            columns=[f"class_{i}" for i in range(n_classes)]
        )

        df_class.to_csv(os.path.join(base_raw, "importance_per_class.csv"))

        # ---- soma por classe
        class_sum = df_class.sum(axis=0)

        class_sum.plot(kind="bar", figsize=(8, 5))
        plt.title("Importância total por classe")
        plt.tight_layout()
        plt.savefig(os.path.join(base_plot, "importance_per_class.png"), dpi=300)
        plt.close()

        # ---- top15 por classe
        for c in range(n_classes):
            top15 = df_class.iloc[:, c].sort_values(ascending=False).head(15)

            plt.figure(figsize=(10, 6))
            plt.barh(top15.index[::-1], top15.values[::-1])
            plt.title(f"Top 15 - Classe {c}")
            plt.tight_layout()
            plt.savefig(os.path.join(base_plot, f"top15_class_{c}.png"), dpi=300)
            plt.close()

        # =====================================================
        # LOW IMPORTANCE
        # =====================================================
        thresholds = [0.05, 0.01, 0.005]

        with open(os.path.join(base_raw, "low_importance.txt"), "w") as f:
            for t in thresholds:
                count = np.sum(global_importance < t)
                f.write(f"< {t}: {count}\n")
                print(f"Features < {t}: {count}")

        # =====================================================
        # BEESWARM
        # =====================================================

        subset = X_array[:500]

        # por classe
        for c in range(n_classes):
            plt.figure(figsize=(12, 8))

            shap.summary_plot(
                shap_vals[:500, :, c],
                subset,
                feature_names=feature_names,
                show=False
            )

            plt.savefig(
                os.path.join(base_plot, f"Beeswarm/beeswarm_class_{c}_{dataset_name}.png"),
                dpi=300,
                bbox_inches="tight"
            )
            plt.close()

        # global
        shap_abs_mean = np.mean(np.abs(shap_vals), axis=2)

        plt.figure(figsize=(12, 8))
        shap.summary_plot(
            shap_abs_mean[:500],
            subset,
            feature_names=feature_names,
            show=False
        )

        plt.savefig(
            os.path.join(base_plot, f"Beeswarm/beeswarm_global_{dataset_name}.png"),
            dpi=300,
            bbox_inches="tight"
        )
        plt.close()

        print("SHAP completo finalizado.")