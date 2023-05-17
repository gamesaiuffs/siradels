from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoPersonagem import TipoPersonagem
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random


class EstrategiaGustavo(Estrategia):
    def __init__(self):
        super().__init__('Gustavo.')

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(estado: Estado) -> int:
        flag_rei = 0
        if flag_rei == 1:
            if estado.jogador_atual.ouro < 3:
                if estado.tabuleiro.personagens[TipoPersonagem.Navegadora.value] in estado.tabuleiro.baralho_personagens:
                    return 6
                elif estado.tabuleiro.personagens[TipoPersonagem.Alquimista.value] in estado.tabuleiro.baralho_personagens:
                    return 5
            if len(estado.jogador_atual.cartas_distrito_mao) > 5:
                if estado.tabuleiro.personagens[TipoPersonagem.Cardeal.value] in estado.tabuleiro.baralho_personagens:
                    return 4
            if estado.tabuleiro.personagens[TipoPersonagem.Ladrao.value] in estado.tabuleiro.baralho_personagens:
                return 2
            if estado.tabuleiro.personagens[TipoPersonagem.Assassina.value] in estado.tabuleiro.baralho_personagens:
                return 1
        elif estado.tabuleiro.personagens[TipoPersonagem.Rei.value] in estado.tabuleiro.baralho_personagens:
            flag_rei = 1
            return 0
        return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        if TipoAcao.ColetarCartas in acoes_disponiveis \
                or TipoAcao.ColetarOuro in acoes_disponiveis:
            if len(estado.jogador_atual.cartas_distrito_mao) == 0:
                return acoes_disponiveis.index(TipoAcao.ColetarCartas)
            menor_custo = 9
            for distrito in estado.jogador_atual.cartas_distrito_mao:
                if menor_custo > distrito.valor_do_distrito:
                    menor_custo = distrito.valor_do_distrito
            if estado.jogador_atual.ouro < menor_custo:
                return acoes_disponiveis.index(TipoAcao.ColetarOuro)
        if TipoAcao.HabilidadeAssassina in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeAssassina)
        if TipoAcao.HabilidadeLadrao in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeLadrao)
        if TipoAcao.HabilidadeCardeal in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeCardeal)
        if TipoAcao.HabilidadeMago in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeMago)
        if TipoAcao.HabilidadeRei in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeRei)
        if TipoAcao.HabilidadeNavegadora in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeNavegadora)
        if TipoAcao.HabilidadeSenhorDaGuerraColetar in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeSenhorDaGuerraColetar)
        if TipoAcao.HabilidadeSenhorDaGuerraDestruir in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeSenhorDaGuerraDestruir)
            
        return random.randint(0, len(acoes_disponiveis) - 1)

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        maior_carta = ''
        val_carta = 0
        for i,carta in enumerate(cartas_compradas):
            if estado.jogador_atual.ouro > carta.valor_do_distrito:
                if carta.valor_do_distrito > val_carta:
                    maior_carta = carta.nome_do_distrito
                    val_carta = carta.valor_do_distrito
                else:
                    continue
            if estado.jogador_atual.ouro < carta.valor_do_distrito:
                continue
        for i,carta in enumerate(cartas_compradas):
            if maior_carta == carta.nome_do_distrito:
                return i
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
        maior_valor_distrito = 0
        for distrito in estado.jogador_atual.cartas_distrito_mao:
            if distrito.valor_do_distrito > maior_valor_distrito:
                maior_valor_distrito = distrito.valor_do_distrito
        for i, distrito in enumerate(distritos_para_construir):
            if distrito.valor_do_distrito == maior_valor_distrito:
                return i + 1
        
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
        alvo = 'Navegadora'
        alvo2 = 'SenhorDaGuerra'
        for i,carta in enumerate(opcoes_personagem):
            if carta.nome == alvo:
                return i
        for i,carta in enumerate(opcoes_personagem):
            if carta.nome == alvo2:
                return i
    
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        alvo = 'Navegadora'
        alvo2 = 'Alquimista'
        for i,carta in enumerate(opcoes_personagem):
            if carta.nome == alvo:
                return i
        for i,carta in enumerate(opcoes_personagem):
            if carta.nome == alvo2:
                return i

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
        return random.randint(0, len(opcoes_jogadores) - 1)

    # Estratégia usada na habilidade do Mago (escolha da carta da mão)
    @staticmethod
    def habilidade_mago_carta(estado: Estado, opcoes_cartas: list[CartaDistrito]) -> int:
        maior_carta = ''
        val_carta = 0
        for i,carta in enumerate(opcoes_cartas):
            if carta.valor_do_distrito <= estado.jogador_atual.ouro:
                if carta.valor_do_distrito > val_carta:
                    maior_carta = carta.nome_do_distrito
                    val_carta = carta.valor_do_distrito
        return random.randint(0, len(opcoes_cartas) - 1)

    # Estratégia usada na habilidade da Navegadora
    @staticmethod
    def habilidade_navegadora(estado: Estado) -> int:
        return 0
        #return random.randint(0, 1)

    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    def habilidade_senhor_da_guerra(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador, int)]) -> int:
        for i, carta in enumerate(distritos_para_destruir):
            if carta not in estado.jogador_atual.distritos_construidos:
                return i
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