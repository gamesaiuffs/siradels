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
from classes.enum.TipoDistrito import TipoDistrito

class ClassificaEstados:    


    @staticmethod
    def inicializar_estados(num_jogadores: int = 6, valor_inicial: int = 0) -> list[np.ndarray]:
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
        modelo = [(np.ones((num_jogadores, 14), dtype=np.ndarray)*valor_inicial)]
        
        return modelo


    @staticmethod
    def salvar_modelo(modelo: list[np.ndarray], num_turnos):
        for j in modelo:
            j = j.astype(np.uint32)
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
        modelo = self.inicializar_estados(6)
        qtd_simulacao = 0
        while qtd_simulacao < qtd_partidas:
            for qtd_jogadores in range(6, 7):       ## ajustar quantidade de jogadores (original: range(4,7))
                qtd_simulacao += 1
                
                # Inicializa variaveis para nova simulacao do jogo
                historico = self.inicializar_estados(6)
                estrategias = []
                for i in range(qtd_jogadores):          # fixo em 6 players
                    estrategias.append(EstrategiaTotalmenteAleatoria(str(i+1)))
                # Cria simulacao
                simulacao = Simulacao(estrategias)
                # Executa simulacao
                estado_final = simulacao.rodar_simulacao()
                i = 1
                # Atualizar modelo com vitorias e acoes escolhidas
                for jogador in estado_final.jogadores:
                    
                    ##
                    carta_cara = 0
                    carta_barata = 10
                    num_dist_cons = 0
                    nobre = 0
                    religioso = 0
                    militar = 0
                    especial = 0
                    ##
                    
                    # Jogador atual

                    if jogador.nome == "Bot - 1":
                    
                    # Set de variaveis

                        for carta in jogador.cartas_distrito_mao:
                            # Custo da carta mais cara
                            if carta.valor_do_distrito > carta_cara:
                                carta_cara = carta.valor_do_distrito
                            # Custo da carta mais barata
                            if carta.valor_do_distrito < carta_barata:
                                carta_barata = carta.valor_do_distrito

                        if jogador.vencedor:
                            venceu = 1
                        else:
                            venceu = 0

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

                        # Coleta estados
                        modelo[0][0, 0] = jogador.ouro
                        modelo[0][0, 1] = len(jogador.cartas_distrito_mao)
                        modelo[0][0, 2] = carta_cara        # Ainda sem importancia
                        modelo[0][0, 3] = carta_barata      # Ainda sem importancia
                        modelo[0][0, 4] = num_dist_cons
                        modelo[0][0, 5] = militar
                        modelo[0][0, 6] = religioso
                        modelo[0][0, 7] = nobre
                        modelo[0][0, 8] = especial
                        modelo[0][0, 9] = jogador.pontuacao
                        modelo[0][0, 10] = 0
                        modelo[0][0, 11] = 0
                        modelo[0][0, 12] = 0
                        modelo[0][0, 13] = venceu
                    
                    # Outros jogadores
                    else:

                        if jogador.vencedor:
                            venceu = 1
                        else:
                            venceu = 0

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

                        modelo[0][i, 0] = jogador.ouro
                        modelo[0][i, 1] = len(jogador.cartas_distrito_mao)
                        modelo[0][i, 2] = 0       # carta_cara (invisivel) inutilizado
                        modelo[0][i, 3] = 0       # carta_barata (invisivel) inutilizado 
                        modelo[0][i, 4] = num_dist_cons           
                        modelo[0][i, 5] = militar
                        modelo[0][i, 6] = religioso
                        modelo[0][i, 7] = nobre
                        modelo[0][i, 8] = especial
                        modelo[0][i, 9] = jogador.pontuacao
                        # Estados intermediarios nao implementados
                        modelo[0][i, 10] = 0              
                        modelo[0][i, 11] = 0
                        modelo[0][i, 12] = 0
                        # Talvez tire
                        modelo[0][i, 13] = venceu
            
                    if i < 5:
                        i += 1

                print(modelo)
                num_turnos += 1
                self.salvar_modelo(modelo, num_turnos)

        #self.salvar_modelo(modelo)
        #print(qtd_simulacao)
