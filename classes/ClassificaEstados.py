# -*- coding: utf-8 -*-
import numpy as np
from classes.Simulacao import Simulacao
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
# Se classificacao: Rotular matrizes inteiras com um array (possivel?) / levar em consideracao diversas outras variaveis (viavel?) / 
# e utilizar isso em estados intermediarios (novas variaveis: personagens) com o metodo proba de sklearn (eficiente?) 

# Testes: Diferentes profundidades / se regressao diferentes penalidades (media ou quadrado);

# Rotulo de pontuacao para regressao funciona nesse caso? como aplicar?
 

class ClassificaEstados:   

    @staticmethod
    def treina_modelo(X: np.ndarray, Y: list()):

        modelo = tree.DecisionTreeClassifier(max_depth=5)
        modelo.fit(X, Y)

        print(modelo.feature_importances_)

        joblib.dump(modelo, "Modelo Teste")

        return modelo

    # Utiliza modelo treinado para obter chance de vitoria
    @staticmethod
    def calcula_porcentagem(dados):

        modelo = joblib.load("Modelo Teste")

        estado_teste = [[ 2,  4,  0,  0,  0,  0,  0, 0],[ 19,  10,  5,  1,  1,  1,  2, 0],[ 1,  2,  4,  3,  1,  0,  0, 0],[ 2,  2,  3,  1,  0,  1,  1, 0],[ 0,  2,  2,  0,  1,  0,  0,  0],[ 0,  1,  2,  0,  0,  0,  1,  0]]
        probabilidade_vitoria = modelo.predict_proba(estado_teste)
        print(probabilidade_vitoria)  # Probabilidade estimada de vitória

        # Mostra dados extras

        return probabilidade_vitoria 

    @staticmethod
    def salvar_modelo(X: np.ndarray, Y = list()):
        #j = j.astype(np.uint32)
        np.savetxt('./classes/tabela_estado/' + 'Jogos' + '.csv', X, delimiter=',', fmt='%6u')
        #np.savetxt('./tabela/' + j.name + '.csv', i, delimiter=',', fmt='%6u')
        np.savetxt('./classes/tabela_estado/' + 'Rotulos' + '.csv', Y, delimiter=',', fmt='%6u')

    # Inicializa as tabelas e salva os estados parciais do número de partidas
    def coleta_estados_finais_publicos(self, qtd_partidas: int):

        qtd_jogadores = 6
        X = [np.empty(8)]
        Y = list()
        qtd_simulacao = 0
        while qtd_simulacao < qtd_partidas:
            for qtd_jogadores in range(6, 7):       ## ajustar quantidade de jogadores (original: range(4,7))
                qtd_simulacao += 1
                
                # Inicializa variaveis para nova simulacao do jogo
                estrategias = []
                
                for i in range(qtd_jogadores):          # fixo em 6 players
                    estrategias.append(EstrategiaTotalmenteAleatoria(str(i+1)))
                
                # Estrategias fixas e especificas
                '''
                estrategias.append(EstrategiaDjonatan())
                estrategias.append(EstrategiaAndrei())
                estrategias.append(EstrategiaBernardo())
                estrategias.append(EstrategiaFelipe())
                estrategias.append(EstrategiaGustavo())
                estrategias.append(EstrategiaJoao())
                '''
                # Cria simulacao
                simulacao = Simulacao(estrategias)
                # Executa simulacao
                estado_final = simulacao.rodar_simulacao()
                i = 1
                # Atualizar modelo com vitorias e acoes escolhidas
                for jogador in estado_final.jogadores:
                    
                    # Set de variaveis gerais
                    num_dist_cons = 0
                    nobre = 0
                    religioso = 0
                    militar = 0
                    especial = 0
                    
                    if jogador.vencedor:
                        Y.append(1)
                    else:
                        Y.append(0)

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
                    # Fim do set
                     
                    # Coloca uma nova linha na tabela com o estado visivel do jogador
                    nova_linha = np.array([jogador.ouro, len(jogador.cartas_distrito_mao), num_dist_cons, militar, religioso, nobre, especial, 0])
                    X = np.vstack((X, nova_linha))

        #np.set_printoptions(suppress=True)
        # Formata tabela (inteiros, deleta a primeira linha nula)
        X = X.astype(int)
        X = np.delete(X, 0, axis=0)
        #print(X)
        #print()
        #print(Y)

        #self.salvar_modelo(X, Y)    
        self.treina_modelo(X, Y)
        self.calcula_porcentagem(0)

