from more_itertools import sort_together
import numpy as np

from classes.classification.ClassificaEstados import ClassificaEstados
from classes.enum.TipoDistrito import TipoDistrito

class ColetaFeatures:
    _proximo_id_partida = 1
    _id_partida_atual = 0
    _contagem_personagens_por_jogador = {}
    _contagem_morto_por_jogador = {}
    _contagem_roubado_por_jogador = {}
    _ordem_turno_por_jogador = {}

    @staticmethod
    def iniciar_partida(jogadores):
        ColetaFeatures._id_partida_atual = ColetaFeatures._proximo_id_partida
        ColetaFeatures._proximo_id_partida += 1

        ColetaFeatures._contagem_personagens_por_jogador = {
            id(jogador): {rank: 0 for rank in range(1, 9)} for jogador in jogadores
        }
        ColetaFeatures._contagem_morto_por_jogador = {id(jogador): 0 for jogador in jogadores}
        ColetaFeatures._contagem_roubado_por_jogador = {id(jogador): 0 for jogador in jogadores}
        ColetaFeatures._ordem_turno_por_jogador = {id(jogador): 0 for jogador in jogadores}

    @staticmethod
    def atualizar_ordem_turno(jogadores_em_ordem_turno):
        # A ordem recebida vem da rodada atual após ordenar pelo coroado.
        for idx, jogador in enumerate(jogadores_em_ordem_turno, start=1):
            ColetaFeatures._ordem_turno_por_jogador[id(jogador)] = idx

    @staticmethod
    def atualizar_contagem_personagens(jogadores):
        for jogador in jogadores:
            rank = jogador.personagem.rank
            jogador_id = id(jogador)
            if jogador_id not in ColetaFeatures._contagem_personagens_por_jogador:
                ColetaFeatures._contagem_personagens_por_jogador[jogador_id] = {r: 0 for r in range(1, 9)}
            if rank in ColetaFeatures._contagem_personagens_por_jogador[jogador_id]:
                ColetaFeatures._contagem_personagens_por_jogador[jogador_id][rank] += 1

    @staticmethod
    def registrar_morto(jogador):
        jogador_id = id(jogador)
        if jogador_id not in ColetaFeatures._contagem_morto_por_jogador:
            ColetaFeatures._contagem_morto_por_jogador[jogador_id] = 0
        ColetaFeatures._contagem_morto_por_jogador[jogador_id] += 1

    @staticmethod
    def registrar_roubado(jogador):
        jogador_id = id(jogador)
        if jogador_id not in ColetaFeatures._contagem_roubado_por_jogador:
            ColetaFeatures._contagem_roubado_por_jogador[jogador_id] = 0
        ColetaFeatures._contagem_roubado_por_jogador[jogador_id] += 1
    
    @staticmethod
    def coleta_features_antigo(jogadores, rodada, nome_observado, coleta, X, model_name):
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
    def coleta_features(jogadores, rodada, X):

        features_jogador, estado_jogadores = [], []

        ordem_turno_fixa = [ColetaFeatures._ordem_turno_por_jogador.get(id(jogador), 0) for jogador in jogadores]
        estado_tabuleiro = [ColetaFeatures._id_partida_atual, rodada] + ordem_turno_fixa

        # fazer o track dos players, os jogadores tem que estar ordenados
        for jogador in jogadores:
            custo_cidade = sum(distrito.valor_do_distrito for distrito in jogador.distritos_construidos)

            features_jogador = [
                jogador.ouro,                                                           # qtd ouro
                1 if jogador.ouro == max([player.ouro for player in jogadores]) else 0, # flag maior ouro
                len(jogador.cartas_distrito_mao),                                       # numero de cartas na mao
                1 if len(jogador.cartas_distrito_mao) == max([len(player.cartas_distrito_mao) for player in jogadores], default=0) else 0, # flag mais cartas
                len(jogador.distritos_construidos),                             # numero de distritos construidos
                1 if len(jogador.distritos_construidos) == max([len(player.distritos_construidos) for player in jogadores], default=0) else 0, # flag mais distritos construidos
                jogador.distritos_construidos.count(TipoDistrito.Militar),      # numero de distritos militar construidos
                jogador.distritos_construidos.count(TipoDistrito.Religioso),    # numero de distritos religioso construidos
                jogador.distritos_construidos.count(TipoDistrito.Comercial),    # numero de distritos comercial construidos
                jogador.distritos_construidos.count(TipoDistrito.Nobre),        # numero de distritos nobre construidos
                jogador.distritos_construidos.count(TipoDistrito.Especial),     # numero de distritos especiais construidos
                max([distrito.valor_do_distrito for distrito in jogador.distritos_construidos], default=0),  # custo distrito mais caro
                min([distrito.valor_do_distrito for distrito in jogador.distritos_construidos], default=0),  # custo distrito mais barato
                custo_cidade / len(jogador.distritos_construidos) if len(jogador.distritos_construidos) != 0 else 1, # custo medio distritos construidos
                custo_cidade, # custo total da cidade
                1 if custo_cidade == max(sum(d.valor_do_distrito for d in player.distritos_construidos) for player in jogadores) else 0,  # flag maior valor de cidade
                ColetaFeatures._contagem_morto_por_jogador.get(id(jogador), 0), # vezes morto
                ColetaFeatures._contagem_roubado_por_jogador.get(id(jogador), 0), # vezes roubado
                ColetaFeatures._contagem_personagens_por_jogador.get(id(jogador), {}).get(1, 0), # personagem rank 1
                ColetaFeatures._contagem_personagens_por_jogador.get(id(jogador), {}).get(2, 0), # personagem rank 2
                ColetaFeatures._contagem_personagens_por_jogador.get(id(jogador), {}).get(3, 0), # personagem rank 3
                ColetaFeatures._contagem_personagens_por_jogador.get(id(jogador), {}).get(4, 0), # personagem rank 4
                ColetaFeatures._contagem_personagens_por_jogador.get(id(jogador), {}).get(5, 0), # personagem rank 5
                ColetaFeatures._contagem_personagens_por_jogador.get(id(jogador), {}).get(6, 0), # personagem rank 6
                ColetaFeatures._contagem_personagens_por_jogador.get(id(jogador), {}).get(7, 0), # personagem rank 7
                ColetaFeatures._contagem_personagens_por_jogador.get(id(jogador), {}).get(8, 0), # personagem rank 8
            ]
            
            estado_jogadores = estado_jogadores + features_jogador

        x_coleta = estado_tabuleiro + estado_jogadores
        X = np.vstack((X, x_coleta))
        return X

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