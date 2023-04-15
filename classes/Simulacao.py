# Imports
from random import shuffle
from classes.model.Acao import *
from classes.model.Tabuleiro import Tabuleiro
from classes.model.Jogador import Jogador


class Simulacao:
    # Construtor
    def __init__(self, num_jogadores: int, automatico: bool):
        # Define o número de jogadores
        self.num_jogadores = num_jogadores
        # Define se a criação dos jogadores será manual ou automática: 0 -> Manual || 1 -> Automática
        self.estado = self.criar_estado_inicial(automatico)
        self.acoes = self.criar_acoes()
        # Primeiro jogador a finalizar cidade (cosntruir 7 ou mais distritos)
        self.jogador_finalizador = None

    # Cria o estado inicial do tabuleiro
    def criar_estado_inicial(self, automatico) -> Estado:
        # Constrói o tabuleiro
        tabuleiro = Tabuleiro(self.num_jogadores, 8)
        if automatico:
            jogadores = self.criar_jogadores_automatico()
        else:
            jogadores = self.criar_jogadores_manual()

        # Loop para distribuição das cartas iniciais
        for jogador in jogadores:
            # Distribui 4 cartas para cada jogador
            jogador.cartas_distrito_mao.extend(tabuleiro.baralho_distritos[0:4])
            # Remove estas cartas do baralho de distritos
            del tabuleiro.baralho_distritos[0:4]

        # Sorteia o jogador inicial
        shuffle(jogadores)
        # O define como rei
        jogadores[0].rei = True

        return Estado(tabuleiro, jogadores)

    # Cria os jogadores de forma automática
    def criar_jogadores_automatico(self) -> list[Jogador]:
        lista_jogadores = []
        # Loop para nomear os jogadores
        for jogador in range(self.num_jogadores):
            # Bot 1, Bot 2, ..., Bot N
            lista_jogadores.append(Jogador(f"Bot {jogador + 1}"))

        return lista_jogadores

    # Cria os jogadores de forma manual
    def criar_jogadores_manual(self) -> list[Jogador]:
        lista_jogadores = []
        # Laço para nomear os jogadores
        for jogador in range(self.num_jogadores):
            # Informar o nome de cada um dos jogadores
            nome_jogador = input("Digite o nome do jogador:")
            lista_jogadores.append(Jogador(nome_jogador))

        return lista_jogadores

    @staticmethod
    # Cria lista de ações (ativas) do jogo
    def criar_acoes() -> list[Acao]:
        # Ações básicas
        acoes = [PassarTurno(), ColetarOuro(), ColetarCartas(), ConstruirDistrito(),
                 # Ações de personagem Rank 1
                 HabilidadeAssassina(),
                 # Ações de personagem Rank 2
                 HabilidadeLadrao(),
                 # Ações de personagem Rank 3
                 HabilidadeMago(),
                 # Ações de personagem Rank 4
                 HabilidadeRei(),
                 # Ações de personagem Rank 5
                 HabilidadeCardeal(),
                 # Ações de personagem Rank 6

                 # Ações de personagem Rank 7
                 HabilidadeNavegadora(),
                 # Ações de personagem Rank 8
                 HabilidadeSenhordaGuerraDestruir(), HabilidadeSenhordaGuerraColetar(),
                 # Ações de personagem Rank 9

                 # Ações de distritos especiais
                 Laboratorio(), Arsenal(), Forja(), Museu()]
        return acoes

    def acoes_disponiveis(self) -> list[Acao]:
        #acoes_disponiveis = []
        return self.acoes
        # for acao in TipoAcao:
        #     if acao == TipoAcao.ColetarOuro:
        #         if not self.estado.jogador_atual().coletou_recursos():
        #             acoes_disponiveis.append(self.acoes[acao.value])
        #     if acao == TipoAcao.ColetarCartas:
        #         if not self.estado.jogador_atual().coletou_recursos():
        #             acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.PassarTurno:
            #     if self.estado.jogador_atual().coletou_recursos():
            #         acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.ConstruirDistrito:
            #     if self.estado.jogador_atual().coletou_recursos() and \
            #             self.estado.jogador_atual().acoes_realizadas[TipoAcao.ConstruirDistrito.value] != 1:
            #         if self.estado.jogador_atual().personagem.nome != "Navegadora":
            #             acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.HabilidadeAssassina:
            #     if self.estado.jogador_atual().acoes_realizadas[
            #         TipoAcao.HabilidadeAssassina.value] != 1 and \
            #             self.estado.jogador_atual().personagem.nome == "Assassino":
            #         acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.HabilidadeLadrao:
            #     if self.estado.jogador_atual().acoes_realizadas[
            #         TipoAcao.HabilidadeLadrao.value] != 1 \
            #             and self.estado.jogador_atual().personagem.nome == "Ladrao":
            #         acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.HabilidadeMago:
            #     if self.estado.jogador_atual().acoes_realizadas[
            #         TipoAcao.HabilidadeMago.value] != 1 and \
            #             self.estado.jogador_atual().personagem.nome == "Mago":
            #         acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.HabilidadeRei:
            #     if self.estado.jogador_atual().acoes_realizadas[
            #         TipoAcao.HabilidadeRei.value] != 1 and \
            #             self.estado.jogador_atual().personagem.nome == "Rei":
            #         acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.HabilidadeCardealAtivo:
            #     if self.estado.jogador_atual().acoes_realizadas[
            #         TipoAcao.HabilidadeCardealAtivo.value] != 1 and \
            #             self.estado.jogador_atual().personagem.nome == "Cardeal" and \
            #             self.estado.jogador_atual().construiu == False:
            #         acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.HabilidadeCardealPassivo:
            #     if self.estado.jogador_atual().acoes_realizadas[
            #         TipoAcao.HabilidadeCardealPassivo.value] != 1 and \
            #             self.estado.jogador_atual().personagem.nome == "Cardeal":
            #         acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.HabilidadeAlquimista:
            #     if self.estado.jogador_atual().acoes_realizadas[
            #         TipoAcao.HabilidadeAlquimista.value] != 1 and \
            #             self.estado.jogador_atual().personagem.nome == "Alquimista":
            #         acoes_disponiveis.append(self.acoes[acao.value])
            #         # Disponivel apenas no final do turno
            # if acao == TipoAcao.HabilidadeNavegadora:
            #     if self.estado.jogador_atual().acoes_realizadas[
            #         TipoAcao.HabilidadeNavegadora.value] != 1 and \
            #             self.estado.jogador_atual().personagem.nome == "Navegadora":
            #         acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.HabilidadeSenhordaGuerra:
            #     if self.estado.jogador_atual().acoes_realizadas[
            #         TipoAcao.HabilidadeSenhordaGuerra.value] != 1 and \
            #             self.estado.jogador_atual().personagem.nome == "SenhordaGuerra":
            #         acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.Laboratorio:
            #     if self.estado.jogador_atual().acoes_realizadas[TipoAcao.Laboratorio.value] != 1 and len(
            #             self.estado.jogador_atual().cartas_distrito_mao) > 0:
            #         for nomeDistrito in self.estado.jogador_atual().distritos_construidos:
            #             if nomeDistrito.nome_do_distrito == "laboratorio":
            #                 acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.Necropole:
            #     if len(self.estado.jogador_atual().distritos_construidos) > 0:
            #         for nomeDistrito in self.estado.jogador_atual().cartas_distrito_mao:
            #             if nomeDistrito.nome_do_distrito == "necropole":
            #                 acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.Estrutura:
            #     if len(self.estado.jogador_atual().cartas_distrito_mao) > 0:
            #         for nomeDistrito in self.estado.jogador_atual().distritos_construidos:
            #             if nomeDistrito.nome_do_distrito == "estrutura":
            #                 acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.Estabulos:
            #     for nomeDistrito in self.estado.jogador_atual().cartas_distrito_mao:
            #         if nomeDistrito.nome_do_distrito == "estabulos" and self.estado.jogador_atual().personagem.nome != "Navegadora":
            #             acoes_disponiveis.append(self.acoes[acao.value])
            #         # if self.estado.jogador_atual().personagem.nome != "Navegadora":
            #         #     acoes_disponiveis.append(self.acoes[acao.value])
            # if acao == TipoAcao.CovilDosLadroes:
            #     for nomeDistrito in self.estado.jogador_atual().cartas_distrito_mao:
            #         if nomeDistrito.nome_do_distrito == "covil dos ladroes":
            #             acoes_disponiveis.append(self.acoes[acao.value])
        return acoes_disponiveis

    @staticmethod
    def imprimir_menu_acoes(acoes: list[Acao]) -> str:
        i = iter(acoes)
        texto = "Escolha uma ação das seguintes: \n\t" + str(next(i))
        for distrito in i:
            texto += ", " + str(distrito)
        return texto

    # Computa a pontuaçào final de cada jogador para definir vencedor
    def computar_pontuacao_final(self):
        for jogador in self.estado.jogadores:
            # Contabiliza pontuação parcial
            # Aqui já é contabilizado 1 ponto/moeda nos seus distritos
            jogador.pontuacao_final = jogador.pontuacao
            # 3 pontos por ter pelo menos 1 distrito de cada tipo
            # [Nobre, Religioso, Comercial, Militar, Especial]
            contador_tipos = [0, 0, 0, 0, 0]
            for tipo_construido in jogador.distritos_construidos:
                if tipo_construido.tipo_de_distrito == TipoDistrito.Nobre:
                    contador_tipos[0] += 1
                elif tipo_construido.tipo_de_distrito == TipoDistrito.Religioso:
                    contador_tipos[1] += 1
                elif tipo_construido.tipo_de_distrito == TipoDistrito.Comercial:
                    contador_tipos[2] += 1
                elif tipo_construido.tipo_de_distrito == TipoDistrito.Militar:
                    contador_tipos[3] += 1
                elif tipo_construido.tipo_de_distrito == TipoDistrito.Especial:
                    contador_tipos[4] += 1
            for qtd_tipo in contador_tipos:
                jogador.pontuacao_final += 3
                if qtd_tipo == 0:
                    jogador.pontuacao_final -= 3
                    break
            # 4 pontos para o primeiro jogador a completar a cidade
            if self.jogador_finalizador == jogador:
                jogador.pontuacao_final += 4
            # 2 pontos para os demais jogadores que tenham completado a cidade
            elif jogador.terminou:
                jogador.pontuacao_final += 2
            # Pontos extras dos distritos ESPECIAIS
            # Cofre Secreto (Ao final da partida, revele o Cofre Secreto da sua mão para marcar 3 pontos extras)
            for distrito in jogador.cartas_distrito_mao:
                if distrito.nome_do_distrito == 'Cofre Secreto':
                    jogador.pontuacao_final += 3
                    break
            for distrito_construido in jogador.distritos_construidos:
                # Estátua (Se você tiver a coroa no final da partida, marque 5 pontos extras)
                if distrito_construido.nome_do_distrito == 'Estátua' and jogador.rei:
                    jogador.pontuacao_final += 5
                # Basílica (Ao final da partida, marque 1 ponto extra para cada distrito especial na sua cidade que tenha um número ímpar como custo)
                if distrito_construido.nome_do_distrito == 'Basílica':
                    for especial_impar in jogador.distritos_construidos:
                        if especial_impar.tipo_de_distrito == TipoDistrito.Especial and especial_impar.valor_do_distrito % 2 == 1:
                            jogador.pontuacao_final += 1
                # Poço dos Desejos (Ao final da partida, marque 1 ponto extra para cada distrito ESPECIAL na sua cidade)
                if distrito_construido.nome_do_distrito == 'Poço dos Desejos':
                    jogador.pontuacao_final += qtd_tipo[4]
                # Tesouro Imperial (Ao final da partida, marque 1 ponto extra para cada ouro em seu tesouro)
                if distrito_construido.nome_do_distrito == 'Tesouro Imperial':
                    jogador.pontuacao_final += jogador.ouro
                # Sala de Mapas (Ao final da partida, marque 1 ponto extra para cada carta da sua mão)
                if distrito_construido.nome_do_distrito == 'Sala de Mapas':
                    jogador.pontuacao_final += len(jogador.cartas_distrito_mao)
                # Portão do Dragão (Ao final da partida, marque 2 pontos extras)
                if distrito_construido.nome_do_distrito == 'Portão do Dragão':
                    jogador.pontuacao_final += 2
                # Capitólio (Se você tiver pelo menos 3 distritos do mesmo tipo no final da partida, marque 3 pontos extras)
                pontuou_capitolio = False
                if distrito_construido.nome_do_distrito == 'Capitólio':
                    for qtd_tipo in contador_tipos:
                        if qtd_tipo >= 3:
                            jogador.pontuacao_final += 3
                            pontuou_capitolio = True
                            break
                # Torre de Marfim (Se a Torre de Marfim for o único distrito ESPECIAL na sua cidade ao final da partida, marque 5 pontos extras)
                if distrito_construido.nome_do_distrito == 'Torre de Marfim':
                    if qtd_tipo[4] == 1:
                        jogador.pontuacao_final += 5
                # Bairro Assombrado (Ao final da partida, o Bairro Assombrado vale como 1 tipo de distrito à sua escolha)
                if distrito_construido.nome_do_distrito == 'Bairro Assombrado':
                    melhor_pontuacao = 0
                    # Transformar bairro assombrado no tipo faltante
                    if qtd_tipo[4] > 1 and (qtd_tipo[0] == 0 ^ qtd_tipo[1] == 0 ^ qtd_tipo[2] == 0 ^ qtd_tipo[3] == 0):
                        ponto_potencial = 3
                        # perde 1 ponto caso também tenha poço dos desejos
                        if jogador.construiu_distrito('Poço dos Desejos'):
                            ponto_potencial -= 1
                        # perde 3 pontos caso pontuou capitólio com exatamente 3 distritos especiais
                        if jogador.construiu_distrito('Capitólio') and \
                                qtd_tipo[4] == 3 and qtd_tipo[0] < 3 and qtd_tipo[1] < 3 and qtd_tipo[2] < 3 and qtd_tipo[3] < 3:
                            ponto_potencial -= 3
                        # ganha 5 pontos caso tenha torre de marfim como único distrito especial
                        if jogador.construiu_distrito('Torre de Marfim') and qtd_tipo[4] == 2:
                            ponto_potencial += 5
                        if ponto_potencial > 0:
                            melhor_pontuacao = ponto_potencial
                    # Transformar bairro assombrado para pontuar capitólio
                    if jogador.construiu_distrito('Capitólio') and not pontuou_capitolio and \
                            (qtd_tipo[0] == 2 or qtd_tipo[1] == 2 or qtd_tipo[2] == 2 or qtd_tipo[3] == 2):
                        ponto_potencial = 3
                        # perde 1 ponto caso também tenha poço dos desejos
                        if jogador.construiu_distrito('Poço dos Desejos'):
                            ponto_potencial -= 1
                        # ganha 5 pontos caso tenha torre de marfim como único distrito especial
                        if jogador.construiu_distrito('Torre de Marfim') and qtd_tipo[4] == 2:
                            ponto_potencial += 5
                        if melhor_pontuacao < ponto_potencial:
                            melhor_pontuacao = ponto_potencial
                    # Transformar bairro assombrado para pontuar torre de marfim
                    if jogador.construiu_distrito('Torre de Marfim') and qtd_tipo[4] == 2:
                        if melhor_pontuacao < 5:
                            melhor_pontuacao = 5
                    jogador.pontuacao_final += melhor_pontuacao
