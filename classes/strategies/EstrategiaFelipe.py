from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoDistrito import TipoDistrito
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random


class EstrategiaFelipe(Estrategia):
    def __init__(self):
        super().__init__('Felipe.')

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(estado: Estado) -> int:
        return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        if TipoAcao.ColetarCartas in acoes_disponiveis:
            if len(estado.jogador_atual.cartas_distrito_mao) == 0 or estado.jogador_atual.ouro >= 6:
                return acoes_disponiveis.index(TipoAcao.ColetarCartas)
            else:
                return acoes_disponiveis.index(TipoAcao.ColetarOuro)
        if TipoAcao.HabilidadeAssassina in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeAssassina)
        if TipoAcao.HabilidadeLadrao in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeLadrao)
        if TipoAcao.HabilidadeMago in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeMago)
        if TipoAcao.HabilidadeNavegadora in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeNavegadora)
        nobre = False
        religioso = False
        militar = False
        for distrito in estado.jogador_atual.distritos_construidos:
            if distrito.tipo_de_distrito == TipoDistrito.Nobre:
                nobre = True
            if distrito.tipo_de_distrito == TipoDistrito.Religioso:
                religioso = True
            if distrito.tipo_de_distrito == TipoDistrito.Militar:
                militar = True
        if TipoAcao.HabilidadeRei in acoes_disponiveis and nobre:
            return acoes_disponiveis.index(TipoAcao.HabilidadeRei)
        if TipoAcao.HabilidadeCardeal in acoes_disponiveis and religioso:
            return acoes_disponiveis.index(TipoAcao.HabilidadeCardeal)
        if TipoAcao.HabilidadeSenhorDaGuerraColetar in acoes_disponiveis and militar:
            return acoes_disponiveis.index(TipoAcao.HabilidadeSenhorDaGuerraColetar)
        if TipoAcao.Laboratorio in acoes_disponiveis and len(estado.jogador_atual.cartas_distrito_mao) > 2:
            return acoes_disponiveis.index(TipoAcao.Laboratorio)
        if TipoAcao.ConstruirDistrito in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.ConstruirDistrito)
        if TipoAcao.HabilidadeSenhorDaGuerraDestruir in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeSenhorDaGuerraDestruir)
        if TipoAcao.HabilidadeRei in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeRei)
        if TipoAcao.HabilidadeCardeal in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeCardeal)
        if TipoAcao.HabilidadeSenhorDaGuerraColetar in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeSenhorDaGuerraColetar)
        if TipoAcao.Museu in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.Museu)
        if TipoAcao.Forja in acoes_disponiveis and len(estado.jogador_atual.cartas_distrito_mao) <= 1:
            return acoes_disponiveis.index(TipoAcao.Forja)
        if TipoAcao.Arsenal in acoes_disponiveis:
            for jogador in estado.jogadores:
                if jogador != estado.jogador_atual:
                    for distrito in jogador.distritos_construidos:
                        if distrito.valor_do_distrito >= 5:
                            return acoes_disponiveis.index(TipoAcao.Arsenal)
        return random.randint(0, len(acoes_disponiveis) - 1)
    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        return random.randint(0, qtd_cartas - 1)

    # Estratégia usada na ação de construir distritos
    @staticmethod
    def construir_distrito(estado: Estado,
                           distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_cardeal: list[(CartaDistrito, Jogador)],
                           distritos_para_construir_necropole: list[(CartaDistrito, CartaDistrito)],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)],
                           distritos_para_construir_estrutura: list[CartaDistrito]) -> int:
        tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_cardeal) + \
                         len(distritos_para_construir_necropole) + len(distritos_para_construir_covil_ladroes) + len(distritos_para_construir_estrutura)
        maior_valor_mao = 0
        for distrito in estado.jogador_atual.cartas_distrito_mao:
            if distrito.valor_do_distrito > maior_valor_mao:
                maior_valor_mao = distrito.valor_do_distrito
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

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Mago (escolha do jogador alvo)
    @staticmethod
    def habilidade_mago_jogador(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        qtd_carta = 0
        jogador_alvo = -1
        for i, jogador in enumerate(opcoes_jogadores):
            if len(jogador.cartas_distrito_mao) > qtd_carta:
                qtd_carta = len(jogador.cartas_distrito_mao)
                jogador_alvo = i
        return i - 1

    # Estratégia usada na habilidade do Mago (escolha da carta da mão)
    @staticmethod
    def habilidade_mago_carta(estado: Estado, opcoes_cartas: list[CartaDistrito]) -> int:
        return random.randint(0, len(opcoes_cartas) - 1)

    # Estratégia usada na habilidade da Navegadora
    @staticmethod
    def habilidade_navegadora(estado: Estado) -> int:
        if len(estado.jogador_atual.cartas_distrito_mao) == 0:
            return 1
        if estado.jogador_atual.ouro - 2 < len(estado.jogador_atual.cartas_distrito_mao) or \
           len(estado.jogador_atual.cartas_distrito_mao) > 3:
            return 0
        return random.randint(0, 1)

    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    def habilidade_senhor_da_guerra(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador, int)]) -> int:
        jogador_mais_pontos = None
        maior_pontuacao = 0
        for jogador in estado.jogadores:
            if jogador == estado.jogador_atual:
                continue
            if maior_pontuacao < jogador.pontuacao:
                maior_pontuacao = jogador.pontuacao
                jogador_mais_pontos = jogador
        for i, (distrito, jogador, muralha) in enumerate(distritos_para_destruir):
            if muralha == 0 and distrito.valor_do_distrito == 1:
                return i + 1
        for i, (distrito, jogador, muralha) in enumerate(distritos_para_destruir):
            if jogador == jogador_mais_pontos:
                return i + 1
        return 0

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
