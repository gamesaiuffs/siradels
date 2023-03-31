from typing import List

from Estado import Estado
from classes.enum.TipoDistrito import TipoDistrito
from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.Jogador import Jogador


class Acao:
    def __init__(self, descricao: str, tipo_acao: TipoAcao):
        self.descricao = descricao
        self.tipo_acao = tipo_acao

    def __str__(self):
        return f'{self.descricao}'

    def ativar(self, estado: Estado):
        estado.jogador_atual().acoes_realizadas[self.tipo_acao.value] = True


class PassarTurno(Acao):
    def __init__(self):
        super().__init__('Passar seu turno.', TipoAcao.PassarTurno)

    def ativar(self, estado: Estado):
        # Efeito passivo do distrito Abrigo para Pobres
        if estado.jogador_atual().ouro == 0:
            for distrito in estado.jogador_atual().distritos_construidos:
                if distrito.nome_do_distrito == 'Abrigo para Pobres':
                    estado.jogador_atual().ouro += 1
                    break
        # Efeito passivo do Alquimista
        if estado.jogador_atual().personagem.nome == 'Alquimista':
            estado.jogador_atual().ouro += estado.jogador_atual().ouro_gasto
        # Otimiza a chamada do jogador atual
        jogador = estado.jogador_atual()
        # Limpa flags de controle e ações realizadas
        jogador.ouro_gasto, jogador.roubado, jogador.morto, jogador.construiu = 0, False, False, False
        jogador.acoes_realizadas = [False for _ in range(len(TipoAcao))]
        # Marca flag de ação utilizada
        super().ativar(estado)
        # Turno deve ser o último a ser atualizado, pois, afeta ponteiro para jogador atual
        estado.turno += 1


class ColetarOuro(Acao):
    def __init__(self):
        super().__init__('Pegue dois ouros do banco.', TipoAcao.ColetarOuro)

    def ativar(self, estado: Estado):
        # Efeito passivo da carta Mina de Ouro
        if estado.jogador_atual().construiu_distrito('Mina de Ouro'):
            estado.jogador_atual().ouro += 1
        # Adiciona dois de ouro ao jogador
        estado.jogador_atual().ouro += 2
        # Marca flag de ação utilizada
        super().ativar(estado)


class ColetarCartas(Acao):
    def __init__(self):
        super().__init__('Compre duas cartas do baralho de distritos, escolha uma e descarte a outra.', TipoAcao.ColetarCartas)

    def ativar(self, estado: Estado):
        # Pescar cartas do baralho
        cartas_compradas = estado.tabuleiro.baralho_distritos[:2]
        del estado.tabuleiro.baralho_distritos[:2]
        # Mostra cartas para escolha
        print('Carta 1:')
        print('\t', cartas_compradas[0].imprimir_tudo())
        print('Carta 2:')
        print('\t', cartas_compradas[1].imprimir_tudo())
        # Aguarda escolha do jogador
        while True:
            escolha = input('Escolha a carta (1 ou 2) com que deseja ficar: ')
            try:
                escolha = int(escolha)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 1 <= escolha <= 2:
                print('Escolha inválida.')
                continue
            # Adicionar na mão do jogador a carta escolhida
            if escolha == 1:
                estado.jogador_atual().cartas_distrito_mao.append(cartas_compradas[0])
                estado.tabuleiro.baralho_distritos.append(cartas_compradas[1])
            elif escolha == 2:
                estado.jogador_atual().cartas_distrito_mao.append(cartas_compradas[1])
                estado.tabuleiro.baralho_distritos.append(cartas_compradas[0])
            break
        # Marca flag de ação utilizada
        super().ativar(estado)


class ConstruirDistrito(Acao):
    def __init__(self):
        super().__init__('Construa um distrito em sua cidade.', TipoAcao.ConstruirDistrito)

    def ativar(self, estado: Estado):
        # Identifica distritos que podem ser construídos
        distritos_para_construir: List[CartaDistrito] = []
        # Identifica distritos que podem ser construídos pelo Cardeal
        distritos_para_construir_cardeal: List[(CartaDistrito, Jogador)] = []
        diferenca = 0
        for carta in estado.jogador_atual().cartas_distrito_mao:
            # Cofre secreto nunca pode ser construído
            if carta.nome_do_distrito != 'Cofre Secreto':
                # Distritos repetidos não podem ser construídos (a não ser que seja o Mago)
                # Também deve possuir ouro suficiente para construir o distrito
                repetido = estado.jogador_atual().construiu_distrito(carta.nome_do_distrito)
                if not repetido or estado.jogador_atual().personagem.nome == 'Mago':
                    if carta.valor_do_distrito <= estado.jogador_atual().ouro:
                        distritos_para_construir.append(carta)
                    # Se você não tiver ouro suficiente para cosntruir um distrito, troque suas cartas pelo ouro de outro jogador (1 carta:1 ouro).
                    elif estado.jogador_atual().personagem.nome == 'Cardeal' and \
                            carta.valor_do_distrito <= len(estado.jogador_atual().cartas_distrito_mao) + estado.jogador_atual().ouro - 1:
                        diferenca = carta.valor_do_distrito - estado.jogador_atual().ouro
                        # Identifica jogadores que podem pagar o ouro que falta
                        for jogador in estado.jogadores:
                            if jogador != estado.jogador_atual() and jogador.ouro >= diferenca:
                                distritos_para_construir_cardeal.append((carta, jogador))
        if len(distritos_para_construir) == 0 and len(distritos_para_construir_cardeal):
            print('Não é possível construir nenhum distrito!')
            return
        # Mostra opções ao jogador
        print(f'0: Não desejo construir nenhum distrito.')
        i = 0
        for carta in distritos_para_construir:
            i += 1
            print(f'{i}: {carta.imprimir_tudo()}')
        for carta, jogador in distritos_para_construir_cardeal:
            i += 1
            print(f'{i}: {carta.imprimir_tudo()} - Jogador: {jogador.nome}')
        # Aguarda escolha do jogador
        while True:
            escolha_construir = input('Digite o número do distrito que deseja construir: ')
            try:
                escolha_construir = int(escolha_construir)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_construir <= len(distritos_para_construir) + len(distritos_para_construir_cardeal):
                print('Escolha inválida.')
                continue
            # Finaliza ação se jogador decidiu não construir
            if escolha_construir == 0:
                return
            # Construção normal
            if escolha_construir <= len(distritos_para_construir):
                distrito = distritos_para_construir[escolha_construir - 1]
                # Retira distrito construído da mão
                estado.jogador_atual().cartas_distrito_mao.remove(distrito)
            # Construção com efeito passivo do Cardeal
            else:
                (distrito, jogador) = distritos_para_construir_cardeal[escolha_construir - len(distritos_para_construir) - 1]
                # Retira distrito construído da mão
                estado.jogador_atual().cartas_distrito_mao.remove(distrito)
                # Jogador escolhido recebe cartas em troca pelo dinheiro pago
                for i in range(diferenca):
                    print(f'Escolha as cartas que trocará pelo ouro recebido do jogador escolhido. Faltam {diferenca - i} cartas.')
                    for j, carta in enumerate(estado.jogador_atual().cartas_distrito_mao):
                        print(f'{j+1}: {carta.imprimir_tudo()}')
                    while True:
                        escolha_carta = input('Digite o número do distrito que deseja trocar pelo ouro: ')
                        try:
                            escolha_carta = int(escolha_carta)
                        except ValueError:
                            print('Escolha inválida.')
                            continue
                        if not 0 < escolha_carta <= len(estado.jogador_atual().cartas_distrito_mao):
                            print('Escolha inválida.')
                            continue
                        # Troca carta pelo ouro
                        carta = estado.jogador_atual().cartas_distrito_mao[escolha_carta - 1]
                        estado.jogador_atual().ouro += 1
                        jogador.ouro -= 1
                        estado.jogador_atual().cartas_distrito_mao.remove(carta)
                        jogador.cartas_distrito_mao.append(carta)
                        break
            # Pontua distrito
            estado.jogador_atual().pontuacao += distrito.valor_do_distrito
            # Constrói distrito e marca Flag de controle
            estado.jogador_atual().distritos_construidos.append(distrito)
            estado.jogador_atual().construiu = True
            # Paga distrito e salva ouro gasto
            estado.jogador_atual().ouro -= distrito.valor_do_distrito
            estado.jogador_atual().ouro_gasto += distrito.valor_do_distrito
            break
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeAssassina(Acao):
    def __init__(self):
        super().__init__('Anuncie um personagem que você deseja assassinar. O personagem assassinado perde o turno.', TipoAcao.HabilidadeAssassina)
    
    def ativar(self, estado: Estado):
        # Identifica quantos personagens estão em jogo (8 ou 9)
        numero_personagens = estado.tabuleiro.numero_personagens
        # Aguarda escolha do jogador
        while True:
            # A Assassina não pode afetar o personagem de rank 1 (ele próprio)
            escolha = input(f'Digite o rank (2 a {numero_personagens}) do personagem que deseja assassinar: ')
            try:
                escolha = int(escolha)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 2 <= escolha <= numero_personagens:
                print('Escolha inválida.')
                continue
            # Marca flag do efeito da Assassina
            for jogador in estado.jogadores:
                if jogador.personagem.rank == escolha:
                    jogador.morto = True
                    break
            break
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeLadrao(Acao):
    def __init__(self):
        super().__init__(
            'Anuncie um personagem que você deseja roubar. O personagem roubado entrega todo seu ouro ao ladrão.', TipoAcao.HabilidadeLadrao)

    def ativar(self, estado: Estado):
        # Identifica quantos personagens estão em jogo (8 ou 9)
        numero_personagens = estado.tabuleiro.numero_personagens
        # Aguarda escolha do jogador
        while True:
            # O Ladrão não pode afetar o personagem de rank 1, 2 (ele próprio) e o personagem morto pela Assassina
            escolha = input(f'Digite o rank (3 a {numero_personagens}) do personagem que deseja roubar '
                            f'(não pode ser o rank do personagem assassinado): ')
            try:
                escolha = int(escolha)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 3 <= escolha <= numero_personagens:
                print('Escolha inválida.')
                continue
            for morto in estado.jogadores:
                if morto.morto and morto.personagem.rank == escolha:
                    print('Escolha inválida.')
                    continue
            # Marca flag do efeito do Ladrão
            for jogador in estado.jogadores:
                if jogador.personagem.rank == escolha:
                    jogador.roubado = True
                    break
            break
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeMago(Acao):
    def __init__(self):
        super().__init__(
            'Olhe a mão de outro jogador e escolha 1 carta. Pague para construí-la imediatamente ou adicione-a à sua mão.', TipoAcao.HabilidadeMago)

    def ativar(self, estado: Estado):
        # Mostra opções ao jogador
        print('Jogadores:')
        for i, jogador in enumerate(estado.jogadores):
            print(f'{i+1}: {jogador}')
        # Aguarda escolha do jogador
        while True:
            escolha_jogador = input('Digite o número do jogador que deseja olhar a mão e pegar 1 carta: ')
            try:
                escolha_jogador = int(escolha_jogador)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 < escolha_jogador <= len(estado.jogadores):
                print('Escolha inválida.')
                continue
        # Mostra opções ao jogador
        print('Mão do jogador escolhido:')
        for i, carta in enumerate(estado.jogadores[escolha_jogador - 1].cartas_distrito_mao):
            print(f'{i + 1}: {carta.imprimir_tudo()}')
        # Aguarda escolha do jogador
        while True:
            escolha_carta = input('Digite o número da carta que deseja pegar para construir ou para sua mão: ')
            try:
                escolha_carta = int(escolha_carta)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 < escolha_carta <= len(estado.jogadores[escolha_jogador - 1].cartas_distrito_mao):
                print('Escolha inválida.')
                continue
        # Remove carta escolhida da mão do jogador escolhido
        distrito = estado.jogadores[escolha_jogador - 1].cartas_distrito_mao[escolha_carta - 1]
        estado.jogadores[escolha_jogador - 1].cartas_distrito_mao.remove(distrito)
        # Adiciona carta escolhida na mão do jogador atual
        estado.jogador_atual().cartas_distrito_mao.append(distrito)
        # Verifica se é possível construir distrito escolhido
        if distrito.valor_do_distrito <= estado.jogador_atual().ouro and distrito.nome_do_distrito != 'Cofre Secreto':
            # Aguarda escolha do jogador
            while True:
                escolha_construir = input('Deseja construir o distrito imediatamente? (0 - Não, 1 - Sim) ')
                try:
                    escolha_construir = int(escolha_construir)
                except ValueError:
                    print('Escolha inválida.')
                    continue
                if not 0 <= escolha_construir <= 1:
                    print('Escolha inválida.')
                    continue
                # Constrói distrito imediatamente
                if escolha_construir == 1:
                    # Pontua distrito
                    estado.jogador_atual().pontuacao += distrito.valor_do_distrito
                    # Paga distrito e salva ouro gasto (Alquimista)
                    estado.jogador_atual().ouro -= distrito.valor_do_distrito
                    estado.jogador_atual().ouro_gasto += distrito.valor_do_distrito
                    # Constrói distrito e marca Flag de controle
                    estado.jogador_atual().distritos_construidos.append(distrito)
                    estado.jogador_atual().construiu = True
                    # Retira distrito construído da mão
                    estado.jogador_atual().cartas_distrito_mao.remove(distrito)
                break
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeRei(Acao):
    def __init__(self):
        super().__init__('Ganhe 1 ouro para cada um dos seus distritos NOBRES.', TipoAcao.HabilidadeRei)

    def ativar(self, estado: Estado):
        # Contabiliza distritos nobres para ganhar ouro
        for distrito in estado.jogador_atual().distritos_construidos:
            # O efeito da carta Escola de magia é ser contabilizada como qualquer tipo, portanto também é nobre
            if distrito.tipo_de_distrito == TipoDistrito.Nobre or distrito.nome_do_distrito == 'Escola de Magia':
                estado.jogador_atual().ouro += 1
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeCardeal(Acao):
    def __init__(self):
        super().__init__('Ganhe 1 carta para cada um dos seus distritos RELIGIOSOS.', TipoAcao.HabilidadeCardeal)

    def ativar(self, estado: Estado):
        # Contabiliza distritos religiosos para ganhar cartas
        for distrito in estado.jogador_atual().distritos_construidos:
            # O efeito da carta Escola de magia é ser contabilizada como qualquer tipo, portanto também é religioso
            if distrito.tipo_de_distrito == TipoDistrito.Religioso or distrito.nome_do_distrito == 'Escola de Magia':
                estado.jogador_atual().cartas_distrito_mao.append(estado.tabuleiro.baralho_distritos.pop(0))
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeNavegadora(Acao):
    def __init__(self):
        super().__init__('Ganhe 4 ouros extras ou 4 cartas extras.', TipoAcao.HabilidadeNavegadora)
    
    def ativar(self, estado: Estado):
        # Aguarda escolha do jogador
        while True:
            escolha = input('Qual recurso deseja ganhar? (0 - ouro, 1 - cartas) ')
            try:
                escolha = int(escolha)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha <= 1:
                print('Escolha inválida.')
                continue
            if escolha == 1:
                estado.jogador_atual().ouro += 4
            elif escolha == 2:
                estado.jogador_atual().cartas_distrito_mao.append(estado.tabuleiro.baralho_distritos[0:4])
                del estado.tabuleiro.baralho_distritos[0:4]
            break
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeSenhordaGuerraDestruir(Acao):
    def __init__(self):
        super().__init__('Destrua 1 distrito, pagando 1 ouro a menos que o custo dele.', TipoAcao.HabilidadeSenhordaGuerraDestruir)

    def ativar(self, estado: Estado):
        # Identifica distritos que podem ser destruídos
        distritos_para_destruir: List[(CartaDistrito, Jogador)] = []
        for jogador in estado.jogadores:
            # Não é possível destruir um distrito próprio ou de um jogador com 7+ distritos
            if jogador != estado.jogador_atual() and not jogador.terminou:
                for carta in jogador.distritos_construidos:
                    # Precisa ter ouro suficiente para destruir o distrito
                    if carta.valor_do_distrito <= estado.jogador_atual().ouro + 1:
                        distritos_para_destruir.append((carta, jogador))
        if len(distritos_para_destruir) == 0:
            print('Não é possível destruir nenhum distrito!')
            return
        # Mostra opções ao jogador
        print('Distritos que podem ser destruídos:')
        for i, (carta, jogador) in enumerate(distritos_para_destruir):
            print(f'{i+1}: {carta.imprimir_tudo()} - Jogador: {jogador.nome}')
        # Aguarda escolha do jogador
        while True:
            escolha = input('Digite o número do distrito que deseja destruir: ')
            try:
                escolha = int(escolha)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 < escolha <= len(distritos_para_destruir):
                print('Escolha inválida.')
                continue
            (distrito, jogador) = distritos_para_destruir[escolha - 1]
            estado.jogador_atual().ouro -= distrito.valor_do_distrito - 1
            jogador.pontuacao -= distrito.valor_do_distrito
            jogador.distritos_construidos.remove(distrito)
            estado.tabuleiro.baralho_distritos.append(distrito)
            break
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeSenhordaGuerraColetar(Acao):
    def __init__(self):
        super().__init__('Ganhe 1 ouro para cada um dos seus distritos MILITARES.', TipoAcao.HabilidadeSenhordaGuerraColetar)

    def ativar(self, estado: Estado):
        # Contabiliza distritos militares para ganhar ouro
        for distrito in estado.jogador_atual().distritos_construidos:
            # O efeito da carta Escola de magia é ser contabilizada como qualquer tipo, portanto também é militar
            if distrito.tipo_de_distrito == TipoDistrito.Militar or distrito.nome_do_distrito == 'Escola de Magia':
                estado.jogador_atual().ouro += 1
        # Marca flag de ação utilizada
        super().ativar(estado)


class CofreSecreto(Acao):
    def __init__(self):
        super().__init__(
            'O Cofre Secreto não pode ser construído. Ao final da partida, revele '
            'o Cofre Secreto da sua mão para marcar 3 pontos.')

    
    def ativar(self, estado: Estado):
        estado.jogador_atual().pontuacao += 3
        estado.jogador_atual().acoes_realizadas[TipoAcao.CofreSecreto.value] = 1


class Laboratorio(Acao):
    def __init__(self):
        super().__init__('Uma vez por turno, descarte 1 carta da sua mao para ganhar 2 ouros.')

    
    def ativar(self, estado: Estado):
        # Printar distritos disponíveis para troca
        for index, distrito in enumerate(estado.jogador_atual().cartas_distrito_mao):
            print(f'''ID: {index + 1}
            \tNome: {distrito.nome_do_distrito}
            \tValor: {distrito.valor_do_distrito}
            \ttipo: {distrito.tipo_de_distrito}
            ''')

        # Escolher qual carta será trocada por 2 ouros
        while True:
            print('Escolha uma carta para descartar [ID]:', end=' ')
            carta = int(input()) - 1
            if 1 <= carta <= len(estado.jogador_atual().cartas_distrito_mao) + 1:
                break
            else:
                print('Escolha inválida! Escolha um ID válido!')

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
            print(f'{i + 1}: {distrito.nome_do_distrito}')

        escolha = int(input('Digite o número do distrito que deseja destruir: '))
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
            f'Deseja construir o Covil dos Ladrões com quantas cartas? (0-{6 if n_cartas_mao >= 6 else n_cartas_mao})'))
        restante = n

        for i in range(n):
            for distrito in estado.jogador_atual().cartas_distrito_mao:
                if i == 0 and distrito.nome_do_distrito == 'covil dos ladroes':
                    covil = estado.jogador_atual().cartas_distrito_mao.pop(i)
                    estado.jogador_atual().distritos_construidos.append(covil)
                print(f'{i + 1}: {distrito.nome_do_distrito}')
            escolha = int(input(f'Informe o distrito: ({n - i} restantes)'))
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
                print(f'{i + 1}: {jogador.nome}')

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
                print(f'{i + 1}: {distrito.nome_do_distrito}')

        escolha = int(input('Digite o número do distrito que deseja construir: '))
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


class Estabulo(Acao):
    def __init__(self):
        super().__init__('A construção dos Estabulos não conta para o seu limite de construção neste turno.')

    
    def ativar(self, estado: Estado):
        for estabulo in estado.jogador_atual().distritos_construidos:
            if estabulo.nome_do_distrito == 'estabulo':

                if estado.jogador_atual().ouro >= estabulo.valor_do_distrito:

                    estado.jogador_atual().pontuacao += estabulo.valor_do_distrito

                    estado.jogador_atual().ouro -= estabulo.valor_do_distrito
                    estado.jogador_atual().distritos_construidos.append(estabulo)
                    estado.jogador_atual().cartas_distrito_mao.remove(estabulo)
                    estado.jogador_atual().ouro_gasto = estabulo.valor_do_distrito

                    if len(estado.jogador_atual().distritos_construidos) == 7:
                        estado.jogador_atual().terminou = True

                else:
                    print('Ouro insuficiente!')
                break
        estado.jogador_atual().acoes_realizadas[TipoAcao.Estabulo.value] = 1
