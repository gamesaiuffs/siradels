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
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold, train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, make_scorer, accuracy_score, confusion_matrix, log_loss, ConfusionMatrixDisplay
from sklearn.model_selection import learning_curve
from sklearn.decomposition import PCA
from sklearn.model_selection import StratifiedGroupKFold
import matplotlib.pyplot as plt
import joblib
from scipy import stats

class ClassificaEstados:   

    @staticmethod
    def coleta_rotulos_treino(nome_observado, nome_vencedor):
        if nome_vencedor != "":              
            Y = 1 if nome_observado == nome_vencedor else 0
            return Y
    
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
        X = np.genfromtxt('./classes/classification/dataset/amostras/' + jogos + '.csv', delimiter=',')
        #jogos = np.genfromtxt('./tabela_estado/' + i.name + '.csv', delimiter=',')
        Y = np.genfromtxt('./classes/classification/dataset/amostras/' + rotulos + '.csv', delimiter=',') 
        #rotulos = np.genfromtxt('./tabela_estado/' + 'Rotulos' + '.csv', delimiter=',') 
        #X = jogos
        #Y = rotulos
        if div == True:
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
            return X_train, X_test, y_train, y_test
        else:
            return X, Y
       
    @staticmethod
    def cross_validation(X, y, group):
        sgkf = StratifiedGroupKFold(n_splits=3)

        # Faça a divisão dos dados
        for train_index, test_index in sgkf.split(X, y, group):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            groups_train, groups_test = group[train_index], group[test_index]
   
        f1_macro_scorer = make_scorer(f1_score, average='macro')
        scores = cross_val_score(estimator=f1_macro_scorer)

        return groups_train, groups_test 
    
    #------------------------------------------------- FIM MANIPULAÇÃO DE AMOSTRAS ------------------------------------------------------------#
    
    @staticmethod
    def pca(X: str):

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

        #output = pca.set_output()  #Estimator  
        #print("Parâmetros: \n", pca.get_params(True))
        #print("Precisão: \n", pca.get_precision())
        return X

    @staticmethod
    def grid_gb(jogos, rotulos):

        resultados_grid = {}

        f1_macro_scorer = make_scorer(f1_score, average='macro')
        precision_scorer = make_scorer(precision_score)
        recall_scorer = make_scorer(recall_score)
        accuracy_scorer = make_scorer(accuracy_score)

        metrics = (f1_macro_scorer, precision_scorer, recall_scorer, accuracy_scorer)
        metrics_names = ('Macro F1', 'Precision', 'Recall', 'Accuracy')

        # Definir a grade de hiperparâmetros
        grid = {
            'max_depth': [3, 5, 7, 10, 20, None],
            'loss': ['log_loss', 'exponential'],
            'n_estimators': [50, 100, 200],
            'criterion': ['friedman_mse', 'squared_error'],
            'min_samples_leaf': [1, 101, 301, 501],
            'min_samples_split': [2, 20, 100, 300],
            'learnin_rate': [0.01, 0.1, 0.3, 0.5, 1],
        }

        for i, metric in enumerate(metrics):
            # Configurar o GridSearchCV
            grid_search = GridSearchCV(
                estimator=GradientBoostingClassifier(random_state=42),
                param_grid=grid,
                cv=10,  # 10-fold cross-validation
                n_jobs=-1,  # Use todos os núcleos disponíveis
                scoring= metric  # Métrica de avaliação
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
                print(f" Metric: {metric}, Score: {score}, Parameters: {params}")

            resultados_grid[metrics_names] = {
                "best_score": best_score,
                "matching_models": matching_models
            }

            joblib.dump(grid_search, f'./classes/classification/models/GB Best {metrics_names[i]}')

        ClassificaEstados.salva_testes(resultados_grid, './classes/classification/results/Gradient Boosting/gradient')

        return

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
    def optuna_MLP(jogos, rotulos):
        # Otimiza SOMENTE acurácia e usando GroupKFold por id_partida (partidas completas no split)
        X, y = ClassificaEstados.ler_amostras(jogos, rotulos, div=False)
        X = np.asarray(X)
        y = np.asarray(y).ravel()
        if X.ndim == 1:
            X = X.reshape(1, -1)

        match_id_col = 1
        if X.shape[1] <= match_id_col:
            raise ValueError(f"X não possui coluna de id_partida na posição {match_id_col}. X.shape={X.shape}")

        match_ids = X[:, match_id_col].astype(int)
        X_feat = np.delete(X, match_id_col, axis=1)

        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('mlp', MLPClassifier(max_iter=500, random_state=42))
        ])

        param_space = {
            'hidden_layer_sizes': [(50,), (100,), (50, 50)],
            'activation': ['tanh', 'relu'],
            'solver': ['adam', 'sgd'],
            'alpha': [0.0001, 0.001],
            'learning_rate': ['constant', 'adaptive']
        }

        cv = GroupKFold(n_splits=5)
        scorer = make_scorer(accuracy_score)

        def objective(trial):
            params = {
                'hidden_layer_sizes': trial.suggest_categorical('hidden_layer_sizes', param_space['hidden_layer_sizes']),
                'activation': trial.suggest_categorical('activation', param_space['activation']),
                'solver': trial.suggest_categorical('solver', param_space['solver']),
                'alpha': trial.suggest_categorical('alpha', param_space['alpha']),
                'learning_rate': trial.suggest_categorical('learning_rate', param_space['learning_rate'])
            }

            pipeline.set_params(mlp__hidden_layer_sizes=params['hidden_layer_sizes'],
                                mlp__activation=params['activation'],
                                mlp__solver=params['solver'],
                                mlp__alpha=params['alpha'],
                                mlp__learning_rate=params['learning_rate'])

            scores = cross_val_score(
                pipeline,
                X_feat,
                y,
                cv=cv,
                groups=match_ids,
                scoring=scorer,
                n_jobs=-1
            )
            return scores.mean()

        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=200, n_jobs=1)

        resultados_optuna = {
            "best_params": study.best_params,
            "best_score": study.best_value,
            "history": [{"trial": t.number, "accuracy": float(t.value), "params": t.params} for t in study.trials]
        }

        save_dir = './classes/classification/results/optuna'
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'MLP_optuna.pkl')
        with open(save_path, "wb") as f:
            pickle.dump(resultados_optuna, f)

        print(f"[optuna_MLP] best_accuracy={resultados_optuna['best_score']:.4f} save_path={save_path}")
        return resultados_optuna
    
    @staticmethod
    def optuna_GB(jogos, rotulos):

        resultados_optuna = {}

        scorers = {
            'F1': make_scorer(f1_score),
            'Precision': make_scorer(precision_score),
            'Accuracy': make_scorer(accuracy_score)
        }

        pipeline = Pipeline([
            ('gb', GradientBoostingClassifier(random_state=42))
        ])

        param_space = {
            'n_estimators': [50, 100, 150],
            'learning_rate': [0.01, 0.1, 0.2],
            'max_depth': [5, 10, 15],
            'min_samples_split': [5, 20, 50],
            'min_samples_leaf': [5, 20, 50],
        }

        for metric_name, scorer in scorers.items():
            def objective(trial):
                params = {
                    'n_estimators': trial.suggest_categorical('n_estimators', param_space['n_estimators']),
                    'learning_rate': trial.suggest_categorical('learning_rate', param_space['learning_rate']),
                    'max_depth': trial.suggest_categorical('max_depth', param_space['max_depth']),
                    'min_samples_split': trial.suggest_categorical('min_samples_split', param_space['min_samples_split']),
                    'min_samples_leaf': trial.suggest_categorical('min_samples_leaf', param_space['min_samples_leaf'])
                }

                pipeline.set_params(gb__n_estimators=params['n_estimators'],
                                    gb__learning_rate=params['learning_rate'],
                                    gb__max_depth=params['max_depth'],
                                    gb__min_samples_split=params['min_samples_split'],
                                    gb__min_samples_leaf=params['min_samples_leaf'])

                score = cross_val_score(pipeline, jogos, rotulos, cv=5, scoring=scorer, n_jobs=-1)
                return score.mean()

            study = optuna.create_study(direction='maximize')
            study.optimize(objective, n_trials=50, n_jobs=-1)

            best_score = study.best_value
            best_params = study.best_params

            print(f"Metric: {metric_name}, Score: {best_score:.4f}, Parameters: {best_params}")

            resultados_optuna[metric_name] = {
                "best_score": best_score,
                "best_params": best_params
            }

            joblib.dump(study, f'./classes/classification/models/GB Best {metric_name}')

        ClassificaEstados.salva_testes(resultados_optuna, './classes/classification/results/GB/gb')

        return
    
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
    def optuna_CART(jogos, rotulos):
        # Otimiza SOMENTE acurácia e usando GroupKFold por id_partida (partidas completas no split)
        X, y = ClassificaEstados.ler_amostras(jogos, rotulos, div=False)
        X = np.asarray(X)
        y = np.asarray(y).ravel()
        if X.ndim == 1:
            X = X.reshape(1, -1)

        match_id_col = 1
        if X.shape[1] <= match_id_col:
            raise ValueError(f"X não possui coluna de id_partida na posição {match_id_col}. X.shape={X.shape}")

        match_ids = X[:, match_id_col].astype(int)
        X_feat = np.delete(X, match_id_col, axis=1)

        base_pipeline = Pipeline([
            ('cart', DecisionTreeClassifier(random_state=42))
        ])

        # Para multiclasse, usar class_weight='balanced' (ou None) é seguro.
        param_space = {
            'max_depth': (2, 50),
            'min_samples_leaf': (2, 200),
            'min_samples_split': (2, 200),
            'class_weight': [None, 'balanced'],
            'criterion': ['gini', 'entropy', 'log_loss']
        }

        cv = GroupKFold(n_splits=5)
        scorer = make_scorer(accuracy_score)

        def objective(trial):
            max_depth = None if trial.suggest_categorical("use_none_max_depth", [True, False]) \
                else int(trial.suggest_float('max_depth', *param_space['max_depth']))

            params = {
                'max_depth': max_depth,
                'criterion': trial.suggest_categorical('criterion', param_space['criterion']),
                'min_samples_leaf': int(trial.suggest_float('min_samples_leaf', *param_space['min_samples_leaf'])),
                'min_samples_split': int(trial.suggest_float('min_samples_split', *param_space['min_samples_split'])),
                'class_weight': trial.suggest_categorical('class_weight', param_space['class_weight']),
            }

            pipeline = clone(base_pipeline)
            pipeline.set_params(cart__max_depth=params['max_depth'],
                                cart__criterion=params['criterion'],
                                cart__min_samples_leaf=params['min_samples_leaf'],
                                cart__min_samples_split=params['min_samples_split'],
                                cart__class_weight=params['class_weight'])

            scores = cross_val_score(
                pipeline,
                X_feat,
                y,
                cv=cv,
                groups=match_ids,
                scoring=scorer,
                n_jobs=-1
            )
            return scores.mean()

        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=200, n_jobs=1)

        resultados_optuna = {
            "best_params": study.best_params,
            "best_score": study.best_value,
            "history": [{"trial": t.number, "accuracy": float(t.value), "params": t.params} for t in study.trials]
        }

        save_dir = './classes/classification/results/optuna'
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'CART_optuna.pkl')
        with open(save_path, "wb") as f:
            pickle.dump(resultados_optuna, f)

        print(f"[optuna_CART] best_accuracy={resultados_optuna['best_score']:.4f} save_path={save_path}")
        return resultados_optuna

    @staticmethod    
    def optuna_RF(X, y, match_ids, n_trials=1000, save_path="rf_optuna.pkl"):

        base_pipeline = Pipeline([
            ("rf", RandomForestClassifier(random_state=42))
        ])

        cv = GroupKFold(n_splits=5)
        scorer = make_scorer(accuracy_score)

        def objective(trial):

            max_depth = None if trial.suggest_categorical(
                "use_none_max_depth", [True, False]
            ) else trial.suggest_int("max_depth", 2, 50)

            params = {
                "n_estimators": trial.suggest_int("n_estimators", 50, 1000),
                "criterion": trial.suggest_categorical(
                    "criterion", ["gini", "entropy", "log_loss"]
                ),
                "max_depth": max_depth,
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 2, 500),
                "min_samples_split": trial.suggest_int("min_samples_split", 2, 500)
            }

            pipeline = clone(base_pipeline)
            pipeline.set_params(**{f"rf__{k}": v for k, v in params.items()})

            scores = cross_val_score(
                pipeline,
                X,
                y,
                cv=cv,
                groups=match_ids,
                scoring=scorer,
                n_jobs=-1
            )

            return scores.mean()

        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=n_trials)

        results = {
            "best_params": study.best_params,
            "best_score": study.best_value,
            "history": [(t.number, t.value) for t in study.trials]
        }

        with open(save_path, "wb") as f:
            pickle.dump(results, f)

        return results
    
    @staticmethod
    def evaluate_rf(X, y, match_ids, best_params):
        model = RandomForestClassifier(
            random_state=42,
            **{k: v for k, v in best_params.items() if k != "use_none_max_depth"}
        )

        if best_params.get("use_none_max_depth"):
            model.set_params(max_depth=None)

        cv = GroupKFold(n_splits=5)

        acc, prec, rec, f1 = [], [], [], []

        for train_idx, test_idx in cv.split(X, y, groups=match_ids):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]

            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            acc.append(accuracy_score(y_test, preds))
            prec.append(precision_score(y_test, preds, average="macro", zero_division=0))
            rec.append(recall_score(y_test, preds, average="macro", zero_division=0))
            f1.append(f1_score(y_test, preds, average="macro", zero_division=0))

        def summarize(vals):
            vals = np.asarray(vals, dtype=float)
            mean = float(np.mean(vals))
            std = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
            sem = std / np.sqrt(len(vals)) if len(vals) > 0 else 0.0
            ci95 = (mean - 1.96 * sem, mean + 1.96 * sem) if len(vals) > 1 else (mean, mean)
            return {"mean": mean, "std": std, "sem": float(sem), "ci95": ci95, "n_folds": len(vals)}

        results = {
            "accuracy": summarize(acc),
            "precision_macro": summarize(prec),
            "recall_macro": summarize(rec),
            "f1_macro": summarize(f1),
            "raw": {"accuracy": acc, "precision_macro": prec, "recall_macro": rec, "f1_macro": f1}
        }

        with open("rf_evaluation.pkl", "wb") as f:
            pickle.dump(results, f)

        return results

    @staticmethod
    def optuna_XGB(jogos, rotulos):
        # Otimiza SOMENTE acurácia e usando GroupKFold por id_partida (partidas completas no split)
        X, y = ClassificaEstados.ler_amostras(jogos, rotulos, div=False)
        X = np.asarray(X)
        y = np.asarray(y).ravel()
        if X.ndim == 1:
            X = X.reshape(1, -1)

        match_id_col = 1
        if X.shape[1] <= match_id_col:
            raise ValueError(f"X não possui coluna de id_partida na posição {match_id_col}. X.shape={X.shape}")

        match_ids = X[:, match_id_col].astype(int)
        X_feat = np.delete(X, match_id_col, axis=1)

        n_classes = int(len(np.unique(y)))

        # Para multiclasse, usar multi:softprob
        base_pipeline = Pipeline([
            ('xgb', XGBClassifier(
                objective='multi:softprob',
                num_class=n_classes,
                eval_metric='mlogloss',
                tree_method='hist',
                random_state=42
            ))
        ])

        param_space = {
            'n_estimators': (50, 1000),
            'max_depth': (2, 20),
            'learning_rate': (0.01, 0.5),
            'subsample': (0.5, 1.0),
            'colsample_bytree': (0.5, 1.0),
            'reg_lambda': (0.0, 10.0),
            'reg_alpha': (0.0, 10.0),
        }

        cv = GroupKFold(n_splits=5)
        scorer = make_scorer(accuracy_score)

        def objective(trial):
            params = {
                'n_estimators': int(trial.suggest_float('n_estimators', *param_space['n_estimators'])),
                'max_depth': int(trial.suggest_float('max_depth', *param_space['max_depth'])),
                'learning_rate': trial.suggest_float('learning_rate', *param_space['learning_rate']),
                'subsample': trial.suggest_float('subsample', *param_space['subsample']),
                'colsample_bytree': trial.suggest_float('colsample_bytree', *param_space['colsample_bytree']),
                'reg_lambda': trial.suggest_float('reg_lambda', *param_space['reg_lambda']),
                'reg_alpha': trial.suggest_float('reg_alpha', *param_space['reg_alpha']),
            }

            pipeline = clone(base_pipeline)
            pipeline.set_params(
                xgb__n_estimators=params['n_estimators'],
                xgb__max_depth=params['max_depth'],
                xgb__learning_rate=params['learning_rate'],
                xgb__subsample=params['subsample'],
                xgb__colsample_bytree=params['colsample_bytree'],
                xgb__reg_lambda=params['reg_lambda'],
                xgb__reg_alpha=params['reg_alpha'],
            )

            scores = cross_val_score(
                pipeline,
                X_feat,
                y,
                cv=cv,
                groups=match_ids,
                scoring=scorer,
                n_jobs=-1
            )
            return scores.mean()

        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=300, n_jobs=1)

        resultados_optuna = {
            "best_params": study.best_params,
            "best_score": study.best_value,
            "history": [{"trial": t.number, "accuracy": float(t.value), "params": t.params} for t in study.trials]
        }

        save_dir = './classes/classification/results/optuna'
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'XGB_optuna.pkl')
        with open(save_path, "wb") as f:
            pickle.dump(resultados_optuna, f)

        print(f"[optuna_XGB] best_accuracy={resultados_optuna['best_score']:.4f} save_path={save_path}")
        return resultados_optuna

    @staticmethod
    def treinar_e_avaliar_CART(jogos, rotulos, best_params):
        # Avalia via GroupKFold garantindo partidas completas no split
        X, y = ClassificaEstados.ler_amostras(jogos, rotulos, div=False)
        X = np.asarray(X)
        y = np.asarray(y).ravel()
        if X.ndim == 1:
            X = X.reshape(1, -1)

        match_id_col = 1
        match_ids = X[:, match_id_col].astype(int)
        X_feat = np.delete(X, match_id_col, axis=1)

        pipeline = Pipeline([
            ('cart', DecisionTreeClassifier(random_state=42, **best_params))
        ])

        cv = GroupKFold(n_splits=5)
        acc, prec, rec, f1 = [], [], [], []

        for train_idx, test_idx in cv.split(X_feat, y, groups=match_ids):
            X_train, X_test = X_feat[train_idx], X_feat[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]

            pipeline.fit(X_train, y_train)
            preds = pipeline.predict(X_test)

            acc.append(accuracy_score(y_test, preds))
            prec.append(precision_score(y_test, preds, average="macro", zero_division=0))
            rec.append(recall_score(y_test, preds, average="macro", zero_division=0))
            f1.append(f1_score(y_test, preds, average="macro", zero_division=0))

        def summarize(vals):
            vals = np.asarray(vals, dtype=float)
            mean = float(np.mean(vals))
            std = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
            sem = std / np.sqrt(len(vals)) if len(vals) > 0 else 0.0
            ci95 = (mean - 1.96 * sem, mean + 1.96 * sem) if len(vals) > 1 else (mean, mean)
            return {"mean": mean, "std": std, "sem": float(sem), "ci95": ci95, "n_folds": len(vals)}

        results = {
            "accuracy": summarize(acc),
            "precision_macro": summarize(prec),
            "recall_macro": summarize(rec),
            "f1_macro": summarize(f1),
            "raw": {"accuracy": acc, "precision_macro": prec, "recall_macro": rec, "f1_macro": f1}
        }

        save_dir = './classes/classification/results/optuna'
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'CART_evaluation.pkl')
        with open(save_path, "wb") as f:
            pickle.dump(results, f)

        print(f"[treinar_e_avaliar_CART] saved evaluation to {save_path}")
        return results

    @staticmethod
    def treinar_e_avaliar_XGB(jogos, rotulos, best_params):
        # Avalia via GroupKFold garantindo partidas completas no split
        X, y = ClassificaEstados.ler_amostras(jogos, rotulos, div=False)
        X = np.asarray(X)
        y = np.asarray(y).ravel()
        if X.ndim == 1:
            X = X.reshape(1, -1)

        match_id_col = 1
        match_ids = X[:, match_id_col].astype(int)
        X_feat = np.delete(X, match_id_col, axis=1)

        n_classes = int(len(np.unique(y)))

        pipeline = Pipeline([
            ('xgb', XGBClassifier(
                objective='multi:softprob',
                num_class=n_classes,
                eval_metric='mlogloss',
                tree_method='hist',
                random_state=42,
                **best_params
            ))
        ])

        cv = GroupKFold(n_splits=5)
        acc, prec, rec, f1 = [], [], [], []

        for train_idx, test_idx in cv.split(X_feat, y, groups=match_ids):
            X_train, X_test = X_feat[train_idx], X_feat[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]

            pipeline.fit(X_train, y_train)
            preds = pipeline.predict(X_test)

            acc.append(accuracy_score(y_test, preds))
            prec.append(precision_score(y_test, preds, average="macro", zero_division=0))
            rec.append(recall_score(y_test, preds, average="macro", zero_division=0))
            f1.append(f1_score(y_test, preds, average="macro", zero_division=0))

        def summarize(vals):
            vals = np.asarray(vals, dtype=float)
            mean = float(np.mean(vals))
            std = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
            sem = std / np.sqrt(len(vals)) if len(vals) > 0 else 0.0
            ci95 = (mean - 1.96 * sem, mean + 1.96 * sem) if len(vals) > 1 else (mean, mean)
            return {"mean": mean, "std": std, "sem": float(sem), "ci95": ci95, "n_folds": len(vals)}

        results = {
            "accuracy": summarize(acc),
            "precision_macro": summarize(prec),
            "recall_macro": summarize(rec),
            "f1_macro": summarize(f1),
            "raw": {"accuracy": acc, "precision_macro": prec, "recall_macro": rec, "f1_macro": f1}
        }

        save_dir = './classes/classification/results/optuna'
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'XGB_evaluation.pkl')
        with open(save_path, "wb") as f:
            pickle.dump(results, f)

        print(f"[treinar_e_avaliar_XGB] saved evaluation to {save_path}")
        return results

    @staticmethod
    def carregar_melhores_parametros(caminho_study):
        study = joblib.load(caminho_study)
        best_params = study.best_params
        return best_params

    @staticmethod
    def treinar_e_avaliar_MLP(jogos, rotulos, best_params):
        # Avalia via GroupKFold garantindo partidas completas no split
        X, y = ClassificaEstados.ler_amostras(jogos, rotulos, div=False)
        X = np.asarray(X)
        y = np.asarray(y).ravel()
        if X.ndim == 1:
            X = X.reshape(1, -1)

        match_id_col = 1
        match_ids = X[:, match_id_col].astype(int)
        X_feat = np.delete(X, match_id_col, axis=1)

        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('mlp', MLPClassifier(max_iter=500, random_state=42, **best_params))
        ])

        cv = GroupKFold(n_splits=5)

        acc, prec, rec, f1 = [], [], [], []
        for train_idx, test_idx in cv.split(X_feat, y, groups=match_ids):
            X_train, X_test = X_feat[train_idx], X_feat[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]

            pipeline.fit(X_train, y_train)
            preds = pipeline.predict(X_test)

            acc.append(accuracy_score(y_test, preds))
            prec.append(precision_score(y_test, preds, average="macro", zero_division=0))
            rec.append(recall_score(y_test, preds, average="macro", zero_division=0))
            f1.append(f1_score(y_test, preds, average="macro", zero_division=0))

        def summarize(vals):
            vals = np.asarray(vals, dtype=float)
            mean = float(np.mean(vals))
            std = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
            sem = std / np.sqrt(len(vals)) if len(vals) > 0 else 0.0
            ci95 = (mean - 1.96 * sem, mean + 1.96 * sem) if len(vals) > 1 else (mean, mean)
            return {"mean": mean, "std": std, "sem": float(sem), "ci95": ci95, "n_folds": len(vals)}

        results = {
            "accuracy": summarize(acc),
            "precision_macro": summarize(prec),
            "recall_macro": summarize(rec),
            "f1_macro": summarize(f1),
            "raw": {"accuracy": acc, "precision_macro": prec, "recall_macro": rec, "f1_macro": f1}
        }

        save_dir = './classes/classification/results/optuna'
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'MLP_evaluation.pkl')
        with open(save_path, "wb") as f:
            pickle.dump(results, f)

        print(f"[treinar_e_avaliar_MLP] saved evaluation to {save_path}")
        return results
        
    @staticmethod
    def treinar_e_avaliar_GB(jogos, rotulos, best_params):
        # Avalia via GroupKFold garantindo partidas completas no split
        X, y = ClassificaEstados.ler_amostras(jogos, rotulos, div=False)
        X = np.asarray(X)
        y = np.asarray(y).ravel()
        if X.ndim == 1:
            X = X.reshape(1, -1)

        match_id_col = 1
        match_ids = X[:, match_id_col].astype(int)
        X_feat = np.delete(X, match_id_col, axis=1)

        pipeline = Pipeline([
            ('gb', GradientBoostingClassifier(random_state=42, **best_params))
        ])

        cv = GroupKFold(n_splits=5)

        acc, prec, rec, f1 = [], [], [], []
        for train_idx, test_idx in cv.split(X_feat, y, groups=match_ids):
            X_train, X_test = X_feat[train_idx], X_feat[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]

            pipeline.fit(X_train, y_train)
            preds = pipeline.predict(X_test)

            acc.append(accuracy_score(y_test, preds))
            prec.append(precision_score(y_test, preds, average="macro", zero_division=0))
            rec.append(recall_score(y_test, preds, average="macro", zero_division=0))
            f1.append(f1_score(y_test, preds, average="macro", zero_division=0))

        def summarize(vals):
            vals = np.asarray(vals, dtype=float)
            mean = float(np.mean(vals))
            std = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
            sem = std / np.sqrt(len(vals)) if len(vals) > 0 else 0.0
            ci95 = (mean - 1.96 * sem, mean + 1.96 * sem) if len(vals) > 1 else (mean, mean)
            return {"mean": mean, "std": std, "sem": float(sem), "ci95": ci95, "n_folds": len(vals)}

        results = {
            "accuracy": summarize(acc),
            "precision_macro": summarize(prec),
            "recall_macro": summarize(rec),
            "f1_macro": summarize(f1),
            "raw": {"accuracy": acc, "precision_macro": prec, "recall_macro": rec, "f1_macro": f1}
        }

        save_dir = './classes/classification/results/optuna'
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'GB_evaluation.pkl')
        with open(save_path, "wb") as f:
            pickle.dump(results, f)

        print(f"[treinar_e_avaliar_GB] saved evaluation to {save_path}")
        return results

    @staticmethod
    def treinar_regressao_logistica(jogos, rotulos, nome_modelo, class_weight=None):
        # Avalia via GroupKFold garantindo partidas completas no split
        X, y = ClassificaEstados.ler_amostras(jogos, rotulos, div=False)
        X = np.asarray(X)
        y = np.asarray(y).ravel()
        if X.ndim == 1:
            X = X.reshape(1, -1)

        match_id_col = 1
        match_ids = X[:, match_id_col].astype(int)
        X_feat = np.delete(X, match_id_col, axis=1)

        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('logreg', LogisticRegression(
                max_iter=2000,
                class_weight=class_weight,
                solver='lbfgs',
                multi_class='auto'
            ))
        ])

        cv = GroupKFold(n_splits=5)

        acc, prec, rec, f1 = [], [], [], []
        for train_idx, test_idx in cv.split(X_feat, y, groups=match_ids):
            X_train, X_test = X_feat[train_idx], X_feat[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]

            pipeline.fit(X_train, y_train)
            preds = pipeline.predict(X_test)

            acc.append(accuracy_score(y_test, preds))
            prec.append(precision_score(y_test, preds, average="macro", zero_division=0))
            rec.append(recall_score(y_test, preds, average="macro", zero_division=0))
            f1.append(f1_score(y_test, preds, average="macro", zero_division=0))

        def summarize(vals):
            vals = np.asarray(vals, dtype=float)
            mean = float(np.mean(vals))
            std = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
            sem = std / np.sqrt(len(vals)) if len(vals) > 0 else 0.0
            ci95 = (mean - 1.96 * sem, mean + 1.96 * sem) if len(vals) > 1 else (mean, mean)
            return {"mean": mean, "std": std, "sem": float(sem), "ci95": ci95, "n_folds": len(vals)}

        results = {
            "accuracy": summarize(acc),
            "precision_macro": summarize(prec),
            "recall_macro": summarize(rec),
            "f1_macro": summarize(f1),
            "raw": {"accuracy": acc, "precision_macro": prec, "recall_macro": rec, "f1_macro": f1}
        }

        save_dir = './classes/classification/results/optuna'
        os.makedirs(save_dir, exist_ok=True)
        safe_name = str(nome_modelo).replace("/", "_").replace("\\", "_")
        save_path = os.path.join(save_dir, f'LogReg_evaluation_{safe_name}.pkl')
        with open(save_path, "wb") as f:
            pickle.dump(results, f)

        print(f"[treinar_regressao_logistica] saved evaluation to {save_path}")
        return results
    
