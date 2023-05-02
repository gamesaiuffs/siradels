from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.model.Jogador import Jogador
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado


class EstrategiaManual(Estrategia):
    def __init__(self):
        super().__init__('Manual.')

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
    def construir_distrito(estado: Estado,
                           distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_cardeal: list[CartaDistrito],
                           distritos_para_construir_necropole: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[CartaDistrito],
                           distritos_para_construir_estrutura: list[CartaDistrito]) -> int:
        print(f'0: Não desejo construir nenhum distrito.')
        i = 0
        for carta in distritos_para_construir:
            i += 1
            print(f'{i}: {carta.imprimir_tudo()}')
        for carta, jogador in distritos_para_construir_cardeal:
            i += 1
            print(f'{i}: {carta.imprimir_tudo()} - Usar efeito do Cardeal no jogador: {jogador.nome}')
        for carta, distrito in distritos_para_construir_necropole:
            i += 1
            print(f'{i}: {carta.imprimir_tudo()} - Distrito para destruir: {distrito.nome_do_distrito}')
        for carta, qtd_ouro, qtd_cartas in distritos_para_construir_covil_ladroes:
            i += 1
            print(f'{i}: {carta.imprimir_tudo()} - Custo em ouro: {qtd_ouro} - Custo em cartas da mão: {qtd_cartas}')
        for carta in distritos_para_construir_estrutura:
            i += 1
            print(f'{i}: {carta.imprimir_tudo()} - Distrito para destruir: Estrutura')
        while True:
            escolha_construir = input('Digite o número do distrito que deseja construir: ')
            try:
                escolha_construir = int(escolha_construir)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_construir <= len(distritos_para_construir) + len(distritos_para_construir_cardeal) + \
                    len(distritos_para_construir_necropole) + len(distritos_para_construir_covil_ladroes) + len(distritos_para_construir_estrutura):
                print('Escolha inválida.')
                continue
            return escolha_construir

    # Estratégia usada na ação de construir distritos (efeito Cardeal)
    @staticmethod
    def construir_distrito_cardeal(estado: Estado, diferenca: int, i: int) -> int:
        print(f'Escolha as cartas que trocará pelo ouro recebido do jogador escolhido. Faltam {diferenca - i} cartas.')
        for j, carta in enumerate(estado.jogador_atual.cartas_distrito_mao):
            print(f'{j}: {carta.imprimir_tudo()}')
        while True:
            escolha_carta = input('Digite o número do distrito que deseja trocar pelo ouro: ')
            try:
                escolha_carta = int(escolha_carta)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_carta < len(estado.jogador_atual.cartas_distrito_mao):
                print('Escolha inválida.')
                continue
            return escolha_carta

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

    # Estratégia usada na habilidade do Mago (escolha do jogador alvo)
    @staticmethod
    def habilidade_mago_jogador(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        print('Jogadores:')
        for i, jogador in enumerate(opcoes_jogadores):
            print(f'{i}: {jogador.nome}')
        while True:
            escolha_jogador = input('Digite o número do jogador que deseja olhar a mão e pegar 1 carta: ')
            try:
                escolha_jogador = int(escolha_jogador)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_jogador < len(opcoes_jogadores):
                print('Escolha inválida.')
                continue
            return escolha_jogador

    # Estratégia usada na habilidade do Mago (escolha da carta da mão)
    @staticmethod
    def habilidade_mago_carta(estado: Estado, opcoes_cartas: list[CartaDistrito]) -> int:
        print('Mão do jogador escolhido:')
        for i, carta in enumerate(opcoes_cartas):
            print(f'{i}: {carta.imprimir_tudo()}')
        while True:
            escolha_carta = input('Digite o número da carta que deseja pegar para construir ou para sua mão: ')
            try:
                escolha_carta = int(escolha_carta)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_carta < len(opcoes_cartas):
                print('Escolha inválida.')
                continue
            return escolha_carta

    # Estratégia usada na habilidade da Navegadora
    @staticmethod
    def habilidade_navegadora(estado: Estado) -> int:
        while True:
            escolha_recurso = input('Qual recurso deseja ganhar? (0 - ouro, 1 - cartas): ')
            try:
                escolha_recurso = int(escolha_recurso)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_recurso <= 1:
                print('Escolha inválida.')
                continue
            return escolha_recurso

    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    def habilidade_senhor_da_guerra(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador, int)]) -> int:
        print(f'0: Não desejo destruir nenhum distrito.')
        for i, (carta, jogador, muralha) in enumerate(distritos_para_destruir):
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

    # Estratégia usada na ação do Arsenal
    @staticmethod
    def arsenal(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
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
            if not 0 < escolha_destruir <= len(distritos_para_destruir):
                print('Escolha inválida.')
                continue
            return escolha_destruir

    # Estratégia usada na ação do Museu
    @staticmethod
    def museu(estado: Estado) -> int:
        # Mostra opções ao jogador
        for i, carta in enumerate(estado.jogador_atual.cartas_distrito_mao):
            print(f'{i}: {carta.imprimir_tudo()}')
        while True:
            escolha_carta = input('Digite o número do distrito que deseja colocar no Museu: ')
            try:
                escolha_carta = int(escolha_carta)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_carta < len(estado.jogador_atual.cartas_distrito_mao):
                print('Escolha inválida.')
                continue
            return escolha_carta
