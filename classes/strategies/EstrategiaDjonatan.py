from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoDistrito import TipoDistrito
from classes.enum.TipoPersonagem import TipoPersonagem
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random


class EstrategiaDjonatan(Estrategia):
    def __init__(self):
        super().__init__('Djonatan.')
    
    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(estado: Estado) -> int:

        qtd_mais_ouro = 0
        qtd_mais_cartas = 0
        for jogador in estado.jogadores:
            if jogador == estado.jogador_atual:
                continue
            if jogador.ouro > qtd_mais_ouro:
                qtd_mais_ouro = jogador.ouro

        for jogador in estado.jogadores:
            if jogador == estado.jogador_atual:
                continue
            if len(jogador.cartas_distrito_mao) > qtd_mais_cartas:
                qtd_mais_cartas = len(jogador.cartas_distrito_mao)

        nobre = 0
        religioso = 0
        militar = 0
        comercial = 0
        for distrito in estado.jogador_atual.distritos_construidos:
            if distrito.tipo_de_distrito == TipoDistrito.Nobre:
                nobre += 1
            if distrito.tipo_de_distrito == TipoDistrito.Religioso:
                religioso += 1
            if distrito.tipo_de_distrito == TipoDistrito.Comercial:
                comercial += 1
            if distrito.tipo_de_distrito == TipoDistrito.Militar:
                militar += 1

        tem_ouro = True
        tem_distrito = True
        if len(estado.jogador_atual.distritos_construidos) == 6:    # se estiver encerrando
            for distrito in estado.jogador_atual.cartas_distrito_mao:
                if distrito.valor_do_distrito > estado.jogador_atual.ouro:  # tem ouro para construir o último
                    tem_ouro = False
                for distrito2 in estado.jogador_atual.distritos_construidos:        
                    if distrito.nome_do_distrito != distrito2.nome_do_distrito \
                        or len(estado.jogador_atual.cartas_distrito_mao) == 0: # tem distrito válido para construir o último
                        tem_distrito = False

        try:
            assassina = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Assassina.value])
        except ValueError:
            assassina = -1
        try:
            ladrao = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Ladrao.value])
        except ValueError:
            ladrao = -1
        try:
            ilusionista = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Ilusionista.value])
        except ValueError:
            ilusionista = -1
        try:
            rei = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Rei.value])
        except ValueError:
            rei = -1
        try:
            bispo = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Bispo.value])
        except ValueError:
            bispo = -1
        try:
            comerciante = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Comerciante.value])
        except ValueError:
            comerciante = -1
        try:
            arquiteta = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Arquiteta.value])
        except ValueError:
            arquiteta = -1
        try:
            senhor_da_guerra = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.SenhorDaGuerra.value])
        except ValueError:
            senhor_da_guerra = -1

        if len(estado.jogador_atual.distritos_construidos) >= 6\
            and estado.jogador_atual.ouro > 1\
            and len(estado.jogador_atual.cartas_distrito_mao)\
            and (tem_ouro and tem_distrito):
            if assassina != -1:
                return assassina
            if bispo != -1:
                return bispo
            if senhor_da_guerra != -1:
                return senhor_da_guerra
            
        if estado.jogador_atual.ouro > 3 or len(estado.jogador_atual.cartas_distrito_mao) == 0:
            if arquiteta != -1:
                return arquiteta
            if ilusionista != -1:
                return ilusionista
            if rei != -1:
                return rei
            
        # Preciso encontrar o tipo de distrito com o maior número de distritos construídos
        # Preciso controlar se vou ou não construir distritos, para construir algum específico

        '''  
        vetor_de_ganhos = [religioso, militar, nobre, comercial+1]
        if max(vetor_de_ganhos) > 0:
            if max(vetor_de_ganhos) == vetor_de_ganhos[1] and comerciante != -1:
                return comerciante
            if max(vetor_de_ganhos) == vetor_de_ganhos[0] and bispo != -1:
                return bispo
            if max(vetor_de_ganhos) == vetor_de_ganhos[1] and senhor_da_guerra != -1:
                return senhor_da_guerra
            if max(vetor_de_ganhos) == vetor_de_ganhos[1] and rei != -1:
                return rei
        '''

        if comerciante != -1:
            return comerciante
        if rei != -1 and nobre > 0:
            return rei
        if ladrao != -1:
            return ladrao
        if rei != -1:
            return rei
        if senhor_da_guerra != -1 and militar > 0:
            return senhor_da_guerra
        if bispo != -1 and religioso > 0:
            return bispo
        
        
        return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

   # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        # Deixa passar turno por último
        acao_escolhida = random.randint(0, len(acoes_disponiveis) - 1)
        while len(acoes_disponiveis) > 1 and acoes_disponiveis[acao_escolhida] == TipoAcao.PassarTurno:
            acao_escolhida = random.randint(0, len(acoes_disponiveis) - 1)
        return acao_escolhida

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        return random.randint(0, qtd_cartas - 1)

    # Estratégia usada na ação de construir distritos
    @staticmethod
    def construir_distrito(estado: Estado, distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)]) -> int:
        tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_covil_ladroes)
        return random.randint(0, tamanho_maximo - 1)

    # Estratégia usada na ação de construir distritos (efeito Covil dos Ladrões)
    @staticmethod
    def construir_distrito_covil_dos_ladroes(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade da Assassina
    @staticmethod
    def habilidade_assassina(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)
        # Retira opções de personagens descartados
        opcoes = []
        for personagem in opcoes_personagem:
            if personagem not in estado.tabuleiro.cartas_visiveis:
                opcoes.append(personagem)
        return random.randint(0, len(opcoes) - 1)

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)
        # Retira opções de personagens descartados
        opcoes = []
        for personagem in opcoes_personagem:
            if personagem not in estado.tabuleiro.cartas_visiveis:
                opcoes.append(personagem)
        return random.randint(0, len(opcoes) - 1)

    # Estratégia usada na habilidade da Ilusionista (escolha do jogador alvo)
    @staticmethod
    def habilidade_ilusionista_trocar(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        return random.randint(0, len(opcoes_jogadores) - 1)
        # Ilusionista sempre troca de mão com o adversário que possui mais cartas, o desempate é uma escolha aleatória entre empatados
        mais_cartas = 0
        for jogador in opcoes_jogadores:
            if len(jogador.cartas_distrito_mao) > mais_cartas:
                mais_cartas = len(jogador.cartas_distrito_mao)
        opcoes = []
        for idx, jogador in enumerate(opcoes_jogadores):
            if len(jogador.cartas_distrito_mao) == mais_cartas:
                opcoes.append(idx)
        return random.sample(opcoes, 1)[0]

    # Estratégia usada na habilidade da Ilusionista (escolha de quantas cartas serão descartadas)
    @staticmethod
    def habilidade_ilusionista_descartar_qtd_cartas(estado: Estado, qtd_maxima: int) -> int:
        return random.randint(1, qtd_maxima)

    # Estratégia usada na habilidade da Ilusionista (escolha de qual carta descartar)
    @staticmethod
    def habilidade_ilusionista_descartar_carta(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    def habilidade_senhor_da_guerra_destruir(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        return random.randint(0, len(distritos_para_destruir) - 1)

    # Estratégia usada na ação do Laboratório
    @staticmethod
    def laboratorio(estado: Estado) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)
