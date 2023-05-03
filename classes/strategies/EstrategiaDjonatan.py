from classes.enum.TipoAcao import TipoAcao
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
        return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

        #define o maior custo
        maior_custo = 0
        for distrito in estado.jogador_atual.cartas_distrito_mao:
                if maior_custo < distrito.valor_do_distrito:
                    maior_custo = distrito.valor_do_distrito
        #define o menor custo
        menor_custo = 10
        for distrito in estado.jogador_atual.cartas_distrito_mao:
            if menor_custo > distrito.valor_do_distrito:
                menor_custo = distrito.valor_do_distrito

        #### seleção ###

        #se não houver ladrão nem assassino e tiver ouro, priorize o mago, se não tiver mago, priorize a alquimista
        if estado.tabuleiro.personagens[1] in estado.tabuleiro.cartas_visiveis and estado.tabuleiro.personagens[2] in estado.tabuleiro.cartas_visiveis and estado.jogador_atual.ouro > menor_custo:
            return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[2])
            if estado.tabuleiro.personagens[2] not in estado.tabuleiro.baralho_personagens:
                return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[5])

        #se tiver muito ouro, priorizar assassina ou ladrão
        if estado.jogador_atual.ouro >= maior_custo:
            if estado.tabuleiro.personagens[1] in estado.tabuleiro.baralho_personagens:
                return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[1])
            elif estado.tabuleiro.personagens[2] in estado.tabuleiro.baralho_personagens:
                return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[2])
            else:
                return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)        
        
        #se tiver muita carta, priorizar o cardeal
        if len(estado.jogador_atual.cartas_distrito_mao) >= maior_custo:
            return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[4])

        #se não tiver nada, priorizar o rei
        if len(estado.jogador_atual.cartas_distrito_mao) == 0 and estado.jogador_atual.ouro < menor_custo:
            return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[0])
        
        #se não houver assassina e não tiver muito ouro, priorize a navegadora
        if estado.tabuleiro.personagens[1] in estado.tabuleiro.cartas_visiveis and estado.jogador_atual.ouro < maior_custo:
            return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[6])

        return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        if TipoAcao.ColetarCartas in acoes_disponiveis \
                or TipoAcao.ColetarOuro in acoes_disponiveis:
            if len(estado.jogador_atual.cartas_distrito_mao) == 0:
                return acoes_disponiveis.index(TipoAcao.ColetarCartas)
            menor_custo = 10
            for distrito in estado.jogador_atual.cartas_distrito_mao:
                if menor_custo > distrito.valor_do_distrito:
                    menor_custo = distrito.valor_do_distrito  
            if estado.jogador_atual.ouro < menor_custo:
                return acoes_disponiveis.index(TipoAcao.ColetarOuro)
        return random.randint(0, len(acoes_disponiveis) - 1)

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        return random.randint(0, qtd_cartas - 1)

    # Estratégia usada na ação de construir distritos
    @staticmethod
    def construir_distrito(estado: Estado,
                           distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_cardeal: list[CartaDistrito],
                           distritos_para_construir_necropole: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[CartaDistrito],
                           distritos_para_construir_estrutura: list[CartaDistrito]) -> int:
        tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_cardeal) + \
                         len(distritos_para_construir_necropole) + len(distritos_para_construir_covil_ladroes) + len(distritos_para_construir_estrutura)
        return random.randint(0, tamanho_maximo)

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

        #mate a navegadora, se não, mate o mago
        if estado.tabuleiro.personagens[6] not in estado.tabuleiro.baralho_personagens:
            return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[6])
        if estado.tabuleiro.personagens[2] not in estado.tabuleiro.baralho_personagens:
            return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[2])

        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)

        #roube o mago, se não tiver mago, roube a arquiteta, se não, roube o senhor da guerra
        if estado.tabuleiro.personagens[2] not in estado.tabuleiro.baralho_personagens:
            return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[2])
        if estado.tabuleiro.personagens[5] not in estado.tabuleiro.baralho_personagens:
            return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[5])
        if estado.tabuleiro.personagens[7] not in estado.tabuleiro.baralho_personagens:
            return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[7])
        
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Mago (escolha do jogador alvo)
    @staticmethod
    def habilidade_mago_jogador(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        #veja quem tem mais cartas
        max_num_cartas = 0
        idx = 0
        
        for i, jogador_alvo in enumerate(opcoes_jogadores):
            if len(jogador_alvo.cartas_distrito_mao) > max_num_cartas:
                max_num_cartas = len(jogador_alvo.cartas_distrito_mao)
                idx = i
        return idx

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

    # Estratégia usada na ação do Laboratório
    @staticmethod
    def laboratorio(estado: Estado) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na ação do Arsenal
    @staticmethod
    def arsenal(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        return random.randint(0, len(distritos_para_destruir))

    # Estratégia usada na ação do Museu
    @staticmethod
    def museu(estado: Estado) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)
