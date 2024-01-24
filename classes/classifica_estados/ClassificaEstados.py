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
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import joblib

# X = features
# Y = rotulos

# Primeira abordagem: Capturar estados individuais finais e visiveis dos jogadores

# Segunda abordagem: Capturar o estado completo com dados privilegiados do jogador atual 
# e dados visiveis dos oponentes, rotulos por estado final de vitoria por pontuacao, metodo proba sklearn

# Duvidas: Arvore de classificacao ou arvore de decisao por regressao?
# Se classificacao: Rotular matrizes inteiras com um array (possivel?) / levar em consid eracao diversas outras variaveis (viavel?) / 
# e utilizar isso em estados intermediarios (novas variaveis: personagens) com o metodo proba de sklearn (eficiente?) 

# Testes: Diferentes profundidades / se regressao diferentes penalidades (media ou quadrado);

# Rotulo de pontuacao para regressao funciona nesse caso? como aplicar?
 

# Eficiência do primeiro modelo funcional:
# F1_Score: 63.11% (Macro), 82.12% (Micro)
# Acccuracy: 82.12%

class ClassificaEstados:   
    
    @staticmethod
    def salvar_resultados(X: np.ndarray, Y = list()):
        #j = j.astype(np.uint32)
        
        np.savetxt('./classes/tabela_estado/' + 'Jogos 2' + '.csv', X, delimiter=',', fmt='%s')   # Features
        #np.savetxt('./tabela_estado/' + j.name + '.csv', i, delimiter=',', fmt='%6u')
        np.savetxt('./classes/tabela_estado/' + 'Rotulos 2' + '.csv', Y, delimiter=',', fmt='%6u')    # Rotulos
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

    @staticmethod
    def ler_resultados() -> list[np.ndarray]:
        X = np.genfromtxt('./classes/tabela_estado/' + 'Jogos 2' + '.csv', delimiter=',')
        #jogos = np.genfromtxt('./tabela_estado/' + i.name + '.csv', delimiter=',')
        Y = np.genfromtxt('./classes/tabela_estado/' + 'Rotulos 2' + '.csv', delimiter=',') 
        #rotulos = np.genfromtxt('./tabela_estado/' + 'Rotulos' + '.csv', delimiter=',') 
        #X = jogos
        #Y = rotulos
        return X, Y
    

    @staticmethod
    def treinar_modelo(X_train: np.ndarray, Y_train: list(), nome, profundidade : int = 1):

        # Definir parametros
        modelo = tree.DecisionTreeClassifier(max_depth=profundidade)
        modelo.fit(X_train, Y_train)

        # Salva o modelo
        joblib.dump(modelo, nome)

        return
    
    @staticmethod
    def testar_modelo(X_test: np.ndarray, Y_test: list()):
        
        # Carrega modelo
        modelo = joblib.load("Modelo Teste 2")
        
        Y_pred = modelo.predict(X_test)

        microf1 = f1_score(Y_pred, Y_test, average='micro')*100
        microf1 = round(microf1, 2)

        macrof1 = f1_score(Y_pred, Y_test, average='macro')*100
        macrof1 = round(macrof1, 2)
        
        accuracy = accuracy_score(Y_pred, Y_test)*100
        accuracy = round(accuracy, 2)

        print(f"Accuracy: {accuracy}%")
        print(f"F1 Score - Micro: {microf1}%")
        print(f"F1 Score - Macro: {macrof1}%")
        return 
        
    # Mostra informacoes do modelo
    @staticmethod
    def modelo_info():

        modelo = joblib.load("Modelo Teste 2")

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
        print("Profundidade: ", modelo.get_depth())
        # Mostra o número de nós
        print("Número de Nós: ", modelo.tree_.node_count)
        # Mostra o número de folhas
        print("Número de Folhas: ", modelo.get_n_leaves())
        # Mostra a precisão atual do modelo
        X, Y = ClassificaEstados.ler_resultados()
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
        ClassificaEstados.testar_modelo(X_test, Y_test)
    
        # Mostra a estrutura visual da �rvore
        plt.figure(figsize=(24, 18))
        plot_tree(modelo, class_names=["Derrota", "Vitória"], filled=True)
        plt.show()    

    def coleta_features(estado, nome_observado, coleta, X):
        estado_jogador_atual, estado_outro_jogador, estado_outros_jogadores, estado_tabuleiro = [], [], [], []
        nobre, religioso, militar, comercial, especial = 0, 0, 0, 0, 0
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
        # Nº total de features: 
        #
        # Ideias de Features:
        # Custo médio da mão, Custo médio dos distritos construídos, contador unico de tipos, ranking do personagem
        

        estado_jogador_atual = [ja.ouro, len(ja.cartas_distrito_mao), len(ja.distritos_construidos), ja_custo_construido, ja_custo_mao, ja.personagem.rank]
        estado_outro_jogador = [jmp.ouro, len(jmp.cartas_distrito_mao), len(jmp.distritos_construidos), jmp_custo_construido, jmp.personagem.rank]
        

        #estado_outros_jogadores.extend(estado_outro_jogador) # Caso coloque todos os jogadores

        # Coloca uma nova linha na tabela com o estado visivel do jogador
        x_coleta = estado_jogador_atual + estado_outro_jogador
        
        X = np.vstack((X, x_coleta))
        
        #print("Jogador escolhido: ", nome_observado)
        #print("Pontuação parcial dele: ", ja.pontuacao)
        #print("Jogador mais forte da rodada: " + jmp.nome)
        #print("Pontuação parcial dele: ", jmp.pontuacao)
        

        if coleta == 1:
            return X
        else:
            return ClassificaEstados.calcula_porcentagem(X)
        
    @staticmethod
    def coleta_rotulos_treino(nome_observado, nome_vencedor):
        if nome_vencedor != "":              
            Y = 1 if nome_observado == nome_vencedor else 0
            return Y

    # Utiliza modelo treinado para obter chance de vitoria
    @staticmethod
    def calcula_porcentagem(dados):

        # Carrega modelo
        modelo = joblib.load("Modelo Teste 2")

        # Calcula probabilidade de vitoria
        probabilidade_vitoria = modelo.predict_proba(dados)

        #probabilidade_vitoria = f"Probabilidade de vitoria: {probabilidade_vitoria[0] * 100}%"

        probabilidade_vitoria = f"Probabilidade de vitoria: {probabilidade_vitoria[0][1] * 100}%"

        print(probabilidade_vitoria)  # Probabilidade estimada de vit�ria

        return probabilidade_vitoria 