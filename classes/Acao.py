# Imports
from abc import abstractmethod
from Estado import Estado
from Jogador import Jogador

class Acao:
    # Construtor
    def __init__(self, descricao: str):
        self.descricao = descricao

    # To String
    def __str__(self):
        return f'descrição do efeito: {self.descricao}'

    @staticmethod
    @abstractmethod
    def ativar_efeito(estado: Estado, jogador: Jogador) -> Estado:
        pass

class ColetarOuro(Acao):
    def __init__(self):
        super().__init__('Colete 2 ouros do banco.')

    @staticmethod
    def ativar_efeito(estado: Estado, jogador_alvo: Jogador):
        estado.jogadores[estado.jogadores.index(jogador_alvo)].ouro += 2

class EfeitoAssassino(Acao):
    def __init__(self):
        super().__init__('Anuncie um personagem que você deseja assassinar. O personagem assassinado perde o turno.')

    @staticmethod
    def ativar_efeito(estado: Estado, jogador_alvo: Jogador):
        estado.jogadores[estado.jogadores.index(jogador_alvo)].morto = True

class EfeitoLadrao(Acao):
    def __init__(self):
        super().__init__('Anuncie um personagem que você deseja roubar. O personagem roubado entrega todo seu ouro ao ladrão.')

    @staticmethod
    def ativar_efeito(estado: Estado, jogador_alvo: Jogador):
        estado.jogadores[estado.jogadores.index(jogador_alvo)].roubado = True

class EfeitoMago(Acao):
    def __init__(self):
        super().__init__('Escolha um jogador para ver sua mão de distritos, em seguida, escolha uma carta e pague para construí-la imediaamente ou adiciona-a à sua mão. (Você pode construir distritos idênticos)')

    @staticmethod
    def ativar_efeito(estado: Estado, jogador_alvo: Jogador):
        for numero_jogadores in range(len(estado.jogadores)):
            print(estado.jogadores[numero_jogadores])

        jogador_escolhido = input()

        for cartas_disponiveis_mao in range(len(estado.jogadores[jogador_escolhido-1].cartas_distrito_mao)):
            print(estado.jogadores[jogador_escolhido-1].cartas_distrito_mao[cartas_disponiveis_mao])

        carta_escohida = input('Carta escolhida: ')
        estado.jogadores[estado.jogadores.index(jogador_alvo)].cartas_distrito_mao.append(estado.jogadores[jogador_escolhido-1].cartas_distrito_mao[carta_escohida])

class EfeitoRei(Acao):
    def __init__(self):
        super().__init__('Pegue a coroa. (Ganhe 1 ouro para cada um dos seus distritos NOBRES)')

    @staticmethod
    def ativar_efeito()