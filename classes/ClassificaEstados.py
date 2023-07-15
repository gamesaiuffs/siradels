# -*- coding: utf-8 -*-
import time
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
from classes.enum.TipoTabelaEstado import TipoTabelaEstado

class ClassificaEstados:    


    @staticmethod
    def inicializar_estados(num_jogadores: int, valor_inicial: int = 0) -> list[np.ndarray]:
        modelo = []
        '''
        # 6 jogadores
        modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Qtd ouro [0,1,2,3,4,5,>=6] = 112
        modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Qtd carta mao [0,1,2,3,4,>=5] = 96
        modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Carta mao mais cara [1 a 6] = 112
        modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Carta mao mais barata [1 a 6] = 112
        modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Qtd distritos construido [0 a 6] = 112
        modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Qtd distrito construido Militar [0,1,2,>=3] = 64
        modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Qtd distrito construido Religioso [0,1,2,>=3] = 64
        modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Qtd distrito construido Nobre [0,1,2,>=3] = 64
        modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Qtd distrito construido especiais [0,1,2,>=3] = 64
        modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Qtd personagens disponiveis [2,3,4,5,6,7] = 128
        modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Pontuacao [0-3,4-7,8-11,12-15,16-19,20-23,>=24] = 112 #
        modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Personagem disponivel para escolha [1,2,3,4,5,6,7,8] = 8176
        modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Personagem visivel descartado [1,2,3,5,6,7,8] = 3088
        #modelo.append(np.ones((num_turnos, num_jogadores*2))*valor_inicial)  # Distancia do rei        
        '''
        """
        MODELO:

        QtdOuro = 0
        QtdCarta = 1
        CartaCara = 2
        CartaBarata = 3
        Construidos = 4
        ConstruidosMilitar = 5
        ConstruidosReligioso = 6
        ConstruidosNobre = 7
        ConstruidosEspecial = 8
        PontuacaoParcial = 9
        QtdPersonagem = 10
        PersonagemDisponivel = 11
        PersonagemDescartado = 12
        Rotulo = 13
        #DistanciaDoRei = 13
        """

        # Array com estado do jogador
        #modelo.append(np.ones(14)*valor_inicial)

        # Matriz com estado dos jogadores
        modelo.append(np.ones(14, num_jogadores)*valor_inicial)
        
        return modelo


    @staticmethod
    def salvar_modelo(modelo: list[np.ndarray], num_turnos):
        for j in zip(modelo):
            np.savetxt('./classes/tabela_estado/' + 'jogo' + str(num_turnos) + '.csv', j, delimiter=',', fmt='%6u')
            #np.savetxt('./tabela/' + j.name + '.csv', i, delimiter=',', fmt='%6u')

    # Carrega o modelo a partir dos arquivos CSV
    @staticmethod
    def ler_modelo() -> list[np.ndarray]:
        modelo = []
        for i in TipoTabelaEstado:
            a = np.genfromtxt('./classes/tabela_estado/' + i.name + '.csv', delimiter=',')
            #a = np.genfromtxt('./tabela/' + i.name + '.csv', delimiter=',')
            modelo.append(a)
        return modelo

    # Inicializa as tabelas e salva os estados parciais do número de partidas
    def simula_estados(self, qtd_partidas: int):

        num_turnos = 0
        qtd_jogadores = 6
        modelo = self.inicializar_estados()
        qtd_simulacao = 0
        while qtd_simulacao < qtd_partidas:
            for qtd_jogadores in range(6, 7):       ## ajustar quantidade de jogadores (original: range(4,7))
                qtd_simulacao += 1
                
                # Inicializa variaveis para nova simulacao do jogo
                historico = self.inicializar_estados()
                estrategias = []
                for i in range(qtd_jogadores):          # fixo em 6 players
                    estrategias.append(EstrategiaTotalmenteAleatoria(str(i+1)))
                # Cria simulacao
                simulacao = Simulacao(estrategias)
                # Executa simulacao
                estado_final = simulacao.rodar_simulacao()
                # Atualizar modelo com vitorias e acoes escolhidas
                for jogador in estado_final.jogadores:

                    if jogador.nome == 'Bot - 1':

                        ##
                        carta_cara = 0
                        carta_barata = 10
                        num_dist_cons = 0
                        nobre = 0
                        religioso = 0
                        militar = 0
                        especial = 0
                        ##
                        
                        # Set de variaveis
                        for carta in enumerate(jogador.cartas_distrito_mao):
                            # Custo da carta mais cara
                            if carta.valor_do_distrito > carta_cara:
                                carta_cara = carta.valor_do_distrito
                            # Custo da carta mais barata
                            if carta.valor_do_distrito < carta_barata:
                                carta_barata = carta.valor_do_distrito
                            # Numero de distritos construidos
                            num_dist_cons += 1

                        for distrito in jogador.distritos_construidos:
                            if distrito.tipo_de_distrito == 2:
                                nobre += 1
                            if distrito.tipo_de_distrito == 0:
                                religioso += 1
                            if distrito.tipo_de_distrito == 1:
                                militar += 1
                            if distrito.tipo_de_distrito == 4:
                                especial += 1

                        # Atribui rotulo

                        if jogador.vencedor:
                            rotulo = "1"
                        else:
                            rotulo = "0"

                        # Coleta estados
                        for array in modelo:
                            array[0] = jogador.ouro
                            array[1] = len(jogador.cartas_distrito_mao)
                            array[2] = carta_cara
                            array[3] = carta_barata
                            array[4] = num_dist_cons
                            array[5] = militar
                            array[6] = religioso
                            array[7] = nobre
                            array[8] = especial
                            array[9] = jogador.pontuacao
                            array[10] = 0
                            array[11] = 0
                            array[12] = 0
                            array[13] = rotulo
                    
                print(modelo)
                num_turnos += 1
                self.salvar_modelo(modelo, num_turnos)

        #self.salvar_modelo(modelo)
        #print(qtd_simulacao)
