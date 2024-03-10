# -*- coding: utf-8 -*-
from more_itertools import sort_together
import numpy as np
import csv
from classes.strategies.EstrategiaBernardo import EstrategiaBernardo
from classes.strategies.EstrategiaDjonatan import EstrategiaDjonatan
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaGustavo import EstrategiaGustavo
from classes.strategies.EstrategiaJoao import EstrategiaJoao
from classes.strategies.EstrategiaAndrei import EstrategiaAndrei
from classes.strategies.EstrategiaMCTS import EstrategiaMCTS
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.enum.TipoDistrito import TipoDistrito
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, make_scorer
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import joblib

class ClassificaEstados:   
    
    # Salva resultados das amostras
    @staticmethod
    def salvar_resultados(X: np.ndarray, Y: list(), jogos: str, rotulos: str):
        #j = j.astype(np.uint32)
        
        np.savetxt('./classes/classification/samples/' + jogos + '.csv', X, delimiter=',', fmt='%s')   # Features
        #np.savetxt('./tabela_estado/' + j.name + '.csv', i, delimiter=',', fmt='%6u')
        np.savetxt('./classes/classification/samples/' + rotulos + '.csv', Y, delimiter=',', fmt='%6u')    # Rotulos
        #np.savetxt('./tabela_estado/' + 'Rotulos' + '.csv', Y, delimiter=',', fmt='%6u')
        # Caminho do arquivo CSV
        '''
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
    def ler_resultados(jogos: str, rotulos: str) -> list[np.ndarray]:
        X = np.genfromtxt('./classes/classification/samples/' + jogos + '.csv', delimiter=',')
        #jogos = np.genfromtxt('./tabela_estado/' + i.name + '.csv', delimiter=',')
        Y = np.genfromtxt('./classes/classification/samples/' + rotulos + '.csv', delimiter=',') 
        #rotulos = np.genfromtxt('./tabela_estado/' + 'Rotulos' + '.csv', delimiter=',') 
        #X = jogos
        #Y = rotulos

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)

        return X_train, X_test, Y_train, Y_test
    
    # Treina o modelo
    @staticmethod
    def treinar_modelo(jogos: str, rotulos: str, nome: str, criterion: str, profundidade : int = 1):

        X_train, X_test, Y_train, Y_test = ClassificaEstados.ler_resultados(jogos, rotulos)

        # Definir parametros
        modelo = tree.DecisionTreeClassifier(criterion=criterion, max_depth=profundidade)
        modelo.fit(X_train, Y_train)

        # Salva o modelo
        joblib.dump(modelo, f'./classes/classification/models/{nome}')

        print("Modelo treinado com sucesso!")

        return 
    
    # Equilibra as amostras em relação as features
    @staticmethod
    def undersampling(jogos_in: str, rotulos_in: str, jogos_out: str, rotulos_out: str):

        idx_remover = []
        X_train, X_test, Y_train, Y_test = ClassificaEstados.ler_resultados(jogos_in, rotulos_in)
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

        ClassificaEstados.salvar_resultados(X, Y, jogos_out, rotulos_out)
   
        return
        
    # Mostra informacoes do modelo
    @staticmethod
    def modelo_info(jogos: str, rotulos: str, model: str):

        modelo = joblib.load(f'./classes/classification/models/{model}')

        # [jogador.ouro, len(jogador.cartas_distrito_mao), num_dist_cons, jogador.personagem.rank]
        
        nomes_das_caracteristicas = [
        "Ouro (JA)", "Cartas na Mão (JA)", "Distritos Construídos (JA)", "Custo Construidos (JA)", "Custo Mão (JA)", "Rank do Personagem(JA)",
        "Ouro (JMP)", "Cartas na Mão (JMP)", "Distritos Construídos (JMP)", "Custo Construidos (JA)", "Rank do Personagem (JMP)",
]
        tree_rules = export_text(modelo, feature_names= nomes_das_caracteristicas)
        # Mostra a estrutura da árvore de decisão no terminal
        print("Estrutura final da árvore: ")
        print(tree_rules)
        # Mostra as importancia de cada variavel do estado
        print("Feature importances: ")
        print(modelo.feature_importances_)
        # Mostra a profundidade da árvore
        print()
        print(f"Modelo Analisado: {model}")
        print("Profundidade: ", modelo.get_depth())
        # Mostra o número de nós
        print("Número de Nós: ", modelo.tree_.node_count)
        # Mostra o número de folhas
        print("Número de Folhas: ", modelo.get_n_leaves())

        # TESTES DO MODELO

        X_train, X_test, Y_train, Y_test = ClassificaEstados.ler_resultados(jogos, rotulos)

        # Y_pred: Rótulos que o modelo previu para os testes
        # Y_test: Rótulos reais dos testes
        Y_pred = modelo.predict(X_test)

        macrof1 = f1_score(Y_pred, Y_test, average='macro')*100
        # Accuracy tem mesmo valor que F1_score: Micro        
        accuracy = accuracy_score(Y_pred, Y_test)*100
        matriz_confusao = confusion_matrix(Y_pred, Y_test)
        #disp = ConfusionMatrixDisplay(confusion_matrix=matriz_confusao, display_labels=nomes_das_caracteristicas)

        TP = matriz_confusao[0, 0]
        FP = matriz_confusao[0, 1]
        FN = matriz_confusao[1, 0]
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)

        print(f"Accuracy: {round(accuracy, 2)}%")
        print(f"F1 Score - Macro: {round(macrof1, 2)}%")
        print(f"Precisão: {round(precision, 2)*100}%")
        print(f"Recall: {round(recall, 2)*100}%")
        print("Matriz de confusão: ")
        print(matriz_confusao)

        # Mostra a curva de aprendizado
        #ClassificaEstados.plot_learning_curve(X_train, Y_train, modelo)

        # Mostra a estrutura visual da árvore
        #ClassificaEstados.plot_tree(model, nomes_das_caracteristicas)

        return

    # Plota árvore
    @staticmethod
    def plot_tree(model_name, f_names):

        modelo = joblib.load(f'./classes/classification/models/{model_name}')

        plt.figure(figsize=(10, 5))
        plot_tree(modelo, feature_names=f_names, class_names=["Lose", "Win"], filled=True)
        plt.show()   
        return

    # Plota curva de aprendizado
    @staticmethod
    def plot_learning_curve(jogos: str, rotulos: str, model_name: str):

        model = joblib.load(f'./classes/classification/models/{model_name}')

        X_train, X_test, Y_train, Y_test = ClassificaEstados.ler_resultados(jogos, rotulos)

        f1_macro_scorer = make_scorer(f1_score, average='macro')

        train_sizes, train_scores, test_scores = learning_curve(model, X_train, Y_train, cv=5, scoring=f1_macro_scorer, n_jobs=-1)

        # Calculando as médias e desvios padrão das pontuações
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)

        # Plotando a curva de aprendizado
        plt.figure(figsize=(10, 7))
        plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1, color="blue")
        plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.1, color="orange")
        plt.plot(train_sizes, train_scores_mean, 'o-', color="blue", label="Score de Treinamento")
        plt.plot(train_sizes, test_scores_mean, 'o-', color="orange", label="Score de Teste")
        plt.title("Curva de Aprendizado da Árvore de Decisão")
        plt.xlabel("Tamanho do Conjunto de Treinamento")
        plt.ylabel("F1 Score Macro")
        plt.legend(loc="best")
        plt.show()
        
        return

    @staticmethod
    def coleta_features(estado, nome_observado, coleta, X, model_name):
        estado_jogador_atual, estado_outro_jogador = [], []
        tipos_distrito = []
        num_dist_cons_JA, num_dist_cons_JMP = 0, 0
        ja_custo_mao, ja_custo_construido, jmp_custo_construido = 0, 0, 0

        # Ordena por pontuação parcial crescente
        ordem = [jogador.pontuacao for jogador in estado.jogadores]
        estado.jogadores = sort_together([ordem, estado.jogadores])[1]

        # Verifica se o jogador observado é o com maior pontuação (para não duplicar)
        i = 4 if estado.jogadores[4].nome != nome_observado else 3

        # JMP (jogador com maior pontuação)
        jmp = estado.jogadores[i]
        
        # JA (jogador atual)
        for jogador in estado.jogadores:
            if jogador.nome == nome_observado:
               ja = jogador 
        
        '''
        #contador de tipos de distritos
        for jogador in estado.jogadores:
            for distrito in jogador.distritos_construidos:
                if distrito.tipo_de_distrito == TipoDistrito.Nobre:
                    nobre += 1
                if distrito.tipo_de_distrito == TipoDistrito.Religioso:
                    religioso += 1
                if distrito.tipo_de_distrito == TipoDistrito.Militar:
                    militar += 1
                if distrito.tipo_de_distrito == TipoDistrito.Especial:
                    especial += 1
        '''
            
        # Média do custo de distritos construídos
        for distrito in ja.distritos_construidos:
            ja_custo_construido += distrito.valor_do_distrito
        for distrito in jmp.distritos_construidos:
            jmp_custo_construido += distrito.valor_do_distrito
        
        # Média do custo de distritos na mão
        for distrito in ja.cartas_distrito_mao:
            ja_custo_mao += distrito.valor_do_distrito

        # Features selecionados
        # [pontuação, ouro, n_dist_mao, n_dist_const, custo_medio_const, custo_medio_mao, rank_person]
        #
        # OBS: vetores JA e JMP são assimétricos 
        # Nº total de features atual: 11 
        #
        # Ideias de Features:
        # Custo médio da mão, Custo médio dos distritos construídos, contador unico de tipos, ranking do personagem
        

        estado_jogador_atual = [ja.ouro, len(ja.cartas_distrito_mao), len(ja.distritos_construidos), ja_custo_construido, ja_custo_mao, ja.personagem.rank]
        estado_outro_jogador = [jmp.ouro, len(jmp.cartas_distrito_mao), len(jmp.distritos_construidos), jmp_custo_construido, jmp.personagem.rank]

        # concatena os vetores
        x_coleta = estado_jogador_atual + estado_outro_jogador
        
        #print("Jogador escolhido: ", nome_observado)
        #print("Pontuação parcial dele: ", ja.pontuacao)
        #print("Jogador mais forte da rodada: " + jmp.nome)
        #print("Pontuação parcial dele: ", jmp.pontuacao)

        if coleta == 1:
            X = np.vstack((X, x_coleta))
            return X
        else:
            return ClassificaEstados.calcula_porcentagem(x_coleta, model_name)

    # Utiliza modelo treinado para obter chance de vitoria
    @staticmethod
    def calcula_porcentagem(data, model_name: str):
        # Carrega modelo
        model = joblib.load(model_name)
        data_vec = [data]

        # Calcula probabilidade de vitória
        win_probability = model.predict_proba(data_vec)
        win_probability = f"Probabilidade de vitoria: {win_probability[0][1] * 100}%"

        print(win_probability)  # Probabilidade estimada de vitória

        return 