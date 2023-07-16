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
from classes.enum.TipoDistrito import TipoDistrito

class ClassificaEstados:    


    @staticmethod
    def inicializar_estados(num_jogadores: int = 6, valor_inicial: int = 0) -> list[np.ndarray]:
        
        """
        MODELO (índices das linhas):
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

        # Matriz com estado dos jogadores
        modelo = [(np.ones((num_jogadores, 14), dtype=np.ndarray)*valor_inicial)]
        
        return modelo


    @staticmethod
    def salvar_modelo(modelo: list[np.ndarray], num_turnos):
        for j in modelo:
            j = j.astype(np.uint32)
            np.savetxt('./classes/tabela_estado/' + 'jogo' + str(num_turnos) + '.csv', j, delimiter=',', fmt='%6u')
            #np.savetxt('./tabela/' + j.name + '.csv', i, delimiter=',', fmt='%6u')

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
                    
                    ##
                    carta_cara = 0
                    carta_barata = 10
                    num_dist_cons = 0
                    nobre = 0
                    religioso = 0
                    militar = 0
                    especial = 0
                    
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
                    ##
                    
                    # Jogador atual
                    print(jogador.nome)
                    if jogador.nome == "Bot - 1":
                    
                    # Set de variaveis

                        for carta in jogador.cartas_distrito_mao:
                            # Custo da carta mais cara
                            if carta.valor_do_distrito > carta_cara:
                                carta_cara = carta.valor_do_distrito
                            # Custo da carta mais barata
                            if carta.valor_do_distrito < carta_barata:
                                carta_barata = carta.valor_do_distrito

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

                        # Resolvido: linha da tabela nula 
                        i -= 1

                    # Outros jogadores
                    else:

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

                    # Controla a entrada de jogadores (linhas) na tabela
                    if i < 5:
                        i += 1

                print(modelo)
                num_turnos += 1
                self.salvar_modelo(modelo, num_turnos)

        #self.salvar_modelo(modelo)
        #print(qtd_simulacao)
