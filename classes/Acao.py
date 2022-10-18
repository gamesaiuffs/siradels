# Imports
from abc import abstractmethod

from importlib_metadata import distribution
from Estado import Estado
from Jogador import Jogador
from Tabuleiro import Tabuleiro
from TipoDistrito import TipoDistrito
from CartaDistrito import CartaDistrito

class Acao:
    # Construtor
    def __init__(self, descricao: str):
        self.descricao = descricao

    # To String
    def __str__(self):
        return f'{self.descricao}'

    @staticmethod
    @abstractmethod
    def ativar_efeito(estado: Estado):
        pass


class ColetarOuro(Acao):
    def __init__(self):
        super().__init__('Colete 2 ouros do banco.')

    @staticmethod
    def ativar_efeito(estado: Estado):
        estado.jogador_atual().ouro += 2


class ColetarCartas(Acao):
    def __init__(self):
        super().__init__('Colete 2 cartas do baralho e escolha uma.')

    @staticmethod
    def ativar_efeito(estado: Estado):
        escolherCartas = estado.tabuleiro.baralho_distritos[0:2]
        estado.tabuleiro.baralho_distritos.pop()
        estado.tabuleiro.baralho_distritos.pop()

        print(escolherCartas[0])
        print(escolherCartas[1])

        escolha = int(input("Digite 1 para a primeira opção, 2 para a segunda: "))
        if escolha == 1:
            estado.jogador_atual().cartas_distrito_mao.append(escolherCartas[0])
            estado.tabuleiro.baralho_distritos.append(escolherCartas[0])
        else:
            estado.jogador_atual().cartas_distrito_mao.append(escolherCartas[1])
            estado.tabuleiro.baralho_distritos.append(escolherCartas[0])


class ConstruirDistrito(Acao):
    def __init__(self):
        super().__init__('Escolha um distrito para construir.')

    @staticmethod
    def ativar_efeito(estado: Estado):
        for i in range(len(estado.jogador_atual().cartas_distrito_mao)):
            print(f"{i+1}: {estado.jogador_atual().cartas_distrito_mao[i]}")

        escolha = int(input("Digite o número do distrito que deseja construir: "))
        if estado.jogador_atual().ouro >= estado.jogador_atual().cartas_distrito_mao[escolha-1].valor_do_distrito:
            estado.jogador_atual().ouro -= estado.jogador_atual().cartas_distrito_mao[escolha-1].valor_do_distrito
            estado.jogador_atual().distritos_construidos.append(estado.jogador_atual().cartas_distrito_mao[escolha-1])
            estado.jogador_atual().cartas_distrito_mao.remove(escolha-1)
        else:
            print("Ouro insuficiente!")


class EfeitoAssassino(Acao):
    def __init__(self):
        super().__init__('Anuncie um personagem que você deseja assassinar. O personagem assassinado perde o turno.')

    @staticmethod
    def ativar_efeito(estado: Estado):
        for numero_jogadores in range(len(estado.jogadores)):
            print(estado.jogadores[numero_jogadores])

        jogador_escolhido = int(input())
        
        estado.jogadores[jogador_escolhido-1].morto = True


class EfeitoLadrao(Acao):
    def __init__(self):
        super().__init__('Anuncie um personagem que você deseja roubar. O personagem roubado entrega todo seu ouro ao ladrão.')

    @staticmethod
    def ativar_efeito(estado: Estado):
        for numero_jogadores in range(len(estado.jogadores)):
            print(estado.jogadores[numero_jogadores])
            
        jogador_escolhido = int(input())
        
        
        estado.jogadores[jogador_escolhido-1].roubado = True


class EfeitoMago(Acao):
    def __init__(self):
        super().__init__('Escolha um jogador para ver sua mão de distritos, em seguida, escolha uma carta e pague para construí-la imediaamente ou adiciona-a à sua mão. (Você pode construir distritos idênticos)')

    @staticmethod
    def ativar_efeito(estado: Estado):
        
        for numero_jogadores in range(len(estado.jogadores)):
            print(estado.jogadores[numero_jogadores])

        jogador_escolhido = int(input())

        for cartas_disponiveis_mao in range(len(estado.jogadores[jogador_escolhido-1].cartas_distrito_mao)):
            print(estado.jogadores[jogador_escolhido-1].cartas_distrito_mao[cartas_disponiveis_mao])

        carta_escohida = int(input('Carta escolhida: '))
        estado.jogador_atual().cartas_distrito_mao.append(estado.jogadores[jogador_escolhido-1].cartas_distrito_mao[carta_escohida-1])


class EfeitoRei(Acao):
    def __init__(self):
        super().__init__('Pegue a coroa. (Receba 1 ouro para cada distrito NOBRE contruído)')

    @staticmethod
    def ativar_efeito(estado: Estado):
        
        for ver_distritos_construidos in range(len(estado.jogador_atual().distritos_construidos)):
            if estado.jogador_atual().distritos_construidos[ver_distritos_construidos] == TipoDistrito.Nobre:
                estado.jogadores[estado.jogadores.index(estado.jogador_atual())].ouro += 1


class EfeitoCardealAtivo(Acao):
    def __init__(self):
        super().__init__('Se você não tiver ouro o suficiente para construir um distrito, troque suas cartas pelo ouro de outro jogador. (1 carta: 1 ouro)')

    @staticmethod
    def ativar_efeito(estado: Estado):
        
        divida = 0
        distritos_trocados = []

        for i, mao_propria in enumerate(estado.jogador_atual().cartas_distrito_mao):
            print(f"{i+1}: {mao_propria}")

        escolha_distrito = int(input("Digite o número do distrito que deseja trocar por ouro: "))
        for i in estado.jogador_atual().cartas_distrito_mao:
            if estado.jogador_atual().cartas_distrito_mao[escolha_distrito-1].valor_do_distrito > estado.jogador_atual().ouro:
                divida = estado.jogador_atual().cartas_distrito_mao[escolha_distrito-1].valor_do_distrito-estado.jogador_atual().ouro
                print(f"Faltam: {divida} para o distrito {i+1}")

            else:
                break

        for i, jogador in enumerate(estado.jogadores):
            print(f"{i+1}: {jogador}")

        jogador_escolhido = int(input("Escolha o jogador alvo: "))
        if estado.jogadores[jogador_escolhido-1].ouro >= divida and len(estado.jogador_atual().cartas_distrito_mao) >= divida+1:
            for i in range(divida+1):
                print("")
                selecionar_distritos = int(input("Selecione os distritos a serem trocados: "))
                distritos_trocados.append(selecionar_distritos)
            
            for i in distritos_trocados:
                estado.jogadores[jogador_escolhido-1].ouro -= divida
                estado.jogadores[jogador_escolhido].distritos_construidos.append(estado.jogador_atual().cartas_distrito_mao[i])
                estado.jogador_atual().cartas_distrito_mao.remove(i)
                estado.jogador_atual().distritos_construidos.append(i)


class EfeitoCardealPassivo(Acao):
    def __init__(self):
        super().__init__('Ganhe 1 carta para cada distrito RELIGIOSO construído')

    @staticmethod
    def ativar_efeito(estado: Estado):
        for ver_distritos_construidos in range(len(estado.jogador_atual().distritos_construidos)):
            if estado.jogador_atual().distritos_construidos[ver_distritos_construidos] == TipoDistrito.Religioso:
                distrito_pescado = estado.tabuleiro.baralho_distritos.pop()
                estado.jogadores[estado.jogadores.index(estado.jogador_atual())].cartas_distrito_mao.append(distrito_pescado)