from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoDistrito import TipoDistrito
from classes.enum.TipoPersonagem import TipoPersonagem
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
        # Escolhe assassina se está com 6 distritos construídos e tem pelo menos 1 distrito na mão
        if assassina != -1 and len(estado.jogador_atual.distritos_construidos) >= 6 and len(estado.jogador_atual.cartas_distrito_mao) > 0:
            return assassina
        # Escolhe ilusionista se não tiver cartas na mão
        if ilusionista != -1 and len(estado.jogador_atual.cartas_distrito_mao) == 0:
            return ilusionista
        # Escolhe ladrao se está com pouco ouro
        if ladrao != -1 and estado.jogador_atual.ouro <= 1:
            return ladrao
        # Escolhe arquiteta se está com muito ouro
        if arquiteta != -1 and estado.jogador_atual.ouro >= 5:
            return arquiteta
        # Escolhe personagem que dá melhor bônus de acordo com os tipos de distritos construídos
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
        if rei != -1 and nobre > 0:
            return rei
        if bispo != -1 and religioso > 0:
            return bispo
        if comerciante != -1 and comercial > 0:
            return comerciante
        if senhor_da_guerra != -1 and militar > 0:
            return senhor_da_guerra
        # Escolhe aleatoriamente caso não encaixe nenhuma regra pré-definida acima
        return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        # Coleta cartas se não tiver nenhuma na mão ou tiver muito ouro
        # Desde que não tenha pego ilusionista ou arquiteta
        if TipoAcao.ColetarCartas in acoes_disponiveis:
            if (len(estado.jogador_atual.cartas_distrito_mao) == 0 or estado.jogador_atual.ouro >= 5)\
                    and estado.jogador_atual.personagem.tipo_personagem != TipoPersonagem.Arquiteta\
                    and estado.jogador_atual.personagem.tipo_personagem != TipoPersonagem.Ilusionista:
                return acoes_disponiveis.index(TipoAcao.ColetarCartas)
            else:
                return acoes_disponiveis.index(TipoAcao.ColetarOuro)
        # Executa ação sempre que tiver esses personagens (assassina e ladrao)
        if TipoAcao.HabilidadeAssassina in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeAssassina)
        if TipoAcao.HabilidadeLadrao in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeLadrao)
        # Usa ação de ilusionista de trocar se tiver poucas cartas na mão, senão usa ação de descartar cartas
        if TipoAcao.HabilidadeIlusionistaTrocar in acoes_disponiveis and len(estado.jogador_atual.cartas_distrito_mao) <= 1:
            return acoes_disponiveis.index(TipoAcao.HabilidadeIlusionistaTrocar)
        if TipoAcao.HabilidadeIlusionistaDescartar in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeIlusionistaDescartar)
        # Se construiu distrito de determinado tipo que comba com ação de personagem escolhido
        # Executa a ação do personagem antes de construir o distrito, senão depois
        nobre = False
        religioso = False
        comercial = False
        militar = False
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
        if TipoAcao.Laboratorio in acoes_disponiveis and len(estado.jogador_atual.cartas_distrito_mao) > 2:
            return acoes_disponiveis.index(TipoAcao.Laboratorio)
        # Se tiver poucas cartas na mão, usa ação da forja
        if TipoAcao.Forja in acoes_disponiveis and len(estado.jogador_atual.cartas_distrito_mao) <= 1:
            return acoes_disponiveis.index(TipoAcao.Forja)
        # Sempre constroi um distrito se puder
        if TipoAcao.ConstruirDistrito in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.ConstruirDistrito)
        # Ações que fazem sentido após construção de distrito
        if TipoAcao.HabilidadeSenhorDaGuerraDestruir in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeSenhorDaGuerraDestruir)
        if TipoAcao.HabilidadeRei in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeRei)
        if TipoAcao.HabilidadeBispo in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeBispo)
        if TipoAcao.HabilidadeComerciante in acoes_disponiveis and comercial:
            return acoes_disponiveis.index(TipoAcao.HabilidadeComerciante)
        if TipoAcao.HabilidadeSenhorDaGuerraColetar in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeSenhorDaGuerraColetar)
        return 0

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        return random.randint(0, qtd_cartas - 1)

    # Estratégia usada na ação de construir distritos
    @staticmethod
    def construir_distrito(estado: Estado,
                           distritos_para_construir: list[CartaDistrito],
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

# Rever a partir daqui

    # Estratégia usada na ação de construir distritos (efeito Covil dos Ladrões)
    @staticmethod
    def construir_distrito_covil_dos_ladroes(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade da Assassina
    @staticmethod
    def habilidade_assassina(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        try:
            mago = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Mago.value])
        except ValueError:
            mago = -1
        try:
            rei = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Rei.value])
        except ValueError:
            rei = -1
        try:
            cardeal = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Cardeal.value])
        except ValueError:
            cardeal = -1
        try:
            alquimista = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Alquimista.value])
        except ValueError:
            alquimista = -1
        try:
            navegadora = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Navegadora.value])
        except ValueError:
            navegadora = -1
        try:
            senhor_da_guerra = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.SenhorDaGuerra.value])
        except ValueError:
            senhor_da_guerra = -1
        if senhor_da_guerra != -1:
            return senhor_da_guerra
        if alquimista != -1:
            return alquimista
        if mago != -1:
            return mago
        if navegadora != -1:
            return navegadora
        if cardeal != -1:
            return cardeal
        if rei != -1:
            return rei
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        try:
            mago = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Mago.value])
        except ValueError:
            mago = -1
        try:
            rei = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Rei.value])
        except ValueError:
            rei = -1
        try:
            cardeal = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Cardeal.value])
        except ValueError:
            cardeal = -1
        try:
            alquimista = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.Alquimista.value])
        except ValueError:
            alquimista = -1
        try:
            senhor_da_guerra = estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[TipoPersonagem.SenhorDaGuerra.value])
        except ValueError:
            senhor_da_guerra = -1
        if alquimista != -1:
            return alquimista
        if mago != -1:
            return mago
        if senhor_da_guerra != -1:
            return senhor_da_guerra
        if cardeal != -1:
            return cardeal
        if rei != -1:
            return rei
        return random.randint(0, len(opcoes_personagem) - 1)

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
        menor_valor = 9
        distrito_escolhido = -1
        for i, distrito in enumerate(estado.jogador_atual.cartas_distrito_mao):
            if distrito.valor_do_distrito < menor_valor:
                menor_valor = distrito.valor_do_distrito
                distrito_escolhido = i
        return distrito_escolhido

    # Estratégia usada na ação do Arsenal
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

    # Estratégia usada na ação do Museu
    @staticmethod
    def museu(estado: Estado) -> int:
        menor_valor = 9
        distrito_escolhido = -1
        for i, distrito in enumerate(estado.jogador_atual.cartas_distrito_mao):
            if menor_valor < distrito.valor_do_distrito:
                menor_valor = distrito.valor_do_distrito
                distrito_escolhido = i
        return distrito_escolhido
