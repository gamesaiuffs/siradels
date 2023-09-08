from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.model.Jogador import Jogador
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado


class EstrategiaManual(Estrategia):
    def __init__(self):
        super().__init__('Manual')

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(estado: Estado) -> int:
        print('\n---------| Personagens |--------')
        for i, personagem in enumerate(estado.tabuleiro.baralho_personagens):
            print(f'{i}: {personagem}')
        while True:
            escolha_personagem = input(f'\nEscolha um personagem disponível: ')
            try:
                escolha_personagem = int(escolha_personagem)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_personagem < len(estado.tabuleiro.baralho_personagens):
                print('Escolha inválida.')
                continue
            return escolha_personagem

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        print('Ações disponíveis: ')
        for i, acao in enumerate(acoes_disponiveis):
            print(f'\t{i}: - {acao}')
        while True:
            escolha_acao = input('Escolha sua ação: ')
            try:
                escolha_acao = int(escolha_acao)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_acao < len(acoes_disponiveis):
                print('Escolha inválida.')
                continue
            return escolha_acao

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        print(f'0: {cartas_compradas[0].imprimir_tudo()}')
        print(f'1: {cartas_compradas[1].imprimir_tudo()}')
        if qtd_cartas == 3:
            print(f'2: {cartas_compradas[2].imprimir_tudo()}')
        while True:
            escolha_carta = input('Escolha a carta com que deseja ficar: ')
            try:
                escolha_carta = int(escolha_carta)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_carta < qtd_cartas:
                print('Escolha inválida.')
                continue
            return escolha_carta

    # Estratégia usada na ação de construir distritos
    @staticmethod
    def construir_distrito(estado: Estado, distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)]) -> int:
        print(f'0: Não desejo construir nenhum distrito.')
        i = 0
        for carta in distritos_para_construir:
            i += 1
            print(f'{i}: {carta.imprimir_tudo()}')
        for carta, qtd_ouro, qtd_cartas in distritos_para_construir_covil_ladroes:
            i += 1
            print(f'{i}: {carta.imprimir_tudo()} - Custo em ouro: {qtd_ouro} - Custo em cartas da mão: {qtd_cartas}')
        while True:
            escolha_construir = input('Digite o número do distrito que deseja construir: ')
            try:
                escolha_construir = int(escolha_construir)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_construir <= len(distritos_para_construir) + len(distritos_para_construir_covil_ladroes):
                print('Escolha inválida.')
                continue
            return escolha_construir

    # Estratégia usada na ação de construir distritos (efeito Covil dos Ladrões)
    @staticmethod
    def construir_distrito_covil_dos_ladroes(estado: Estado, qtd_cartas: int, i: int) -> int:
        print(f'Escolha as cartas que usará para pagar o custo. Faltam {qtd_cartas - i} cartas.')
        for j, carta in enumerate(estado.jogador_atual.cartas_distrito_mao):
            print(f'{j}: {carta.imprimir_tudo()}')
        while True:
            escolha_carta = input('Digite o número do distrito que deseja descartar: ')
            try:
                escolha_carta = int(escolha_carta)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_carta < len(estado.jogador_atual.cartas_distrito_mao):
                print('Escolha inválida.')
                continue
            return escolha_carta

    # Estratégia usada na habilidade da Assassina
    @staticmethod
    def habilidade_assassina(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        for i, personagem in enumerate(opcoes_personagem):
            print(f'{i}: {personagem}')
        while True:
            escolha_personagem = input(f'Digite o número do personagem que deseja assassinar: ')
            try:
                escolha_personagem = int(escolha_personagem)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_personagem < len(opcoes_personagem):
                print('Escolha inválida.')
                continue
            return escolha_personagem

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        for i, personagem in enumerate(opcoes_personagem):
            print(f'{i}: {personagem}')
        while True:
            escolha_personagem = input(f'Digite o número do personagem que deseja roubar: ')
            try:
                escolha_personagem = int(escolha_personagem)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_personagem < len(opcoes_personagem):
                print('Escolha inválida.')
                continue
            return escolha_personagem

    # Estratégia usada na habilidade da Ilusionista (escolha do jogador alvo)
    @staticmethod
    def habilidade_ilusionista_trocar(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        print('Jogadores:')
        for i, jogador in enumerate(opcoes_jogadores):
            print(f'{i}: {jogador.nome}')
        while True:
            escolha_jogador = input('Digite o número do jogador com o qual deseja trocar de mão: ')
            try:
                escolha_jogador = int(escolha_jogador)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_jogador < len(opcoes_jogadores):
                print('Escolha inválida.')
                continue
            return escolha_jogador

    # Estratégia usada na habilidade da Ilusionista (escolha de quantas cartas serão descartadas)
    @staticmethod
    def habilidade_ilusionista_descartar_qtd_cartas(estado: Estado, qtd_maxima: int) -> int:
        print(f'Escolha a quantidade de cartas para descartar, sendo no máximo {qtd_maxima} cartas.')
        while True:
            escolha_qtd = input('Digite a quantidade desejada: ')
            try:
                escolha_qtd = int(escolha_qtd)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 1 <= escolha_qtd <= qtd_maxima:
                print('Escolha inválida.')
                continue
            return escolha_qtd

    # Estratégia usada na habilidade da Ilusionista (escolha de qual carta descartar)
    @staticmethod
    def habilidade_ilusionista_descartar_carta(estado: Estado, qtd_cartas: int, i: int) -> int:
        print(f'Escolha as cartas para descartar. Faltam {qtd_cartas - i} cartas.')
        for j, carta in enumerate(estado.jogador_atual.cartas_distrito_mao):
            print(f'{j}: {carta.imprimir_tudo()}')
        while True:
            escolha_carta = input('Digite o número do distrito que deseja descartar: ')
            try:
                escolha_carta = int(escolha_carta)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_carta < len(estado.jogador_atual.cartas_distrito_mao):
                print('Escolha inválida.')
                continue
            return escolha_carta

    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    def habilidade_senhor_da_guerra_destruir(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        print(f'0: Não desejo destruir nenhum distrito.')
        for i, (carta, jogador) in enumerate(distritos_para_destruir):
            print(f'{i + 1}: {carta.imprimir_tudo()} - Jogador: {jogador.nome}')
        while True:
            escolha_destruir = input('Digite o número do distrito que deseja destruir: ')
            try:
                escolha_destruir = int(escolha_destruir)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_destruir <= len(distritos_para_destruir):
                print('Escolha inválida.')
                continue
            return escolha_destruir

    # Estratégia usada na ação do Laboratório
    @staticmethod
    def laboratorio(estado: Estado) -> int:
        for i, carta in enumerate(estado.jogador_atual.cartas_distrito_mao):
            print(f'{i}: {carta.imprimir_tudo()}')
        while True:
            escolha_carta = input('Digite o número do distrito que deseja descartar pelo ouro: ')
            try:
                escolha_carta = int(escolha_carta)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_carta < len(estado.jogador_atual.cartas_distrito_mao):
                print('Escolha inválida.')
                continue
            return escolha_carta
