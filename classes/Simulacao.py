from random import shuffle
from classes.model.Acao import *
from classes.model.Tabuleiro import Tabuleiro
from classes.model.Jogador import Jogador
from classes.strategies import Estrategia


class Simulacao:
    # Construtor
    def __init__(self, estrategias: tuple, num_personagens: int = 8, automatico: bool = True):
        # Define o número de jogadores
        self.num_jogadores = len(estrategias)
        # Define se a criação dos jogadores: 0 -> Manual ou 1 -> Automática
        self.estado = self.criar_estado_inicial(num_personagens, automatico)
        # Instância as ações do jogo
        self.acoes = self.criar_acoes()
        # Primeiro jogador a finalizar cidade (construir 7 ou mais distritos)
        self.jogador_finalizador = None
        # Estratégias de cada jogador
        self.estrategias: dict[Jogador, Estrategia] = self.criar_estrategias(estrategias)

    # Cria o estado inicial do tabuleiro
    def criar_estado_inicial(self, num_personagens, automatico) -> Estado:
        # Constrói o tabuleiro
        tabuleiro = Tabuleiro(num_personagens)
        if automatico:
            jogadores = self.criar_jogadores_automatico()
        else:
            jogadores = self.criar_jogadores_manual()
        # Distribui 4 cartas para cada jogador
        for jogador in jogadores:
            jogador.cartas_distrito_mao.extend(tabuleiro.baralho_distritos[0:4])
            del tabuleiro.baralho_distritos[0:4]
        # Sorteia o jogador inicial da primeira rodada
        shuffle(jogadores)
        # O define como rei
        jogadores[0].rei = True
        return Estado(tabuleiro, jogadores)

    # Cria os jogadores de forma automática
    def criar_jogadores_automatico(self) -> list[Jogador]:
        lista_jogadores = []
        for jogador in range(self.num_jogadores):
            lista_jogadores.append(Jogador(f'Bot'))
        return lista_jogadores

    # Cria os jogadores de forma manual
    def criar_jogadores_manual(self) -> list[Jogador]:
        lista_jogadores = []
        # Laço para nomear os jogadores
        for jogador in range(self.num_jogadores):
            # Informar o nome de cada um dos jogadores
            nome_jogador = input('Digite o nome do jogador:')
            lista_jogadores.append(Jogador(nome_jogador))
        return lista_jogadores

    # Instância as estratégais para os jogadores
    def criar_estrategias(self, estrategias: tuple[Estrategia]) -> dict[Jogador, Estrategia]:
        jogador_estrategia: dict[Jogador, Estrategia] = dict()
        for (jogador, estrategia) in zip(self.estado.jogadores, estrategias):
            jogador.nome += ' - ' + estrategia.descricao
            jogador_estrategia.update({jogador: estrategia})
        return jogador_estrategia

    # Cria lista de ações (ativas) do jogo
    @staticmethod
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
                 # Nenhuma
                 # Ações de personagem Rank 7
                 HabilidadeNavegadora(),
                 # Ações de personagem Rank 8
                 HabilidadeSenhorDaGuerraDestruir(), HabilidadeSenhordaGuerraColetar(),
                 # Ações de personagem Rank 9
                 # Nenhuma
                 # Ações de distritos especiais
                 Laboratorio(), Arsenal(), Forja(), Museu()]
        return acoes

    # Executa uma simulação do jogo e retorna estado final
    def rodar_simulacao(self) -> Estado:
        final_jogo = False
        # Laço de rodadas do jogo
        while not final_jogo:
            # Preparação para nova rodada
            self.estado.tabuleiro.cartas_nao_visiveis = []
            self.estado.tabuleiro.cartas_visiveis = []
            self.estado.tabuleiro.criar_baralho_personagem(self.num_jogadores)
            self.estado.turno = 1
            self.estado.rodada += 1
            for jogador in self.estado.jogadores:
                jogador.acoes_realizadas[TipoAcao.PassarTurno.value] = False
            self.estado.ordenar_jogadores_coroado()
            # Fase de escolha de personagens
            for jogador in self.estado.jogadores:
                # Marca jogador atual
                self.estado.jogador_atual = jogador
                # print(f'Turno atual: {jogador.nome}')
                escolha_personagem = self.estrategias[jogador].escolher_personagem(self.estado)
                jogador.personagem = self.estado.tabuleiro.baralho_personagens[escolha_personagem]
                self.estado.tabuleiro.baralho_personagens.remove(jogador.personagem)
            # Fase de ações
            # Os jogadores seguem a ordem do rank dos seus personagens como ordem de turno
            for rank in range(1, 9):
                for jogador in self.estado.jogadores:
                    if jogador.personagem.rank == rank:
                        # Marca jogador atual
                        self.estado.jogador_atual = jogador
                        # Aplica habilidades/efeitos de início de turno
                        # Aplica habilidade passiva do Rei
                        if jogador.personagem.nome == 'Rei':
                            for antigorei in self.estado.jogadores:
                                antigorei.rei = False
                            jogador.rei = True
                        # Aplica habilidade da Assassina
                        if jogador.morto:
                            jogador.morto = False
                            self.estado.turno += 1
                            continue
                        # Aplica habilidade do Ladrão
                        if jogador.roubado:
                            for ladrao in self.estado.jogadores:
                                if ladrao.personagem.nome == 'Ladrão':
                                    ladrao.ouro += jogador.ouro
                                    jogador.ouro = 0
                                    break
                        # Laço de turnos do jogo
                        while True:
                            # Mostra o estado atual
                            # print(self.estado)
                            # Mostra o jogador atual
                            # print(f'Turno atual: {jogador.nome}, {jogador.personagem}')
                            # Mostra apenas ações disponíveis segundo regras do jogo
                            acoes_disponiveis = self.acoes_disponiveis()
                            escolha_acao = self.estrategias[jogador].escolher_acao(self.estado, acoes_disponiveis)
                            # Pula uma linha
                            # print()
                            # Executa ação escolhida
                            self.acoes[acoes_disponiveis[escolha_acao].value].ativar(self.estado, self.estrategias[jogador])
                            # Finaliza turno se jogador escolheu a ação de passar o turno
                            if jogador.acoes_realizadas[TipoAcao.PassarTurno.value]:
                                break
                        # Identifica gatilhos de final de jogo
                        # Identifica se o jogador construiu o Monumento
                        monumento = False
                        for construido in jogador.distritos_construidos:
                            if construido.nome_do_distrito == 'Monumento':
                                monumento = True
                                break
                        # Marca fim de jogo e jogador finalizador (monumento conta como 2 distritos para fins de uma cidade completa)
                        if len(jogador.distritos_construidos) >= 7 or (len(jogador.distritos_construidos) == 6 and monumento):
                            jogador.terminou = True
                            if self.jogador_finalizador is None:
                                self.jogador_finalizador = jogador
                            final_jogo = True
                        # Quebra laço, pois não existem personagens com ranks repetidos
                        break
        # Rotina de final de jogo
        self.computar_pontuacao_final()
        self.estado.ordenar_jogadores_pontuacao()
        # Mostra estado final
        # print(self.estado)
        self.estado.jogadores[0].vencedor = True
        # print()
        # for jogador in self.estado.jogadores:
        #    print(f'{jogador.nome} - Pontuação final: {jogador.pontuacao_final}')
        return self.estado

    # Retorna apenas as ações disponíveis para o estado atual da simulação
    def acoes_disponiveis(self) -> list[TipoAcao]:
        acoes_disponiveis = []
        acoes_realizadas = self.estado.jogador_atual.acoes_realizadas
        # Deve ter coletado recursos primeiro para poder realizar demais ações no turno
        if acoes_realizadas[TipoAcao.ColetarOuro.value] or acoes_realizadas[TipoAcao.ColetarCartas.value]:
            acoes_disponiveis.append(TipoAcao.PassarTurno)
            # Só pode construir 1 distrito por turno (Navegadora não pode cosntruir distritos no turno)
            if not acoes_realizadas[TipoAcao.ConstruirDistrito.value] and self.estado.jogador_atual.personagem.nome != 'Navegadora':
                acoes_disponiveis.append(TipoAcao.ConstruirDistrito)
            # As habilidades dos personagens só podem ser utilizadas uma única vez
            # O jogador deve possuir a carta do personagem para usar a sua habilidade
            if not acoes_realizadas[TipoAcao.HabilidadeAssassina.value] and self.estado.jogador_atual.personagem.nome == 'Assassina':
                acoes_disponiveis.append(TipoAcao.HabilidadeAssassina)
            if not acoes_realizadas[TipoAcao.HabilidadeLadrao.value] and self.estado.jogador_atual.personagem.nome == 'Ladrão':
                acoes_disponiveis.append(TipoAcao.HabilidadeLadrao)
            if not acoes_realizadas[TipoAcao.HabilidadeMago.value] and self.estado.jogador_atual.personagem.nome == 'Mago':
                acoes_disponiveis.append(TipoAcao.HabilidadeMago)
            if not acoes_realizadas[TipoAcao.HabilidadeRei.value] and self.estado.jogador_atual.personagem.nome == 'Rei':
                acoes_disponiveis.append(TipoAcao.HabilidadeRei)
            if not acoes_realizadas[TipoAcao.HabilidadeCardeal.value] and self.estado.jogador_atual.personagem.nome == 'Cardeal':
                acoes_disponiveis.append(TipoAcao.HabilidadeCardeal)
            if not acoes_realizadas[TipoAcao.HabilidadeNavegadora.value] and self.estado.jogador_atual.personagem.nome == 'Navegadora':
                acoes_disponiveis.append(TipoAcao.HabilidadeNavegadora)
            if self.estado.jogador_atual.personagem.nome == 'Senhor da Guerra':
                if not acoes_realizadas[TipoAcao.HabilidadeSenhorDaGuerraDestruir.value]:
                    acoes_disponiveis.append(TipoAcao.HabilidadeSenhorDaGuerraDestruir)
                if not acoes_realizadas[TipoAcao.HabilidadeSenhorDaGuerraColetar.value]:
                    acoes_disponiveis.append(TipoAcao.HabilidadeSenhorDaGuerraColetar)
            # As habilidades dos distritos especiais só podem ser utilizadas uma única vez
            # O jogador deve ter o distrito construído na sua cidade para usar a sua habilidade
            if not acoes_realizadas[TipoAcao.Laboratorio.value] and self.estado.jogador_atual.construiu_distrito('Laboratório'):
                # Deve possuir ao menos 1 carta na mão
                if len(self.estado.jogador_atual.cartas_distrito_mao) > 0:
                    acoes_disponiveis.append(TipoAcao.Laboratorio)
            if not acoes_realizadas[TipoAcao.Arsenal.value] and self.estado.jogador_atual.construiu_distrito('Arsenal'):
                acoes_disponiveis.append(TipoAcao.Arsenal)
            if not acoes_realizadas[TipoAcao.Forja.value] and self.estado.jogador_atual.construiu_distrito('Forja'):
                # Deve possuir ao menos 2 ouros
                if self.estado.jogador_atual.ouro >= 2:
                    acoes_disponiveis.append(TipoAcao.Forja)
            if not acoes_realizadas[TipoAcao.Museu.value] and self.estado.jogador_atual.construiu_distrito('Museu'):
                # Deve possuir ao menos 1 carta na mão
                if len(self.estado.jogador_atual.cartas_distrito_mao) > 0:
                    acoes_disponiveis.append(TipoAcao.Museu)
        # Só pode coletar recursos uma vez ao turno (coletar ouro ou carta)
        else:
            acoes_disponiveis.append(TipoAcao.ColetarOuro)
            acoes_disponiveis.append(TipoAcao.ColetarCartas)
        return acoes_disponiveis

    # Mostra menu com ações
    @staticmethod
    def imprimir_menu_acoes(acoes: list[Acao]) -> str:
        i = iter(acoes)
        texto = 'Escolha uma ação das seguintes: \n\t' + str(next(i))
        for distrito in i:
            texto += ', ' + str(distrito)
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
            jogador.pontuacao_final += 3
            for qtd_tipo in contador_tipos:
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
                    jogador.pontuacao_final += contador_tipos[4]
                # Tesouro Imperial (Ao final da partida, marque 1 ponto extra para cada ouro em seu tesouro)
                if distrito_construido.nome_do_distrito == 'Tesouro Imperial':
                    jogador.pontuacao_final += jogador.ouro
                # Sala de Mapas (Ao final da partida, marque 1 ponto extra para cada carta da sua mão)
                if distrito_construido.nome_do_distrito == 'Sala de Mapas':
                    jogador.pontuacao_final += len(jogador.cartas_distrito_mao)
                # Portão do Dragão (Ao final da partida, marque 2 pontos extras)
                if distrito_construido.nome_do_distrito == 'Portão do Dragão':
                    jogador.pontuacao_final += 2
                # Capitólio (Se tiver pelo menos 3 distritos do mesmo tipo no final da partida, marque 3 pontos extras)
                pontuou_capitolio = False
                if distrito_construido.nome_do_distrito == 'Capitólio':
                    for qtd_tipo in contador_tipos:
                        if qtd_tipo >= 3:
                            jogador.pontuacao_final += 3
                            pontuou_capitolio = True
                            break
                # Torre de Marfim (Se a Torre de Marfim for o único distrito ESPECIAL na sua cidade ao final da partida, marque 5 pontos extras)
                if distrito_construido.nome_do_distrito == 'Torre de Marfim':
                    if contador_tipos[4] == 1:
                        jogador.pontuacao_final += 5
                # Bairro Assombrado (Ao final da partida, o Bairro Assombrado vale como 1 tipo de distrito à sua escolha)
                if distrito_construido.nome_do_distrito == 'Bairro Assombrado':
                    melhor_pontuacao = 0
                    # Identifica se falta somente 1 tipo de distrito e tem mais de um distrito especial
                    if contador_tipos[4] > 1 and \
                            ((contador_tipos[0] == 0 and contador_tipos[1] * contador_tipos[2] * contador_tipos[3] != 0) or
                             (contador_tipos[1] == 0 and contador_tipos[0] * contador_tipos[2] * contador_tipos[3] != 0) or
                             (contador_tipos[2] == 0 and contador_tipos[1] * contador_tipos[0] * contador_tipos[3] != 0) or
                             (contador_tipos[3] == 0 and contador_tipos[1] * contador_tipos[2] * contador_tipos[0] != 0)):
                        ponto_potencial = 3
                        # perde 1 ponto caso também tenha poço dos desejos
                        if jogador.construiu_distrito('Poço dos Desejos'):
                            ponto_potencial -= 1
                        # perde 3 pontos caso pontuou capitólio com exatamente 3 distritos especiais
                        if jogador.construiu_distrito('Capitólio') and \
                                contador_tipos[4] == 3 and contador_tipos[0] < 3 and contador_tipos[1] < 3 and contador_tipos[2] < 3 and contador_tipos[3] < 3:
                            ponto_potencial -= 3
                        # ganha 5 pontos caso tenha torre de marfim como único distrito especial
                        if jogador.construiu_distrito('Torre de Marfim') and contador_tipos[4] == 2:
                            ponto_potencial += 5
                        if ponto_potencial > 0:
                            melhor_pontuacao = ponto_potencial
                    # Transformar bairro assombrado para pontuar capitólio
                    if jogador.construiu_distrito('Capitólio') and not pontuou_capitolio and \
                            (contador_tipos[0] == 2 or contador_tipos[1] == 2 or contador_tipos[2] == 2 or contador_tipos[3] == 2):
                        ponto_potencial = 3
                        # perde 1 ponto caso também tenha poço dos desejos
                        if jogador.construiu_distrito('Poço dos Desejos'):
                            ponto_potencial -= 1
                        # ganha 5 pontos caso tenha torre de marfim como único distrito especial
                        if jogador.construiu_distrito('Torre de Marfim') and contador_tipos[4] == 2:
                            ponto_potencial += 5
                        if melhor_pontuacao < ponto_potencial:
                            melhor_pontuacao = ponto_potencial
                    # Transformar bairro assombrado para pontuar torre de marfim
                    if jogador.construiu_distrito('Torre de Marfim') and contador_tipos[4] == 2:
                        if melhor_pontuacao < 5:
                            melhor_pontuacao = 5
                    jogador.pontuacao_final += melhor_pontuacao
