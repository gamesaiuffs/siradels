# Imports
from abc import abstractmethod
from Estado import Estado
from Jogador import Jogador
from Tabuleiro import Tabuleiro
from classes.TipoDistrito import TipoDistrito

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

class ColetarCartas(Acao):
    def __init__(self):
        super().__init__('Colete 2 cartas do baralho e escolha uma.')

    @staticmethod
    def ativar_efeito(estado: Estado, jogador_alvo: Jogador):
        escolherCartas = estado.tabuleiro.baralho_distritos[0:2]
        estado.tabuleiro.baralho_distritos.pop()
        estado.tabuleiro.baralho_distritos.pop()

        print(escolherCartas[0])
        print(escolherCartas[1])

        escolha = int(input("Digite 1 para a primeira opção, 2 para a segunda: "))
        if escolha == 1:
            estado.jogadores[estado.jogadores.index(jogador_alvo)].cartas_distrito_mao.append(escolherCartas[0])
            estado.tabuleiro.baralho_distritos.append(escolherCartas[0])
        else:
            estado.jogadores[estado.jogadores.index(jogador_alvo)].cartas_distrito_mao.append(escolherCartas[1])
            estado.tabuleiro.baralho_distritos.append(escolherCartas[0])

class ConstruirDistrito(Acao):
    def __init__(self):
        super().__init__('Escolha um distrito para construir.')

    @staticmethod
    def ativar_efeito(estado: Estado, jogador_alvo: Jogador):
        for i in range(len(estado.jogadores[estado.jogadores.index(jogador_alvo)].cartas_distrito_mao)):
            print(f"{i+1}: {estado.jogadores[estado.jogadores.index(jogador_alvo)].cartas_distrito_mao[i]}")

        escolha = int(input("Digite o número do distrito que deseja construir: "))
        estado.jogadores[estado.jogadores.index(jogador_alvo)].distritos_construidos.append(estado.jogadores[estado.jogadores.index(jogador_alvo)].cartas_distrito_mao[escolha-1])
        estado.jogadores[estado.jogadores.index(jogador_alvo)].ouro -= estado.jogadores[estado.jogadores.index(jogador_alvo)].cartas_distrito_mao[escolha-1].valor_do_distrito
        estado.jogadores[estado.jogadores.index(jogador_alvo)].cartas_distrito_mao.pop(escolha-1)


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

        jogador_escolhido = int(input())

        for cartas_disponiveis_mao in range(len(estado.jogadores[jogador_escolhido-1].cartas_distrito_mao)):
            print(estado.jogadores[jogador_escolhido-1].cartas_distrito_mao[cartas_disponiveis_mao])

        carta_escohida = int(input('Carta escolhida: '))
        estado.jogadores[estado.jogadores.index(jogador_alvo)].cartas_distrito_mao.append(estado.jogadores[jogador_escolhido-1].cartas_distrito_mao[carta_escohida])


class EfeitoRei(Acao):
    def __init__(self):
        super().__init__('Pegue a coroa. (Receba 1 ouro para cada distrito NOBRE contruído)')

    @staticmethod
    def ativar_efeito(estado: Estado, jogador_alvo: Jogador):
        
        for ver_distritos_construidos in range(len(jogador_alvo.distritos_construidos)):
            if jogador_alvo.distritos_construidos[ver_distritos_construidos] == TipoDistrito.Nobre:
                estado.jogadores[estado.jogadores.index(jogador_alvo)].ouro += 1
        estado.jogadores[estado.jogadores.index(jogador_alvo)].rei = True

class EfeitoNavegadora(Acao):
    def __init__(self):
        super().__init__('Colete 4 ouros extras ou 4 cartas extras.')

    @staticmethod
    def ativar_efeito(estado: Estado, jogador_alvo: Jogador):
        #finalizar habilidade
