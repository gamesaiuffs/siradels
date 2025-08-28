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

        # Podem ser adicionadas mais informações
        # https://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html

        info_dict = {
            "Feature Importances": feat_imp
        }

        for chave, valor in info_dict.items():
            if isinstance(valor, np.ndarray):
                info_dict[chave] = valor.tolist()

        return info_dict
    
    # Plota árvore
    @staticmethod
    def plot_tree(model_name: str, nomes_caracteristicas):

        modelo = joblib.load(f'./classes/classification/models/{model_name}')

        tree_rules = export_text(modelo, feature_names=nomes_caracteristicas)
        # Mostra a estrutura da árvore de decisão no terminal
        print("Estrutura final da árvore: ")
        print(tree_rules)

        plt.figure(figsize=(10, 5))
        plot_tree(modelo, feature_names=nomes_caracteristicas, class_names=["Lose", "Win"], filled=True)
        plt.show()   
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

        # Extrai dados
        x = [t.number for t in study.trials if t.value is not None]
        y = [t.value for t in study.trials if t.value is not None]

        # Plota
        plt.figure(figsize=(10, 5))
        plt.plot(x, y, marker='o', linestyle='-', color='blue', label='Score por trial')
        plt.title("Evolução do Score por Trial")
        plt.xlabel("Trial #")
        plt.ylabel(f"{metric} Score")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"./classes/classification/results/study/trials/{metric}_trial.png")
        #plt.show()
    
    @staticmethod
    def plot_importances(importances: dict, model_name: str):
        
        #filtered = {k: v for k, v in importances.items() if v > 0.01}
        filtered = {k: v for k, v in importances.items()}

        # Ordena por importância decrescente
        sorted_importances = dict(sorted(filtered.items(), key=lambda x: x[1], reverse=True))
        print(sorted_importances)
        # Plot
        plt.figure(figsize=(10, 5))
        plt.barh(list(sorted_importances.keys()), list(sorted_importances.values()))
        plt.xlabel("Importance")
        plt.title(f"{model_name} Feature importances > 0.01")
        plt.gca().invert_yaxis()
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
        plt.title("Accuracy of Models Across Game Progress Phases")
        plt.xlabel("Game Progress Phase")
        plt.ylabel("Accuracy")
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
        plt.title("F1 Score of Models Across Game Progress Phases")
        plt.xlabel("Game Progress Phase")
        plt.ylabel("F1 Score")
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
        plt.title("Precision of Models Across Game Progress Phases")
        plt.xlabel("Game Progress Phase")
        plt.ylabel("Precision")
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
        plt.title("Recall of Models Across Game Progress Phases")
        plt.xlabel("Game Progress Phase")
        plt.ylabel("Recall")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig("./classes/classification/results/performance_tests/recall_across_phases.png")
        plt.close()     
        return