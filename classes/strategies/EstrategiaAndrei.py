from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoDistrito import TipoDistrito
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random


class EstrategiaAndrei(Estrategia):
    def __init__(self):
        super().__init__('Andrei.')

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(estado: Estado) -> int:
        #Variaveis de flag
        rank = 8
        posicao_atual_no_vetor = 0

        #ESCOLHER SEMPRE O REI
        for personagem in estado.tabuleiro.baralho_personagens:
            if personagem.tipo_personagem == 0:
                return posicao_atual_no_vetor
        posicao_atual_no_vetor = 0

        #ESCOLHER SEMPRE O MENOR RANK DISPONIVEL
        for personagem in estado.tabuleiro.baralho_personagens:
            if personagem.rank < rank:
                rank = personagem.rank
                posicao_do_escolhido = posicao_atual_no_vetor

            posicao_atual_no_vetor += 1

        return posicao_do_escolhido

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        
        #COLETA DE INFORMAÇÕES DA MAO ATUAL
        maior_custo = 0
        menor_custo = 10
        for distrito in estado.jogador_atual.cartas_distrito_mao:
            if distrito.valor_do_distrito > maior_custo: #descobre o distrito mais caro da mao
                maior_custo = distrito.valor_do_distrito
            if distrito.valor_do_distrito < menor_custo: #descobre o distrito mais barato da mao
                menor_custo = distrito.valor_do_distrito
        
        #PEGAR OURO OU CARTAS?
        if TipoAcao.ColetarCartas in acoes_disponiveis or TipoAcao.ColetarOuro in acoes_disponiveis:
            if len(estado.jogador_atual.cartas_distrito_mao) == 0:      #coletar carta caso não tenha nenhuma
                return acoes_disponiveis.index(TipoAcao.ColetarCartas)
            elif estado.jogador_atual.ouro > maior_custo:               #coletar carta caso tenha ouro sobrando
                return acoes_disponiveis.index(TipoAcao.ColetarCartas)
            else:
                return acoes_disponiveis.index(TipoAcao.ColetarOuro)

        #PASSAR TURNO
        if TipoAcao.PassarTurno in acoes_disponiveis and len(acoes_disponiveis) == 1:
            return 0

        return random.randint(1, len(acoes_disponiveis) - 1)

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        
        #ESCOLHER SEMPRE A DE MENOR VALOR
        menor_valor = cartas_compradas[-1].valor_do_distrito
        carta_escolhida = cartas_compradas[-1]
        for carta in cartas_compradas:
            #verifica se já possui
            if carta in estado.jogador_atual.distritos_construidos or carta in estado.jogador_atual.cartas_distrito_mao:
                continue
            #coleta sempre que for nobre
            if carta.tipo_de_distrito == 2:
                return cartas_compradas.index(carta)
            #coleta sempre que for especial
            if carta.tipo_de_distrito == 4:     
                return cartas_compradas.index(carta)
            #salva a de menor valor
            if carta.valor_do_distrito < menor_valor:
                menor_valor = carta.valor_do_distrito   
                carta_escolhida = carta

        return cartas_compradas.index(carta_escolhida)
        #return random.randint(0, qtd_cartas - 1)

    # Estratégia usada na ação de construir distritos by Felipe (adaptado)
    @staticmethod
    def construir_distrito(estado: Estado,
                           distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_cardeal: list[(CartaDistrito, Jogador)],
                           distritos_para_construir_necropole: list[(CartaDistrito, CartaDistrito)],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)],
                           distritos_para_construir_estrutura: list[CartaDistrito]) -> int:
        tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_cardeal) + \
                         len(distritos_para_construir_necropole) + len(distritos_para_construir_covil_ladroes) + len(distritos_para_construir_estrutura)

        #construir nobre
        #i = 0
        # for distrito in estado.jogador_atual.cartas_distrito_mao:
        #     if distrito.tipo_de_distrito == 2:
        #         return i
        #     i += 1
            
        maior_valor_mao = 0
        for distrito in estado.jogador_atual.cartas_distrito_mao:
            if distrito.valor_do_distrito > maior_valor_mao:
                maior_valor_mao = distrito.valor_do_distrito
                
        # Estrutura
        for i, distrito in enumerate(distritos_para_construir_estrutura):
            if distrito.valor_do_distrito == maior_valor_mao:
                return len(distritos_para_construir) + \
                       len(distritos_para_construir_cardeal) + \
                       len(distritos_para_construir_necropole) + \
                       len(distritos_para_construir_covil_ladroes) + i + 1
                       
        menor_valor_construido = 9
        for distrito in estado.jogador_atual.distritos_construidos:
            if distrito.valor_do_distrito < menor_valor_construido:
                menor_valor_construido = distrito.valor_do_distrito
        for i, (_, distrito) in enumerate(distritos_para_construir_necropole):
            if distrito.valor_do_distrito == menor_valor_construido:
                return len(distritos_para_construir) + \
                       len(distritos_para_construir_cardeal) + i + 1
                       
        for i, distrito in enumerate(distritos_para_construir):
            if distrito == maior_valor_mao:
                return i + 1
            
        if len(distritos_para_construir_necropole) > 0:
            return len(distritos_para_construir) + \
                   len(distritos_para_construir_cardeal) + 1
                   
        jogador_mais_ouro = estado.jogador_atual
        qtd_mais_ouro = 0
        jogador_mais_carta = estado.jogador_atual
        qtd_mais_carta = 0
        for jogador in estado.jogadores:
            if jogador == estado.jogador_atual:
                continue
            if jogador.ouro > qtd_mais_ouro:
                qtd_mais_ouro = jogador.ouro
                jogador_mais_ouro = jogador
            if len(jogador.cartas_distrito_mao) > qtd_mais_carta:
                qtd_mais_carta = len(jogador.cartas_distrito_mao)
                jogador_mais_carta = jogador
        for i, (distrito, jogador) in enumerate(distritos_para_construir_cardeal):
            if jogador == jogador_mais_carta or jogador == jogador_mais_ouro:
                return len(distritos_para_construir) + i + 1
            
        return random.randint(1, tamanho_maximo)


    # Estratégia usada na ação de construir distritos (efeito Cardeal)
    @staticmethod
    def construir_distrito_cardeal(estado: Estado, diferenca: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na ação de construir distritos (efeito Covil dos Ladrões)
    @staticmethod
    def construir_distrito_covil_dos_ladroes(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade da Assassina
    @staticmethod
    def habilidade_assassina(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Mago (escolha do jogador alvo)
    @staticmethod
    def habilidade_mago_jogador(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        return random.randint(0, len(opcoes_jogadores) - 1)

    # Estratégia usada na habilidade do Mago (escolha da carta da mão)
    @staticmethod
    def habilidade_mago_carta(estado: Estado, opcoes_cartas: list[CartaDistrito]) -> int:
        return random.randint(0, len(opcoes_cartas) - 1)

    # Estratégia usada na habilidade da Navegadora
    @staticmethod
    def habilidade_navegadora(estado: Estado) -> int:
        return random.randint(0, 1)

    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    def habilidade_senhor_da_guerra(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador, int)]) -> int:
        return random.randint(0, len(distritos_para_destruir))

    # Estratégia usada na ação do Laboratório by Felipe
    @staticmethod
    def laboratorio(estado: Estado) -> int:
        menor_valor = 9
        distrito_escolhido = -1
        for i, distrito in enumerate(estado.jogador_atual.cartas_distrito_mao):
            if distrito.valor_do_distrito < menor_valor:
                menor_valor = distrito.valor_do_distrito
                distrito_escolhido = i
        return distrito_escolhido

    # Estratégia usada na ação do Arsenal by Felipe
    @staticmethod
    def arsenal(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        jogador_mais_pontos = estado.jogador_atual
        for jogador in estado.jogadores:
            if jogador.pontuacao > jogador_mais_pontos.pontuacao:
                jogador_mais_pontos = jogador
        maior_valor = 0
        distrito_escolhido = -1
        for i, (distrito, jogador) in enumerate(distritos_para_destruir):
            if jogador != jogador_mais_pontos:
                continue
            if distrito.valor_do_distrito > maior_valor:
                maior_valor = distrito.valor_do_distrito
                distrito_escolhido = i
        return distrito_escolhido

    # Estratégia usada na ação do Museu by Felipe
    @staticmethod
    def museu(estado: Estado) -> int:
        menor_valor = 9
        distrito_escolhido = -1
        for i, distrito in enumerate(estado.jogador_atual.cartas_distrito_mao):
            if menor_valor < distrito.valor_do_distrito:
                menor_valor = distrito.valor_do_distrito
                distrito_escolhido = i
        return distrito_escolhido
