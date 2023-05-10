from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoPersonagem import TipoPersonagem
from classes.enum.TipoDistrito import TipoDistrito as Td
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random

class EstrategiaJoao(Estrategia):
    def __init__(self):
        super().__init__('Joao   .')

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(estado: Estado) -> int:
        jogador = estado.jogador_atual
        personagens = estado.tabuleiro.baralho_personagens[:]
        ouros = [jogador.ouro for jogador in estado.jogadores]
        lenCartas = [len(jogador.cartas_distrito_mao) for jogador in estado.jogadores]
        distritos = jogador.cartas_distrito_mao
        distritosConstruidos = jogador.distritos_construidos
        custoDistritos = [distrito.valor_do_distrito for distrito in distritos]
        ouros.sort()
        qntDistritosMilitar = sum(1 if carta.tipo_de_distrito == Td.Militar else 0 for carta in distritosConstruidos)

        if len(jogador.cartas_distrito_mao) == 0 and (navegadora := TipoPersonagem.Navegadora) in personagens:
            return estado.tabuleiro.baralho_personagens.index(navegadora)
        if qntDistritosMilitar >= 2 and (senhorDaGuerra := TipoPersonagem.SenhorDaGuerra) in personagens:
            return estado.tabuleiro.baralho_personagens.index(senhorDaGuerra)
        if len(personagens) and (rei := TipoPersonagem.Rei) in personagens:
            return estado.tabuleiro.baralho_personagens.index(rei)
        if len(distritos) == 0 and (mago := TipoPersonagem.Mago) in personagens:
            return estado.tabuleiro.baralho_personagens.index(mago)
        if custoDistritos and max(custoDistritos) == 6 and (alquimista := TipoPersonagem.Alquimista) in personagens:
            return estado.tabuleiro.baralho_personagens.index(alquimista)
        if custoDistritos and jogador.ouro <min(custoDistritos) <max(lenCartas) and (cardeal := TipoPersonagem.Cardeal) in personagens:
            return estado.tabuleiro.baralho_personagens.index(cardeal)

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

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Mago (escolha do jogador alvo)'
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
