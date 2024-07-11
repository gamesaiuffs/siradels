from random import shuffle

from classes.enum.TipoAcaoOpenAI import TipoAcaoOpenAI
from classes.model.Acao import *
from classes.model.Tabuleiro import Tabuleiro
from classes.model.Jogador import Jogador
from classes.strategies import Estrategia


class Simulacao:
    # Construtor
    def __init__(self, estrategias: list[Estrategia], num_personagens: int = 8, automatico: bool = True, treino_openaigym: bool = False):
        # Define o número de jogadores
        self.num_jogadores: int = len(estrategias)
        # Define número de cartas de personagens utilizado (pode ser 8 ou 9)
        self.num_personagens = num_personagens
        # Define se deve imprimir estado do jogo a cada turno (automatico = False)
        self.automatico: bool = automatico
        # Inicializa o jogo num estado inicial válido
        self.estado: Estado = self.criar_estado_inicial(num_personagens)
        # Instância as ações do jogo
        self.acoes: list[Acao] = self.criar_acoes()
        # Primeiro jogador a finalizar cidade (construir 7 ou mais distritos)
        self.jogador_finalizador: Jogador | None = None
        # Flag para final de jogo (estado final)
        self.final_jogo = False
        # Estratégias de cada jogador
        self.estrategias: dict[Jogador, Estrategia] = self.criar_estrategias(estrategias)
        # Flag para indicar treino da OpenAI Gym
        self.treino_openaigym = treino_openaigym
        # Flag para indicar início de nova rodada
        self.nova_rodada = True

    # Cria o estado inicial do tabuleiro
    def criar_estado_inicial(self, num_personagens: int) -> Estado:
        # Constrói o tabuleiro
        tabuleiro = Tabuleiro(num_personagens)
        jogadores = self.criar_jogadores()
        # Distribui 4 cartas para cada jogador
        for jogador in jogadores:
            jogador.cartas_distrito_mao.extend(tabuleiro.baralho_distritos[0:4])
            del tabuleiro.baralho_distritos[0:4]
        # Sorteia o jogador inicial da primeira rodada
        shuffle(jogadores)
        # O define como rei
        jogadores[0].rei = True
        # Limpa flags de jogador finalizador e de final de jogo
        self.jogador_finalizador = None
        self.final_jogo = False
        return Estado(tabuleiro, jogadores)

    # Cria os jogadores de forma automática
    def criar_jogadores(self) -> list[Jogador]:
        lista_jogadores = []
        for jogador in range(self.num_jogadores):
            lista_jogadores.append(Jogador())
        return lista_jogadores

    # Instância as estratégais para os jogadores
    def criar_estrategias(self, estrategias: list[Estrategia]) -> dict[Jogador, Estrategia]:
        jogador_estrategia: dict[Jogador, Estrategia] = dict()
        shuffle(estrategias)
        for (jogador, estrategia) in zip(self.estado.jogadores, estrategias):
            jogador.nome = estrategia.descricao
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
                 HabilidadeIlusionistaTrocar(), HabilidadeIlusionistaDescartar(),
                 # Ações de personagem Rank 4
                 HabilidadeRei(),
                 # Ações de personagem Rank 5
                 HabilidadeBispo(),
                 # Ações de personagem Rank 6
                 HabilidadeComerciante(),
                 # Ações de personagem Rank 7
                 # Habilidade passiva
                 # Ações de personagem Rank 8
                 HabilidadeSenhorDaGuerraDestruir(), HabilidadeSenhordaGuerraColetar(),
                 # Ações de personagem Rank 9
                 # Nenhuma
                 # Ações de distritos especiais
                 Laboratorio(), Forja()]
        return acoes

    # Executa uma simulação do jogo e retorna estado final
    def rodar_simulacao(self) -> Estado:
        # Laço de rodadas do jogo
        while not self.final_jogo:
            self.iniciar_rodada()
            self.executar_rodada()
        # Rotina de final de jogo
        self.computar_pontuacao_final()
        self.estado.ordenar_jogadores_pontuacao()
        self.estado.jogadores[0].vencedor = True
        # Mostra estado final
        if not self.automatico:
            print('-----ESTADO FINAL-----')
            print(self.estado)
            for jogador in self.estado.jogadores:
                print(f'{jogador.nome} - Pontuação final: {jogador.pontuacao_final}')
        return self.estado

    def iniciar_rodada(self) -> None:
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
        self.nova_rodada = False
        self.estado.escolher_personagem = True

    def executar_rodada(self, idx_escolha_personagem: int | None = None):
        rank_final = -1
        for jogador in self.estado.jogadores:
            # Marca jogador atual
            self.estado.jogador_atual = jogador
            # print(f'Turno atual: {jogador.nome}')
            if self.treino_openaigym and jogador.nome == 'Agente':
                escolha_personagem = idx_escolha_personagem
                rank_final = self.estado.tabuleiro.baralho_personagens[escolha_personagem].rank + 1
            else:
                escolha_personagem = self.estrategias[jogador].escolher_personagem(self.estado)
            jogador.personagem = self.estado.tabuleiro.baralho_personagens[escolha_personagem]
            self.estado.tabuleiro.baralho_personagens.remove(jogador.personagem)
        # Fase de ações
        self.estado.escolher_personagem = False
        self.estado.inicio_turno_acoes = True
        if rank_final == -1:
            rank_final = self.num_personagens + 1
        self.executar_turno_jogador(1, rank_final)

    def executar_turno_jogador(self, rank_inicial: int, rank_final: int):
        # Os jogadores seguem a ordem do rank dos seus personagens como ordem de turno
        for rank in range(rank_inicial, rank_final):
            for jogador in self.estado.jogadores:
                if jogador.personagem.rank == rank:
                    # Marca jogador atual
                    self.estado.jogador_atual = jogador
                    # Verificações de início de turno
                    if self.estado.inicio_turno_acoes:
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
                            jogador.roubado = False
                            for ladrao in self.estado.jogadores:
                                if ladrao.personagem.nome == 'Ladrão':
                                    ladrao.ouro += jogador.ouro
                                    jogador.ouro = 0
                                    break
                        # Aplica habilidade passiva do Comerciante
                        if jogador.personagem.nome == 'Comerciante':
                            jogador.ouro += 1
                        # Aplica habilidade passiva da Arquiteta
                        if jogador.personagem.nome == 'Arquiteta' and len(self.estado.tabuleiro.baralho_distritos) > 0:
                            qtd_cartas = 2
                            # Cartas insuficientes no baralho para pescar
                            if len(self.estado.tabuleiro.baralho_distritos) < qtd_cartas:
                                qtd_cartas = len(self.estado.tabuleiro.baralho_distritos)
                            # Pescar cartas do baralho
                            cartas_compradas = self.estado.tabuleiro.baralho_distritos[:qtd_cartas]
                            del self.estado.tabuleiro.baralho_distritos[:qtd_cartas]
                            self.estado.jogador_atual.cartas_distrito_mao.extend(cartas_compradas)
                    # Laço de ações no turno do jogo
                    while True:
                        # Mostra estado e jogador atual caso a simulação esteja no modo manual
                        if not self.automatico and self.estrategias[jogador].imprimir:
                            print('/--------------------------/', end='')
                            print(self.estado)
                            print(f'Turno atual: {jogador.nome}, {jogador.personagem}')
                        # Mostra apenas ações disponíveis segundo regras do jogo
                        acoes_disponiveis = self.acoes_disponiveis()
                        escolha_acao = self.estrategias[jogador].escolher_acao(self.estado, acoes_disponiveis)
                        if not self.automatico and self.estrategias[jogador].imprimir:
                            print(f'Ação escolhida: {self.acoes[acoes_disponiveis[escolha_acao].value]}')
                            print('/--------------------------/')
                        # Interrompe turno para que o modelo execute a ação segundo política aprendida pelo Agente sendo treinado
                        if self.treino_openaigym:
                            if self.estado.coletar_recursos:
                                return
                            elif self.estado.construir_distrito:
                                return
                        # Executa ação escolhida
                        self.acoes[acoes_disponiveis[escolha_acao].value].ativar(self.estado, self.estrategias[jogador])
                        # Finaliza turno se jogador escolheu a ação de passar o turno
                        if jogador.acoes_realizadas[TipoAcao.PassarTurno.value]:
                            break
                    # Identifica gatilhos de final de jogo
                    # Marca fim de jogo e jogador finalizador (monumento conta como 2 distritos para fins de uma cidade completa)
                    if len(jogador.distritos_construidos) >= 7:
                        jogador.terminou = True
                        if self.jogador_finalizador is None:
                            self.jogador_finalizador = jogador
                        self.final_jogo = True
                    # Quebra laço, pois não existem personagens com ranks repetidos
                    break
        if rank_final == self.num_personagens + 1:
            self.nova_rodada = True

    def executar_coletar_recursos(self, action: TipoAcaoOpenAI, jogador: Jogador):
        acao_escolhida = TipoAcao.ColetarOuro if action == TipoAcaoOpenAI.ColetarOuro else TipoAcao.ColetarCartas
        # Executa ação escolhida
        self.acoes[acao_escolhida.value].ativar(self.estado, self.estrategias[jogador])
        # Continua turno
        self.estado.inicio_turno_acoes = False
        self.executar_turno_jogador(jogador.personagem.rank, jogador.personagem.rank + 1)

    def executar_construir_distrito(self, idx_distrito_escolhido: int, jogador: Jogador):
        # Se nenhum distrito pode ser construído executa ação igual para marcá-la como indisponível
        if idx_distrito_escolhido == -1:
            self.acoes[TipoAcao.ConstruirDistrito.value].ativar(self.estado, self.estrategias[jogador])
        else:
            # Executa ação para cosntruir distrito escolhido
            self.acoes[TipoAcao.ConstruirDistrito.value].ativar(self.estado, idx_distrito_escolhido)
        # Finaliza turno do agente
        self.executar_turno_jogador(jogador.personagem.rank, jogador.personagem.rank + 1)
        # Finaliza turno dos demais jogadores da rodada
        self.estado.inicio_turno_acoes = True
        self.executar_turno_jogador(jogador.personagem.rank + 1, self.num_personagens + 1)

    # Retorna apenas as ações disponíveis para o estado atual da simulação
    def acoes_disponiveis(self) -> list[TipoAcao]:
        acoes_disponiveis = []
        acoes_realizadas = self.estado.jogador_atual.acoes_realizadas
        # Deve ter coletado recursos primeiro para poder realizar demais ações no turno
        self.estado.coletar_recursos = not (acoes_realizadas[TipoAcao.ColetarOuro.value] or acoes_realizadas[TipoAcao.ColetarCartas.value])
        if not self.estado.coletar_recursos:
            acoes_disponiveis.append(TipoAcao.PassarTurno)
            # Ação de construir distrito
            self.estado.construir_distrito = not acoes_realizadas[TipoAcao.ConstruirDistrito.value]
            if self.estado.construir_distrito:
                acoes_disponiveis.append(TipoAcao.ConstruirDistrito)
            # As habilidades dos personagens só podem ser utilizadas uma única vez
            # O jogador deve possuir a carta do personagem para usar a sua habilidade
            if not acoes_realizadas[TipoAcao.HabilidadeAssassina.value] and self.estado.jogador_atual.personagem.nome == 'Assassina':
                acoes_disponiveis.append(TipoAcao.HabilidadeAssassina)
            if not acoes_realizadas[TipoAcao.HabilidadeLadrao.value] and self.estado.jogador_atual.personagem.nome == 'Ladrão':
                acoes_disponiveis.append(TipoAcao.HabilidadeLadrao)
            if self.estado.jogador_atual.personagem.nome == 'Ilusionista':
                if not acoes_realizadas[TipoAcao.HabilidadeIlusionistaTrocar.value] and not acoes_realizadas[TipoAcao.HabilidadeIlusionistaDescartar.value]:
                    acoes_disponiveis.append(TipoAcao.HabilidadeIlusionistaTrocar)
                    acoes_disponiveis.append(TipoAcao.HabilidadeIlusionistaDescartar)
            if not acoes_realizadas[TipoAcao.HabilidadeRei.value] and self.estado.jogador_atual.personagem.nome == 'Rei':
                acoes_disponiveis.append(TipoAcao.HabilidadeRei)
            if not acoes_realizadas[TipoAcao.HabilidadeBispo.value] and self.estado.jogador_atual.personagem.nome == 'Bispo':
                acoes_disponiveis.append(TipoAcao.HabilidadeBispo)
            if not acoes_realizadas[TipoAcao.HabilidadeComerciante.value] and self.estado.jogador_atual.personagem.nome == 'Comerciante':
                acoes_disponiveis.append(TipoAcao.HabilidadeComerciante)
            if self.estado.jogador_atual.personagem.nome == 'Senhor da Guerra':
                if not acoes_realizadas[TipoAcao.HabilidadeSenhorDaGuerraDestruir.value]:
                    acoes_disponiveis.append(TipoAcao.HabilidadeSenhorDaGuerraDestruir)
                if not acoes_realizadas[TipoAcao.HabilidadeSenhorDaGuerraColetar.value]:
                    acoes_disponiveis.append(TipoAcao.HabilidadeSenhorDaGuerraColetar)
            # As habilidades dos distritos especiais só podem ser utilizadas uma única vez
            # O jogador deve ter o distrito construído na sua cidade para usar a sua habilidade
            if not acoes_realizadas[TipoAcao.Laboratorio.value] and self.estado.jogador_atual.construiu_distrito('Laboratório'):
                acoes_disponiveis.append(TipoAcao.Laboratorio)
            if not acoes_realizadas[TipoAcao.Forja.value] and self.estado.jogador_atual.construiu_distrito('Forja'):
                acoes_disponiveis.append(TipoAcao.Forja)
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

    # Computa a pontuação final de cada jogador para definir vencedor
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
            for distrito_construido in jogador.distritos_construidos:
                # Estátua (Se você tiver a coroa no final da partida, marque 5 pontos extras)
                if distrito_construido.nome_do_distrito == 'Estátua' and jogador.rei:
                    jogador.pontuacao_final += 5
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
                # Bairro Assombrado (Ao final da partida, o Bairro Assombrado vale como 1 tipo de distrito à sua escolha)
                if distrito_construido.nome_do_distrito == 'Bairro Assombrado':
                    ponto_potencial = 0
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
                    jogador.pontuacao_final += ponto_potencial
