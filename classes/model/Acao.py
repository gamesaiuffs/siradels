from typing import List

from classes.model.Estado import Estado
from classes.enum.TipoDistrito import TipoDistrito
from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
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
            if estado.jogador_atual().construiu_distrito('Abrigo para Pobres'):
                estado.jogador_atual().ouro += 1
        # Efeito passivo do distrito Parque
        if len(estado.jogador_atual().cartas_distrito_mao) == 0:
            if estado.jogador_atual().construiu_distrito('Parque'):
                # Pescar cartas do baralho e adicionar na mão do jogador
                cartas_compradas = estado.tabuleiro.baralho_distritos[:2]
                del estado.tabuleiro.baralho_distritos[:2]
                estado.jogador_atual().cartas_distrito_mao.extend(cartas_compradas)
        # Efeito passivo do Alquimista
        if estado.jogador_atual().personagem.nome == 'Alquimista':
            estado.jogador_atual().ouro += estado.jogador_atual().ouro_gasto
        # Otimiza a chamada do jogador atual
        jogador = estado.jogador_atual()
        # Limpa flags de controle e ações realizadas
        jogador.ouro_gasto, jogador.roubado, jogador.construiu = 0, False, False
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
        qtd_cartas = 2
        # Efeito passivo da carta Observatório
        if estado.jogador_atual().construiu_distrito('Observatório'):
            qtd_cartas = 3
        # Baralho vazio
        if not estado.tabuleiro.baralho_distritos:
            print('Baralho vazio!')
            super().ativar(estado)
            return
        # Cartas insuficientes no baralho para pescar
        if len(estado.tabuleiro.baralho_distritos) < qtd_cartas:
            qtd_cartas = len(estado.tabuleiro.baralho_distritos)
        # Pescar cartas do baralho
        cartas_compradas = estado.tabuleiro.baralho_distritos[:qtd_cartas]
        del estado.tabuleiro.baralho_distritos[:qtd_cartas]
        # Efeito passivo da carta Biblioteca
        # Se só existe uma carta no baralho ela é a única opção
        if estado.jogador_atual().construiu_distrito('Biblioteca') or qtd_cartas == 1:
            estado.jogador_atual().cartas_distrito_mao.extend(cartas_compradas)
            super().ativar(estado)
            return
        # Mostra cartas para escolha
        print(f'0: {cartas_compradas[0].imprimir_tudo()}')
        print(f'1: {cartas_compradas[1].imprimir_tudo()}')
        if qtd_cartas == 3:
            print(f'2: {cartas_compradas[2].imprimir_tudo()}')
        # Aguarda escolha do jogador
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
            # Adicionar na mão do jogador a carta escolhida e descarta cartas que não foram escolhidas
            if escolha_carta == 0:
                estado.jogador_atual().cartas_distrito_mao.append(cartas_compradas[0])
                estado.tabuleiro.baralho_distritos.append(cartas_compradas[1])
            elif escolha_carta == 1:
                estado.jogador_atual().cartas_distrito_mao.append(cartas_compradas[1])
                estado.tabuleiro.baralho_distritos.append(cartas_compradas[0])
            elif escolha_carta == 2:
                estado.jogador_atual().cartas_distrito_mao.append(cartas_compradas[2])
                estado.tabuleiro.baralho_distritos.extend(cartas_compradas[:1])
            if qtd_cartas == 3 and 0 <= escolha_carta < 2:
                estado.tabuleiro.baralho_distritos.append(cartas_compradas[2])
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
        # Identifica distritos que podem ser destruídos para construir a necrópole sem custo
        distritos_para_construir_necropole: List[(CartaDistrito, CartaDistrito)] = []
        # Identifica opções especiais para construir o covil dos ladrões (divisão do custo em ouro e cartas da mão)
        distritos_para_construir_covil_ladroes: List[(CartaDistrito, int, int)] = []
        # Identifica opções de construção ao destruir a Estrutura
        distritos_para_construir_estrutura: List[CartaDistrito] = []
        # Identifica se o jogador construiu a Fábrica (afeta custo dos distritos especiais)
        fabrica = estado.jogador_atual().construiu_distrito('Fábrica')
        # Identifica se o jogador construiu a Estrutura (adiciona opções de construção sem custo)
        estrutura = estado.jogador_atual().construiu_distrito('Estrutura')
        # Identifica se o jogador construiu a Pedreira (adiciona opções de construção repetida)
        pedreira = estado.jogador_atual().construiu_distrito('Pedreira')
        # Identifica se o jogador possui a Necrópole na mão
        diferenca = 0
        for carta in estado.jogador_atual().cartas_distrito_mao:
            # O Monumento não pode ser construído se a cidade já possuir 5 ou mais distritos
            if carta.nome_do_distrito == 'Monumento' and len(estado.jogador_atual().distritos_construidos) >= 5:
                continue
            # Cofre secreto nunca pode ser construído
            if carta.nome_do_distrito == 'Cofre Secreto':
                continue
            # Distritos repetidos não podem ser construídos (a não ser que seja o Mago ou tenha construído a Pedreira)
            repetido = estado.jogador_atual().construiu_distrito(carta.nome_do_distrito)
            if repetido and not (estado.jogador_atual().personagem.nome == 'Mago' or pedreira):
                continue
            # Pode construir sem custo ao destruir Estrutura
            if estrutura:
                distritos_para_construir_estrutura.append(carta)
            # Deve possuir ouro suficiente para construir o distrito (Fábrica dá desconto para distritos especiais)
            if carta.valor_do_distrito <= estado.jogador_atual().ouro or \
                    (fabrica and carta.tipo_de_distrito == TipoDistrito.Especial and carta.valor_do_distrito - 1 <= estado.jogador_atual().ouro):
                distritos_para_construir.append(carta)
            # Habilidade do Cardeal
            # se não tiver ouro suficiente para construir um distrito, troque as suas cartas pelo ouro de outro jogador (1 carta: 1 ouro).
            # Fábrica concede 1 de desconto para distritos especiais
            elif estado.jogador_atual().personagem.nome == 'Cardeal' and \
                    carta.valor_do_distrito <= len(estado.jogador_atual().cartas_distrito_mao) + estado.jogador_atual().ouro - 1 or \
                    (fabrica and carta.valor_do_distrito - 1 <= len(estado.jogador_atual().cartas_distrito_mao) + estado.jogador_atual().ouro - 1):
                diferenca = carta.valor_do_distrito - estado.jogador_atual().ouro
                # Fábrica concede 1 de desconto para distritos especiais
                if fabrica and carta.tipo_de_distrito == TipoDistrito.Especial:
                    diferenca -= 1
                # Identifica jogadores que podem pagar o ouro que falta
                for jogador in estado.jogadores:
                    if jogador != estado.jogador_atual() and jogador.ouro >= diferenca:
                        distritos_para_construir_cardeal.append((carta, jogador))
            # A necrópole pode ser construída sem custo destruindo um dos seus distritos
            if carta.nome_do_distrito == 'Necrópole':
                for distrito_construido in estado.jogador_atual().distritos_construidos:
                    # O caso da Estrutura foi tratado em separado
                    if distrito_construido.nome_do_distrito != 'Estrutura':
                        distritos_para_construir_necropole.append((carta, distrito_construido))
            # O covil dos ladrões pode ser construído com um custo misto de ouro e cartas da mão
            if carta.nome_do_distrito == 'Covil dos Ladrões':
                qtd_cartas = len(estado.jogador_atual().cartas_distrito_mao) - 1
                # Não é necessário ter mais que 6 cartas no pagamento, pois o custo do distrito é 6 (5 com fábrica)
                if qtd_cartas > 6:
                    qtd_cartas = 6
                if fabrica and qtd_cartas > 5:
                    qtd_cartas = 5
                qtd_ouro = carta.valor_do_distrito - 1
                # Fábrica concede 1 de desconto para distritos especiais
                if fabrica:
                    qtd_ouro -= 1
                while qtd_ouro + qtd_cartas >= carta.valor_do_distrito:
                    if qtd_ouro > estado.jogador_atual().ouro:
                        qtd_ouro -= 1
                        continue
                    distritos_para_construir_covil_ladroes.append((carta, qtd_ouro, carta.valor_do_distrito - qtd_ouro))
                    if qtd_ouro > 0:
                        qtd_ouro -= 1
                    else:
                        qtd_cartas -= 1
        if len(distritos_para_construir) + len(distritos_para_construir_cardeal) + len(distritos_para_construir_necropole) + \
                len(distritos_para_construir_covil_ladroes) + len(distritos_para_construir_estrutura) == 0:
            print('Não é possível construir nenhum distrito!')
            super().ativar(estado)
            return
        # Mostra opções ao jogador
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
        # Aguarda escolha do jogador
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
            # Finaliza ação se jogador decidiu não construir
            if escolha_construir == 0:
                super().ativar(estado)
                return
            # Construção normal
            if escolha_construir <= len(distritos_para_construir):
                distrito = distritos_para_construir[escolha_construir - 1]
                # Retira distrito construído da mão
                estado.jogador_atual().cartas_distrito_mao.remove(distrito)
                # Paga distrito e salva ouro gasto
                estado.jogador_atual().ouro -= distrito.valor_do_distrito
                estado.jogador_atual().ouro_gasto += distrito.valor_do_distrito
                # Fábrica concede 1 de desconto para distritos especiais
                if fabrica and distrito.tipo_de_distrito == TipoDistrito.Especial:
                    estado.jogador_atual().ouro += 1
                    estado.jogador_atual().ouro_gasto -= 1
            # Construção com efeito passivo do Cardeal
            elif escolha_construir <= len(distritos_para_construir) + len(distritos_para_construir_cardeal):
                (distrito, jogador) = distritos_para_construir_cardeal[escolha_construir - len(distritos_para_construir) - 1]
                # Retira distrito construído da mão
                estado.jogador_atual().cartas_distrito_mao.remove(distrito)
                # Paga distrito e salva ouro gasto
                estado.jogador_atual().ouro -= distrito.valor_do_distrito
                estado.jogador_atual().ouro_gasto += distrito.valor_do_distrito
                # Fábrica concede 1 de desconto para distritos especiais
                if fabrica and distrito.tipo_de_distrito == TipoDistrito.Especial:
                    estado.jogador_atual().ouro += 1
                    estado.jogador_atual().ouro_gasto -= 1
                # Jogador escolhido recebe cartas em troca pelo dinheiro pago
                for i in range(diferenca):
                    print(f'Escolha as cartas que trocará pelo ouro recebido do jogador escolhido. Faltam {diferenca - i} cartas.')
                    for j, carta in enumerate(estado.jogador_atual().cartas_distrito_mao):
                        print(f'{j}: {carta.imprimir_tudo()}')
                    while True:
                        escolha_carta = input('Digite o número do distrito que deseja trocar pelo ouro: ')
                        try:
                            escolha_carta = int(escolha_carta)
                        except ValueError:
                            print('Escolha inválida.')
                            continue
                        if not 0 <= escolha_carta < len(estado.jogador_atual().cartas_distrito_mao):
                            print('Escolha inválida.')
                            continue
                        # Troca carta pelo ouro
                        carta = estado.jogador_atual().cartas_distrito_mao[escolha_carta]
                        estado.jogador_atual().ouro += 1
                        jogador.ouro -= 1
                        estado.jogador_atual().cartas_distrito_mao.remove(carta)
                        jogador.cartas_distrito_mao.append(carta)
                        break
            # Construção de necrópole sem custo de ouro
            elif escolha_construir <= len(distritos_para_construir) + len(distritos_para_construir_cardeal) + len(distritos_para_construir_necropole):
                (distrito, destruido) = distritos_para_construir_necropole[escolha_construir -
                                                                           len(distritos_para_construir) -
                                                                           len(distritos_para_construir_cardeal) - 1]
                # Retira distrito construído da mão
                estado.jogador_atual().cartas_distrito_mao.remove(distrito)
                # Destrói distrito escolhido e remove pontos parciais
                estado.jogador_atual().distritos_construidos.remove(destruido)
                estado.tabuleiro.baralho_distritos.append(destruido)
                estado.jogador_atual().pontuacao -= destruido.valor_do_distrito
            # Construção de covil dos ladrões com custo misto de ouro e cartas
            elif escolha_construir <= len(distritos_para_construir) + len(distritos_para_construir_cardeal) + len(distritos_para_construir_necropole) + \
                    len(distritos_para_construir_covil_ladroes):
                (distrito, qtd_ouro, qtd_cartas) = distritos_para_construir_covil_ladroes[escolha_construir -
                                                                                          len(distritos_para_construir) -
                                                                                          len(distritos_para_construir_cardeal) -
                                                                                          len(distritos_para_construir_necropole) - 1]
                # Retira distrito construído da mão
                estado.jogador_atual().cartas_distrito_mao.remove(distrito)
                # Paga distrito e salva ouro gasto
                estado.jogador_atual().ouro -= qtd_ouro
                estado.jogador_atual().ouro_gasto += qtd_ouro
                # Escolhe carta para pagar o resto do custo
                for i in range(qtd_cartas):
                    print(f'Escolha as cartas que usará para pagar o custo. Faltam {qtd_cartas - i} cartas.')
                    for j, carta in enumerate(estado.jogador_atual().cartas_distrito_mao):
                        print(f'{j}: {carta.imprimir_tudo()}')
                    while True:
                        escolha_carta = input('Digite o número do distrito que deseja descartar: ')
                        try:
                            escolha_carta = int(escolha_carta)
                        except ValueError:
                            print('Escolha inválida.')
                            continue
                        if not 0 <= escolha_carta < len(estado.jogador_atual().cartas_distrito_mao):
                            print('Escolha inválida.')
                            continue
                        # Descarta carta escolhida
                        carta = estado.jogador_atual().cartas_distrito_mao[escolha_carta]
                        estado.jogador_atual().cartas_distrito_mao.remove(carta)
                        estado.tabuleiro.baralho_distritos.append(carta)
                        break
            # Construção sem custo destruíndo a Estrutura
            else:
                distrito = distritos_para_construir_estrutura[escolha_construir -
                                                              len(distritos_para_construir) -
                                                              len(distritos_para_construir_cardeal) -
                                                              len(distritos_para_construir_necropole) -
                                                              len(distritos_para_construir_covil_ladroes) - 1]
                # Retira distrito construído da mão
                estado.jogador_atual().cartas_distrito_mao.remove(distrito)
                # Identifica estrutura
                for destruido in estado.jogador_atual().distritos_construidos:
                    if destruido.nome_do_distrito == 'Estrutura':
                        # Destrói estrutura e remove pontos parciais
                        estado.jogador_atual().distritos_construidos.remove(destruido)
                        estado.tabuleiro.baralho_distritos.append(destruido)
                        estado.jogador_atual().pontuacao -= destruido.valor_do_distrito
                        break
            # Pontua distrito
            estado.jogador_atual().pontuacao += distrito.valor_do_distrito
            # Constrói distrito
            estado.jogador_atual().distritos_construidos.append(distrito)
            break
        # Marca flag de ação utilizada (a construção dos estábulos não conta para o limite de construções do turno)
        if not estado.jogador_atual().distritos_construidos[-1].nome_do_distrito == 'Estábulos':
            super().ativar(estado)


class HabilidadeAssassina(Acao):
    def __init__(self):
        super().__init__('Assassina: Anuncie um personagem que você deseja assassinar. O personagem assassinado perde o turno.', TipoAcao.HabilidadeAssassina)

    def ativar(self, estado: Estado):
        # Mostra opções ao jogador
        # A Assassina não pode afetar o personagem de rank 1 (ele próprio)
        # Não faz sentido escolher um personagem descartado visível
        i = 0
        opcoes_personagem: List[CartaPersonagem] = []
        for personagem in estado.tabuleiro.personagens:
            if personagem.rank > 1 and personagem not in estado.tabuleiro.cartas_visiveis:
                opcoes_personagem.append(personagem)
                print(f'{i}: {personagem}')
                i += 1
        # Aguarda escolha do jogador
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
            # Marca flag do efeito da Assassina
            for jogador in estado.jogadores:
                if jogador.personagem == opcoes_personagem[escolha_personagem]:
                    jogador.morto = True
                    break
            break
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeLadrao(Acao):
    def __init__(self):
        super().__init__(
            'Ladrão: Anuncie um personagem que você deseja roubar. O personagem roubado entrega todo seu ouro ao ladrão.', TipoAcao.HabilidadeLadrao)

    def ativar(self, estado: Estado):
        # O Ladrão não pode afetar o personagem morto pela Assassina
        personagem_assassinado = None
        for jogador in estado.jogadores:
            if jogador.morto:
                personagem_assassinado = jogador.personagem
        # O Ladrão não pode afetar o personagem de rank 1 e 2 (ele próprio)
        # Não faz sentido escolher um personagem descartado visível
        i = 0
        opcoes_personagem: List[CartaPersonagem] = []
        for personagem in estado.tabuleiro.personagens:
            if personagem != personagem_assassinado and personagem.rank > 2 and personagem not in estado.tabuleiro.cartas_visiveis:
                opcoes_personagem.append(personagem)
                # Mostra opções ao jogador
                print(f'{i}: {personagem}')
                i += 1
        # Aguarda escolha do jogador
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
            # Marca flag do efeito do Ladrão
            for jogador in estado.jogadores:
                if jogador.personagem == opcoes_personagem[escolha_personagem]:
                    jogador.roubado = True
                    break
            break
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeMago(Acao):
    def __init__(self):
        super().__init__(
            'Mago: Olhe a mão de outro jogador e escolha 1 carta. Pague para construí-la imediatamente ou adicione-a à sua mão.', TipoAcao.HabilidadeMago)

    def ativar(self, estado: Estado):
        # Mostra opções ao jogador (não pode escolher a si mesmo)
        print('Jogadores:')
        i = 0
        opcoes_jogadores: List[Jogador] = []
        for jogador in estado.jogadores:
            if jogador != estado.jogador_atual() and not jogador.cartas_distrito_mao:
                opcoes_jogadores.append(jogador)
                print(f'{i}: {jogador.nome}')
                i += 1
        if not opcoes_jogadores:
            print('Não existe opção válida para aplicar o efeito.')
            super().ativar(estado)
            return
        # Aguarda escolha do jogador
        while True:
            escolha_jogador = input('Digite o número do jogador que deseja olhar a mão e pegar 1 carta: ')
            try:
                escolha_jogador = int(escolha_jogador)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_jogador < len(opcoes_jogadores) - 1:
                print('Escolha inválida.')
                continue
            break
        # Mostra opções ao jogador
        print('Mão do jogador escolhido:')
        for i, carta in enumerate(opcoes_jogadores[escolha_jogador].cartas_distrito_mao):
            print(f'{i}: {carta.imprimir_tudo()}')
        # Aguarda escolha do jogador
        while True:
            escolha_carta = input('Digite o número da carta que deseja pegar para construir ou para sua mão: ')
            try:
                escolha_carta = int(escolha_carta)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_carta < len(opcoes_jogadores[escolha_jogador].cartas_distrito_mao):
                print('Escolha inválida.')
                continue
            break
        # Remove carta escolhida da mão do jogador escolhido
        distrito = opcoes_jogadores[escolha_jogador].cartas_distrito_mao[escolha_carta]
        opcoes_jogadores[escolha_jogador].cartas_distrito_mao.remove(distrito)
        # Adiciona carta escolhida na mão do jogador atual
        estado.jogador_atual().cartas_distrito_mao.append(distrito)
        # Identifica distritos que podem ser construídos
        distritos_para_construir: List[CartaDistrito] = []
        # Identifica distritos que podem ser destruídos para construir a necrópole sem custo
        distritos_para_construir_necropole: List[(CartaDistrito, CartaDistrito)] = []
        # Identifica opções especiais para construir o covil dos ladrões (divisão do custo em ouro e cartas da mão)
        distritos_para_construir_covil_ladroes: List[(CartaDistrito, int, int)] = []
        # Identifica opções de construção ao destruir a Estrutura
        distritos_para_construir_estrutura: List[CartaDistrito] = []
        # Identifica se o jogador construiu a Fábrica (afeta custo dos distritos especiais)
        fabrica = estado.jogador_atual().construiu_distrito('Fábrica')
        # Identifica se o jogador construiu a Estrutura (adiciona opções de construção sem custo)
        estrutura = estado.jogador_atual().construiu_distrito('Estrutura')
        # Verifica se é permitido construir distrito escolhido
        permitido = True
        # O Monumento não pode ser construído se a cidade já possuir 5 ou mais distritos
        if distrito.nome_do_distrito == 'Monumento' and len(estado.jogador_atual().distritos_construidos) >= 5:
            permitido = False
        # Cofre secreto nunca pode ser construído
        if distrito.nome_do_distrito == 'Cofre Secreto':
            permitido = False
        if permitido:
            # Pode construir sem custo ao destruir Estrutura
            if estrutura:
                distritos_para_construir_estrutura.append(distrito)
            # Deve possuir ouro suficiente para construir o distrito (Fábrica dá desconto para distritos especiais)
            if distrito.valor_do_distrito <= estado.jogador_atual().ouro or \
                    (fabrica and distrito.tipo_de_distrito == TipoDistrito.Especial and distrito.valor_do_distrito - 1 <= estado.jogador_atual().ouro):
                distritos_para_construir.append(distrito)
            # A necrópole pode ser construída sem custo destruindo um dos seus distritos
            if distrito.nome_do_distrito == 'Necrópole':
                for distrito_construido in estado.jogador_atual().distritos_construidos:
                    # O caso da Estrutura foi tratado em separado
                    if distrito_construido.nome_do_distrito != 'Estrutura':
                        distritos_para_construir_necropole.append((distrito, distrito_construido))
            # O covil dos ladrões pode ser construído com um custo misto de ouro e cartas da mão
            if distrito.nome_do_distrito == 'Covil dos Ladrões':
                qtd_cartas = len(estado.jogador_atual().cartas_distrito_mao) - 1
                # Não é necessário ter mais que 6 cartas no pagamento, pois o custo do distrito é 6 (5 com fábrica)
                if qtd_cartas > 6:
                    qtd_cartas = 6
                if fabrica and qtd_cartas > 5:
                    qtd_cartas = 5
                qtd_ouro = distrito.valor_do_distrito - 1
                # Fábrica concede 1 de desconto para distritos especiais
                if fabrica:
                    qtd_ouro -= 1
                while qtd_ouro + qtd_cartas >= distrito.valor_do_distrito:
                    if qtd_ouro > estado.jogador_atual().ouro:
                        qtd_ouro -= 1
                        continue
                    distritos_para_construir_covil_ladroes.append((distrito, qtd_ouro, distrito.valor_do_distrito - qtd_ouro))
                    if qtd_ouro > 0:
                        qtd_ouro -= 1
                    else:
                        qtd_cartas -= 1
        if len(distritos_para_construir) + len(distritos_para_construir_necropole) + \
                len(distritos_para_construir_covil_ladroes) + len(distritos_para_construir_estrutura) == 0 or not permitido:
            print('Não é possível construir o distrito!')
        else:
            # Mostra opções ao jogador
            print(f'0: Não desejo construir o distrito.')
            i = 0
            for carta in distritos_para_construir:
                i += 1
                print(f'{i}: {carta.imprimir_tudo()}')
            for carta, distrito in distritos_para_construir_necropole:
                i += 1
                print(f'{i}: {carta.imprimir_tudo()} - Distrito para destruir: {distrito.nome_do_distrito}')
            for carta, qtd_ouro, qtd_cartas in distritos_para_construir_covil_ladroes:
                i += 1
                print(f'{i}: {carta.imprimir_tudo()} - Custo em ouro: {qtd_ouro} - Custo em cartas da mão: {qtd_cartas}')
            for carta in distritos_para_construir_estrutura:
                i += 1
                print(f'{i}: {carta.imprimir_tudo()} - Distrito para destruir: Estrutura')
            # Aguarda escolha do jogador
            while True:
                escolha_construir = input('Digite o número do distrito que deseja construir: ')
                try:
                    escolha_construir = int(escolha_construir)
                except ValueError:
                    print('Escolha inválida.')
                    continue
                if not 0 <= escolha_construir <= len(distritos_para_construir) + \
                        len(distritos_para_construir_necropole) + len(distritos_para_construir_covil_ladroes) + len(distritos_para_construir_estrutura):
                    print('Escolha inválida.')
                    continue
                # Finaliza ação se jogador decidiu não construir
                if escolha_construir == 0:
                    break
                # Construção normal
                if escolha_construir <= len(distritos_para_construir):
                    distrito = distritos_para_construir[escolha_construir - 1]
                    # Retira distrito construído da mão
                    estado.jogador_atual().cartas_distrito_mao.remove(distrito)
                    # Paga distrito e salva ouro gasto
                    estado.jogador_atual().ouro -= distrito.valor_do_distrito
                    estado.jogador_atual().ouro_gasto += distrito.valor_do_distrito
                    # Fábrica concede 1 de desconto para distritos especiais
                    if fabrica and distrito.tipo_de_distrito == TipoDistrito.Especial:
                        estado.jogador_atual().ouro += 1
                        estado.jogador_atual().ouro_gasto -= 1
                # Construção de necrópole sem custo de ouro
                elif escolha_construir <= len(distritos_para_construir) + len(distritos_para_construir_necropole):
                    (distrito, destruido) = distritos_para_construir_necropole[escolha_construir - len(distritos_para_construir) - 1]
                    # Retira distrito construído da mão
                    estado.jogador_atual().cartas_distrito_mao.remove(distrito)
                    # Destrói distrito escolhido e remove pontos parciais
                    estado.jogador_atual().distritos_construidos.remove(destruido)
                    estado.tabuleiro.baralho_distritos.append(destruido)
                    estado.jogador_atual().pontuacao -= destruido.valor_do_distrito
                # Construção de covil dos ladrões com custo misto de ouro e cartas
                elif escolha_construir <= len(distritos_para_construir) + len(distritos_para_construir_necropole) + len(distritos_para_construir_covil_ladroes):
                    (distrito, qtd_ouro, qtd_cartas) = distritos_para_construir_covil_ladroes[escolha_construir -
                                                                                              len(distritos_para_construir) -
                                                                                              len(distritos_para_construir_necropole) - 1]
                    # Retira distrito construído da mão
                    estado.jogador_atual().cartas_distrito_mao.remove(distrito)
                    # Paga distrito e salva ouro gasto
                    estado.jogador_atual().ouro -= qtd_ouro
                    estado.jogador_atual().ouro_gasto += qtd_ouro
                    # Escolhe carta para pagar o resto do custo
                    for i in range(qtd_cartas):
                        print(f'Escolha as cartas que usará para pagar o custo. Faltam {qtd_cartas - i} cartas.')
                        for j, carta in enumerate(estado.jogador_atual().cartas_distrito_mao):
                            print(f'{j}: {carta.imprimir_tudo()}')
                        while True:
                            escolha_carta = input('Digite o número do distrito que deseja descartar: ')
                            try:
                                escolha_carta = int(escolha_carta)
                            except ValueError:
                                print('Escolha inválida.')
                                continue
                            if not 0 <= escolha_carta < len(estado.jogador_atual().cartas_distrito_mao):
                                print('Escolha inválida.')
                                continue
                            # Descarta carta escolhida
                            carta = estado.jogador_atual().cartas_distrito_mao[escolha_carta]
                            estado.jogador_atual().cartas_distrito_mao.remove(carta)
                            estado.tabuleiro.baralho_distritos.append(carta)
                            break
                # Construção sem custo destruíndo a Estrutura
                else:
                    distrito = distritos_para_construir_estrutura[escolha_construir -
                                                                  len(distritos_para_construir) -
                                                                  len(distritos_para_construir_necropole) -
                                                                  len(distritos_para_construir_covil_ladroes) - 1]
                    # Retira distrito construído da mão
                    estado.jogador_atual().cartas_distrito_mao.remove(distrito)
                    # Identifica estrutura
                    for destruido in estado.jogador_atual().distritos_construidos:
                        if destruido.nome_do_distrito == 'Estrutura':
                            # Destrói estrutura e remove pontos parciais
                            estado.jogador_atual().distritos_construidos.remove(destruido)
                            estado.tabuleiro.baralho_distritos.append(destruido)
                            estado.jogador_atual().pontuacao -= destruido.valor_do_distrito
                            break
                # Pontua distrito
                estado.jogador_atual().pontuacao += distrito.valor_do_distrito
                # Constrói distrito
                estado.jogador_atual().distritos_construidos.append(distrito)
                break
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeRei(Acao):
    def __init__(self):
        super().__init__('Rei: Ganhe 1 ouro para cada um dos seus distritos NOBRES.', TipoAcao.HabilidadeRei)

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
        super().__init__('Cardeal: Ganhe 1 carta para cada um dos seus distritos RELIGIOSOS.', TipoAcao.HabilidadeCardeal)

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
        super().__init__('Navegadora: Ganhe 4 ouros extras ou 4 cartas extras.', TipoAcao.HabilidadeNavegadora)

    def ativar(self, estado: Estado):
        # Aguarda escolha do jogador
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
            if escolha_recurso == 0:
                estado.jogador_atual().ouro += 4
            elif escolha_recurso == 1:
                estado.jogador_atual().cartas_distrito_mao.extend(estado.tabuleiro.baralho_distritos[0:4])
                del estado.tabuleiro.baralho_distritos[0:4]
            break
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeSenhordaGuerraDestruir(Acao):
    def __init__(self):
        super().__init__('Senhor da Guerra: Destrua 1 distrito, pagando 1 ouro a menos que o custo dele.', TipoAcao.HabilidadeSenhordaGuerraDestruir)

    def ativar(self, estado: Estado):
        # Identifica distritos que podem ser destruídos
        distritos_para_destruir: List[(CartaDistrito, Jogador, int)] = []
        # É permitido destruir um dos seus próprios distritos
        for jogador in estado.jogadores:
            # Não é possível destruir um distrito de um jogador com 7+ distritos
            if not jogador.terminou:
                # Identifica se jogador construiu a Muralha (aumenta o custo de destruição)
                muralha = 1 if jogador.construiu_distrito('Muralha') else 0
                for carta in jogador.distritos_construidos:
                    # Trata caso especial da Muralha (efeito dela não afeta a si própria)
                    if carta.nome_do_distrito == 'Muralha' and carta.valor_do_distrito - 1 <= estado.jogador_atual().ouro:
                        distritos_para_destruir.append((carta, jogador, muralha))
                    # Não é possível destruir a Torre de Menagem
                    # Precisa ter ouro suficiente para destruir o distrito
                    elif not carta.nome_do_distrito == 'Torre de Menagem' and carta.valor_do_distrito - 1 + muralha <= estado.jogador_atual().ouro:
                        distritos_para_destruir.append((carta, jogador, muralha))
        if len(distritos_para_destruir) == 0:
            print('Não é possível destruir nenhum distrito!')
            super().ativar(estado)
            return
        # Mostra opções ao jogador
        print(f'0: Não desejo destruir nenhum distrito.')
        for i, (carta, jogador, muralha) in enumerate(distritos_para_destruir):
            print(f'{i + 1}: {carta.imprimir_tudo()} - Jogador: {jogador.nome}')
        # Aguarda escolha do jogador
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
            if escolha_destruir == 0:
                super().ativar(estado)
                return
            # Paga o custo e destrói distrito escolhido do jogador alvo
            (distrito, jogador, muralha) = distritos_para_destruir[escolha_destruir - 1]
            # Trata caso especial da Muralha (efeito dela não afeta a si mesmo)
            if distrito.nome_do_distrito == 'Muralha':
                estado.jogador_atual().ouro -= distrito.valor_do_distrito - 1
            else:
                estado.jogador_atual().ouro -= distrito.valor_do_distrito - 1 + muralha
            jogador.pontuacao -= distrito.valor_do_distrito
            jogador.distritos_construidos.remove(distrito)
            estado.tabuleiro.baralho_distritos.append(distrito)
            # Indentifica se o distrito destruído foi o Museu e aplica efeitos secundários
            if distrito.nome_do_distrito == 'Museu':
                jogador.pontuacao -= len(jogador.distritos_museu)
                estado.tabuleiro.baralho_distritos.extend(jogador.distritos_museu)
                jogador.distritos_museu = []
            break
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeSenhordaGuerraColetar(Acao):
    def __init__(self):
        super().__init__('Senhor da Guerra: Ganhe 1 ouro para cada um dos seus distritos MILITARES.', TipoAcao.HabilidadeSenhordaGuerraColetar)

    def ativar(self, estado: Estado):
        # Contabiliza distritos militares para ganhar ouro
        for distrito in estado.jogador_atual().distritos_construidos:
            # O efeito da carta Escola de magia é ser contabilizada como qualquer tipo, portanto também é militar
            if distrito.tipo_de_distrito == TipoDistrito.Militar or distrito.nome_do_distrito == 'Escola de Magia':
                estado.jogador_atual().ouro += 1
        # Marca flag de ação utilizada
        super().ativar(estado)


class Laboratorio(Acao):
    def __init__(self):
        super().__init__('Laboratório: Uma vez por turno, descarte 1 carta da sua mão para ganhar 2 ouros.', TipoAcao.Laboratorio)

    def ativar(self, estado: Estado):
        # Mostra opções ao jogador
        for i, carta in enumerate(estado.jogador_atual().cartas_distrito_mao):
            print(f'{i}: {carta.imprimir_tudo()}')
        while True:
            escolha_carta = input('Digite o número do distrito que deseja descartar pelo ouro: ')
            try:
                escolha_carta = int(escolha_carta)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_carta < len(estado.jogador_atual().cartas_distrito_mao):
                print('Escolha inválida.')
                continue
            # Descarta carta pelo ouro
            carta = estado.jogador_atual().cartas_distrito_mao.pop(escolha_carta)
            estado.tabuleiro.baralho_distritos.append(carta)
            estado.jogador_atual().ouro += 2
            break
        # Marca flag de ação utilizada
        super().ativar(estado)


class Arsenal(Acao):
    def __init__(self):
        super().__init__('Arsenal: No seu turno, destrua o Arsenal para destruir 1 distrito à sua escolha.', TipoAcao.Arsenal)

    def ativar(self, estado: Estado):
        # Identifica distritos que podem ser destruídos
        distritos_para_destruir: List[(CartaDistrito, Jogador)] = []
        # É permitido destruir um dos seus próprios distritos
        for jogador in estado.jogadores:
            # Não é possível destruir um distrito de um jogador com 7+ distritos
            if not jogador.terminou:
                for carta in jogador.distritos_construidos:
                    # Não é possível destruir o próprio Arsenal
                    if carta.nome_do_distrito != 'Arsenal':
                        distritos_para_destruir.append((carta, jogador))
        if len(distritos_para_destruir) == 0:
            print('Não é possível destruir nenhum distrito!')
            super().ativar(estado)
            return
        # Mostra opções ao jogador
        print(f'0: Não desejo destruir nenhum distrito.')
        for i, (carta, jogador) in enumerate(distritos_para_destruir):
            print(f'{i + 1}: {carta.imprimir_tudo()} - Jogador: {jogador.nome}')
        # Aguarda escolha do jogador
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
            if escolha_destruir == 0:
                super().ativar(estado)
                return
            # Paga o custo e destrói distrito escolhido do jogador alvo
            (distrito, jogador) = distritos_para_destruir[escolha_destruir - 1]
            jogador.pontuacao -= distrito.valor_do_distrito
            jogador.distritos_construidos.remove(distrito)
            estado.tabuleiro.baralho_distritos.append(distrito)
            # Indentifica se o distrito destruído foi o Museu e aplica efeitos secundários
            if distrito.nome_do_distrito == 'Museu':
                jogador.pontuacao -= len(jogador.distritos_museu)
                estado.tabuleiro.baralho_distritos.extend(jogador.distritos_museu)
                jogador.distritos_museu = []
            # Identifica e destrói Arsenal
            for arsenal in estado.jogador_atual().distritos_construidos:
                if arsenal.nome_do_distrito == 'Arsenal':
                    estado.jogador_atual().distritos_construidos.remove(arsenal)
                    estado.tabuleiro.baralho_distritos.append(arsenal)
                    estado.jogador_atual().pontuacao -= arsenal.valor_do_distrito
                    break
            break
        # Marca flag de ação utilizada
        super().ativar(estado)


class Forja(Acao):
    def __init__(self):
        super().__init__('Forja: Uma vez por turno, pague 2 ouros para receber 3 cartas.', TipoAcao.Forja)

    def ativar(self, estado: Estado):
        # Pescar cartas do baralho e adicionar na mão do jogador
        cartas_compradas = estado.tabuleiro.baralho_distritos[:3]
        del estado.tabuleiro.baralho_distritos[:3]
        estado.jogador_atual().cartas_distrito_mao.extend(cartas_compradas)
        # Paga custo do efeito
        estado.jogador_atual().ouro -= 2
        # Marca flag de ação utilizada
        super().ativar(estado)


class Museu(Acao):
    def __init__(self):
        super().__init__('Museu: Uma vez por turno, coloque 1 carta da sua mão, voltada para baixo, sob o museu.'
                         'Ao final da partida, marque 1 ponto extra para cada carta sob o Museu', TipoAcao.Museu)

    def ativar(self, estado: Estado):
        # Mostra opções ao jogador
        for i, carta in enumerate(estado.jogador_atual().cartas_distrito_mao):
            print(f'{i}: {carta.imprimir_tudo()}')
        while True:
            escolha_carta = input('Digite o número do distrito que deseja colocar no Museu: ')
            try:
                escolha_carta = int(escolha_carta)
            except ValueError:
                print('Escolha inválida.')
                continue
            if not 0 <= escolha_carta < len(estado.jogador_atual().cartas_distrito_mao):
                print('Escolha inválida.')
                continue
            # Descarta carta e atualiza pontuação parcial
            carta = estado.jogador_atual().cartas_distrito_mao.pop(escolha_carta)
            estado.jogador_atual().distritos_museu.append(carta)
            estado.jogador_atual().pontuacao += 1
            break
        # Marca flag de ação utilizada
        super().ativar(estado)
