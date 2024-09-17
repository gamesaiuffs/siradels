from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoDistrito import TipoDistrito
from classes.enum.TipoPersonagem import TipoPersonagem
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random


class EstrategiaJean(Estrategia):
    def __init__(self):
        super().__init__('Jean.')

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(estado: Estado) -> int:
        # Flags de quais personagens estão disponíves para escolha
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
        # Regras de preferência por escolha de personagens
        # Escolhe ilusionista se tiver menos de duas cartas na mao
        if ilusionista != -1 and len(estado.jogador_atual.cartas_distrito_mao) < 2:
            return ilusionista
        # Escolhe arquiteta se está com muito ouro
        if arquiteta != -1 and estado.jogador_atual.ouro > 4:
            return arquiteta
        # Escolhe personagem para coleta de ouro se tem 2 ou menos
        nobre = 0
        religioso = 0
        comercial = 0
        militar = 0
        for distrito in estado.jogador_atual.distritos_construidos:
            if distrito.tipo_de_distrito == TipoDistrito.Nobre:
                nobre += 1
            if distrito.tipo_de_distrito == TipoDistrito.Religioso:
                religioso += 1
            if distrito.tipo_de_distrito == TipoDistrito.Comercial:
                comercial += 1
            if distrito.tipo_de_distrito == TipoDistrito.Militar:
                militar += 1
        if estado.jogador_atual.ouro < 3:
            if comerciante != -1 and comercial > 1:
                return comerciante
            if bispo != -1 and religioso > 1:
                return bispo
            if rei != -1 and nobre > 1:
                return rei
            if senhor_da_guerra != -1 and militar > 1:
                return senhor_da_guerra
        # Escolhe aleatoriamente caso não encaixe nenhuma regra pré-definida acima
        return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        if estado.jogador_atual.ouro < 3:
            if TipoAcao.HabilidadeRei in acoes_disponiveis:
                return acoes_disponiveis.index(TipoAcao.HabilidadeRei)
            if TipoAcao.HabilidadeLadrao in acoes_disponiveis:
                return acoes_disponiveis.index(TipoAcao.HabilidadeLadrao)
            if TipoAcao.HabilidadeBispo in acoes_disponiveis:
                return acoes_disponiveis.index(TipoAcao.HabilidadeBispo)
            if TipoAcao.HabilidadeComerciante in acoes_disponiveis:
                return acoes_disponiveis.index(TipoAcao.HabilidadeComerciante)
            if TipoAcao.HabilidadeSenhorDaGuerraColetar in acoes_disponiveis:
                return acoes_disponiveis.index(TipoAcao.HabilidadeSenhorDaGuerraColetar)                                    
        else:
            if estado.jogador_atual.ouro > 4 and TipoAcao.ColetarCartas in acoes_disponiveis:
                return acoes_disponiveis.index(TipoAcao.ColetarCartas)
        # Deixa passar turno por último
        if TipoAcao.HabilidadeIlusionistaDescartar in acoes_disponiveis and len(estado.jogador_atual.cartas_distrito_mao)>0:
            return acoes_disponiveis.index(TipoAcao.HabilidadeIlusionistaDescartar)

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
        # Escolhe sempre construir o distrito mais caro da mão sempre que possível
        maior_valor_mao = 0
        for distrito in estado.jogador_atual.cartas_distrito_mao:
            if distrito.valor_do_distrito > maior_valor_mao:
                maior_valor_mao = distrito.valor_do_distrito
        for i, distrito in enumerate(distritos_para_construir):
            if distrito == maior_valor_mao:
                return i

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
        menor_valor_mao = 10
        for distrito in estado.jogador_atual.cartas_distrito_mao:
            if distrito.valor_do_distrito < menor_valor_mao:
                menor_valor_mao = distrito.valor_do_distrito
        if len(estado.jogador_atual.cartas_distrito_mao) > 0:
            for i, distrito in enumerate(estado.jogador_atual.cartas_distrito_mao):
                if distrito == menor_valor_mao:
                    return i
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

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
