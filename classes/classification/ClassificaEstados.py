# -*- coding: utf-8 -*-
from more_itertools import sort_together
import numpy as np
import json
from classes.strategies.EstrategiaBernardo import EstrategiaBernardo
from classes.strategies.EstrategiaDjonatan import EstrategiaDjonatan
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaGustavo import EstrategiaGustavo
from classes.strategies.EstrategiaJoao import EstrategiaJoao
from classes.strategies.EstrategiaAndrei import EstrategiaAndrei
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.enum.TipoDistrito import TipoDistrito
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, make_scorer, accuracy_score, confusion_matrix, log_loss, ConfusionMatrixDisplay
from sklearn.model_selection import learning_curve
from sklearn.model_selection import StratifiedGroupKFold
import matplotlib.pyplot as plt
import joblib

class ClassificaEstados:   

    @staticmethod
    def coleta_features(jogadores, nome_observado, coleta, X, model_name):
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


        #print(ja.nome, jmp.nome, ja_custo_mao, ja.distritos_construidos)

        # OBS: vetores JA e JMP são assimétricos 
        # Nº total de features atual: 23 
        
        # Cria o vetor dos dois jogadores
        estado_tabuleiro = [jogadores[4].pontuacao, jogadores[3].pontuacao, jogadores[2].pontuacao, jogadores[1].pontuacao, jogadores[0].pontuacao]
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
            return ClassificaEstados.calcula_porcentagem(x_coleta, model_name)

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
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
            return X_train, X_test, Y_train, Y_test
        else:
            return X, Y
       
    @staticmethod
    def cross_validation(X, y):
        sgkf = StratifiedGroupKFold(n_splits=3)

        # Faça a divisão dos dados
        for train_index, test_index in sgkf.split(X, y, groups):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            groups_train, groups_test = groups[train_index], groups[test_index]
   
        groups = np.array([1, 1, 2, 2, 3]) 
        f1_macro_scorer = make_scorer(f1_score, average='macro')
        scores = cross_val_score(estimator=f1_macro_scorer)

        return X_test, y_test 
    
    # Equilibra as amostras em relação as features
    @staticmethod
    def undersampling(jogos_in: str, rotulos_in: str, jogos_out: str, rotulos_out: str):

        idx_remover = []
        X_train, X_test, Y_train, Y_test = ClassificaEstados.ler_amostras(jogos_in, rotulos_in)
        X = np.concatenate((X_train, X_test), axis=0)
        Y = np.concatenate((Y_train, Y_test), axis=0)
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

        ClassificaEstados.salvar_amostras(X, Y, jogos_out, rotulos_out)
   
        return

    #------------------------------------------------- FIM MANIPULAÇÃO DE AMOSTRAS ------------------------------------------------------------#
    
    # Treina o modelo
    @staticmethod
    def treinar_modelo(circuito: bool, jogos: str, rotulos: str, nome: str, criterion: str, min_samples: int,  peso_vitoria, profundidade):

        if circuito != True:
            X_train, X_test, Y_train, Y_test = ClassificaEstados.ler_amostras(jogos, rotulos)
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
    
    # Testa modelo
    @staticmethod
    def testar_modelo(jogos: str, rotulos: str, model: str, circuito: bool):

        modelo = joblib.load(f'./classes/classification/models/{model}')
        if circuito != True:
            X_train, X_test, Y_train, Y_test = ClassificaEstados.ler_amostras(jogos, rotulos)
        else:
            X_test = jogos
            Y_test = rotulos

        # Y_pred: Rótulos que o modelo previu para os testes
        # Y_test: Rótulos reais dos testes
        Y_pred = modelo.predict(X_test)

        macrof1 = round(f1_score(y_true=Y_test, y_pred=Y_pred, average='macro'), 2)
        # Accuracy tem mesmo valor que F1_score: Micro        
        accuracy = round(accuracy_score(y_true=Y_test, y_pred=Y_pred), 2)
        #matriz_confusao = confusion_matrix(y_true=Y_test, y_pred=Y_pred )
        #matriz_confusao.tolist() if isinstance(matriz_confusao, np.ndarray) else matriz_confusao    
        precisionv = round(precision_score(y_true=Y_test, y_pred=Y_pred, zero_division=0), 2)
        recallv = round(recall_score(y_true=Y_test, y_pred=Y_pred, zero_division=0), 2)
        precisionm = round(precision_score(y_true=Y_test, y_pred=Y_pred, average='macro', zero_division=0), 2)
        recallm = round(recall_score(y_true=Y_test, y_pred=Y_pred, average='macro', zero_division=0) , 2)
        auc = round(roc_auc_score(y_true=Y_test, y_score=Y_pred), 2)

        '''
        print(f"Nome do modelo: {modelo}")
        print(f"Precisão Geral: {round(precisionm, 2)}%")
        print(f"Recall Geral: {round(recallm, 2)}%")
        print("Matriz de confusão: ")
        print(matriz_confusao)
        '''

        model_test_info = {
            "Name": model,
            "F1 Macro": macrof1,
            "Win Precision": precisionv,
            "Win Recall": recallv,
            "Accuracy": accuracy,
            "AUC": auc,
            "Macro Precision": precisionm,
            "Macro Recall": recallm
        }

        return model_test_info

    @staticmethod
    def circuito_treino_teste(jogos: str, rotulos: str, n_features: int):

        # Quantidade de modelos treinados atual: 40 
        # Adicionar profundidade e/ou outros recursos

        X_train, X_test, Y_train, Y_test = ClassificaEstados.ler_amostras(jogos, rotulos)

        criterion_range = ["gini", "log_loss"]
        criterion = "log_loss"
        min_samples_range = 501
        class_weight_range = {0: 1, 1: 5}

        # min_samples (500, 0, -25)
        while min_samples_range != 1:
            min_samples_range = min_samples_range - 50
            class_weight_range[1] = 5
            # Itera pelos pesos da vitória (5, 0, -1) <- (De 5 até 0 diminuindo 1 por vez)
            while class_weight_range[1] != 1:
                win_weight = class_weight_range[1]
                class_weight_range[1] = class_weight_range[1] - 1

                # Treina o modelo com os parâmetros iterados
                nome_modelo = f"{criterion} {min_samples_range}ms {win_weight}mw {n_features}f"
                ClassificaEstados.treinar_modelo(True, X_train, Y_train, nome_modelo, criterion,  min_samples_range, class_weight_range, None)
                # Profundidade None por enquanto

                dados_dict = ClassificaEstados.testar_modelo(X_test, Y_test, nome_modelo, True)
                # Talvez desacoplar o teste do treino

                # Salva testes realizados
                ClassificaEstados.salva_testes(dados_dict, "./classes/classification/results/testes modelos")

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

    # Avalia testes
    @staticmethod
    def avalia_testes():
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

                f1_model_info = ClassificaEstados.modelo_info(modelo["Name"])
                modelo_f1 = {
                    "Tested Model": modelo,
                    "Adictional Information": f1_model_info
                }

            if modelo["Name"] == nome_precision:

                precision_model_info = ClassificaEstados.modelo_info(modelo["Name"])
                modelo_precision = {
                    "Tested Model": modelo,
                    "Adictional Information": precision_model_info
                }

            if modelo["Name"] == nome_recall:

                recall_model_info = ClassificaEstados.modelo_info(modelo["Name"])
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
    def modelo_info(model: str):

        modelo = joblib.load(f'./classes/classification/models/{model}')
            
        # Mostra as importancia de cada variavel do estado
        feat_imp = modelo.feature_importances_
        profundidade = modelo.get_depth()
        n_nos = modelo.tree_.node_count
        n_folhas = modelo.get_n_leaves()
        n_folhas = int(n_folhas)
        
        # Podem ser adicionadas mais informações
        # https://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html

        info_dict = {
            "Features Importances": feat_imp,
            "Depth": profundidade,
            "Node Number": n_nos,
            "Leaves Number": n_folhas
        }

        for chave, valor in info_dict.items():
            if isinstance(valor, np.ndarray):
                info_dict[chave] = valor.tolist()

        return info_dict
    
    # Plota árvore
    @staticmethod
    def plot_tree(model_name: str):

        modelo = joblib.load(f'./classes/classification/models/{model_name}')

        nomes_das_caracteristicas = [

        # Board features
        "Score P1", "Score P2", "Score P3", "Score P4", "Score P5",

        # AP features
        "Gold Amount (AP)", "Number of cards in Hand (AP)", "Number of Builded Districts (AP)", "Cost of citadel (AP)", "Cost of Hand (AP)", "Builded District Types (AP)", "District Types in Hand (AP)", "Low Cost District in Hand (AP)", "High Cost District in Hand (AP)", "Special District in Hand (AP)", "Special District Builded (AP)", "Character Rank (AP)",

        # MVP features
        "Gold Amount (MVP)", "Number of Cards in Hand (MVP)", "Number of Builded Districts (MVP)", "Cost of citadel (MVP)", "Builded District Types (MVP)", "District Types in Hand (MVP)", "Low Cost District in Hand (MVP)", "High Cost District in Hand (MVP)", "Special District in Hand (MVP)", "Special District Builded (MVP)", "Character Rank (MVP)",

]
        tree_rules = export_text(modelo, feature_names= nomes_das_caracteristicas)
        # Mostra a estrutura da árvore de decisão no terminal
        print("Estrutura final da árvore: ")
        print(tree_rules)

        plt.figure(figsize=(10, 5))
        plot_tree(modelo, feature_names=nomes_das_caracteristicas, class_names=["Lose", "Win"], filled=True)
        plt.show()   
        return

    # Plota curva de aprendizado
    @staticmethod
    def plot_learning_curve(jogos: str, rotulos: str, model_name: str):

        model = joblib.load(f'./classes/classification/models/{model_name}')

        X, Y = ClassificaEstados.ler_amostras(jogos, rotulos, False)

        f1_macro_scorer = make_scorer(f1_score, average='macro')

        train_sizes_f1, train_scores_f1, test_scores_f1 = learning_curve(model, X, Y, cv=5, scoring=f1_macro_scorer, n_jobs=-1)
        train_sizes_p, train_scores_p, test_scores_p = learning_curve(model, X, Y, cv=5, scoring=precision_score, n_jobs=-1)
        train_sizes_r, train_scores_r, test_scores_r = learning_curve(model, X, Y, cv=5, scoring=recall_score, n_jobs=-1)
        

        ''' Faz sentido tirar a media dos Folds, quando eles são os pontos de referência?
        # Calculando as médias e desvios padrão das pontuações
        train_scores_mean = np.mean(train_scores_f1, axis=1)
        train_scores_std = np.std(train_scores_f1, axis=1)
        test_scores_mean = np.mean(test_scores_f1, axis=1)
        test_scores_std = np.std(test_scores_f1, axis=1)

        # Plotando a curva de aprendizado
        plt.figure(figsize=(10, 7))
        plt.fill_between(train_sizes_f1, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1, color="blue")
        plt.fill_between(train_sizes_f1, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.1, color="orange")
        #plt.plot(train_sizes, precision_scores, 'o-', color="green", label="Precisão")
        #plt.plot(train_sizes, recall_scores, 'o-', color="red", label="Recall")
        '''

        plt.plot(train_sizes_f1, train_scores_f1, 'o-', color="orange", label="F1 Train")
        plt.plot(train_sizes_f1, test_scores_f1, 'o-', color="blue", label="F1 Test")
        plt.plot(train_sizes_f1, test_scores_p, 'o-', color="red", label="Precision Test")
        plt.plot(train_sizes_f1, test_scores_r, 'o-', color="yellow", label="Recall Test")

        plt.title("Curva de Aprendizado da Árvore de Decisão")
        plt.xlabel("Tamanho do Conjunto de Treinamento")
        plt.ylabel("Scores")
        plt.legend(loc="best")
        plt.show()
        
        return

    # Utiliza modelo treinado para obter chance de vitoria
    @staticmethod
    def calcula_porcentagem(data, model_name: str):
        # Carrega modelo
        model = joblib.load(model_name)
        data_vec = [data]

        # Calcula probabilidade de vitória
        win_probability = model.predict_proba(data_vec)
        win_probability = f"Probabilidade estimada de vitoria: {win_probability[0][1] * 100}%"

        print(win_probability)  # Probabilidade estimada de vitória

        return 