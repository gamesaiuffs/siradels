from classes.model.Estado import Estado
from classes.enum.TipoDistrito import TipoDistrito
from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.model.Jogador import Jogador
from classes.strategies.Estrategia import Estrategia


class Acao:
    def __init__(self, descricao: str, tipo_acao: TipoAcao):
        self.descricao: str = descricao
        self.tipo_acao: TipoAcao = tipo_acao

    def __str__(self):
        return f'{self.descricao}'

    def ativar(self, estado: Estado, estrategia: Estrategia | int = None):
        estado.jogador_atual.acoes_realizadas[self.tipo_acao.value] = True


class PassarTurno(Acao):
    def __init__(self):
        super().__init__('Passar seu turno.', TipoAcao.PassarTurno)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        # Otimiza a chamada do jogador atual
        jogador = estado.jogador_atual
        # Limpa flags de controle e ações realizadas
        jogador.acoes_realizadas = [False for _ in range(len(TipoAcao))]
        jogador.qtd_construido_turno = 0
        # Marca flag de ação utilizada
        super().ativar(estado)
        # Turno deve ser o último a ser atualizado, pois, afeta ponteiro para jogador atual
        estado.turno += 1


class ColetarOuro(Acao):
    def __init__(self):
        super().__init__('Pegue dois ouros do banco.', TipoAcao.ColetarOuro)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        # Adiciona dois de ouro ao jogador
        estado.jogador_atual.ouro += 2
        # Marca flag de ação utilizada
        super().ativar(estado)


class ColetarCartas(Acao):
    def __init__(self):
        super().__init__('Compre duas cartas do baralho de distritos, escolha uma e descarte a outra.', TipoAcao.ColetarCartas)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        qtd_cartas = 2
        # Baralho vazio
        if not estado.tabuleiro.baralho_distritos:
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
        if estado.jogador_atual.construiu_distrito('Biblioteca') or qtd_cartas == 1:
            estado.jogador_atual.cartas_distrito_mao.extend(cartas_compradas)
            super().ativar(estado)
            return
        # Aplica estratégia do jogador
        escolha_carta = estrategia.coletar_cartas(estado, cartas_compradas, qtd_cartas)
        # Adicionar na mão do jogador a carta escolhida e descarta cartas que não foram escolhidas
        if escolha_carta == 0:
            estado.jogador_atual.cartas_distrito_mao.append(cartas_compradas[0])
            estado.tabuleiro.baralho_distritos.append(cartas_compradas[1])
        elif escolha_carta == 1:
            estado.jogador_atual.cartas_distrito_mao.append(cartas_compradas[1])
            estado.tabuleiro.baralho_distritos.append(cartas_compradas[0])
        # Marca flag de ação utilizada
        super().ativar(estado)


class ConstruirDistrito(Acao):
    def __init__(self):
        super().__init__('Construa um distrito em sua cidade.', TipoAcao.ConstruirDistrito)

    def ativar(self, estado: Estado, estrategia: Estrategia | int = None):
        distritos_para_construir, distritos_para_construir_covil_ladroes = ConstruirDistrito.distritos_possiveis_construir(estado.jogador_atual)
        # Verifica se é possível construir ao menos 1 distrito da mão
        if len(distritos_para_construir) + len(distritos_para_construir_covil_ladroes) == 0:
            super().ativar(estado)
            return
        # Aplica estratégia do jogador
        if isinstance(estrategia, int):
            escolha_construir = estrategia
        else:
            escolha_construir = estrategia.construir_distrito(estado, distritos_para_construir, distritos_para_construir_covil_ladroes)
        # Construção normal
        if escolha_construir < len(distritos_para_construir):
            distrito = distritos_para_construir[escolha_construir]
            # Retira distrito construído da mão
            estado.jogador_atual.cartas_distrito_mao.remove(distrito)
            # Paga distrito
            estado.jogador_atual.ouro -= distrito.valor_do_distrito
            # Fábrica concede 1 de desconto para distritos especiais
            if estado.jogador_atual.construiu_distrito('Fábrica') and distrito.tipo_de_distrito == TipoDistrito.Especial:
                estado.jogador_atual.ouro += 1
        # Construção de covil dos ladrões com custo misto de ouro e cartas
        else:
            (distrito, qtd_ouro, qtd_cartas) = distritos_para_construir_covil_ladroes[escolha_construir - len(distritos_para_construir)]
            # Retira distrito construído da mão
            estado.jogador_atual.cartas_distrito_mao.remove(distrito)
            # Paga distrito
            estado.jogador_atual.ouro -= qtd_ouro
            # Escolhe carta para pagar o resto do custo
            for i in range(qtd_cartas):
                # Aplica estratégia do jogador
                escolha_carta = estrategia.construir_distrito_covil_dos_ladroes(estado, qtd_cartas, i)
                carta = estado.jogador_atual.cartas_distrito_mao[escolha_carta]
                estado.jogador_atual.cartas_distrito_mao.remove(carta)
                estado.tabuleiro.baralho_distritos.append(carta)
        # Constrói distrito para o Jogador
        estado.jogador_atual.construir(distrito)
        # Marca flag de ação utilizada (dependendo de o Jogador ter ou não a Arquiteta)
        if (estado.jogador_atual.qtd_construido_turno == 1 and estado.jogador_atual.personagem.nome != 'Arquiteta') \
           or estado.jogador_atual.qtd_construido_turno == 3:
            super().ativar(estado)

    @staticmethod
    def distritos_possiveis_construir(jogador_atual: Jogador) -> tuple[list[CartaDistrito], list[CartaDistrito]]:
        # Identifica distritos que podem ser construídos
        distritos_para_construir: list[CartaDistrito] = []
        # Identifica opções especiais para construir o covil dos ladrões (divisão do custo em ouro e cartas da mão)
        distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)] = []
        # Identifica se o jogador construiu a Fábrica (afeta custo dos distritos especiais)
        fabrica = jogador_atual.construiu_distrito('Fábrica')
        # Identifica se o jogador construiu a Pedreira (adiciona opções de construção repetida)
        pedreira = jogador_atual.construiu_distrito('Pedreira')
        # Enumera opções de construção
        for carta in jogador_atual.cartas_distrito_mao:
            # Distritos repetidos não podem ser construídos (exceto que tenha construído a Pedreira)
            repetido = jogador_atual.construiu_distrito(carta.nome_do_distrito)
            if repetido and not pedreira:
                continue
            # Deve possuir ouro suficiente para construir o distrito (Fábrica dá desconto para distritos especiais)
            if carta.valor_do_distrito <= jogador_atual.ouro or \
                    (fabrica and carta.tipo_de_distrito == TipoDistrito.Especial and carta.valor_do_distrito - 1 <= jogador_atual.ouro):
                distritos_para_construir.append(carta)
            # O covil dos ladrões pode ser construído com um custo misto de ouro e cartas da mão
            if carta.nome_do_distrito == 'Covil dos Ladrões':
                qtd_cartas = len(jogador_atual.cartas_distrito_mao) - 1
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
                    if qtd_ouro > jogador_atual.ouro:
                        qtd_ouro -= 1
                        continue
                    distritos_para_construir_covil_ladroes.append((carta, qtd_ouro, carta.valor_do_distrito - qtd_ouro))
                    if qtd_ouro > 0:
                        qtd_ouro -= 1
                    else:
                        qtd_cartas -= 1
        return distritos_para_construir, distritos_para_construir_covil_ladroes


class HabilidadeAssassina(Acao):
    def __init__(self):
        super().__init__('Assassina: Anuncie um personagem que você deseja assassinar. O personagem assassinado perde o turno.', TipoAcao.HabilidadeAssassina)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        # A Assassina não pode afetar o personagem de rank 1 (ele próprio)
        # Não faz sentido escolher um personagem descartado visível
        opcoes_personagem: list[CartaPersonagem] = []
        for personagem in estado.tabuleiro.personagens:
            if personagem.rank > 1 and personagem not in estado.tabuleiro.cartas_visiveis:
                opcoes_personagem.append(personagem)
        # Aplica estratégia do jogador
        escolha_personagem = estrategia.habilidade_assassina(estado, opcoes_personagem)
        # Marca flag do efeito da Assassina
        for jogador in estado.jogadores:
            if jogador.personagem == opcoes_personagem[escolha_personagem]:
                jogador.morto = True
                break
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeLadrao(Acao):
    def __init__(self):
        super().__init__(
            'Ladrão: Anuncie um personagem que você deseja roubar. O personagem roubado entrega todo seu ouro ao ladrão.', TipoAcao.HabilidadeLadrao)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        # O Ladrão não pode afetar o personagem morto pela Assassina
        personagem_assassinado = None
        for jogador in estado.jogadores:
            if jogador.morto:
                personagem_assassinado = jogador.personagem
                break
        # O Ladrão não pode afetar o personagem de rank 1 e 2 (ele próprio)
        # Não faz sentido escolher um personagem descartado visível
        opcoes_personagem: list[CartaPersonagem] = []
        for personagem in estado.tabuleiro.personagens:
            if personagem != personagem_assassinado and personagem.rank > 2 and personagem not in estado.tabuleiro.cartas_visiveis:
                opcoes_personagem.append(personagem)
        # Aplica estratégia do jogador
        escolha_personagem = estrategia.habilidade_ladrao(estado, opcoes_personagem)
        # Marca flag do efeito do Ladrão
        for jogador in estado.jogadores:
            if jogador.personagem == opcoes_personagem[escolha_personagem]:
                jogador.roubado = True
                break
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeIlusionistaTrocar(Acao):
    def __init__(self):
        super().__init__('Ilusionista: Troque sua mão com a de outro jogador.', TipoAcao.HabilidadeIlusionistaTrocar)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        opcoes_jogadores: list[Jogador] = []
        for jogador in estado.jogadores:
            if jogador != estado.jogador_atual and len(jogador.cartas_distrito_mao) > 0:
                opcoes_jogadores.append(jogador)
        # Opção de escolha para o efeito (0- Trocar cartas com outro Jogador ou 1- descartar e pescar cartas)
        # Se existem jogadores com cartas e o jogador atual também tem cartas na mão, ambas opções são válidas
        if not opcoes_jogadores:
            super().ativar(estado)
            return
        # Aplica efeito troca de mão com outro jogador
        escolha_jogador = estrategia.habilidade_ilusionista_trocar(estado, opcoes_jogadores)
        try:
            estado.jogador_atual.cartas_distrito_mao, opcoes_jogadores[escolha_jogador].cartas_distrito_mao \
            = opcoes_jogadores[escolha_jogador].cartas_distrito_mao, estado.jogador_atual.cartas_distrito_mao
        except IndexError:
            print(estrategia)
            print(escolha_jogador)
            print(opcoes_jogadores)
            print(opcoes_jogadores[escolha_jogador])
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeIlusionistaDescartar(Acao):
    def __init__(self):
        super().__init__('Ilusionista: Descarte quantas cartas quiser para ganhar um número igual de cartas.', TipoAcao.HabilidadeIlusionistaDescartar)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        # Computa quantidade máxima de cartas que pode ser descartada
        qtd_maxima = len(estado.jogador_atual.cartas_distrito_mao) \
            if len(estado.jogador_atual.cartas_distrito_mao) <= len(estado.tabuleiro.baralho_distritos) else len(estado.tabuleiro.baralho_distritos)
        if qtd_maxima == 0:
            super().ativar(estado)
            return
        qtd_cartas = estrategia.habilidade_ilusionista_descartar_qtd_cartas(estado, qtd_maxima)
        # Escolhe carta para descartar
        for i in range(qtd_cartas):
            # Aplica estratégia do jogador
            escolha_carta = estrategia.habilidade_ilusionista_descartar_carta(estado, qtd_cartas, i)
            carta = estado.jogador_atual.cartas_distrito_mao[escolha_carta]
            estado.jogador_atual.cartas_distrito_mao.remove(carta)
            estado.tabuleiro.baralho_distritos.append(carta)
        # Repõem cartas descartadas com o baralho
        cartas_compradas = estado.tabuleiro.baralho_distritos[:qtd_cartas]
        del estado.tabuleiro.baralho_distritos[:qtd_cartas]
        estado.jogador_atual.cartas_distrito_mao.extend(cartas_compradas)
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeRei(Acao):
    def __init__(self):
        super().__init__('Rei: Ganhe 1 ouro para cada um dos seus distritos NOBRES.', TipoAcao.HabilidadeRei)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        # Contabiliza distritos nobres
        for distrito in estado.jogador_atual.distritos_construidos:
            # O efeito da carta Escola de magia é ser contabilizada como qualquer tipo, portanto também é nobre
            if distrito.tipo_de_distrito == TipoDistrito.Nobre or distrito.nome_do_distrito == 'Escola de Magia':
                estado.jogador_atual.ouro += 1
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeBispo(Acao):
    def __init__(self):
        super().__init__('Bispo: Ganhe 1 ouro para cada um dos seus distritos RELIGIOSOS.', TipoAcao.HabilidadeBispo)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        # Contabiliza distritos religiosos
        for distrito in estado.jogador_atual.distritos_construidos:
            # O efeito da carta Escola de magia é ser contabilizada como qualquer tipo, portanto também é religioso
            if distrito.tipo_de_distrito == TipoDistrito.Religioso or distrito.nome_do_distrito == 'Escola de Magia':
                estado.jogador_atual.ouro += 1
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeComerciante(Acao):
    def __init__(self):
        super().__init__('Comerciante: Ganhe 1 ouro para cada um dos seus distritos COMERCIAIS.', TipoAcao.HabilidadeComerciante)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        # Contabiliza distritos comerciais
        for distrito in estado.jogador_atual.distritos_construidos:
            # O efeito da carta Escola de magia é ser contabilizada como qualquer tipo, portanto também é comercial
            if distrito.tipo_de_distrito == TipoDistrito.Comercial or distrito.nome_do_distrito == 'Escola de Magia':
                estado.jogador_atual.ouro += 1
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeSenhorDaGuerraDestruir(Acao):
    def __init__(self):
        super().__init__('Senhor da Guerra: Destrua 1 distrito, pagando 1 ouro a menos que o custo dele.', TipoAcao.HabilidadeSenhorDaGuerraDestruir)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        # Identifica distritos que podem ser destruídos
        distritos_para_destruir: list[(CartaDistrito, Jogador)] = []
        # É permitido destruir um dos seus próprios distritos
        for jogador in estado.jogadores:
            # Não é possível destruir um distrito de um jogador com 7+ distritos
            # Também não é possível destruir os distritos de quem tiver o bispo
            if not jogador.terminou and jogador.personagem.nome != 'Bispo':
                # Identifica distritos que podem ser destruídos
                for carta in jogador.distritos_construidos:
                    # Não é possível destruir a Torre de Menagem
                    # Precisa ter ouro suficiente para destruir o distrito
                    if not carta.nome_do_distrito == 'Torre de Menagem' and carta.valor_do_distrito - 1 <= estado.jogador_atual.ouro:
                        distritos_para_destruir.append((carta, jogador))
        # Verifica se é possível destruir algum distrito
        if len(distritos_para_destruir) == 0:
            super().ativar(estado)
            return
        # Aplica estratégia do jogador
        escolha_destruir = estrategia.habilidade_senhor_da_guerra_destruir(estado, distritos_para_destruir)
        if escolha_destruir == 0:
            super().ativar(estado)
            return
        # Paga o custo e destrói distrito escolhido do jogador alvo
        (distrito, jogador) = distritos_para_destruir[escolha_destruir - 1]
        estado.jogador_atual.ouro -= distrito.valor_do_distrito - 1
        jogador.destruir(estado, distrito)
        # Marca flag de ação utilizada
        super().ativar(estado)


class HabilidadeSenhordaGuerraColetar(Acao):
    def __init__(self):
        super().__init__('Senhor da Guerra: Ganhe 1 ouro para cada um dos seus distritos MILITARES.', TipoAcao.HabilidadeSenhorDaGuerraColetar)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        # Contabiliza distritos militares
        for distrito in estado.jogador_atual.distritos_construidos:
            # O efeito da carta Escola de magia é ser contabilizada como qualquer tipo, portanto também é militar
            if distrito.tipo_de_distrito == TipoDistrito.Militar or distrito.nome_do_distrito == 'Escola de Magia':
                estado.jogador_atual.ouro += 1
        # Marca flag de ação utilizada
        super().ativar(estado)


class Laboratorio(Acao):
    def __init__(self):
        super().__init__('Laboratório: Uma vez por turno, descarte 1 carta da sua mão para ganhar 2 ouros.', TipoAcao.Laboratorio)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        # Se o jogador não tiver cartas na mão não é possível ativar o efeito
        if not estado.jogador_atual.cartas_distrito_mao:
            super().ativar(estado)
            return
        # Aplica estratégia do jogador
        escolha_carta = estrategia.laboratorio(estado)
        # Descarta carta pelo ouro
        carta = estado.jogador_atual.cartas_distrito_mao.pop(escolha_carta)
        estado.tabuleiro.baralho_distritos.append(carta)
        estado.jogador_atual.ouro += 2
        # Marca flag de ação utilizada
        super().ativar(estado)


class Forja(Acao):
    def __init__(self):
        super().__init__('Forja: Uma vez por turno, pague 2 ouros para receber 3 cartas.', TipoAcao.Forja)

    def ativar(self, estado: Estado, estrategia: Estrategia = None):
        # Se o jogador não tiver ao menos 2 de ouro não é possível ativar o efeito
        if estado.jogador_atual.ouro < 2:
            super().ativar(estado)
            return
        # Pescar cartas do baralho e adicionar na mão do jogador
        qtd_cartas = len(estado.tabuleiro.baralho_distritos)
        if qtd_cartas > 3:
            qtd_cartas = 3
        if qtd_cartas > 0:
            cartas_compradas = estado.tabuleiro.baralho_distritos[:qtd_cartas]
            del estado.tabuleiro.baralho_distritos[:qtd_cartas]
            estado.jogador_atual.cartas_distrito_mao.extend(cartas_compradas)
            # Paga custo do efeito
            estado.jogador_atual.ouro -= 2
        # Marca flag de ação utilizada
        super().ativar(estado)
