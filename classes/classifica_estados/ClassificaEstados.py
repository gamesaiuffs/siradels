# -*- coding: utf-8 -*-
import numpy as np
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
import joblib

# X = features
# Y = amostras

# Primeira abordagem: Capturar estados individuais finais e visiveis dos jogadores

# Segunda abordagem: Capturar o estado completo com dados privilegiados do jogador atual 
# e dados visiveis dos oponentes, rotulos por estado final de vitoria por pontuacao, metodo proba sklearn

# Duvidas: Arvore de classificacao ou arvore de decisao por regressao?
# Se classificacao: Rotular matrizes inteiras com um array (possivel?) / levar em consid eracao diversas outras variaveis (viavel?) / 
# e utilizar isso em estados intermediarios (novas variaveis: personagens) com o metodo proba de sklearn (eficiente?) 

# Testes: Diferentes profundidades / se regressao diferentes penalidades (media ou quadrado);

# Rotulo de pontuacao para regressao funciona nesse caso? como aplicar?
 

class ClassificaEstados:   
    
    @staticmethod
    def salvar_resultados(X: np.ndarray, Y = list()):
        #j = j.astype(np.uint32)
        
        np.savetxt('./classes/tabela_estado/' + 'Jogos' + '.csv', X, delimiter=',', fmt='%s')   # Features
        #np.savetxt('./tabela_estado/' + j.name + '.csv', i, delimiter=',', fmt='%6u')
        np.savetxt('./classes/tabela_estado/' + 'Rotulos' + '.csv', Y, delimiter=',', fmt='%6u')    # Rotulos
        #np.savetxt('./tabela_estado/' + 'Rotulos' + '.csv', Y, delimiter=',', fmt='%6u')


    @staticmethod
    def ler_resultados() -> list[np.ndarray]:
        jogos = np.genfromtxt('./classes/tabela_estado/' + 'Jogos' + '.csv', delimiter=',')
        #jogos = np.genfromtxt('./tabela_estado/' + i.name + '.csv', delimiter=',')
        rotulos = np.genfromtxt('./classes/tabela_estado/' + 'Rotulos' + '.csv', delimiter=',') 
        #rotulos = np.genfromtxt('./tabela_estado/' + 'Rotulos' + '.csv', delimiter=',') 
        X = jogos
        Y = rotulos
        return X, Y
    

    @staticmethod
    def treinar_modelo(X: np.ndarray, Y: list()):

        # Definir parametros
        modelo = tree.DecisionTreeClassifier(max_depth=5)
        modelo.fit(X, Y)

        # Salva o modelo
        joblib.dump(modelo, "Modelo Teste")

        return modelo
    
    # Mostra informacoes do modelo
    @staticmethod
    def modelo_info():

        modelo = joblib.load("Modelo Teste")

        # Mostra as importancia de cada variavel do estado
        print(modelo.feature_importances_)


    def coleta_estados_treino(estado, rodada_aleatoria, nome, nome_vencedor, coletou):

        if rodada_aleatoria == estado.rodada:
            X = []  

            estado_jogador_atual = []
            estado_outros_jogadores = []
            estado_outro_jogador = []
            estado_tabuleiro = []

            # Set de variaveis gerais
            num_dist_cons = 0
            nobre = 0
            religioso = 0
            militar = 0
            especial = 0

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
                    num_dist_cons += 1

                if jogador.nome == nome:
                    estado_jogador_atual = [jogador.ouro, len(jogador.cartas_distrito_mao), num_dist_cons, militar, religioso, nobre, especial, jogador.personagem.rank]

                else:

                    estado_outro_jogador = [jogador.ouro, len(jogador.cartas_distrito_mao), num_dist_cons, militar, religioso, nobre, especial, jogador.personagem.rank]
                    estado_outros_jogadores.extend(estado_outro_jogador)
                    
                    #Pega estado visivel do jogador com mais pontos
                    '''
                    if jogador.pontuacao > maior_pontuacao:
                        jmp = jogador   #jmp = jogador com mais pontos
                        maior_pontuacao = jogador.pontuacao
                jogador_mais_forte = [jmp.ouro, len(jmp.cartas_distrito_mao), num_dist_cons, militar, religioso, nobre, especial, jmp.personagem.rank]
                    '''

            # Coloca uma nova linha na tabela com o estado visivel do jogador
            estado_tabuleiro = estado_jogador_atual + estado_outros_jogadores
            X = estado_tabuleiro
            #X = np.delete(X, 0, axis=0) # Primeira linha nula
            return X

        else:
            if nome_vencedor != "" and coletou == 1:              
                if nome == nome_vencedor:
                    Y = 1
                else:
                    Y = 0
               # if :      # O jogo ainda esta acontecendo na rodada sorteada
                return Y

    # Utiliza modelo treinado para obter chance de vitoria
    @staticmethod
    def calcula_porcentagem(dados):

        # Carrega modelo
        modelo = joblib.load("Modelo Teste")

        # Estado de teste para calcular probabilidade de vitoria
        #estado_teste = [[0.0,1.0,2.0,0.0,1.0,0.0,0.0,3.0,0.0,4.0,1.0,0.0,1.0,0.0,0.0,2.0,0.0,6.0,1.0,0.0,1.0,0.0,0.0,4.0,6.0,4.0,2.0,0.0,1.0,0.0,0.0,5.0,0.0,7.0,3.0,0.0,1.0,0.0,0.0,8.0,1.0,4.0,4.0,1.0,1.0,0.0,0.0,7.0]]
        
        # Calcula probabilidade de vitoria
        probabilidade_vitoria = modelo.predict_proba(dados)

        #probabilidade_vitoria = f"Probabilidade de vitoria: {probabilidade_vitoria[0] * 100}%"

        probabilidade_vitoria = f"Probabilidade de vitoria: {probabilidade_vitoria[0][1] * 100}%"

        print(probabilidade_vitoria)  # Probabilidade estimada de vitória

        return probabilidade_vitoria 


    @staticmethod
    def classificar_estado(estado, nome):

        estado_jogador_atual = []
        estado_outros_jogadores = []
        estado_outro_jogador = []
        estado_tabuleiro = []
        #maior_pontuacao = 0
        # Coleta os estados finais publicos dos jogadores e individual do alvo
        for jogador in estado.jogadores:
            
            # Set de variaveis gerais
            num_dist_cons = 0
            nobre = 0
            religioso = 0
            militar = 0
            especial = 0

            for distrito in jogador.distritos_construidos:
                if distrito.tipo_de_distrito == TipoDistrito.Nobre:
                    nobre += 1
                if distrito.tipo_de_distrito == TipoDistrito.Religioso:
                    religioso += 1
                if distrito.tipo_de_distrito == TipoDistrito.Militar:
                    militar += 1
                if distrito.tipo_de_distrito == TipoDistrito.Especial:
                    especial += 1
                num_dist_cons += 1
            
            if jogador.nome == nome:

                estado_jogador_atual = [jogador.ouro, len(jogador.cartas_distrito_mao), num_dist_cons, militar, religioso, nobre, especial, jogador.personagem.rank]

            # Pega o estado visivel de todos os outros jogadores
            else:

                estado_outro_jogador = [jogador.ouro, len(jogador.cartas_distrito_mao), num_dist_cons, militar, religioso, nobre, especial, jogador.personagem.rank]
                estado_outros_jogadores.extend(estado_outro_jogador)
                
                #Pega estado visivel do jogador com mais pontos
                '''
                if jogador.pontuacao > maior_pontuacao:
                    jmp = jogador   #jmp = jogador com mais pontos
                    maior_pontuacao = jogador.pontuacao
            jogador_mais_forte = [jmp.ouro, len(jmp.cartas_distrito_mao), num_dist_cons, militar, religioso, nobre, especial, jmp.personagem.rank]
                '''

        # Coloca uma nova linha na tabela com o estado visivel do jogador
        estado_tabuleiro = estado_jogador_atual + estado_outros_jogadores

        ClassificaEstados.calcula_porcentagem([estado_tabuleiro])
