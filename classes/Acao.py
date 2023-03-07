from Estado import Estado
from classes.enum.TipoDistrito import TipoDistrito
from classes.enum.TipoAcao import TipoAcao


class Acao:
    def __init__(self, descricao: str, tipo_acao: TipoAcao):
        self.descricao = descricao
        self.tipo_acao = tipo_acao

    def __str__(self):
        return f'{self.descricao}'

    def ativar(self, estado: Estado):
        estado.jogador_atual().acoes_realizadas[self.tipo_acao.value] = True


class ColetarOuro(Acao):
    def __init__(self):
        super().__init__('Pegue dois ouros do banco.', TipoAcao.ColetarOuro)

    def ativar(self, estado: Estado):
        if estado.jogador_atual().construiu_distrito('Mina de Ouro'):
            estado.jogador_atual().ouro += 1
        estado.jogador_atual().ouro += 2
        estado.jogador_atual().acoes_realizadas += self.tipo_acao
        super().ativar(estado)


class ColetarCartas(Acao):
    def __init__(self):
        super().__init__('Compre duas cartas do baralho de distritos, escolha uma e descarte a outra.', TipoAcao.ColetarCartas)

    def ativar(self, estado: Estado):
        cartas_compradas = estado.tabuleiro.baralho_distritos[:2]
        del estado.tabuleiro.baralho_distritos[:2]

        print("Carta 1:")
        print(cartas_compradas[0].imprimir_tudo())
        print("\nCarta 2:")
        print(cartas_compradas[1].imprimir_tudo())

        escolha = ''
        while escolha != '1' or escolha != '2':
            escolha = input("Escolha a carta (1 ou 2) que deseja ficar: ")
            if escolha == '1':
                estado.jogador_atual().cartas_distrito_mao.append(cartas_compradas[0])
                estado.tabuleiro.baralho_distritos.append(cartas_compradas[1])
            elif escolha == '2':
                estado.jogador_atual().cartas_distrito_mao.append(cartas_compradas[1])
                estado.tabuleiro.baralho_distritos.append(cartas_compradas[0])
            else:
                print("Escolha inválida.")
        super().ativar(estado)


class ConstruirDistrito(Acao):
    def __init__(self):
        super().__init__('Escolha um distrito para construir.')

    
    def ativar(self, estado: Estado):
        for i, carta in enumerate(estado.jogador_atual().cartas_distrito_mao):
            if not carta.nome_do_distrito == 'cofre secreto':
                print(f"{i + 1}: {carta.imprimir_tudo()}")

        escolha = int(input("Digite o número do distrito que deseja construir: "))
        if estado.jogador_atual().ouro >= estado.jogador_atual().cartas_distrito_mao[escolha - 1].valor_do_distrito:

            estado.jogador_atual().pontuacao += estado.jogador_atual().cartas_distrito_mao[
                escolha - 1].valor_do_distrito

            estado.jogador_atual().ouro -= estado.jogador_atual().cartas_distrito_mao[escolha - 1].valor_do_distrito
            estado.jogador_atual().distritos_construidos.append(estado.jogador_atual().cartas_distrito_mao[escolha - 1])
            estado.jogador_atual().ouro_gasto = estado.jogador_atual().cartas_distrito_mao[
                escolha - 1].valor_do_distrito
            estado.jogador_atual().cartas_distrito_mao.pop(escolha - 1)
            estado.jogador_atual().construiu = True

            if len(estado.jogador_atual().distritos_construidos) == 7:
                estado.jogador_atual().terminou = True
                
            estado.jogador_atual().acoes_realizadas[TipoAcao.ConstruirDistrito.value] = 1

        else:
            print("Ouro insuficiente!")


class EfeitoAssassino(Acao):
    def __init__(self):
        super().__init__('Anuncie um personagem que você deseja assassinar. O personagem assassinado perde o turno.')

    
    def ativar(self, estado: Estado):
        # for numero_jogadores in range(len(estado.jogadores)):
        #     print(estado.jogadores[numero_jogadores])

        # jogador_escolhido = int(input())

        # estado.jogadores[jogador_escolhido - 1].morto = True
        # estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoAssassino.value] = 1
        print("Rank do personagem: ")

        personagem_escolhido = int(input())
        
        for index, jogador in enumerate(estado.jogadores):
            if jogador.personagem.rank == personagem_escolhido:
                jogador_escolhido = jogador
                break
            else:
                jogador_escolhido = None
                
        if jogador_escolhido != None:
            print(jogador_escolhido)
            estado.jogadores[index].morto = True
        
        estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoAssassino.value] = 1


class EfeitoLadrao(Acao):
    def __init__(self):
        super().__init__(
            'Anuncie um personagem que você deseja roubar. O personagem roubado entrega todo seu ouro ao ladrão.')

    
    def ativar(self, estado: Estado):
        print("Rank do personagem: ")

        personagem_escolhido = int(input())
        
        for index, jogador in enumerate(estado.jogadores):
            if jogador.personagem.rank == personagem_escolhido:
                jogador_escolhido = jogador
                break
            else:
                jogador_escolhido = None
                
        if jogador_escolhido != None:
            print(jogador_escolhido)
            estado.jogadores[index].roubado = True
        
        estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoLadrao.value] = 1


class EfeitoMago(Acao):
    def __init__(self):
        super().__init__(
            'Escolha um jogador para ver sua mão de distritos, em seguida, '
            'escolha uma carta e pague para construí-la imediatamente ou adiciona-a à sua mão. '
            '(Você pode construir distritos idênticos)')

    
    def ativar(self, estado: Estado):

        for numero_jogadores in range(len(estado.jogadores)):
            print(estado.jogadores[numero_jogadores])

        jogador_escolhido = int(input("selecione o jogador: "))

        for i, carta in enumerate(estado.jogadores[jogador_escolhido - 1].cartas_distrito_mao):
            if not carta.nome_do_distrito == 'cofre secreto':
                print(f"{i + 1}: {carta}")

        carta_escohida = int(input('Carta escolhida: '))
        estado.jogador_atual().cartas_distrito_mao.append(
            estado.jogadores[jogador_escolhido - 1].cartas_distrito_mao[carta_escohida - 1])
        estado.jogadores[jogador_escolhido - 1].cartas_distrito_mao.pop(carta_escohida - 1)

        deseja_construir = input("deseja construir imediatamente? (s/n) ").lower()
        if deseja_construir == "s":
            estado.jogador_atual().distritos_construidos.append(estado.jogador_atual().cartas_distrito_mao[-1])
            estado.jogador_atual().ouro -= estado.jogador_atual().cartas_distrito_mao[-1].valor_do_distrito
            estado.jogador_atual().pontuacao += estado.jogador_atual().cartas_distrito_mao[-1].valor_do_distrito
            estado.jogador_atual().cartas_distrito_mao.remove(estado.jogador_atual().cartas_distrito_mao[-1])
            if len(estado.jogador_atual().distritos_construidos) == 7:
                estado.jogador_atual().terminou = True
        estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoMago.value] = 1


class EfeitoRei(Acao):
    def __init__(self):
        super().__init__('Receba 1 ouro para cada distrito NOBRE contruído')

    
    def ativar(self, estado: Estado):
        for _, distrito in enumerate(estado.jogador_atual().distritos_construidos):
            if distrito.tipo_de_distrito == TipoDistrito.Nobre or distrito.nome_do_distrito == 'escola de magia':
                estado.jogador_atual().ouro += 1
                estado.jogador_atual().pontuacao += 1
        estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoRei.value] = 1


class EfeitoCardealAtivo(Acao):
    def __init__(self):
        super().__init__(
            'Se você não tiver ouro o suficiente para construir um distrito, '
            'troque suas cartas pelo ouro de outro jogador. (1 carta: 1 ouro)')

    
    def ativar(self, estado: Estado):

        divida = 0
        distritos_trocados = []

        for i, mao_propria in enumerate(estado.jogador_atual().cartas_distrito_mao):
            if not mao_propria.nome_do_distrito == 'cofre secreto':
                print(f"{i + 1}: {mao_propria}")

        escolha_distrito = int(input("Digite o número do distrito que deseja construir: "))
        for i in estado.jogador_atual().cartas_distrito_mao:
            if estado.jogador_atual().cartas_distrito_mao[escolha_distrito - 1].valor_do_distrito \
                    > estado.jogador_atual().ouro:
                divida = estado.jogador_atual().cartas_distrito_mao[
                             escolha_distrito - 1].valor_do_distrito - estado.jogador_atual().ouro
                print(f"Faltam: {divida} para o distrito {i + 1}")

            else:
                break
        
        if len(estado.jogador_atual().cartas_distrito_mao) <= divida:
            return
        
        for i, jogador in enumerate(estado.jogadores):
            print(f"{i + 1}: {jogador.nome}")
        while True:
            if all([jogador.ouro < divida for jogador in estado.jogadores]):
                return

            jogador_escolhido = int(input("Escolha o jogador alvo: "))
            if estado.jogadores[jogador_escolhido - 1].ouro >= divida:
                break
        for i in range(divida + 1):
            for mao_propria in estado.jogador_atual().cartas_distrito_mao:
                print(f"{i + 1}: {mao_propria}")

            while True:
                selecionar_distritos = int(input("\nSelecione os distritos a serem trocados: "))
                if all([distrito != selecionar_distritos for distrito in distritos_trocados]):
                    distritos_trocados.append(selecionar_distritos)
                    break

        estado.jogador_atual().distritos_construidos.append(
            estado.jogador_atual().cartas_distrito_mao[escolha_distrito])
        estado.jogador_atual().pontuacao += estado.jogador_atual().cartas_distrito_mao[
            escolha_distrito].valor_do_distrito
        for i in distritos_trocados:
            estado.jogadores[jogador_escolhido - 1].ouro -= divida
            estado.jogadores[jogador_escolhido - 1].distritos_construidos.append(
                estado.jogador_atual().cartas_distrito_mao[i])
            estado.jogador_atual().cartas_distrito_mao.remove(i)

        if len(estado.jogador_atual().distritos_construidos) == 7:
            estado.jogador_atual().terminou = True
        estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoCardealAtivo.value] = 1
        estado.jogador_atual().acoes_realizadas[TipoAcao.ConstruirDistrito.value] = 1


class EfeitoCardealPassivo(Acao):
    def __init__(self):
        super().__init__('Ganhe 1 carta para cada distrito RELIGIOSO construído')

    
    def ativar(self, estado: Estado):
        for _, distrito in enumerate(estado.jogador_atual().distritos_construidos):
            if distrito.tipo_de_distrito == TipoDistrito.Religioso or distrito.nome_do_distrito == 'escola de magia':
                distrito_pescado = estado.tabuleiro.baralho_distritos.pop()
                estado.jogadores[estado.jogadores.index(estado.jogador_atual())].cartas_distrito_mao.append(
                    distrito_pescado)
        estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoCardealPassivo.value] = 1


class EfeitoNavegadora(Acao):
    def __init__(self):
        super().__init__('Ganhe 4 ouros extras ou 4 cartas extras. Você não pode construir distritos.')

    
    def ativar(self, estado: Estado):
        escolha = int(input("1 - Ouro 2 - Carta"))
        if escolha == 1:
            estado.jogador_atual().ouro += 4
            print(estado.jogador_atual().ouro)
        elif escolha == 2:
            estado.jogador_atual().cartas_distrito_mao.append(estado.tabuleiro.baralho_distritos[0:4])
            for i in range(4):
                estado.tabuleiro.baralho_distritos.pop(i)  # testar
        else:
            pass
        estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoNavegadora.value] = 1


class EfeitoSenhordaGuerra(Acao):
    def __init__(self):
        super().__init__(
            "Destrua 1 distrito pagando 1 ouro a menos que o custo dele. "
            "(Ganhe 1 ouro para cada um dos seus distritos militares)")

    
    def ativar(self, estado: Estado):
        # da ouro por militar
        # implementar distrito especial "muralha"
        multa_muralha = 0

        for _, distrito in enumerate(estado.jogador_atual().distritos_construidos):
            if distrito.tipo_de_distrito == TipoDistrito.Militar or distrito.nome_do_distrito == 'escola de magia':
                estado.jogador_atual().ouro += 1
                estado.jogador_atual().pontuacao += 1
        # efeito destruir
        for i, jogador in enumerate(estado.jogadores):
            for distritos in jogador.distritos_construidos:
                print(f"{i + 1}: {distritos}", end=" | ")

            print("\n")
        escolha_jogador = input("Deseja destruir? (s/n)").lower()
        if escolha_jogador == "s":
            for numero_jogadores, jogador in enumerate(estado.jogadores):
                print(numero_jogadores + 1)
                print(jogador)
            jogador_escolhido = int(input("Escolha jogador:"))
            for numero_cartas, carta in enumerate(estado.jogadores[jogador_escolhido - 1].distritos_construidos):
                print(numero_cartas, carta)

                if carta == 'muralha':
                    multa_muralha += 1

            jogador = estado.jogadores[jogador_escolhido]
            destruir_carta = int(input("Digite o distrito que deseja destruir:"))
            if not estado.jogadores[jogador_escolhido - 1].terminou:
                if estado.jogador_atual().ouro >= \
                        jogador.distritos_construidos[jogador_escolhido - 1].valor_do_distrito - 1 + multa_muralha:
                    estado.jogador_atual().ouro -= jogador.distritos_construidos[
                                                       jogador_escolhido - 1].valor_do_distrito - 1 + multa_muralha
                    estado.jogadores[jogador_escolhido - 1].pontuacao -= \
                        jogador.distritos_construidos[jogador_escolhido - 1].valor_do_distrito - 1
                    estado.jogadores[jogador_escolhido - 1].distritos_construidos.pop(destruir_carta)
                # testar
            else:
                print("o jogador possui 7 distritos construídos!")
        estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoSenhordaGuerra.value] = 1


class EfeitoAlquimista(Acao):
    def __init__(self):
        super().__init__(
            "Ao final do seu turno,você pega de volta todo o ouro pago para construir "
            "distritos neste turno. Você não pode pagar mais ouro do que tem.")

    
    def ativar(self, estado: Estado):
        if estado.jogador_atual().construiu or estado.jogador_atual().construiu_estabulo:
            estado.jogador_atual().ouro += estado.jogador_atual().ouro_gasto
        estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoAlquimista.value] = 1


class CofreSecreto(Acao):
    def __init__(self):
        super().__init__(
            "O Cofre Secreto não pode ser construído. Ao final da partida, revele "
            "o Cofre Secreto da sua mão para marcar 3 pontos.")

    
    def ativar(self, estado: Estado):
        estado.jogador_atual().pontuacao += 3
        estado.jogador_atual().acoes_realizadas[TipoAcao.CofreSecreto.value] = 1


class Laboratorio(Acao):
    def __init__(self):
        super().__init__("Uma vez por turno, descarte 1 carta da sua mao para ganhar 2 ouros.")

    
    def ativar(self, estado: Estado):
        # Printar distritos disponíveis para troca
        for index, distrito in enumerate(estado.jogador_atual().cartas_distrito_mao):
            print(f"""ID: {index + 1}
            \tNome: {distrito.nome_do_distrito}
            \tValor: {distrito.valor_do_distrito}
            \ttipo: {distrito.tipo_de_distrito}
            """)

        # Escolher qual carta será trocada por 2 ouros
        while True:
            print("Escolha uma carta para descartar [ID]:", end=" ")
            carta = int(input()) - 1
            if 1 <= carta <= len(estado.jogador_atual().cartas_distrito_mao) + 1:
                break
            else:
                print("Escolha inválida! Escolha um ID válido!")

        # Remover carta escolhida e adicionar os 2 ouros
        carta_descartada = estado.jogador_atual().cartas_distrito_mao.pop(carta)
        estado.tabuleiro.baralho_distritos.append(carta_descartada)
        estado.jogador_atual().ouro += 2
        estado.jogador_atual().acoes_realizadas[TipoAcao.Laboratorio.value] = 1


class Necropole(Acao):
    def __init__(self):
        super().__init__(
            'Você pode construir a Necrópole destruindo 1 distrito na sua cidade, '
            'em vez de pagar o custo da Necrópole.')

    
    def ativar(self, estado: Estado):
        for i, distrito in enumerate(estado.jogador_atual().distritos_construidos):
            print(f"{i + 1}: {distrito.nome_do_distrito}")

        escolha = int(input("Digite o número do distrito que deseja destruir: "))
        for index, distrito in enumerate(estado.jogador_atual().cartas_distrito_mao):
            if distrito.nome_do_distrito == 'necropole':
                distrito_encontrado = estado.jogador_atual().distritos_construidos.pop(escolha - 1)
                estado.tabuleiro.baralho_distritos.append(distrito_encontrado)
                necropole = estado.jogador_atual().cartas_distrito_mao.pop(index)
                estado.jogador_atual().distritos_construidos.append(necropole)
                estado.jogador_atual().pontuacao += necropole.valor_do_distrito
                estado.jogador_atual().pontuacao -= distrito_encontrado.valor_do_distrito
        estado.jogador_atual().acoes_realizadas[TipoAcao.Necropole.value] = 1


class CovilDosLadroes(Acao):
    def __init__(self):
        super().__init__(
            'Pague parte ou todo o custo do Covil dos Ladrões com cartas da sua mão, '
            'em vez de ouro, a uma taxa de 1 carta: 1 ouro.')

    
    def ativar(self, estado: Estado):
        n_cartas_mao = len(estado.jogador_atual().cartas_distrito_mao) - 1
        n = int(input(
            f"Deseja construir o Covil dos Ladrões com quantas cartas? (0-{6 if n_cartas_mao >= 6 else n_cartas_mao})"))
        restante = n

        for i in range(n):
            for distrito in estado.jogador_atual().cartas_distrito_mao:
                if i == 0 and distrito.nome_do_distrito == 'covil dos ladroes':
                    covil = estado.jogador_atual().cartas_distrito_mao.pop(i)
                    estado.jogador_atual().distritos_construidos.append(covil)
                print(f"{i + 1}: {distrito.nome_do_distrito}")
            escolha = int(input(f"Informe o distrito: ({n - i} restantes)"))
            estado.jogador_atual().cartas_distrito_mao.pop(escolha - 1)
            restante -= 1
        estado.jogador_atual().ouro -= restante
        estado.jogador_atual().acoes_realizadas[TipoAcao.CovilDosLadroes.value] = 1


# continuar pontuação parcial !!!!

class Teatro(Acao):
    def __init__(self):
        super().__init__(
            'Ao final de cada fase de escolha, você pode trocar a sua carta de '
            'personagem escolhida com a carta de personagem de um oponente.')

    
    def ativar(self, estado: Estado):
        for i, jogador in enumerate(estado.jogadores):
            if jogador != estado.jogador_atual():
                print(f"{i + 1}: {jogador.nome}")

        escolha = int(input('Digite o número do jogador que deseja trocar o personagem: '))

        personagem_temp = estado.jogador_atual().personagem
        estado.jogador_atual().personagem = estado.jogadores[escolha].personagem
        estado.jogadores[escolha].personagem = personagem_temp
        estado.jogador_atual().acoes_realizadas[TipoAcao.Teatro.value] = 1


class Estrutura(Acao):
    def __init__(self):
        super().__init__(
            'Você pode construir um distrito destruindo a Estrutura, em vez de pagar os custos do distrito em questão.')

    
    def ativar(self, estado: Estado):
        for i, distrito in enumerate(estado.jogador_atual().cartas_distrito_mao):
            if not distrito.nome_do_distrito == 'cofre secreto':
                print(f"{i + 1}: {distrito.nome_do_distrito}")

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
        estado.jogador_atual().acoes_realizadas[TipoAcao.Estrutura.value] = 1


class PassarTurno(Acao):
    def __init__(self):
        super().__init__("Passar turno")

    
    def ativar(self, estado: Estado):
        for _, distrito in enumerate(estado.jogador_atual().distritos_construidos):
            if distrito.nome_do_distrito == 'abrigo para pobres' and estado.jogador_atual().ouro == 0:
                estado.jogador_atual().ouro += 1

        jogador = estado.jogador_atual()
        jogador.ouro_gasto, jogador.roubado, jogador.morto, jogador.construiu = 0, False, False, False
        jogador.acoes_realizadas = [0 for _ in range(len(TipoAcao))]
        jogador.acoes_realizadas[TipoAcao.PassarTurno.value] = 1
        estado.turno += 1
        


class Estabulo(Acao):
    def __init__(self):
        super().__init__("A construção dos Estabulos não conta para o seu limite de construção neste turno.")

    
    def ativar(self, estado: Estado):
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
        estado.jogador_atual().acoes_realizadas[TipoAcao.Estabulo.value] = 1
