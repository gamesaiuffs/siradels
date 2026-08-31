# -*- coding: utf-8 -*-
import ast
import glob
import os
import pickle
import traceback
from more_itertools import sort_together
import numpy as np
import json
import optuna
import pandas as pd
from sklearn.base import clone
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from classes.strategies.EstrategiaDjonatan import EstrategiaDjonatan
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaAndrei import EstrategiaAndrei
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.enum.TipoDistrito import TipoDistrito
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import GroupKFold, train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, make_scorer, accuracy_score, confusion_matrix, log_loss, ConfusionMatrixDisplay
from sklearn.model_selection import learning_curve
from sklearn.decomposition import PCA
from sklearn.model_selection import StratifiedGroupKFold
import matplotlib.pyplot as plt
import joblib

class ClassificaEstados:   
    
    # Salva resultados das amostras
    @staticmethod
    def salvar_amostras(X: np.ndarray, Y: list, jogos: str, rotulos: str):
        #j = j.astype(np.uint32)
        
        np.savetxt('./classes/classification/dataset/amostras/' + jogos + '.csv', X, delimiter=',', fmt='%s')   # Features
        np.savetxt('./classes/classification/dataset/amostras/' + rotulos + '.csv', Y, delimiter=',', fmt='%6u')    # Rotulos

        '''
        # Caminho do arquivo CSV
        caminho_arquivo_csv = 'seu_arquivo.csv'

        # Abre o arquivo CSV no modo de adição ('a')
        with open(caminho_arquivo_csv, mode='a', newline='') as arquivo_csv:
            # Cria um objeto escritor CSV
            escritor_csv = csv.writer(arquivo_csv)

            # Adiciona os novos dados ao final do arquivo
            escritor_csv.writerows(novos_dados)
        '''
        return

    # Ler amostras salvas
    @staticmethod
    def ler_amostras(jogos: str, rotulos: str, div: bool = True):
        X = np.genfromtxt('./classes/classification/dataset/amostras/' + jogos + '.csv', delimiter=',', dtype=np.float32)
        #jogos = np.genfromtxt('./tabela_estado/' + i.name + '.csv', delimiter=',')
        Y = np.genfromtxt('./classes/classification/dataset/amostras/' + rotulos + '.csv', delimiter=',', dtype=np.int8) 
        #rotulos = np.genfromtxt('./tabela_estado/' + 'Rotulos' + '.csv', delimiter=',') 
        #X = jogos
        #Y = rotulos
        if div == True:
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
            return X_train, X_test, y_train, y_test
        else:
            return X, Y
    
    #------------------------------------------------- FIM MANIPULAÇÃO DE AMOSTRAS ------------------------------------------------------------#
    
    @staticmethod
    def pca(X: str, n_features: int = 137):

        pca = PCA(n_features)
        pca.fit(X)

        while sum(pca.explained_variance_ratio_) >= 0.96:

            print(n_features)

            n_features = n_features-1
            pca = PCA(n_features)
            pca.fit(X)
        
        print("Valores: \n", pca.explained_variance_ratio_)
        print("Soma: ", sum(pca.explained_variance_ratio_))
        X = pca.transform(X)

        return X


    @staticmethod
    def grid_rf(jogos, rotulos):

        resultados_grid = {}

        f1_binary = make_scorer(f1_score, pos_label=1)
        f1_macro_scorer = make_scorer(f1_score, average='macro')
        precision_scorer = make_scorer(precision_score)
        recall_scorer = make_scorer(recall_score)
        accuracy_scorer = make_scorer(accuracy_score)

        metrics = (f1_macro_scorer, precision_scorer, recall_scorer, accuracy_scorer)
        metrics_names = ('Macro F1', 'Precision', 'Recall', 'Accuracy')

        # Definir a grade de hiperparâmetros
        grid = {
            'max_depth': [15, 20, 30, 50, None],
            'n_estimators': [50, 100, 200],
            'criterion': ['gini', 'entropy', 'log_loss'],
            'class_weight': [{0: 1, 1: 5}, {0: 1, 1: 4}, {0: 1, 1: 3}, {0: 1, 1: 2}, {0: 1, 1: 1}],
            'min_samples_leaf': [1, 101, 301, 501],
            'min_samples_split': [2, 20, 100, 300],
        }

        #for i, metric in enumerate(metrics):
            # Configurar o GridSearchCV
        grid_search = GridSearchCV(
            estimator=RandomForestClassifier(random_state=42),
            param_grid=grid,
            cv=10,  # 10-fold cross-validation
            n_jobs=-1,  # Use todos os núcleos disponíveis
            scoring=f1_binary   # Métrica de avaliação
        )

        # Treinar o modelo
        grid_search.fit(jogos, rotulos)

        best_score = grid_search.best_score_
        cv_results = grid_search.cv_results_

        matching_models = [
            (score, params) for score, params in zip(cv_results['mean_test_score'], cv_results['params']) if score == best_score
        ]

        # Exibir os modelos com a mesma pontuação do melhor estimador
        for score, params in matching_models:
            print(f" Metric: {f1_binary}, Score: {score}, Parameters: {params}")

            # Armazenar no dicionário com a métrica como chave
            resultados_grid["F1 score"] = {
                "best_score": best_score,
                "matching_models": matching_models
            }

        joblib.dump(grid_search, f'./classes/classification/models/RF Best {metrics_names[3]}')
        
        ClassificaEstados.salva_testes(resultados_grid, './classes/classification/results/Random Forest/forest_f1')

        return

    @staticmethod
    def grid_cart(jogos, rotulos):

        resultados_grid = {}
        f1_binary = make_scorer(f1_score, pos_label=1)
        f1_macro_scorer = make_scorer(f1_score, average='macro')
        precision_scorer = make_scorer(precision_score)
        recall_scorer = make_scorer(recall_score)
        accuracy_scorer = make_scorer(accuracy_score)

        metrics = (f1_macro_scorer, precision_scorer, recall_scorer)
        metrics_names = ('Macro F1', 'Precision', 'Recall', 'F1 Score')
        grid = {
            'max_depth': [15, 20, 30, 50],
            'criterion': ["gini", "log_loss", "entropy"],
            'min_samples_leaf': [1, 101, 301, 501],
            'min_samples_split': [2, 20, 100, 300],
            'class_weight': [{0: 1, 1: 5}, {0: 1, 1: 4}, {0: 1, 1: 3}, {0: 1, 1: 2}, {0: 1, 1: 1}],
        }
        metrics = (f1_macro_scorer, precision_scorer, recall_scorer, accuracy_scorer)
        metrics_names = ('Macro F1', 'Precision', 'Recall', 'Accuracy')

        for i, metric in enumerate(metrics):
            # Definir a grade de hiperparâmetros
            grid = {
                'max_depth': [15, 20, 30, 50, None],
                'criterion': ["gini", "log_loss", "entropy"],
                'min_samples_leaf': [1, 101, 301, 501],
                'min_samples_split': [2, 20, 100, 300],
                'class_weight': [{0: 1, 1: 5}, {0: 1, 1: 4}, {0: 1, 1: 3}, {0: 1, 1: 2}, {0: 1, 1: 1}],
            }

        #for i, metric in enumerate(metrics):
            # Definir a grade de hiperparâmetros

        # Configurar o GridSearchCV
        grid_search = GridSearchCV(
            estimator=DecisionTreeClassifier(random_state=42),
            param_grid=grid,
            cv=10,  # 10-fold cross-validation
            n_jobs=-1,  # Use todos os núcleos disponíveis
            scoring= f1_binary  # Métrica de avaliação
        )

        # Treinar o modelo
        grid_search.fit(jogos, rotulos)

        best_score = grid_search.best_score_
        cv_results = grid_search.cv_results_

        #print(cv_results)
        
        matching_models = [
            (score, params) for score, params in zip(cv_results['mean_test_score'], cv_results['params']) if score == best_score
        ]

        # Exibir os modelos com a mesma pontuação do melhor estimador
        for score, params in matching_models:
            print(f" Metric: {f1_binary}, Score: {score}, Parameters: {params}")

            resultados_grid[metrics_names[i]] = {
                "best_score": best_score,
                "matching_models": matching_models
            }
            
            joblib.dump(grid_search, f'./classes/classification/models/CART Best {metrics_names[i]}')
        
        ClassificaEstados.salva_testes(resultados_grid, './classes/classification/results/CART/cart_f1')

        return


    # Mostra informacoes do modelo
    @staticmethod
    def modelo_info(model_path: str, feature_names: list):

        pipeline = joblib.load(model_path)
        modelo = pipeline[-1]
        print(type(modelo))
        '''
        # mostra o número de estimadores e a profundidade média das árvores
        print(f"Número de estimadores: {len(modelo.estimators_)}")
        profundidades = [tree.tree_.max_depth for tree in modelo.estimators_]
        print(f"Profundidade média das árvores: {np.mean(profundidades):.2f}")
        print(f"Profundidade mínima: {min(profundidades)}")
        print(f"Profundidade máxima: {max(profundidades)}")
        
        '''
        # Mostra as importancia de cada variavel do estado
        feat_imp = modelo.feature_importances_
        feat_imp = dict(zip(feature_names, feat_imp))
        '''
        profundidade = modelo.get_depth()
        n_nos = modelo.tree_.node_count
        n_folhas = modelo.get_n_leaves()
        n_folhas = int(n_folhas)
        info_dict = {
            "Feature Importances": feat_imp,
            "Depth": profundidade,
            "Node Number": n_nos,
            "Leaves Number": n_folhas
        }
        '''

        # Podem ser adicionadas mais informações
        # https://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html

        info_dict = {
            "Feature Importances": feat_imp
        }

        for chave, valor in info_dict.items():
            if isinstance(valor, np.ndarray):
                info_dict[chave] = valor.tolist()

        return info_dict


    # Utiliza modelo treinado para obter chance de vitoria
    @staticmethod
    def calcula_porcentagem(data, model_name: str, nome_jogador):
        # Carrega modelo
        model = joblib.load(f'./classes/classification/models/{model_name}')
        data_vec = [data]

        # Calcula probabilidade de vitória
        win_probability = model.predict_proba(data_vec)
        win_probability = f"Probabilidade estimada de vitoria para o jogador {nome_jogador}: {round(win_probability[0][1] * 100, 2)}%"

        print(win_probability)  # Probabilidade estimada de vitória

        return 
    
    # Trabalho de IA
    @staticmethod
    def grid_gb(jogos, rotulos):

        resultados_grid = {}

        f1_macro_scorer = make_scorer(f1_score, average='macro')
        f1_scorer = make_scorer(f1_score)
        precision_scorer = make_scorer(precision_score)
        recall_scorer = make_scorer(recall_score)
        accuracy_scorer = make_scorer(accuracy_score)

        metrics = (f1_macro_scorer, f1_scorer, precision_scorer, recall_scorer, accuracy_scorer)
        metrics_names = ('Macro F1', 'F1', 'Precision', 'Recall', 'Accuracy')

        grid = {
            'max_depth': [3, 5, 7, 10, 20, None],
            'loss': ['log_loss', 'exponential'],
            'n_estimators': [20, 50, 100],
            'criterion': ['friedman_mse', 'squared_error'],
            'min_samples_leaf': [1, 101, 301, 501],
            'min_samples_split': [2, 20, 100, 300],
            'learning_rate': [0.01, 0.1, 0.3, 0.5, 1],  
        }

        for i, metric in enumerate(metrics):
            grid_search = GridSearchCV(
                estimator=GradientBoostingClassifier(random_state=42),
                param_grid=grid,
                cv=5,
                n_jobs=-1,
                scoring=metric,
                verbose=2
            )

            grid_search.fit(jogos, rotulos)

            best_score = grid_search.best_score_
            cv_results = grid_search.cv_results_

            matching_models = [
                (score, params) for score, params in zip(cv_results['mean_test_score'], cv_results['params']) if score == best_score
            ]

            for score, params in matching_models:
                print(f"Metric: {metrics_names[i]}, Score: {score:.4f}, Parameters: {params}")

            resultados_grid[metrics_names[i]] = {
                "best_score": best_score,
                "matching_models": matching_models
            }

            joblib.dump(grid_search, f'./classes/classification/models/GB Best {metrics_names[i]}')

        ClassificaEstados.salva_testes(resultados_grid, './classes/classification/results/Gradient Boosting/gradient')

        return
    
    @staticmethod
    def optuna_MLP(jogos, rotulos, n_trials=1000):
        return ClassificaEstados._run_optuna_with_balanced_folds(
            jogos=jogos,
            rotulos=rotulos,
            model_key="MLP",
            n_trials=n_trials
        )
    
    @staticmethod
    def optuna_GB(jogos, rotulos):
        # Mantida por compatibilidade: agora usa XGB.
        return ClassificaEstados.optuna_XGB(jogos, rotulos)
    
    @staticmethod
    def early_stopping_callback(patience):
        best_score = -float("inf")
        no_improve_count = 0

        def callback(study, trial):
            nonlocal best_score, no_improve_count

            if trial.value is not None and trial.value > best_score:
                best_score = trial.value
                no_improve_count = 0
            else:
                no_improve_count += 1

            if no_improve_count >= patience:
                print(f"Early stopping triggered after {patience} trials without improvement.")
                study.stop()

        return callback

    @staticmethod
    def optuna_CART(jogos, rotulos, n_trials=1000):
        return ClassificaEstados._run_optuna_with_balanced_folds(
            jogos=jogos,
            rotulos=rotulos,
            model_key="CART",
            n_trials=n_trials
        )

    @staticmethod    
    def optuna_RF(jogos, rotulos, n_trials=1000, total_partidas=None):
        return ClassificaEstados._run_optuna_with_balanced_folds(
            jogos=jogos,
            rotulos=rotulos,
            model_key="RF",
            n_trials=n_trials,
            total_partidas=total_partidas
        )
    
    @staticmethod
    def evaluate_rf(jogos, rotulos, best_params, total_partidas=None):
        return ClassificaEstados.treinar_e_avaliar_RF(
            jogos=jogos,
            rotulos=rotulos,
            best_params=best_params,
            total_partidas=total_partidas
        )

    @staticmethod
    def optuna_XGB(jogos, rotulos, n_trials=1000, total_partidas=None):
        return ClassificaEstados._run_optuna_with_balanced_folds(
            jogos=jogos,
            rotulos=rotulos,
            model_key="XGB",
            n_trials=n_trials,
            total_partidas=total_partidas
        )

    @staticmethod
    def treinar_e_avaliar_CART(jogos, rotulos, best_params, total_partidas=None):
        return ClassificaEstados._run_evaluation_with_balanced_folds(
            jogos=jogos,
            rotulos=rotulos,
            best_params=best_params,
            model_key="CART",
            total_partidas=total_partidas
        )

    @staticmethod
    def treinar_e_avaliar_XGB(jogos, rotulos, best_params, total_partidas=None):
        return ClassificaEstados._run_evaluation_with_balanced_folds(
            jogos=jogos,
            rotulos=rotulos,
            best_params=best_params,
            model_key="XGB",
            total_partidas=total_partidas
        )

    @staticmethod
    def preparar_dataset_combinado_otimizacao_teste(jogos, rotulos, total_partidas=None, seed=42):
        X_raw, y_raw = ClassificaEstados.ler_amostras(jogos, rotulos, div=False)
        X_raw = np.asarray(X_raw, dtype=np.float32)
        y_raw = np.asarray(y_raw).astype(int).ravel()
        if X_raw.ndim == 1:
            X_raw = X_raw.reshape(1, -1)

        round_mask = X_raw[:, 1] >= 2
        X_raw = X_raw[round_mask]
        y_raw = y_raw[round_mask]

        match_ids = X_raw[:, 0].astype(int)
        features = np.delete(X_raw, 0, axis=1).astype(np.float32)

        unique_matches = np.unique(match_ids)
        available = len(unique_matches)
        if available < 100:
            raise ValueError(f"Número de partidas insuficiente após filtro de rodada>=2: {available}.")

        max_divisible = (available // 100) * 100
        if total_partidas is None:
            total_partidas = max_divisible
        if total_partidas % 100 != 0:
            raise ValueError(f"total_partidas deve ser divisível por 100. Recebido: {total_partidas}.")
        if total_partidas > available:
            raise ValueError(f"total_partidas ({total_partidas}) > partidas disponíveis ({available}).")

        rng = np.random.default_rng(seed)
        selected_matches = rng.choice(unique_matches, size=total_partidas, replace=False)
        selected_set = set(int(m) for m in selected_matches.tolist())
        selected_mask = np.array([int(m) in selected_set for m in match_ids], dtype=bool)

        X_sel = features[selected_mask]
        y_sel = y_raw[selected_mask]
        return X_sel, y_sel


    @staticmethod
    def treinar_modelo_final_XGB_grande(jogos, rotulos, best_params, total_partidas=None, seed=42, save_name="XGB_final.pkl"):
        X, y = ClassificaEstados.preparar_dataset_combinado_otimizacao_teste(
            jogos=jogos,
            rotulos=rotulos,
            total_partidas=total_partidas,
            seed=seed
        )

        pipeline = ClassificaEstados._make_pipeline("XGB", best_params, y)
        pipeline.fit(X, y)

        save_dir = "./classes/classification/results/modelos"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, save_name)

        with open(save_path, "wb") as f:
            pickle.dump(pipeline, f)

        print(f"[XGB_final] saved model to {save_path}")
        return pipeline
    
    @staticmethod
    def carregar_melhores_parametros(caminho_study):
        study = joblib.load(caminho_study)
        best_params = study.best_params
        return best_params

    @staticmethod
    def treinar_e_avaliar_MLP(jogos, rotulos, best_params, total_partidas=None):
        return ClassificaEstados._run_evaluation_with_balanced_folds(
            jogos=jogos,
            rotulos=rotulos,
            best_params=best_params,
            model_key="MLP",
            total_partidas=total_partidas
        )

    @staticmethod
    def treinar_e_avaliar_RF(jogos, rotulos, best_params, total_partidas=None):
        return ClassificaEstados._run_evaluation_with_balanced_folds(
            jogos=jogos,
            rotulos=rotulos,
            best_params=best_params,
            model_key="RF",
            total_partidas=total_partidas
        )

    @staticmethod
    def treinar_regressao_logistica(jogos, rotulos, nome_modelo, class_weight=None, total_partidas=None):
        return ClassificaEstados._run_evaluation_with_balanced_folds(
            jogos=jogos,
            rotulos=rotulos,
            best_params={"class_weight": class_weight},
            model_key="LOGREG",
            total_partidas=total_partidas,
            nome_modelo=nome_modelo
        )

    @staticmethod
    def treinar_e_avaliar_progress_CART(jogos, rotulos):
        return ClassificaEstados._run_evaluation_with_progress_folds(
            jogos, rotulos, "CART"
        )

    @staticmethod
    def treinar_e_avaliar_progress_RF(jogos, rotulos):
        return ClassificaEstados._run_evaluation_with_progress_folds(
            jogos, rotulos, "RF"
        )

    @staticmethod
    def treinar_e_avaliar_progress_XGB(jogos, rotulos):
        return ClassificaEstados._run_evaluation_with_progress_folds(
            jogos, rotulos, "XGB"
        )

    @staticmethod
    def treinar_e_avaliar_progress_MLP(jogos, rotulos):
        return ClassificaEstados._run_evaluation_with_progress_folds(
            jogos, rotulos, "MLP"
        )

    @staticmethod
    def treinar_e_avaliar_progress_LogReg(jogos, rotulos):
        return ClassificaEstados._run_evaluation_with_progress_folds(
            jogos, rotulos, "LOGREG"
        )

    @staticmethod
    def _summarize(vals):
        vals = np.asarray(vals, dtype=float)
        mean = float(np.mean(vals))
        std = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
        sem = std / np.sqrt(len(vals)) if len(vals) > 0 else 0.0
        ci95 = (mean - 1.96 * sem, mean + 1.96 * sem) if len(vals) > 1 else (mean, mean)
        return {"mean": mean, "std": std, "sem": float(sem), "ci95": ci95, "n_folds": len(vals)}

    @staticmethod
    def _swap_players_in_row(row, from_pos, to_pos):
        row = row.copy()
        # Aqui a feature de id_partida já foi removida.
        turn_start = 1
        players_start = 6
        n_players = 5
        player_block = (len(row) - players_start) // n_players

        i = int(from_pos) 
        j = int(to_pos)
        if i == j:
            return row

        idx_turn_i = turn_start + i
        idx_turn_j = turn_start + j
        row[idx_turn_i], row[idx_turn_j] = row[idx_turn_j], row[idx_turn_i]

        bi_start = players_start + (i * player_block)
        bj_start = players_start + (j * player_block)
        bi_end = bi_start + player_block
        bj_end = bj_start + player_block

        bloco_i = row[bi_start:bi_end].copy()
        bloco_j = row[bj_start:bj_end].copy()
        row[bi_start:bi_end] = bloco_j
        row[bj_start:bj_end] = bloco_i
        return row

    @staticmethod
    def _balance_fold_classes_by_swapping(X_fold, y_fold, rng):
        X_bal = np.asarray(X_fold).copy()
        y_bal = np.asarray(y_fold).astype(int).copy()
        labels = np.array([0, 1, 2, 3, 4], dtype=int)

        n = len(y_bal)
        base = n // len(labels)
        remainder = n % len(labels)
        target = {int(lbl): base for lbl in labels}
        for lbl in labels[:remainder]:
            target[int(lbl)] += 1

        while True:
            counts = {int(lbl): int(np.sum(y_bal == lbl)) for lbl in labels}
            surplus = [lbl for lbl in labels if counts[int(lbl)] > target[int(lbl)]]
            deficit = [lbl for lbl in labels if counts[int(lbl)] < target[int(lbl)]]
            if not surplus or not deficit:
                break

            src = int(max(surplus, key=lambda c: counts[int(c)] - target[int(c)]))
            dst = int(max(deficit, key=lambda c: target[int(c)] - counts[int(c)]))
            src_idx = np.where(y_bal == src)[0]
            if len(src_idx) == 0:
                break

            chosen = int(rng.choice(src_idx))
            X_bal[chosen] = ClassificaEstados._swap_players_in_row(X_bal[chosen], src, dst)
            y_bal[chosen] = dst

        return X_bal, y_bal

    @staticmethod
    def _prepare_progress_folds(jogos, rotulos, seed=42):
        X_raw, y_raw = ClassificaEstados.ler_amostras(jogos, rotulos, div=False)

        X_raw = np.asarray(X_raw, dtype=np.float32)
        y_raw = np.asarray(y_raw).astype(int).ravel()

        match_ids = X_raw[:, 0].astype(int)
        rounds = X_raw[:, 1].astype(int)

        features = np.delete(X_raw, 0, axis=1).astype(np.float32)

        # agrupar por partida
        matches = {}
        for i, m in enumerate(match_ids):
            matches.setdefault(m, []).append(i)

        # bins de progresso
        bins = {
            0: [],  # 0-20
            1: [],  # 20-40
            2: [],  # 40-60
            3: [],  # 60-80
            4: []   # 80-100
        }

        for m, idxs in matches.items():
            idxs = sorted(idxs, key=lambda i: rounds[i])
            total = len(idxs)

            for pos, i in enumerate(idxs):
                progress = pos / total
                bin_id = min(int(progress * 5), 4)

                bins[bin_id].append(i)

        rng = np.random.default_rng(seed)
        folds_by_bin = {}

        for bin_id, indices in bins.items():
            indices = np.array(indices)
            rng.shuffle(indices)

            split = np.array_split(indices, 10)
            folds = []

            for part in split:
                X_fold = features[part]
                y_fold = y_raw[part]
                m_fold = match_ids[part]

                folds.append((X_fold, y_fold, m_fold))

            folds_by_bin[bin_id] = folds

        return folds_by_bin

    @staticmethod
    def _prepare_balanced_folds(jogos, rotulos, total_partidas=None, seed=42):
        X_raw, y_raw = ClassificaEstados.ler_amostras(jogos, rotulos, div=False)
        X_raw = np.asarray(X_raw, dtype=np.float32)
        y_raw = np.asarray(y_raw).astype(int).ravel()
        if X_raw.ndim == 1:
            X_raw = X_raw.reshape(1, -1)

        # Coluna 0 = id_partida e coluna 1 = rodada.
        round_mask = X_raw[:, 1] >= 2
        X_raw = X_raw[round_mask]
        y_raw = y_raw[round_mask]
        match_ids = X_raw[:, 0].astype(int)
        features = np.delete(X_raw, 0, axis=1).astype(np.float32)

        unique_matches = np.unique(match_ids)
        available = len(unique_matches)
        if available < 100:
            raise ValueError(f"Número de partidas insuficiente após filtro de rodada>=2: {available}.")

        max_divisible = (available // 100) * 100
        if total_partidas is None:
            total_partidas = max_divisible
        if total_partidas % 100 != 0:
            raise ValueError(f"total_partidas deve ser divisível por 100. Recebido: {total_partidas}.")
        if total_partidas > available:
            raise ValueError(f"total_partidas ({total_partidas}) > partidas disponíveis ({available}).")

        rng = np.random.default_rng(seed)
        selected_matches = rng.choice(unique_matches, size=total_partidas, replace=False)
        selected_set = set(int(m) for m in selected_matches.tolist())
        selected_mask = np.array([int(m) in selected_set for m in match_ids], dtype=bool)

        X_sel = features[selected_mask]
        y_sel = y_raw[selected_mask]
        m_sel = match_ids[selected_mask]

        shuffled_matches = np.array(sorted(list(selected_set)))
        rng.shuffle(shuffled_matches)

        half = total_partidas // 2
        matches_A = shuffled_matches[:half]
        matches_B = shuffled_matches[half:]

        def build_folds(matches_subset, n_folds):
            split_matches = np.array_split(matches_subset, n_folds)
            folds = []
            for fm in split_matches:
                fm_set = set(int(m) for m in fm.tolist())
                mask = np.array([int(m) in fm_set for m in m_sel], dtype=bool)
                X_fold = X_sel[mask]
                y_fold = y_sel[mask]
                m_fold = m_sel[mask]
                X_fold, y_fold = ClassificaEstados._balance_fold_classes_by_swapping(X_fold, y_fold, rng)
                folds.append((X_fold, y_fold, m_fold))
            return folds

        folds_A = build_folds(matches_A, n_folds=5)
        folds_B = build_folds(matches_B, n_folds=10)
        return folds_A, folds_B

    #------------------------------------------------- ABLAÇÕES DE FEATURES ------------------------------------------------------------#

    # Offsets dentro do bloco de 26 features de cada jogador (ver FEATURE_NAMES em Principal.py).
    # 16 -> times_killed, 17 -> times_robbed, 18..25 -> role_rank_1..8. Essas colunas acumulam
    # quantas vezes o jogador foi alvo de cada papel/ação ao longo da partida e podem funcionar
    # como uma "impressão digital" da política do agente (Comentário 3 / Reviewer 2).
    ABLATION_NO_HISTORY_OFFSETS = list(range(16, 26))

    # Features de gap relativo entre o jogador e o líder: gold_diff_max(1), hand_diff_max(3),
    # built_diff_max(5), city_cost_diff_max(15). O Reviewer 5 argumenta que elas podem entregar
    # a resposta pronta ao modelo em vez de deixá-lo aprender a relação a partir dos valores brutos.
    ABLATION_NO_GAP_OFFSETS = [1, 3, 5, 15]

    @staticmethod
    def _drop_player_offsets(X, offsets, players_start=6, n_players=5):
        X = np.asarray(X)
        old_block = (X.shape[1] - players_start) // n_players
        keep_local = [i for i in range(old_block) if i not in offsets]

        cols_to_keep = list(range(players_start))
        for p in range(n_players):
            base = players_start + p * old_block
            cols_to_keep += [base + i for i in keep_local]

        return X[:, cols_to_keep]

    @staticmethod
    def _prepare_balanced_folds_reduced(jogos, rotulos, drop_offsets, total_partidas=None, seed=42):
        folds_A, folds_B = ClassificaEstados._prepare_balanced_folds(
            jogos=jogos, rotulos=rotulos, total_partidas=total_partidas, seed=seed
        )

        def reduce(folds):
            return [
                (ClassificaEstados._drop_player_offsets(X, drop_offsets), y, m)
                for X, y, m in folds
            ]

        return reduce(folds_A), reduce(folds_B)

    @staticmethod
    def _prepare_progress_folds_reduced(jogos, rotulos, drop_offsets, seed=42):
        folds_by_bin = ClassificaEstados._prepare_progress_folds(jogos, rotulos, seed=seed)
        return {
            bin_id: [
                (ClassificaEstados._drop_player_offsets(X, drop_offsets), y, m)
                for X, y, m in folds
            ]
            for bin_id, folds in folds_by_bin.items()
        }

    @staticmethod
    def _run_evaluation_with_balanced_folds_reduced(jogos, rotulos, best_params, model_key, drop_offsets, ablation_name, total_partidas=None):
        _, folds_B = ClassificaEstados._prepare_balanced_folds_reduced(
            jogos=jogos, rotulos=rotulos, drop_offsets=drop_offsets, total_partidas=total_partidas
        )

        save_dir = "./classes/classification/results/modelos"
        os.makedirs(save_dir, exist_ok=True)

        results = ClassificaEstados._evaluate_from_folds(folds_B, model_key, best_params)

        models = results["models"]
        with open(os.path.join(save_dir, f"{model_key}_{ablation_name}_models.pkl"), "wb") as f:
            pickle.dump(models, f)

        results_to_save = dict(results)
        results_to_save.pop("models", None)

        with open(os.path.join(save_dir, f"{model_key}_{ablation_name}_evaluation.pkl"), "wb") as f:
            pickle.dump(results_to_save, f)

        print(f"[ablation_{ablation_name}_{model_key}] saved evaluation to {save_dir}")
        return results

    @staticmethod
    def _run_evaluation_with_progress_folds_reduced(jogos, rotulos, model_key, drop_offsets, ablation_name, total_partidas=None, seed=42):
        held_out_matches = ClassificaEstados._held_out_match_sets(jogos, rotulos, total_partidas=total_partidas, seed=seed)
        folds_by_bin = ClassificaEstados._prepare_progress_folds_reduced(jogos, rotulos, drop_offsets=drop_offsets, seed=seed)

        model_path = f"./classes/classification/results/modelos/{model_key}_{ablation_name}_models.pkl"
        with open(model_path, "rb") as f:
            models = pickle.load(f)

        labels = ["0-20%", "20-40%", "40-60%", "60-80%", "80-100%"]
        results = {}

        for bin_id, folds in folds_by_bin.items():
            X_bin = np.vstack([f[0] for f in folds])
            y_bin = np.concatenate([f[1] for f in folds])
            m_bin = np.concatenate([f[2] for f in folds])
            results[labels[bin_id]] = ClassificaEstados._evaluate_models_on_bins(models, X_bin, y_bin, m_bin, held_out_matches)

        save_dir = "./classes/classification/results/progress"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{model_key}_{ablation_name}_progress_evaluation.pkl")

        with open(save_path, "wb") as f:
            pickle.dump(results, f)

        print(f"[ablation_progress_{ablation_name}_{model_key}] saved to {save_path}")
        return results

    @staticmethod
    def treinar_e_avaliar_ablation(jogos, rotulos, best_params, model_key, ablation_name, total_partidas=None):
        offsets = {
            "NO_HISTORY": ClassificaEstados.ABLATION_NO_HISTORY_OFFSETS,
            "NO_GAP": ClassificaEstados.ABLATION_NO_GAP_OFFSETS,
        }[ablation_name]

        return ClassificaEstados._run_evaluation_with_balanced_folds_reduced(
            jogos=jogos, rotulos=rotulos, best_params=best_params, model_key=model_key,
            drop_offsets=offsets, ablation_name=ablation_name, total_partidas=total_partidas
        )

    @staticmethod
    def treinar_e_avaliar_progress_ablation(jogos, rotulos, model_key, ablation_name):
        offsets = {
            "NO_HISTORY": ClassificaEstados.ABLATION_NO_HISTORY_OFFSETS,
            "NO_GAP": ClassificaEstados.ABLATION_NO_GAP_OFFSETS,
        }[ablation_name]

        return ClassificaEstados._run_evaluation_with_progress_folds_reduced(
            jogos=jogos, rotulos=rotulos, model_key=model_key,
            drop_offsets=offsets, ablation_name=ablation_name
        )

    #------------------------------------------------- FIM ABLAÇÕES DE FEATURES ------------------------------------------------------------#

    @staticmethod
    def _make_pipeline(model_key, params, y_train):
        params = dict(params or {})

        if model_key == "CART":
            params = {k: v for k, v in params.items() if k != "use_none_max_depth"}
            if params.get("max_depth", "KEEP") == "KEEP":
                params.pop("max_depth", None)
            return Pipeline([("cart", DecisionTreeClassifier(random_state=42, **params))])

        if model_key == "RF":
            use_none = bool(params.pop("use_none_max_depth", False))
            if use_none:
                params["max_depth"] = None
            return Pipeline([("rf", RandomForestClassifier(random_state=42, **params))])

        if model_key == "XGB":
            n_classes = int(len(np.unique(y_train)))
            return Pipeline([("xgb", XGBClassifier(
                objective="multi:softprob",
                num_class=n_classes,
                eval_metric="mlogloss",
                tree_method="hist",
                random_state=42,
                **params
            ))])

        if model_key == "MLP":
            return Pipeline([
                ("scaler", StandardScaler()),
                ("mlp", MLPClassifier(max_iter=500, random_state=42, **params))
            ])

        if model_key == "LOGREG":
            class_weight = params.get("class_weight", None)
            return Pipeline([
                ("scaler", StandardScaler()),
                ("logreg", LogisticRegression(
                    max_iter=2000,
                    class_weight=class_weight,
                    solver="lbfgs",
                    multi_class="auto"
                ))
            ])

        raise ValueError(f"model_key inválido: {model_key}")

    @staticmethod
    def _optuna_params(model_key, trial):
        if model_key == "CART":
            return {
                "criterion": trial.suggest_categorical("criterion", ["gini", "entropy", "log_loss"]),
                "max_depth": trial.suggest_int("max_depth", 3, 40),
                "min_samples_split": trial.suggest_int("min_samples_split", 2, 100),
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 50),
                "max_features": trial.suggest_categorical("max_features", [None, "sqrt", "log2"]),
                "class_weight": trial.suggest_categorical("class_weight", [None, "balanced"]),
                "ccp_alpha": trial.suggest_float("ccp_alpha", 0.0, 0.01)
            }
        if model_key == "RF":
            return {
                "n_estimators": trial.suggest_int("n_estimators", 200, 1200),
                "criterion": trial.suggest_categorical("criterion", ["gini", "entropy", "log_loss"]),
                "max_depth": trial.suggest_int("max_depth", 5, 40),
                "min_samples_split": trial.suggest_int("min_samples_split", 2, 100),
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 50),
                "max_features": trial.suggest_categorical("max_features", ["sqrt", "log2", 0.3, 0.5, 0.7]),
                "bootstrap": trial.suggest_categorical("bootstrap", [True, False]),
                "class_weight": trial.suggest_categorical("class_weight", [None, "balanced", "balanced_subsample"])
            }
        if model_key == "XGB":
            return {
                "n_estimators": trial.suggest_int("n_estimators", 300, 1500),
                "max_depth": trial.suggest_int("max_depth", 3, 10),
                "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
                "subsample": trial.suggest_float("subsample", 0.6, 1.0),
                "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
                "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
                "gamma": trial.suggest_float("gamma", 0, 5),
                "reg_lambda": trial.suggest_float("reg_lambda", 1e-2, 10.0, log=True),
                "reg_alpha": trial.suggest_float("reg_alpha", 1e-3, 10.0, log=True),
            }
        if model_key == "MLP":
            return {
                "hidden_layer_sizes": trial.suggest_categorical(
                    "hidden_layer_sizes",
                    [(64,), (128,), (256,), (64, 64), (128, 64), (128, 128)]
                ),
                "activation": trial.suggest_categorical("activation", ["relu", "tanh"]),
                "solver": "adam",
                "alpha": trial.suggest_float("alpha", 1e-5, 1e-2, log=True),
                "learning_rate_init": trial.suggest_float("learning_rate_init", 1e-4, 1e-2, log=True),
                "batch_size": trial.suggest_categorical("batch_size", [64, 128, 256]),
                "early_stopping": True
            }
        raise ValueError(f"Sem espaço de busca Optuna para model_key={model_key}")

    @staticmethod
    def _cross_val_accuracy_from_folds(folds, model_key, params):
        scores = []
        for i in range(len(folds)):
            X_val, y_val, _ = folds[i]
            train_parts = [folds[j] for j in range(len(folds)) if j != i]
            X_train = np.vstack([p[0] for p in train_parts])
            y_train = np.concatenate([p[1] for p in train_parts])

            pipeline = ClassificaEstados._make_pipeline(model_key, params, y_train)
            pipeline.fit(X_train, y_train)
            preds = pipeline.predict(X_val)
            scores.append(accuracy_score(y_val, preds))
        return float(np.mean(scores))

    @staticmethod
    def _evaluate_from_folds(folds, model_key, params):
        acc, prec, rec, f1 = [], [], [], []
        models = []
        for i in range(len(folds)):
            X_test, y_test, _ = folds[i]
            train_parts = [folds[j] for j in range(len(folds)) if j != i]
            X_train = np.vstack([p[0] for p in train_parts])
            y_train = np.concatenate([p[1] for p in train_parts])

            pipeline = ClassificaEstados._make_pipeline(model_key, params, y_train)
            pipeline.fit(X_train, y_train)

            models.append(pipeline)

            preds = pipeline.predict(X_test)

            acc.append(accuracy_score(y_test, preds))
            prec.append(precision_score(y_test, preds, average="macro", zero_division=0))
            rec.append(recall_score(y_test, preds, average="macro", zero_division=0))
            f1.append(f1_score(y_test, preds, average="macro", zero_division=0))

        return {
            "accuracy": ClassificaEstados._summarize(acc),
            "precision_macro": ClassificaEstados._summarize(prec),
            "recall_macro": ClassificaEstados._summarize(rec),
            "f1_macro": ClassificaEstados._summarize(f1),
            "raw": {"accuracy": acc, "precision_macro": prec, "recall_macro": rec, "f1_macro": f1},
            "models": models
        }

    # Retorna, para cada um dos 10 modelos finais salvos em {model_key}_models.pkl (um por fold de
    # _prepare_balanced_folds), o conjunto de id_partida que esse modelo NUNCA viu no treino: o
    # proprio fold held-out dele em matches_B, mais TODO o matches_A (usado so pelo Optuna para
    # busca de hiperparametros, nunca para treinar os modelos finais via _evaluate_from_folds).
    @staticmethod
    def _held_out_match_sets(jogos, rotulos, total_partidas=None, seed=42):
        folds_A, folds_B = ClassificaEstados._prepare_balanced_folds(
            jogos=jogos, rotulos=rotulos, total_partidas=total_partidas, seed=seed
        )

        matches_A_all = set()
        for (_, _, m) in folds_A:
            matches_A_all.update(int(mm) for mm in m.tolist())

        held_out = []
        for (_, _, m) in folds_B:
            fold_matches = set(int(mm) for mm in m.tolist())
            held_out.append(fold_matches | matches_A_all)
        return held_out

    # Avalia cada um dos 10 modelos (um por fold de treino) SOMENTE nas linhas cujo id_partida
    # pertence ao fold held-out daquele modelo especifico. _prepare_progress_folds constroi os
    # bins de progresso a partir de todas as partidas, sem excluir as que ja foram usadas no
    # treino, entao avaliar um modelo no bin inteiro (sem esse filtro) mistura desempenho real
    # com desempenho sobre dados que o proprio modelo ja viu no treino.
    @staticmethod
    def _evaluate_models_on_bins(models, X, y, m, held_out_matches):
        acc, prec, rec, f1 = [], [], [], []

        for i, model in enumerate(models):
            mask = np.isin(m, list(held_out_matches[i]))
            if not np.any(mask):
                continue

            preds = model.predict(X[mask])
            y_true = y[mask]

            acc.append(accuracy_score(y_true, preds))
            prec.append(precision_score(y_true, preds, average="macro", zero_division=0))
            rec.append(recall_score(y_true, preds, average="macro", zero_division=0))
            f1.append(f1_score(y_true, preds, average="macro", zero_division=0))

        return {
            "accuracy": ClassificaEstados._summarize(acc),
            "precision_macro": ClassificaEstados._summarize(prec),
            "recall_macro": ClassificaEstados._summarize(rec),
            "f1_macro": ClassificaEstados._summarize(f1),
            "raw": {
                "accuracy": acc,
                "precision_macro": prec,
                "recall_macro": rec,
                "f1_macro": f1
            }
        }

    @staticmethod
    def _run_optuna_with_balanced_folds(jogos, rotulos, model_key, n_trials=200, total_partidas=None):
        folds_A, _ = ClassificaEstados._prepare_balanced_folds(
            jogos=jogos,
            rotulos=rotulos,
            total_partidas=total_partidas
        )

        def objective(trial):
            params = ClassificaEstados._optuna_params(model_key, trial)
            return ClassificaEstados._cross_val_accuracy_from_folds(folds_A, model_key, params)

        callback = ClassificaEstados.early_stopping_callback(patience=100)
        study = optuna.create_study(direction="maximize", storage="sqlite:///C:/Users/djona/Programação/siradels/siradels/classes/classification/results/optuna/optuna.db")
        study.optimize(objective, n_trials=n_trials, n_jobs=1, callbacks=[callback])

        resultados_optuna = {
            "best_params": study.best_params,
            "best_score": study.best_value,
            "history": [{"trial": t.number, "accuracy": float(t.value), "params": t.params} for t in study.trials]
        }

        save_dir = "./classes/classification/results/optuna"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{model_key}_optuna.pkl")
        with open(save_path, "wb") as f:
            pickle.dump(resultados_optuna, f)

        print(f"[optuna_{model_key}] best_accuracy={resultados_optuna['best_score']:.4f} save_path={save_path}")
        return resultados_optuna

    @staticmethod
    def _run_evaluation_with_balanced_folds(jogos, rotulos, best_params, model_key, total_partidas=None, nome_modelo=None):
        _, folds_B = ClassificaEstados._prepare_balanced_folds(
            jogos=jogos,
            rotulos=rotulos,
            total_partidas=total_partidas
        )
        
        save_dir = "./classes/classification/results/modelos"
        os.makedirs(save_dir, exist_ok=True)

        results = ClassificaEstados._evaluate_from_folds(folds_B, model_key, best_params)

        models = results["models"]

        with open(os.path.join(save_dir, f"{model_key}_models.pkl"), "wb") as f:
            pickle.dump(models, f)

        results_to_save = dict(results)
        results_to_save.pop("models", None)

        if model_key == "LOGREG":
            safe_name = str(nome_modelo).replace("/", "_").replace("\\", "_")
            save_name = f"LogReg_evaluation_{safe_name}.pkl"
        else:
            save_name = f"{model_key}_evaluation.pkl"

        with open(os.path.join(save_dir, save_name), "wb") as f:
            pickle.dump(results_to_save, f)

        print(f"[treinar_e_avaliar_{model_key}] saved evaluation to {save_dir}")
        return results

    @staticmethod
    def _run_evaluation_with_progress_folds(jogos, rotulos, model_key, total_partidas=None, seed=42):
        held_out_matches = ClassificaEstados._held_out_match_sets(jogos, rotulos, total_partidas=total_partidas, seed=seed)
        folds_by_bin = ClassificaEstados._prepare_progress_folds(jogos, rotulos, seed=seed)

        model_path = f"./classes/classification/results/modelos/{model_key}_models.pkl"

        with open(model_path, "rb") as f:
            models = pickle.load(f)

        results = {}

        labels = [
            "0-20%",
            "20-40%",
            "40-60%",
            "60-80%",
            "80-100%"
        ]

        for bin_id, folds in folds_by_bin.items():

            # junta todos os folds do bin
            X_bin = np.vstack([f[0] for f in folds])
            y_bin = np.concatenate([f[1] for f in folds])
            m_bin = np.concatenate([f[2] for f in folds])

            res = ClassificaEstados._evaluate_models_on_bins(models, X_bin, y_bin, m_bin, held_out_matches)

            results[labels[bin_id]] = res

        # salvar
        save_dir = "./classes/classification/results/progress"
        os.makedirs(save_dir, exist_ok=True)

        save_path = os.path.join(save_dir, f"{model_key}_progress_evaluation.pkl")

        with open(save_path, "wb") as f:
            pickle.dump(results, f)

        print(f"[progress_eval_{model_key}] saved to {save_path}")

        return results

    #------------------------------------------------- BASELINES DE PREDIÇÃO (HEURÍSTICA / ALEATÓRIO) ------------------------------------------------------------#

    # HIGHEST_SCORE: vence quem tem maior pontuação parcial no momento (também é uma heurística).
    # MOST_DISTRICTS: vence quem tem mais distritos construídos no momento.
    # RANDOM: nenhuma informação é usada, os 5 jogadores estão sempre "empatados".
    # Layout da linha (id_partida já removido): [rodada, 5x ordem_turno, 5x bloco_jogador]
    # Offsets dentro do bloco de cada jogador (ver ColetaFeatures.coleta_features):
    #   4  -> número de distritos construídos
    #   14 -> custo total da cidade, que equivale exatamente à pontuação parcial do jogador
    #         (ver Jogador.construir/destruir)
    _BASELINE_FEATURE_OFFSET = {
        "HIGHEST_SCORE": 14,
        "MOST_DISTRICTS": 4,
    }

    # Em vez de sortear 1 vencedor entre os empatados (o que dependeria de uma seed de rng
    # e poderia enviesar o resultado), cada linha empatada é expandida em N sub-amostras,
    # uma prevendo cada jogador empatado, todas com o mesmo rótulo verdadeiro. As métricas
    # (accuracy/precision/recall/F1) são então calculadas normalmente sobre o conjunto expandido.
    # Isso corresponde exatamente ao valor esperado de um desempate aleatório uniforme, mas
    # de forma determinística (sem RNG e sem variância entre execuções).
    @staticmethod
    def _expandir_predicoes_baseline(baseline_key, X, y, n_players=5):
        y = np.asarray(y).astype(int)

        if baseline_key == "RANDOM":
            tied_mask = np.ones((X.shape[0], n_players), dtype=bool)
        elif baseline_key in ClassificaEstados._BASELINE_FEATURE_OFFSET:
            players_start = 6
            offset = ClassificaEstados._BASELINE_FEATURE_OFFSET[baseline_key]
            player_block = (X.shape[1] - players_start) // n_players

            values = np.stack([
                X[:, players_start + i * player_block + offset]
                for i in range(n_players)
            ], axis=1)

            max_values = values.max(axis=1, keepdims=True)
            tied_mask = values == max_values
        else:
            raise ValueError(f"baseline_key inválido: {baseline_key}")

        linhas_idx, classes_preditas = np.nonzero(tied_mask)
        y_expandido = y[linhas_idx]
        return y_expandido, classes_preditas

    @staticmethod
    def _evaluate_baseline_from_folds(folds, baseline_key):
        acc, prec, rec, f1 = [], [], [], []

        for i in range(len(folds)):
            X_test, y_test, _ = folds[i]
            y_exp, preds_exp = ClassificaEstados._expandir_predicoes_baseline(baseline_key, X_test, y_test)

            acc.append(accuracy_score(y_exp, preds_exp))
            prec.append(precision_score(y_exp, preds_exp, average="macro", zero_division=0))
            rec.append(recall_score(y_exp, preds_exp, average="macro", zero_division=0))
            f1.append(f1_score(y_exp, preds_exp, average="macro", zero_division=0))

        return {
            "accuracy": ClassificaEstados._summarize(acc),
            "precision_macro": ClassificaEstados._summarize(prec),
            "recall_macro": ClassificaEstados._summarize(rec),
            "f1_macro": ClassificaEstados._summarize(f1),
            "raw": {"accuracy": acc, "precision_macro": prec, "recall_macro": rec, "f1_macro": f1},
        }

    # Avalia um baseline (HIGHEST_SCORE, MOST_DISTRICTS ou RANDOM) nos mesmos 10 folds balanceados usados para os modelos supervisionados.
    @staticmethod
    def avaliar_baseline(jogos, rotulos, baseline_key, total_partidas=None, seed=42):
        _, folds_B = ClassificaEstados._prepare_balanced_folds(
            jogos=jogos,
            rotulos=rotulos,
            total_partidas=total_partidas,
            seed=seed
        )

        results = ClassificaEstados._evaluate_baseline_from_folds(folds_B, baseline_key)

        save_dir = "./classes/classification/results/evaluation"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{baseline_key}_evaluation.pkl")

        with open(save_path, "wb") as f:
            pickle.dump(results, f)

        print(f"[avaliar_baseline_{baseline_key}] saved evaluation to {save_path}")
        return results

    # Avalia um baseline por fase de progresso da partida (0-20%, ..., 80-100%), usando os
    # mesmos 10 sub-folds por fase que _prepare_progress_folds já constrói (mantém o mesmo
    # formato n_folds=10 dos *_progress_evaluation.pkl dos modelos, mas aqui a variância
    # reflete apenas a divisão em folds, já que o cálculo em si é determinístico).
    @staticmethod
    def avaliar_baseline_progress(jogos, rotulos, baseline_key, seed=42):
        folds_by_bin = ClassificaEstados._prepare_progress_folds(jogos, rotulos, seed=seed)

        labels = ["0-20%", "20-40%", "40-60%", "60-80%", "80-100%"]
        results = {}

        for bin_id, folds in folds_by_bin.items():
            acc, prec, rec, f1 = [], [], [], []

            for X_fold, y_fold, _ in folds:
                y_exp, preds_exp = ClassificaEstados._expandir_predicoes_baseline(baseline_key, X_fold, y_fold)

                acc.append(accuracy_score(y_exp, preds_exp))
                prec.append(precision_score(y_exp, preds_exp, average="macro", zero_division=0))
                rec.append(recall_score(y_exp, preds_exp, average="macro", zero_division=0))
                f1.append(f1_score(y_exp, preds_exp, average="macro", zero_division=0))

            results[labels[bin_id]] = {
                "accuracy": ClassificaEstados._summarize(acc),
                "precision_macro": ClassificaEstados._summarize(prec),
                "recall_macro": ClassificaEstados._summarize(rec),
                "f1_macro": ClassificaEstados._summarize(f1),
                "raw": {"accuracy": acc, "precision_macro": prec, "recall_macro": rec, "f1_macro": f1}
            }

        save_dir = "./classes/classification/results/progress"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{baseline_key}_progress_evaluation.pkl")

        with open(save_path, "wb") as f:
            pickle.dump(results, f)

        print(f"[avaliar_baseline_progress_{baseline_key}] saved to {save_path}")
        return results


def carregar_best_params(model_key):

    caminho = f"./classes/classification/results/optuna/{model_key}_optuna.pkl"

    with open(caminho, "rb") as f:
        resultados = pickle.load(f)

    return resultados["best_params"]

def carregar_resultados_optuna(model_key):

    caminho = f"./classes/classification/results/optuna/{model_key}_optuna.pkl"

    with open(caminho, "rb") as f:
        resultados = pickle.load(f)

    return resultados

def carregar_resultados_avaliacao(model_key):
    caminho = f"./classes/classification/results/evaluation/{model_key}_evaluation.pkl"

    with open(caminho, "rb") as f:
        resultados = pickle.load(f)

    return resultados

def carregar_resultados_progress(model_key):
    caminho = f"./classes/classification/results/progress/{model_key}_progress_evaluation.pkl"

    with open(caminho, "rb") as f:
        resultados = pickle.load(f)

    return resultados