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

        if len(estado.jogador_atual.distritos_construidos) >= 6:
            if assassina != -1:
                return assassina
            
            if bispo != -1:
                return bispo

            if senhor_da_guerra != -1:
                return senhor_da_guerra
            
        if estado.jogador_atual.ouro > 3:
            if arquiteta != -1:
                return arquiteta
            
        if estado.jogador_atual.cartas_distrito_mao == 0:
            if ilusionista != -1:
                return ilusionista
            
            if rei != -1:
                return rei
        
        if ladrao != -1:
            return ladrao
        
        if rei != -1:
            return rei
        
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
        if comerciante != -1 and comercial > 1:
            return comerciante
        if rei != -1 and nobre > 0:
            return rei
        if bispo != -1 and religioso > 0:
            return bispo
        if senhor_da_guerra != -1 and militar > 0:
            return senhor_da_guerra
        if comerciante != -1:
            return comerciante
        return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        
        if TipoAcao.ColetarCartas in acoes_disponiveis:
            if len(estado.jogador_atual.cartas_distrito_mao) == 0 or estado.jogador_atual.ouro >= 5\
                    and estado.jogador_atual.personagem.tipo_personagem != TipoPersonagem.Ilusionista\
                    and estado.jogador_atual.personagem.tipo_personagem != TipoPersonagem.Arquiteta:
                return acoes_disponiveis.index(TipoAcao.ColetarCartas)
            else:
                return acoes_disponiveis.index(TipoAcao.ColetarOuro)
        if TipoAcao.HabilidadeAssassina in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeAssassina)
        if TipoAcao.HabilidadeLadrao in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeLadrao)
        if TipoAcao.HabilidadeIlusionistaTrocar in acoes_disponiveis and len(estado.jogador_atual.cartas_distrito_mao) == 0:
            return acoes_disponiveis.index(TipoAcao.HabilidadeIlusionistaTrocar)
        #if TipoAcao.HabilidadeIlusionistaDescartar in acoes_disponiveis:
        #    return acoes_disponiveis.index(TipoAcao.HabilidadeIlusionistaDescartar)
        nobre = False
        religioso = False
        militar = False
        comercial = False
        for distrito in estado.jogador_atual.distritos_construidos:
            if distrito.tipo_de_distrito == TipoDistrito.Nobre:
                nobre = True
            if distrito.tipo_de_distrito == TipoDistrito.Religioso:
                religioso = True
            if distrito.tipo_de_distrito == TipoDistrito.Comercial:
                comercial = True
            if distrito.tipo_de_distrito == TipoDistrito.Militar:
                militar = True
        if TipoAcao.HabilidadeRei in acoes_disponiveis and nobre:
            return acoes_disponiveis.index(TipoAcao.HabilidadeRei)
        if TipoAcao.HabilidadeBispo in acoes_disponiveis and religioso:
            return acoes_disponiveis.index(TipoAcao.HabilidadeBispo)
        if TipoAcao.HabilidadeComerciante in acoes_disponiveis and comercial:
            return acoes_disponiveis.index(TipoAcao.HabilidadeComerciante)
        if TipoAcao.HabilidadeSenhorDaGuerraColetar in acoes_disponiveis and militar:
            return acoes_disponiveis.index(TipoAcao.HabilidadeSenhorDaGuerraColetar)
        # Se tiver muitas cartas na mão usa ação do laboratório
        if TipoAcao.Laboratorio in acoes_disponiveis and estado.jogador_atual.ouro == 0:
            return acoes_disponiveis.index(TipoAcao.Laboratorio)
        # Se tiver poucas cartas na mão, usa ação da forja
        if TipoAcao.Forja in acoes_disponiveis and len(estado.jogador_atual.cartas_distrito_mao) <= 1:
            return acoes_disponiveis.index(TipoAcao.Forja)
        # Sempre constroi um distrito se puder
        if TipoAcao.ConstruirDistrito in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.ConstruirDistrito)
        if TipoAcao.HabilidadeRei in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeRei)
        if TipoAcao.HabilidadeBispo in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeBispo)
        if TipoAcao.HabilidadeComerciante in acoes_disponiveis and comercial:
            return acoes_disponiveis.index(TipoAcao.HabilidadeComerciante)
        if TipoAcao.HabilidadeSenhorDaGuerraColetar in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeSenhorDaGuerraColetar)
        if TipoAcao.HabilidadeSenhorDaGuerraDestruir in acoes_disponiveis:
            for jogador in estado.jogadores:
                for distrito in jogador.distritos_construidos:
                    if distrito.valor_do_distrito == 0:
                        return acoes_disponiveis.index(TipoAcao.HabilidadeSenhorDaGuerraDestruir)
        
        return 0

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        maior_custo = 0
        idx = 0

        # caso de faltar 1 distrito
        for i, carta in enumerate(cartas_compradas):
            if len(estado.jogador_atual.distritos_construidos) == 6 and carta.valor_do_distrito < estado.jogador_atual.ouro and carta not in estado.jogador_atual.distritos_construidos:   
                return i

            if carta.tipo_de_distrito == 4: # Se for especial
                return i
            
            if carta.valor_do_distrito > maior_custo and carta not in estado.jogador_atual.distritos_construidos: # se não, mais caro
                maior_custo = carta.valor_do_distrito
                idx = i
            return idx
        return random.randint(0, qtd_cartas - 1)

    # Estratégia usada na ação de construir distritos
    @staticmethod
    def construir_distrito(estado: Estado,
                           distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)]) -> int:
        tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_covil_ladroes)

        tipos = [0, 0, 0, 0, 0]        
        contador_tipos = 0
        maior_valor_mao = 0
        for distrito in estado.jogador_atual.cartas_distrito_mao:
            if distrito.valor_do_distrito > maior_valor_mao:
                maior_valor_mao = distrito.valor_do_distrito

        '''
        for i, distrito in enumerate(estado.jogador_atual.distritos_construidos):
            if distrito.tipo_de_distrito == 4:
                tipos[4] = 1
            if distrito.tipo_de_distrito == 3:
                tipos[3] = 1
            if distrito.tipo_de_distrito == 2:
                tipos[2] = 1
            if distrito.tipo_de_distrito == 1:
                tipos[1] = 1
            if distrito.tipo_de_distrito == 0:
                tipos[0] = 1
        for i in tipos:
            if i == 1:
                contador_tipos += 1
            
        if contador_tipos == 4:
            for i, distritoI in enumerate(estado.jogador_atual.cartas_distrito_mao):
                for distritoJ in estado.jogador_atual.distritos_construidos:
                    if (distritoI.tipo_de_distrito != distritoJ.tipo_de_distrito) and distritoJ not in estado.jogador_atual.distritos_construidos:
                        return i
        '''

        for i, distrito in enumerate(estado.jogador_atual.cartas_distrito_mao): # Tenta construir especial
            if distrito.tipo_de_distrito == 4:
                return i

        for i, distrito in enumerate(distritos_para_construir):
            if distrito == maior_valor_mao:
                return i
        return random.randint(0, tamanho_maximo - 1)

    # Estratégia usada na ação de construir distritos (efeito Covil dos Ladrões)
    @staticmethod
    def construir_distrito_covil_dos_ladroes(estado: Estado, qtd_cartas: int, i: int) -> int:
        idx = 0
        menor_custo = 10
        for i, distrito in enumerate(estado.jogador_atual.cartas_distrito_mao):
            if distrito in estado.jogador_atual.distritos_construidos:
                return i
            if distrito.valor_do_distrito > menor_custo:
                menor_custo == distrito.valor_do_distrito
                idx = i
            return idx
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade da Assassina
    @staticmethod
    def habilidade_assassina(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        
        try:
            ladrao = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Ladrao.value])
        except ValueError:
            ladrao = -1
        try:
            rei = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Rei.value])
        except ValueError:
            rei = -1
        try:
            bispo = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Bispo.value])
        except ValueError:
            bispo = -1
        try:
            arquiteta = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Arquiteta.value])
        except ValueError:
            arquiteta = -1
        try:
            ilusionista = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Ilusionista.value])
        except ValueError:
            ilusionista = -1
        try:
            senhor_da_guerra = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.SenhorDaGuerra.value])
        except ValueError:
            senhor_da_guerra = -1

        if arquiteta != -1:
            return arquiteta
        if rei != -1:
            return rei
        if ladrao != -1:
            return ladrao
        if senhor_da_guerra != -1:
            return senhor_da_guerra
        if ilusionista != -1:
            return ilusionista
        if bispo != -1:
            return bispo
        return random.randint(1, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        try:
            rei = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Rei.value])
        except ValueError:
            rei = -1
        try:
            bispo = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Bispo.value])
        except ValueError:
            bispo = -1
        try:
            arquiteta = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Arquiteta.value])
        except ValueError:
            arquiteta = -1
        try:
            ilusionista = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Ilusionista.value])
        except ValueError:
            ilusionista = -1
        try:
            senhor_da_guerra = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.SenhorDaGuerra.value])
        except ValueError:
            senhor_da_guerra = -1

        for jogador in estado.jogadores:
            if len(jogador.distritos_construidos) == 6:
                return bispo

        if arquiteta != -1:
            return arquiteta
        if ilusionista != -1:
            return ilusionista
        if rei != -1:
            return rei
        if senhor_da_guerra != -1:
            return senhor_da_guerra
        return random.randint(1, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade ativa da ilusionista (escolha do jogador alvo)
    @staticmethod
    def habilidade_ilusionista_trocar(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
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
        for i, distrito in enumerate(estado.jogador_atual.cartas_distrito_mao):
            for distrito2 in estado.jogador_atual.distritos_construidos:
                if distrito.nome_do_distrito == distrito2.nome_do_distrito:
                    return i

        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    def habilidade_senhor_da_guerra_destruir(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        # Adaptar
        for jogador in estado.jogadores:
            for i, distrito in enumerate(jogador.distritos_construidos):
                if distrito.valor_do_distrito == 0:
                    return i

    # Estratégia usada na ação do Laboratório
    @staticmethod
    def laboratorio(estado: Estado) -> int:
        # Descartar distritos de mesmo nome
        for i, distrito in enumerate(estado.jogador_atual.cartas_distrito_mao):
            for distrito2 in estado.jogador_atual.distritos_construidos:
                if distrito.nome_do_distrito == distrito2.nome_do_distrito:
                    return i

        # Descarta o distrito de menor valor da mão
        menor_valor = 9
        distrito_escolhido = 0
        for i, distrito in enumerate(estado.jogador_atual.cartas_distrito_mao):
            if distrito.valor_do_distrito < menor_valor:
                menor_valor = distrito.valor_do_distrito
                distrito_escolhido = i
        return distrito_escolhido