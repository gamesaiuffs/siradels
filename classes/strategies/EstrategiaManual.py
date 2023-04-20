from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
from classes.model.Acao import Acao


class EstrategiaManual(Estrategia):

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(jogador: Jogador, estado: Estado) -> int:
        # Informa opções ao jogador
        print('\n---------| Personagens |--------')
        for i, personagem in enumerate(estado.tabuleiro.baralho_personagens):
            print(f'{i}: {personagem}')
        # Aguarda escolha do jogador
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
    def escolher_acao(jogador: Jogador, estado: Estado, acoes: list[Acao]) -> int:
        # Informa opções ao jogador
        print('Ações disponíveis: ')
        for i, acao in enumerate(acoes):
            print(f'\t{i}: - {acao.descricao}')
        # Aguarda escolha do jogador
        while True:
            escolha_acao = input('Escolha sua ação: ')
            try:
                escolha_acao = int(escolha_acao)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_acao < len(acoes):
                print('Escolha inválida.')
                continue
            return escolha_acao
