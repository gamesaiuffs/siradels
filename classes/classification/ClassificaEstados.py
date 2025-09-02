# -*- coding: utf-8 -*-
import ast
import glob
import shap
import os
import pickle
import traceback
from more_itertools import sort_together
import numpy as np
import json
import optuna
import pandas as pd
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

class ClassificaEstados:   

    @staticmethod
    def coleta_features(jogadores, rodada, nome_observado, coleta, X, model_name):
        # Inicializa vetores
        estado_jogador_atual, estado_outro_jogador, ja_tipos_mao_v, ja_tipos_board_v, jmp_tipos_board_v =  [], [], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]                                             
        # Conta tipos de distritos na mão e construídos
        ja_custo_mao, ja_custo_construido, jmp_custo_construido = 0, 0, 0 
        ja_tipos_mao, jmp_tipos_board, ja_tipos_board = 0, 0, 0
        ja_especiais_mao, ja_especiais_board, jmp_especiais_board = 0, 0, 0
        # Conta custos de distritos da mão do JA, separando em baixo valor e alto valor (Não aumenta muito a complexidade e espaço e ainda da os valores)
        ja_custo123_mao, ja_custo456_mao, ja_custo123_board = 0, 0, 0 
        ja_custo456_board, jmp_custo123_board, jmp_custo456_board = 0, 0, 0

        # Ordena por pontuação parcial crescente
        ordem = [jogador.pontuacao for jogador in jogadores]
        jogadores = sort_together([ordem, jogadores])[1]

        # Verifica se o jogador observado é o com maior pontuação (para não duplicar)
        i = 4 if jogadores[4].nome != nome_observado else 3

        # JMP (jogador com maior pontuação)
        jmp = jogadores[i]
        
        # JA (jogador atual)
        for jogador in jogadores:
            if jogador.nome == nome_observado:
               ja = jogador 
        
        # Coleta tipos variados em vetores booleanos
        for jogador in jogadores:
            # Jogador atual (JA)
            if jogador.nome == nome_observado:
                # Itera sob seus distritos (mão e contruídos)
                for distrito in jogador.cartas_distrito_mao:
                    if distrito.tipo_de_distrito == TipoDistrito.Nobre:
                        ja_tipos_mao_v[0] = 1
                    if distrito.tipo_de_distrito == TipoDistrito.Religioso:
                        ja_tipos_mao_v[1] = 1
                    if distrito.tipo_de_distrito == TipoDistrito.Militar:
                        ja_tipos_mao_v[2] = 1
                    if distrito.tipo_de_distrito == TipoDistrito.Comercial:
                        ja_tipos_mao_v[3] = 1
                    if distrito.tipo_de_distrito == TipoDistrito.Especial:
                        ja_tipos_mao_v[4] = 1
                        ja_especiais_mao += 1

                for distrito in jogador.distritos_construidos:
                    if distrito.tipo_de_distrito == TipoDistrito.Nobre:
                        ja_tipos_board_v[0] = 1
                    if distrito.tipo_de_distrito == TipoDistrito.Religioso:
                        ja_tipos_board_v[1] = 1
                    if distrito.tipo_de_distrito == TipoDistrito.Militar:
                        ja_tipos_board_v[2] = 1
                    if distrito.tipo_de_distrito == TipoDistrito.Comercial:
                        ja_tipos_board_v[3] = 1 
                    if distrito.tipo_de_distrito == TipoDistrito.Especial:
                        ja_tipos_board_v[4] = 1
                        ja_especiais_board += 1

            # Jogador com mais pontos (JMP)
            elif jogador.nome == jmp.nome:
                # Itera sob seus distritos (mão e contruídos)
                for distrito in jogador.distritos_construidos:
                    if distrito.tipo_de_distrito == TipoDistrito.Nobre:
                        jmp_tipos_board_v[0] = 1
                    if distrito.tipo_de_distrito == TipoDistrito.Religioso:
                        jmp_tipos_board_v[1] = 1
                    if distrito.tipo_de_distrito == TipoDistrito.Militar:
                        jmp_tipos_board_v[2] = 1
                    if distrito.tipo_de_distrito == TipoDistrito.Comercial:
                        jmp_tipos_board_v[3] = 1
                    if distrito.tipo_de_distrito == TipoDistrito.Especial:
                        jmp_tipos_board_v[4] = 1
                        jmp_especiais_board += 1

        # Computa vetores booleanos
        for i in jmp_tipos_board_v:
            if ja_tipos_mao_v[i] == 1:
                ja_tipos_mao += 1
        for i in jmp_tipos_board_v:
            if jmp_tipos_board_v[i] == 1:
                ja_tipos_board += 1
        for i in jmp_tipos_board_v:
            if jmp_tipos_board_v[i] == 1:
                jmp_tipos_board += 1

        # Custo total de distritos construídos
        for distrito in ja.distritos_construidos:

            # Separa em baixo e alto custo
            if distrito.valor_do_distrito <= 3:
                ja_custo123_board += 1 
            else:
                ja_custo456_board += 1

            # Contabiliza o total para média
            ja_custo_construido += distrito.valor_do_distrito

        # Total do custo de distritos na mão
        for distrito in ja.cartas_distrito_mao:
             # Separa em baixo e alto custo           
            if distrito.valor_do_distrito <= 3:
                ja_custo123_mao += 1 
            else:
                ja_custo456_mao += 1

            # Contabiliza o total para média
            ja_custo_mao += distrito.valor_do_distrito

        for distrito in jmp.distritos_construidos:

            # Separa em baixo e alto custo
            if distrito.valor_do_distrito <= 3:
                jmp_custo123_board += 1 
            else:
                jmp_custo456_board += 1

            # Contabiliza o total para média
            jmp_custo_construido += distrito.valor_do_distrito
        

        # Média dos valores (diminui range de valores)
        try:
            ja_custo_mao = round(ja_custo_mao / len(ja.cartas_distrito_mao), 2) 
        except:
            ja_custo_mao = 0
        try:
            ja_custo_construido = round(ja_custo_construido / len(ja.distritos_construidos), 2) 
        except:
            ja_custo_construido = 0
        try:
            jmp_custo_construido = round(jmp_custo_construido / len(jmp.distritos_construidos), 2)
        except:
            jmp_custo_construido = 0

        num_max_dist_const = 0
        for jogador in jogadores:
            if len(jogador.distritos_construidos) > 0:
                num_max_dist_const = len(jogador.distritos_construidos)

        #print(ja.nome, jmp.nome, ja_custo_mao, ja.distritos_construidos)

        # OBS: vetores JA e JMP são assimétricos 
        # Nº total de features atual: 30
        
        # Cria o vetor dos dois jogadores
        estado_tabuleiro = [rodada, num_max_dist_const, jogadores[4].pontuacao, jogadores[3].pontuacao, jogadores[2].pontuacao, jogadores[1].pontuacao, jogadores[0].pontuacao]
        estado_jogador_atual = [ja.ouro, len(ja.cartas_distrito_mao), len(ja.distritos_construidos), ja_custo_construido, ja_custo_mao, ja_tipos_board, ja_tipos_mao, ja_custo123_board, ja_custo456_board, ja_custo123_mao, ja_custo456_mao, ja_especiais_mao, ja_especiais_board, ja.personagem.rank]
        estado_outro_jogador = [jmp.ouro, len(jmp.cartas_distrito_mao), len(jmp.distritos_construidos), jmp_custo_construido, jmp_tipos_board, jmp_custo123_board, jmp_custo456_board, jmp_especiais_board, jmp.personagem.rank]

        # Concatena os vetores em um vetor estado de amostra
        x_coleta = estado_tabuleiro + estado_jogador_atual + estado_outro_jogador
        
        #print("Jogador escolhido: ", nome_observado)
        #print("Pontuação parcial dele: ", ja.pontuacao)
        #print("Jogador mais forte da rodada: " + jmp.nome)
        #print("Pontuação parcial dele: ", jmp.pontuacao)

        # Retorna o vetor se está coletando, se não, manda para avaliação 
        if coleta == 1:
            X = np.vstack((X, x_coleta))
            return X
        else:
            return ClassificaEstados.calcula_porcentagem(x_coleta, model_name, nome_observado)

    @staticmethod
    def coleta_rotulos_treino(nome_observado, nome_vencedor):
        if nome_vencedor != "":              
            Y = 1 if nome_observado == nome_vencedor else 0
            return Y
    
    # Salva resultados das amostras
    @staticmethod
    def salvar_amostras(X: np.ndarray, Y: list, jogos: str, rotulos: str):
        #j = j.astype(np.uint32)
        
        np.savetxt('./classes/classification/samples/' + jogos + '.csv', X, delimiter=',', fmt='%s')   # Features
        #np.savetxt('./tabela_estado/' + j.name + '.csv', i, delimiter=',', fmt='%6u')
        np.savetxt('./classes/classification/samples/' + rotulos + '.csv', Y, delimiter=',', fmt='%6u')    # Rotulos
        #np.savetxt('./tabela_estado/' + 'Rotulos' + '.csv', Y, delimiter=',', fmt='%6u')
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
        X = np.genfromtxt('./classes/classification/samples/' + jogos + '.csv', delimiter=',')
        #jogos = np.genfromtxt('./tabela_estado/' + i.name + '.csv', delimiter=',')
        Y = np.genfromtxt('./classes/classification/samples/' + rotulos + '.csv', delimiter=',') 
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
    
    # Equilibra as amostras em relação as features
    @staticmethod
    def undersampling(jogos_in: str, rotulos_in: str, jogos_out: str, rotulos_out: str, fim_jogo: bool = False):

        idx_remover = []
        X, Y = ClassificaEstados.ler_amostras(jogos_in, rotulos_in, False)
        
        if fim_jogo == False:
            wins = np.sum(Y == 1)
            loses = np.sum(Y == 0)
            print("Wins: ", wins)
            print("Loses: ", loses)

            for indice, linha in enumerate(reversed(Y)):
                if linha == 0 and loses > wins:
                    idx_remover.append(len(Y) - 1 - indice)
                    loses = loses - 1
                    print("Iterações restantes: ", loses-wins)

            X = np.delete(X, idx_remover, axis=0)
            Y = np.delete(Y, idx_remover, axis=0)

            wins = np.sum(Y == 1)
            loses = np.sum(Y == 0)
            print("Wins: ", wins)
            print("Loses: ", loses)

        else:
            for indice, linha in enumerate(reversed(X)):
                if linha[0] < 15:
                    idx_remover.append(len(Y) - 1 - indice)

            X = np.delete(X, idx_remover, axis=0)
            Y = np.delete(Y, idx_remover, axis=0)

        ClassificaEstados.salvar_amostras(X, Y, jogos_out, rotulos_out)
   
        return

    #------------------------------------------------- FIM MANIPULAÇÃO DE AMOSTRAS ------------------------------------------------------------#
    
    # Treina o modelo
    @staticmethod
    def treinar_modelo(circuito: bool, jogos: str, rotulos: str, nome: str, criterion: str, min_samples: int,  peso_vitoria, profundidade):

        if circuito != True:
            X_train, X_test, Y_train, Y_test = ClassificaEstados.ler_amostras(jogos, rotulos, True)
        else:
            X_train = jogos
            Y_train = rotulos

        # Definir parametros
        modelo = DecisionTreeClassifier(criterion=criterion, max_depth=profundidade, min_samples_leaf=min_samples, class_weight=peso_vitoria)
        modelo.fit(X_train, Y_train)

        # Salva o modelo
        joblib.dump(modelo, f'./classes/classification/models/{nome}')

        if circuito == False:
            print("Modelo treinado com sucesso!")

        return 
    
    # Treina floresta
    @staticmethod
    def treinar_floresta(circuito: bool, jogos: str, rotulos: str, nome: str, n_arvores: int, criterio: str, min_samples: int,  peso_vitoria, profundidade):

        if circuito != True:
            X_train, X_test, Y_train, Y_test = ClassificaEstados.ler_amostras(jogos, rotulos, True)
        else:
            X_train = jogos
            Y_train = rotulos

        # Definir parametros
        modelo = RandomForestClassifier(n_estimators=n_arvores, criterion=criterio, max_depth=profundidade, min_samples_leaf=min_samples, class_weight=peso_vitoria, random_state=42)
        modelo.fit(X_train, Y_train)

        # Salva o modelo
        joblib.dump(modelo, f'./classes/classification/models/{nome}')

        if circuito == False:
            print("Modelo treinado com sucesso!")

        return 
    
    # Treina gradient boosting
    @staticmethod
    def treinar_gradiente(circuito: bool, jogos: str, rotulos: str, nome: str, n_arvores: int, criterio: str, min_samples: int, log_opt, rate, profundidade):

        if circuito != True:
            X_train, X_test, Y_train, Y_test = ClassificaEstados.ler_amostras(jogos, rotulos, True)
        else:
            X_train = jogos
            Y_train = rotulos

        # Definir parametros
        modelo = GradientBoostingClassifier(n_estimators=n_arvores, loss=log_opt, learning_rate=rate, criterion=criterio, min_samples_leaf=min_samples, max_depth=profundidade, random_state=42)
        modelo.fit(X_train, Y_train)

        # Salva o modelo
        joblib.dump(modelo, f'./classes/classification/models/{nome}')

        if circuito == False:
            print("Modelo treinado com sucesso!")

        return 
    
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
    
    # Testa modelo
    @staticmethod
    def testa_modelos(models_paths, pasta_csv):
        arquivos_X = sorted(glob.glob(f'{pasta_csv}/X_*.csv'))
        arquivos_Y = sorted(glob.glob(f'{pasta_csv}/Y_*.csv'))

        for arq_X, arq_Y in zip(arquivos_X, arquivos_Y):
            X = pd.read_csv(arq_X).values
            Y = pd.read_csv(arq_Y).values.ravel()

            fase = arq_X.split('/')[-1].replace('X_', '').replace('.csv', '')

            print(f'\n== Avaliando fase {fase} ==')

            for path in models_paths:
                model = joblib.load(path)
                nome = path.split('/')[-1]

                y_pred = model.predict(X)

                acc = accuracy_score(Y, y_pred)
                prec = precision_score(Y, y_pred, zero_division=0)
                rec = recall_score(Y, y_pred, zero_division=0)
                f1 = f1_score(Y, y_pred, zero_division=0)

                print(f'{nome}: Acc={acc:.4f} Prec={prec:.4f} Rec={rec:.4f} F1={f1:.4f}')

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

    # Implementar o grid search e ciclar amostras e validação cruzada
    @staticmethod
    def circuito_treino_teste(jogos: str, rotulos: str, n_features: int):   # Substituído pelas funções de GridSearchCV

        criterion_range = ["gini", "log_loss", "entropy"]
        min_samples_range = 501
        class_weight_range = {0: 1, 1: 5}


        X_train, X_test, Y_train, Y_test = ClassificaEstados.ler_amostras(jogos, rotulos, True)
        for criterio in criterion_range:
            criterion = criterio
            # min_samples (501, 1, -50)
            while min_samples_range != 1:
                min_samples_range = min_samples_range - 50
                class_weight_range[1] = 5
                # Itera pelos pesos da vitória (5, 0, -1) <- (De 5 até 0 diminuindo 1 por vez)
                while class_weight_range[1] != 1:
                    win_weight = class_weight_range[1]
                    class_weight_range[1] = class_weight_range[1] - 1

                    # Treina o modelo com os parâmetros iterados
                    nome_modelo = f"{criterion} {min_samples_range}ms {win_weight}mw {n_features}f"
                    ClassificaEstados.treinar_modelo(True, X_train, Y_train, nome_modelo, criterion, min_samples_range, class_weight_range, None)
                    # Profundidade None por enquanto

                    dados_dict = ClassificaEstados.testar_modelo(X_test, Y_test, nome_modelo, True)
                    # Talvez desacoplar o teste do treino

                    # Salva testes realizados
                    ClassificaEstados.salva_testes(dados_dict, "./classes/classification/results/testes modelos")

                # Repete bloco para class_weight = "balanced"
                nome_modelo = f"{criterion} {min_samples_range}ms balanced {n_features}f"
                ClassificaEstados.treinar_modelo(True, X_train, Y_train, nome_modelo, criterion,  min_samples_range, "balanced", None)
                dados_dict = ClassificaEstados.testar_modelo(X_test, Y_test, nome_modelo, True)
                ClassificaEstados.salva_testes(dados_dict, "./classes/classification/results/testes modelos")
        ClassificaEstados.avalia_testes()
        return
    
    # Salva testes
    @staticmethod
    def salva_testes(dados_dict: dict, arquivo: str):
        try:
            with open(f"{arquivo}.json", "r", encoding="utf-8") as json_file:
                dados_json = json.load(json_file)
        except FileNotFoundError:
            dados_json = []

        dados_json.append(dados_dict)

        with open(f"{arquivo}.json", "w", encoding="utf-8") as json_file:
            json.dump(dados_json, json_file, indent=4)
        return

    # Avalia testes
    @staticmethod
    def avalia_testes(feature_names):

        melhor_f1 = float("-inf")
        melhor_precision = float("-inf")
        melhor_recall = float("-inf")

        with open('./classes/classification/results/testes modelos.json', 'r', encoding="utf-8") as arquivo_json:
            dados = json.load(arquivo_json) 

        # Pega melhores pontuações
        for modelo in dados:

            if modelo["F1 Macro"] > melhor_f1:
                melhor_f1 = modelo["F1 Macro"]
                nome_f1 = modelo["Name"]
            if modelo["Win Precision"] > melhor_precision:
                melhor_precision = modelo["Win Precision"]
                nome_precision = modelo["Name"]
            if modelo["Win Recall"] > melhor_recall:
                melhor_recall = modelo["Win Recall"]
                nome_recall = modelo["Name"]

        # Pega melhores modelos por pontuação
        for modelo in dados:

            if modelo["Name"] == nome_f1:

                f1_model_info = ClassificaEstados.modelo_info(modelo["Name"], feature_names)
                modelo_f1 = {
                    "Tested Model": modelo,
                    "Adictional Information": f1_model_info
                }

            if modelo["Name"] == nome_precision:

                precision_model_info = ClassificaEstados.modelo_info(modelo["Name"], feature_names)
                modelo_precision = {
                    "Tested Model": modelo,
                    "Adictional Information": precision_model_info
                }

            if modelo["Name"] == nome_recall:

                recall_model_info = ClassificaEstados.modelo_info(modelo["Name"], feature_names)
                modelo_recall = {
                    "Tested Model": modelo,
                    "Adictional Information": recall_model_info
                }

        # Dicionário aninhado grau 3
        melhores_modelos = {
            "Top F1": modelo_f1,
            "Top Precision": modelo_precision,
            "Top Recall": modelo_recall
        }

        ClassificaEstados.salva_testes(melhores_modelos, "./classes/classification/results/best results/top modelos")

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

        resultados_optuna = {}

        # Scorers
        scorers = {
            'F1': make_scorer(f1_score),
            'Precision': make_scorer(precision_score),
            'Accuracy': make_scorer(accuracy_score)
        }

        # Pipeline
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

        for metric_name, scorer in scorers.items():
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

            joblib.dump(study, f'./classes/classification/models/MLP Best {metric_name}')

        ClassificaEstados.salva_testes(resultados_optuna, './classes/classification/results/MLP/mlp')

        return
    
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
        resultados_optuna = {}

        scorers = {
            'Accuracy': make_scorer(accuracy_score),
            'Precision': make_scorer(precision_score),
            'F1 Score': make_scorer(f1_score)
        }

        save_path = './classes/classification/models/CART'
        os.makedirs(save_path, exist_ok=True)

        for metric_name, scorer in scorers.items():
            base_pipeline = Pipeline([
                ('cart', DecisionTreeClassifier(random_state=42))
            ])

            param_space = {
                'max_depth': (2, 50),
                'min_samples_leaf': (2, 500),
                'min_samples_split': (2, 500),
                'class_weight': ['{0: 1, 1: 5}', '{0: 1, 1: 4}', '{0: 1, 1: 3}', '{0: 1, 1: 2}', '{0: 1, 1: 1}'],
                'criterion': ['gini', 'entropy', 'log_loss']
            }

            def objective(trial):
                max_depth = None if trial.suggest_categorical("use_none_max_depth", [True, False]) \
                    else int(trial.suggest_float('max_depth', *param_space['max_depth']))

                params = {
                    'max_depth': max_depth,
                    'criterion': trial.suggest_categorical('criterion', param_space['criterion']),
                    'min_samples_leaf': int(trial.suggest_float('min_samples_leaf', *param_space['min_samples_leaf'])),
                    'min_samples_split': int(trial.suggest_float('min_samples_split', *param_space['min_samples_split'])),
                    'class_weight': ast.literal_eval(trial.suggest_categorical('class_weight', param_space['class_weight']))
                }

                pipeline = clone(base_pipeline)
                pipeline.set_params(cart__max_depth=params['max_depth'],
                                    cart__criterion=params['criterion'],
                                    cart__min_samples_leaf=params['min_samples_leaf'],
                                    cart__min_samples_split=params['min_samples_split'],
                                    cart__class_weight=params['class_weight'])

                return cross_val_score(pipeline, jogos, rotulos, cv=5, scoring=scorer, n_jobs=-1).mean()

            study = optuna.create_study(direction='maximize')
            study.optimize(objective, n_trials=10000, n_jobs=1, callbacks=[ClassificaEstados.early_stopping_callback(patience=100)])

            best_score = study.best_value
            best_trials = [t for t in study.trials if t.value == best_score]

            print(f"Metric: {metric_name}, Best Score: {best_score:.4f}, Trials: {len(best_trials)}")

            for i, trial in enumerate(best_trials):
                params = trial.params
                max_depth = None if params.get("use_none_max_depth") else int(params['max_depth'])

                pipeline = clone(base_pipeline)
                pipeline.set_params(cart__max_depth=max_depth,
                                    cart__criterion=params['criterion'],
                                    cart__min_samples_leaf=int(params['min_samples_leaf']),
                                    cart__min_samples_split=int(params['min_samples_split']),
                                    cart__class_weight=ast.literal_eval(params['class_weight']))
                pipeline.fit(jogos, rotulos)

                joblib.dump(pipeline, os.path.join(save_path, f'CART_{metric_name.replace(" ", "_")}_BestModel_{i}.joblib'))

            joblib.dump(study, os.path.join(save_path, f'CART_Best_{metric_name.replace(" ", "_")}.pkl'))

            resultados_optuna[metric_name] = {
                "best_score": best_score,
                "n_models_saved": len(best_trials)
            }
            
        return
    
    @staticmethod
    def optuna_RF(jogos, rotulos):
        resultados_optuna = {}

        scorers = {
            'Accuracy': make_scorer(accuracy_score),
            'Precision': make_scorer(precision_score),
            'F1 Score': make_scorer(f1_score)
        }
        param_space = {
            'n_estimators': (50, 1000),
            'max_depth': (2, 50),
            'min_samples_leaf': (2, 500),
            'min_samples_split': (2, 500),
            'criterion': ['gini', 'entropy', 'log_loss'],
            'class_weight': ['{0: 1, 1: 5}', '{0: 1, 1: 4}', '{0: 1, 1: 3}', '{0: 1, 1: 2}', '{0: 1, 1: 1}']
        }

        save_path = './classes/classification/models/RF'
        os.makedirs(save_path, exist_ok=True)

        for metric_name, scorer in scorers.items():
            base_pipeline = Pipeline([
                ('rf', RandomForestClassifier(random_state=42))
            ])

            def objective(trial):
                max_depth = None if trial.suggest_categorical("use_none_max_depth", [True, False]) \
                    else int(trial.suggest_float('max_depth', *param_space['max_depth']))

                params = {
                    'n_estimators': int(trial.suggest_float('n_estimators', *param_space['n_estimators'])),
                    'criterion': trial.suggest_categorical('criterion', param_space['criterion']),
                    'max_depth': max_depth,
                    'min_samples_leaf': int(trial.suggest_float('min_samples_leaf', *param_space['min_samples_leaf'])),
                    'min_samples_split': int(trial.suggest_float('min_samples_split', *param_space['min_samples_split'])),
                    'class_weight': ast.literal_eval(trial.suggest_categorical('class_weight', param_space['class_weight']))
                }

                pipeline = clone(base_pipeline)
                pipeline.set_params(rf__n_estimators=params['n_estimators'],
                                    rf__criterion=params['criterion'],
                                    rf__max_depth=params['max_depth'],
                                    rf__min_samples_leaf=params['min_samples_leaf'],
                                    rf__min_samples_split=params['min_samples_split'],
                                    rf__class_weight=params['class_weight'])

                return cross_val_score(pipeline, jogos, rotulos, cv=5, scoring=scorer, n_jobs=-1).mean()

            study = optuna.create_study(direction='maximize')
            study.optimize(objective, n_trials=10000, n_jobs=1, callbacks=[ClassificaEstados.early_stopping_callback(patience=100)])

            best_score = study.best_value
            best_trials = [t for t in study.trials if t.value == best_score]

            print(f"Metric: {metric_name}, Best Score: {best_score:.4f}, Trials: {len(best_trials)}")

            for i, trial in enumerate(best_trials):
                params = trial.params
                max_depth = None if params.get("use_none_max_depth") else int(params['max_depth'])

                pipeline = clone(base_pipeline)
                pipeline.set_params(rf__n_estimators=int(params['n_estimators']),
                                    rf__criterion=params['criterion'],
                                    rf__max_depth=max_depth,
                                    rf__min_samples_leaf=int(params['min_samples_leaf']),
                                    rf__min_samples_split=int(params['min_samples_split']),
                                    rf__class_weight=ast.literal_eval(params['class_weight']))
                pipeline.fit(jogos, rotulos)

                joblib.dump(pipeline, os.path.join(save_path, f'RF_{metric_name.replace(" ", "_")}_BestModel_{i}.joblib'))

            joblib.dump(study, os.path.join(save_path, f'RF_Best_{metric_name.replace(" ", "_")}.pkl'))

            resultados_optuna[metric_name] = {
                "best_score": best_score,
                "n_models_saved": len(best_trials)
            }

        return

    @staticmethod
    def carregar_melhores_parametros(caminho_study):
        study = joblib.load(caminho_study)
        best_params = study.best_params
        return best_params

    @staticmethod
    def treinar_e_avaliar_MLP(jogos, rotulos, best_params):
        # monta o pipeline com os melhores hiperparâmetros
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('mlp', MLPClassifier(max_iter=500, random_state=42, **best_params))
        ])

        # métricas
        scorers = {
            'accuracy': make_scorer(accuracy_score),
            'precision': make_scorer(precision_score),
            'recall': make_scorer(recall_score),
            'f1_score': make_scorer(f1_score)
        }

        resultados = {}
        for nome, scorer in scorers.items():
            scores = cross_val_score(pipeline, jogos, rotulos, cv=5, scoring=scorer, n_jobs=-1)
            resultados[nome] = np.mean(scores)

        return resultados
        
    @staticmethod
    def treinar_e_avaliar_GB(jogos, rotulos, best_params):
        pipeline = Pipeline([
            ('gb', GradientBoostingClassifier(random_state=42, **best_params))
        ])

        scorers = {
            'accuracy': make_scorer(accuracy_score),
            'precision': make_scorer(precision_score),
            'recall': make_scorer(recall_score),
            'f1_score': make_scorer(f1_score)
        }

        resultados = {}
        for nome, scorer in scorers.items():
            scores = cross_val_score(pipeline, jogos, rotulos, cv=5, scoring=scorer, n_jobs=-1)
            resultados[nome] = np.mean(scores)

        return resultados
    
