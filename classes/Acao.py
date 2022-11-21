# Imports
from abc import abstractmethod

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
        for i, carta in range(len(estado.jogador_atual().cartas_distrito_mao)):
            if not carta.nome_do_distrito == 'cofre secreto':
                print(f"{i+1}: {carta}")

        escolha = int(input("Digite o número do distrito que deseja construir: "))
        if estado.jogador_atual().ouro >= estado.jogador_atual().cartas_distrito_mao[escolha-1].valor_do_distrito:

            estado.jogador_atual().pontuacao += estado.jogador_atual().cartas_distrito_mao[escolha-1].valor_do_distrito

            estado.jogador_atual().ouro -= estado.jogador_atual().cartas_distrito_mao[escolha-1].valor_do_distrito
            estado.jogador_atual().distritos_construidos.append(estado.jogador_atual().cartas_distrito_mao[escolha-1])
            estado.jogador_atual().cartas_distrito_mao.pop(escolha-1)
            estado.jogador_atual().construiu = True
            estado.jogador_atual().ouro_gasto = estado.jogador_atual().cartas_distrito_mao[escolha-1].valor_do_distrito

            if len(estado.jogador_atual().distritos_construidos) == 7:
                estado.jogador_atual().terminou = True

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
        super().__init__('Escolha um jogador para ver sua mão de distritos, em seguida, escolha uma carta e pague para construí-la imediatamente ou adiciona-a à sua mão. (Você pode construir distritos idênticos)')

    @staticmethod
    def ativar_efeito(estado: Estado):
        
        for numero_jogadores in range(len(estado.jogadores)):
            print(estado.jogadores[numero_jogadores])

        jogador_escolhido = int(input("selecione o jogador: "))

        for i, carta in range(len(estado.jogadores[jogador_escolhido-1].cartas_distrito_mao)):
            if not carta.nome_do_distrito == 'cofre secreto':
                print(f"{i+1}: {carta}")

        carta_escohida = int(input('Carta escolhida: '))
        estado.jogador_atual().cartas_distrito_mao.append(estado.jogadores[jogador_escolhido-1].cartas_distrito_mao[carta_escohida-1])
        estado.jogadores[jogador_escolhido-1].cartas_distrito_mao.pop(carta_escohida-1)

        deseja_construir = input("deseja construir imediatamente? (s/n) ").lower()
        if deseja_construir == "s":
            estado.jogador_atual().distritos_construidos.append(estado.jogador_atual().cartas_distrito_mao[-1])
            estado.jogador_atual().ouro -= estado.jogador_atual().cartas_distrito_mao[-1].valor_do_distrito
            estado.jogador_atual().pontuacao += estado.jogador_atual().cartas_distrito_mao[-1].valor_do_distrito
            estado.jogador_atual().cartas_distrito_mao.remove(estado.jogador_atual().cartas_distrito_mao[-1])
            if len(estado.jogador_atual().distritos_construidos) == 7:
                estado.jogador_atual().terminou = True


class EfeitoRei(Acao):
    def __init__(self):
        super().__init__('Pegue a coroa. (Receba 1 ouro para cada distrito NOBRE contruído)')

    @staticmethod
    def ativar_efeito(estado: Estado):
        
        for ver_distritos_construidos in range(len(estado.jogador_atual().distritos_construidos)):
            if estado.jogador_atual().distritos_construidos[ver_distritos_construidos] == TipoDistrito.Nobre:
                estado.jogador_atual().ouro += 1
                estado.jogador_atual().pontuacao += 1


class EfeitoCardealAtivo(Acao):
    def __init__(self):
        super().__init__('Se você não tiver ouro o suficiente para construir um distrito, troque suas cartas pelo ouro de outro jogador. (1 carta: 1 ouro)')

    @staticmethod
    def ativar_efeito(estado: Estado):
        
        divida = 0
        distritos_trocados = []

        for i, mao_propria in enumerate(estado.jogador_atual().cartas_distrito_mao):
            if not mao_propria.nome_do_distrito == 'cofre secreto':
                print(f"{i+1}: {mao_propria}")

        escolha_distrito = int(input("Digite o número do distrito que deseja trocar por ouro: "))
        for i in estado.jogador_atual().cartas_distrito_mao:
            if estado.jogador_atual().cartas_distrito_mao[escolha_distrito-1].valor_do_distrito > estado.jogador_atual().ouro:
                divida = estado.jogador_atual().cartas_distrito_mao[escolha_distrito-1].valor_do_distrito-estado.jogador_atual().ouro
                print(f"Faltam: {divida} para o distrito {i+1}")

            else:
                break

        for i, jogador in enumerate(estado.jogadores):
            print(f"{i+1}: {jogador.nome}")

        if len(estado.jogador_atual().cartas_distrito_mao) < divida:
            return
        
        for i, jogador in enumerate(estado.jogadores):
            print(f"{i+1}: {jogador.nome}")
        while True:
            if all([jogador.ouro < divida for jogador in estado.jogadores]):
                return

            jogador_escolhido = int(input("Escolha o jogador alvo: "))
            if estado.jogadores[jogador_escolhido-1].ouro >= divida:
                break
        for i in range(divida+1):
            for i, mao_propria in enumerate(estado.jogador_atual().cartas_distrito_mao):
                print(f"{i+1}: {mao_propria}")
            
            while True:
                selecionar_distritos = int(input("\nSelecione os distritos a serem trocados: "))
                if all([distrito != selecionar_distritos for distrito in distritos_trocados]):
                    distritos_trocados.append(selecionar_distritos) 
                    break
        
        estado.jogador_atual().distritos_construidos.append(estado.jogador_atual().cartas_distrito_mao[escolha_distrito])
        estado.jogador_atual().pontuacao += estado.jogador_atual().cartas_distrito_mao[escolha_distrito].valor_do_distrito
        for i in distritos_trocados:
            estado.jogadores[jogador_escolhido-1].ouro -= divida
            estado.jogadores[jogador_escolhido-1].distritos_construidos.append(estado.jogador_atual().cartas_distrito_mao[i])
            estado.jogador_atual().cartas_distrito_mao.remove(i)

        if len(estado.jogador_atual().distritos_construidos) == 7:
            estado.jogador_atual().terminou = True


class EfeitoCardealPassivo(Acao):
    def __init__(self):
        super().__init__('Ganhe 1 carta para cada distrito RELIGIOSO construído')

    @staticmethod
    def ativar_efeito(estado: Estado):
        for ver_distritos_construidos in range(len(estado.jogador_atual().distritos_construidos)):
            if estado.jogador_atual().distritos_construidos[ver_distritos_construidos] == TipoDistrito.Religioso:
                distrito_pescado = estado.tabuleiro.baralho_distritos.pop()
                estado.jogadores[estado.jogadores.index(estado.jogador_atual())].cartas_distrito_mao.append(distrito_pescado)



class AbrigoParaPobres(Acao):
    def __init__(self):
        super().__init__("Se não houver ouro no seu tesouro no fim do seu turno, ganhe 1 ouro.")

    @staticmethod
    def ativar_efeito(estado: Estado):
        estado.jogador_atual().ouro += 1 


class TesouroImperial(Acao):
    def __init__(self):
        super().__init__("Ao final da partida, marque um ponto extra para cada ouro em seu tesouro.")

    @staticmethod
    def ativar_efeito(estado: Estado):
        estado.jogador_atual().pontuacao += estado.jogador_atual().ouro 


class CofreSecreto(Acao):
    def __init__(self):
        super().__init__("O Cofre Secreto não pode ser construído. Ao final da partida, revele o Cofre Secreto da sua mão para marcar 3 pontos.")

    @staticmethod
    def ativar_efeito(estado: Estado):
        estado.jogador_atual().pontuacao += 3 


class Laboratorio(Acao):
    def __init__(self):
        super().__init__("Uma vez por turno, descarte 1 carta da sua mao para ganhar 2 ouros.")

    @staticmethod
    def ativar_efeito(estado: Estado):
        # Printar distritos disponíveis para troca
        for index, distrito in enumerate(estado.jogador_atual().cartas_distrito_mao):
            print(f"""ID: {index+1}
            \tNome: {distrito.nome_do_distrito}
            \tValor: {distrito.valor_do_distrito}
            \ttipo: {distrito.tipo_de_distrito}
            """)

        # Escolher qual carta será trocada por 2 ouros
        while True:
            print("Escolha uma carta para descartar [ID]:", end=" ")
            carta = int(input()) - 1
            if carta >= 1 and carta <= len(estado.jogador_atual().cartas_distrito_mao) + 1: break
            else: 
                print("Escolha inválida! Escolha um ID válido!")

        # Remover carta escolhida e adicionar os 2 ouros
        carta_descartada = estado.jogador_atual().cartas_distrito_mao.pop(carta)
        estado.tabuleiro.baralho_distritos.append(carta_descartada)
        estado.jogador_atual().ouro += 2


class EfeitoNavegadora(Acao):
    def __init__(self):
        super().__init__('Ganhe 4 ouros extras ou 4 cartas extras.Você não pode construir distritos.')

    @staticmethod
    def ativar_efeito(estado: Estado):
        escolha = int(input("verifica escolha"))
        if escolha ==1:
            estado.jogador_atual().ouro +=4
            print(estado.jogador_atual().ouro)
        elif escolha ==2:
            estado.jogador_atual().cartas_distrito_mao.append(estado.tabuleiro.baralho_distritos[0:4])
            for i in range(4):
                estado.tabuleiro.baralho_distritos.pop(i)#testar
        else:
            pass
#----------
class EfeitoSenhordaGuerra(Acao):
    def __init__(self):
        super().__init__("Destrua 1 distrito pagando 1 ouro a menos que o custo dele.(Ganhe 1 ouro para cada um dos seus distritos militares).")
    @staticmethod
    def ativar_efeito(estado: Estado):
        #da ouro por militar
        #implementar distrito especial "muralha"
        multa_muralha = 0

        for ver_distritos_construidos in range(len(estado.jogador_atual().distritos_construidos)):
            if estado.jogador_atual().distritos_construidos[ver_distritos_construidos] == TipoDistrito.Militar:
                estado.jogadores[estado.jogadores.index(estado.jogador_atual())].ouro += 1
                estado.jogador_atual().pontuacao += 1
        #efeito destruir
        for i, jogador in enumerate(estado.jogadores):
            for distritos in jogador.distritos_construidos:
                print(f"{i+1}: {distritos}", end=" | ")

            print("\n")
        escolha_jogador = input("Deseja destruir? (s/n)").lower()
        if escolha_jogador == "s":
            for numero_jogadores,jogador in enumerate(estado.jogadores):
                print(numero_jogadores+1)
                print(jogador)
            jogador_escolhido=int(input("Escolha jogador:"))
            for numero_cartas,carta in enumerate(estado.jogadores[jogador_escolhido-1].distritos_construidos):
                print(numero_cartas,carta)

                if carta == 'muralha':
                    multa_muralha += 1

            destruir_carta=int(input("Digite o distrito que deseja destruir:"))
            if estado.jogadores[jogador_escolhido-1].terminou == False:
                if estado.jogador_atual().ouro >= jogador.distritos_construidos[jogador_escolhido-1].valor_do_distrito-1+multa_muralha:#falta colocar valor do distrito
                    estado.jogador_atual().ouro -= jogador.distritos_construidos[jogador_escolhido-1].valor_do_distrito-1+multa_muralha
                    estado.jogadores[jogador_escolhido-1].pontuacao -= jogador.distritos_construidos[jogador_escolhido-1].valor_do_distrito-1
                    estado.jogadores[jogador_escolhido-1].distritos_construidos.pop(destruir_carta)
                #testar
            else:
                print("o jogador possui 7 distritos construídos!")
#-----------
class EfeitoAlquimista(Acao):
    def __init__(self):
        super().__init__("Ao final do seu turno,você pega de volta todo o ouro pago para construir distritos neste turno.Você não pode pagar mais ouro do que tem.")
    @staticmethod
    def ativar_efeito(estado: Estado):
        if estado.jogador_atual().construiu or estado.jogador_atual().construiu_estabulo:
            estado.jogador_atual().ouro += estado.jogador_atual().ouro_gasto



class PortalDoDragao(Acao):
    def __init__(self):
        super().__init__('Ao final da partida, marque 2 pontos extras')
    
    @staticmethod
    def ativar_efeito(estado: Estado):
        estado.jogadores[estado.jogadores.index(estado.jogador_atual())].pontuacao += 2


class Necropole(Acao):
    def __init__(self):
        super().__init__('Você pode construir a Necrópole destruindo 1 distrito na sua cidade, em vez de pagar o custo da Necrópole')
    
    @staticmethod
    def ativar_efeito(estado: Estado):
        for i, distrito in enumerate(estado.jogador_atual().distritos_construidos):
            print(f"{i+1}: {distrito.nome_do_distrito}")
        
        escolha = int(input("Digite o número do distrito que deseja destruir: "))
        for index, distrito in enumerate(estado.jogador_atual().distritos_construidos):
            if distrito.nome_do_distrito == 'necropole':
                distrito_encontrado = estado.jogador_atual().distritos_construidos.pop(escolha-1)
                estado.tabuleiro.baralho_distritos.append(distrito_encontrado)
                necropole = estado.jogador_atual().cartas_distrito_mao.pop(index)
                estado.jogador_atual().distritos_construidos.append(necropole)
                estado.jogador_atual().pontuacao += necropole.valor_do_distrito
                estado.jogador_atual().pontuacao -= distrito_encontrado.valor_do_distrito


class CovilDosLadroes(Acao):
    def __init__(self):
        super().__init__('Pague parte ou todo o custo do Covil dos Ladrões com cartas da sua mão, em vez de ouro, a uma taxa de 1 carta: 1 ouro')
    
    @staticmethod
    def ativar_efeito(estado: Estado):
        n_cartas_mao = len(estado.jogador_atual().cartas_distrito_mao) - 1
        n = int(input(f"Deseja construir o Covil dos Ladrões com quantas cartas? (0-{6 if n_cartas_mao >= 6 else n_cartas_mao})"))
        restante = n

        for i in range(n):
            for i, distrito in enumerate(estado.jogador_atual().cartas_distrito_mao):
                if i == 0 and distrito.nome_do_distrito == 'covil dos ladroes':
                    covil = estado.jogador_atual().cartas_distrito_mao.pop(i)
                    estado.jogador_atual().distritos_construidos.append(covil)
                print(f"{i+1}: {distrito.nome_do_distrito}")
            escolha = input(f"Informe o distrito: ({n - i} restantes)")
            estado.jogador_atual().cartas_distrito_mao.pop(escolha-1)
            restante -= 1
        estado.jogador_atual().ouro -= restante
        


#continuar pontuação parcial !!!!
 
class Teatro(Acao):
    def __init__(self):
        super().__init__('Ao final de cada fase de escolha, você pode trocar a sua carta de personagem escolhida com a carta de personagem de um oponente')

    @staticmethod
    def ativar_efeito(estado: Estado):
        for i, jogador in enumerate(estado.jogadores):
            if jogador != estado.jogador_atual():
                print(f"{i+1}: {jogador.nome}")
        
        escolha = int(input('Digite o número do jogador que deseja trocar o personagem: '))
        
        personagem_temp = estado.jogador_atual().personagem
        estado.jogador_atual().personagem = estado.jogadores[escolha].personagem
        estado.jogadores[escolha].personagem = personagem_temp
    

class MinaDeOuro(Acao):
    def __init__(self):
        super().__init__('Se você optar por ganhar ouro ao coletar recursos, ganhe 1 ouro extra.')
    
    @staticmethod
    def ativar_efeito(estado: Estado):
        estado.jogador_atual().ouro += 1


class EscolaDeMagia(Acao):
    def __init__(self):
        super().__init__('Ao usar habilidades que obtêm recursos pelos seus distritos, a Escola de Magia vale como o tipo de distrito à sua escolha.')
    
    @staticmethod
    def ativar_efeito(estado: Estado):
        for i, tipo in enumerate(TipoDistrito):
            print(f"{i+1}: {tipo._name_}")
        
        escolha = int(input('Digite o número do tipo de distrito'))
        for distrito in estado.jogador_atual().distritos_construidos:
            if distrito.nome_do_distrito == 'escola de magia':
                estado.jogador_atual().distritos_construidos.tipo_do_distrito = TipoDistrito(escolha)


class Estrutura(Acao):
    def __init__(self):
        super().__init__('Você pode construir um distrito destruindo a Estrutura, em vez de pagar os custos do distrito em questão.')

    @staticmethod
    def ativar_efeito(estado: Estado):
        for i, distrito in enumerate(estado.jogador_atual().cartas_distrito_mao):
            if not distrito.nome_do_distrito == 'cofre secreto':
                print(f"{i+1}: {distrito.nome_do_distrito}")
        
        escolha = int(input("Digite o número do distrito que deseja construir: "))
        for distrito in estado.jogador_atual().distritos_construidos:
            if distrito.nome_do_distrito == 'estrutura':
                estado.jogador_atual().distritos_construidos.remove(distrito)
                estado.tabuleiro.baralho_distritos.append(distrito)
                estado.jogador_atual().pontuacao -= distrito.valor_do_distrito
                break

        distrito = estado.jogador_atual().cartas_distrito_mao.pop(escolha)
        estado.tabuleiro.baralho_distritos.append(distrito)
        estado.jogador_atual().pontuacao += distrito.valor_do_distrito

class PassarTurno(Acao):
    def __init__(self, estado: Estado):
        super().__init__("Passar turno")
        estado.turno += 1
        jogador = estado.jogador_atual()
        jogador.ouro_gasto, jogador.roubado, jogador.morto, jogador.construiu, jogador.acoes_realizadas = 0, False, False, False, [0 for _ in range(23)]

class Estabulo(Acao):
    def __init__(self):
        super().__init__("A construção dos Estabulos não conta para o seu limite de construção neste turno.")

        @staticmethod
        def ativar_efeito( estado: Estado):
            for estabulo in estado.jogador_atual().distritos_construidos:
                if estabulo.nome_do_distrito == "estabulo":
                    
                    if estado.jogador_atual().ouro >= estabulo.valor_do_distrito:

                        estado.jogador_atual().pontuacao += estabulo.valor_do_distrito

                        estado.jogador_atual().ouro -= estabulo.valor_do_distrito
                        estado.jogador_atual().distritos_construidos.append(estabulo)
                        estado.jogador_atual().cartas_distrito_mao.remove(estabulo)
                        estado.jogador_atual().construiu_estabulo = True
                        estado.jogador_atual().ouro_gasto = estabulo.valor_do_distrito

                        if len(estado.jogador_atual().distritos_construidos) == 7:
                            estado.jogador_atual().terminou = True

                    else:
                        print("Ouro insuficiente!")
                    break
