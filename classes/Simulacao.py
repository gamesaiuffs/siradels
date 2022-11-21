# Imports
from random import shuffle
from Acao import *
from TipoAcao import TipoAcao


class Simulacao:
    # Construtor
    def __init__(self, num_jogadores: int, automatico: bool):
        # Define o número de jogadores
        self.num_jogadores = num_jogadores
        # Define se a criação dos jogadores será manual ou automática: 0 -> Manual || 1 -> Automática
        self.estado = self.criar_estado_inicial(automatico)
        self.acoes = self.criar_acoes()

    # Cria o estado inicial do tabuleiro
    def criar_estado_inicial(self, automatico) -> Estado:
        # Constrói o tabuleiro
        tabuleiro = Tabuleiro(self.num_jogadores)
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
            lista_jogadores.append(Jogador(f"Bot {jogador+1}"))
        
        return lista_jogadores

    # Cria os jogadores de forma manual
    def criar_jogadores_manual(self) -> list[Jogador]:
        lista_jogadores = []
        # Loop para nomear os jogadores
        for jogador in range(self.num_jogadores):
            # O usuário deve digitar o nome de cada um dos jogadores
            nome_jogador = input("Digite o nome do jogador:")
            lista_jogadores.append(Jogador(nome_jogador))

        return lista_jogadores

    @staticmethod
    def criar_acoes() -> list[Acao]:
        acoes = [ColetarOuro(),
                ColetarCartas(),
                ConstruirDistrito(),
                EfeitoAssassino(),
                EfeitoLadrao(),
                EfeitoMago(),
                EfeitoRei(),
                EfeitoCardealAtivo(),
                EfeitoCardealPassivo(),
                EfeitoAlquimista(),
                EfeitoNavegadora(), 
                EfeitoSenhordaGuerra(),
                AbrigoParaPobres(),
                TesouroImperial(),
                CofreSecreto(),
                Laboratorio(),
                PortalDoDragao(),
                Necropole(),
                Teatro(),
                MinaDeOuro(),
                EscolaDeMagia(),
                Estrutura(),
                Estabulo(),
                CovilDosLadroes(),
                PassarTurno()]
        return acoes

    def acoes_disponiveis(self) -> list[Acao]:
        acoes_disponiveis = []

        #adicionar flag nas ações

        if self.estado.jogador_atual().morto:
            return acoes_disponiveis.append(self.acoes[24])

        for acao in TipoAcao:
            match acao:
                case TipoAcao.ColetarOuro:
                    if self.estado.jogador_atual().coletou_recursos == False:
                        acoes_disponiveis.append(self.acoes[acao.value])
                case TipoAcao.ColetarCartas:
                    if self.estado.jogador_atual().coletou_recursos == False:
                        acoes_disponiveis.append(self.acoes[acao.value])
                case TipoAcao.PassarTurno:
                    if self.estado.jogador_atual().coletou_recursos == True:
                        acoes_disponiveis.append(self.acoes[acao.value])
                case TipoAcao.ConstruirDistrito:
                    if self.estado.jogador_atual().coletou_recursos == True and self.estado.jogador_atual().acoes_realizadas[TipoAcao.ConstruirDistrito] == 2:
                        if self.estado.jogador_atual().personagem.nome != "Navegadora":
                            acoes_disponiveis.append(self.acoes[acao.value])
                case TipoAcao.EfeitoAssassino:
                    if self.estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoAssassino] == 3 and self.estado.jogador_atual().personagem.nome == "Assassino":
                        acoes_disponiveis.append(self.acoes[acao.value])
                case TipoAcao.EfeitoLadrao:
                    if self.estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoLadrao] == 3 and self.estado.jogador_atual().personagem.nome == "Ladrao":
                        acoes_disponiveis.append(self.acoes[acao.value])
                case TipoAcao.EfeitoMago:
                    if self.estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoMago] == 3 and self.estado.jogador_atual().personagem.nome == "Mago":
                        acoes_disponiveis.append(self.acoes[acao.value])
                case TipoAcao.EfeitoRei:
                    if self.estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoRei] == 3 and self.estado.jogador_atual().personagem.nome == "Rei":
                        acoes_disponiveis.append(self.acoes[acao.value])
                case TipoAcao.EfeitoCardealAtivo:
                    if self.estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoCardealAtivo] == 3 and self.estado.jogador_atual().personagem.nome == "Cardeal":
                        acoes_disponiveis.append(self.acoes[acao.value])
                case TipoAcao.EfeitoCardealPassivo:
                    if self.estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoCardealPassivo] == 3 and self.estado.jogador_atual().personagem.nome == "Cardeal":
                        acoes_disponiveis.append(self.acoes[acao.value])
                case TipoAcao.EfeitoAlquimista:
                    if self.estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoAlquimista] == 3 and self.estado.jogador_atual().personagem.nome == "Alquimista":
                        acoes_disponiveis.append(self.acoes[acao.value])
                        # Disponivel apenas no final do turno
                case TipoAcao.EfeitoNavegadora:
                    if self.estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoNavegadora] == 3 and self.estado.jogador_atual().personagem.nome == "Navegadora":
                        acoes_disponiveis.append(self.acoes[acao.value])
                case TipoAcao.EfeitoSenhordaGuerra:
                    if self.estado.jogador_atual().acoes_realizadas[TipoAcao.EfeitoSenhordaGuerra] == 3 and self.estado.jogador_atual().personagem.nome == "SenhordaGuerra":
                        acoes_disponiveis.append(self.acoes[acao.value])
                    '''
    AbrigoParaPobres = 12
    TesouroImperial = 13
    CofreSecreto = 14
    Laboratorio = 15
    PortalDoDragao = 16
    Necropole = 17
    Teatro = 18
    MinaDeOuro = 19
    EscolaDeMagia = 20
    Estrutura = 21
    Estabulo = 22
    CovilDosLadroes = 23
    PassarTurno = 24
                '''
        return acoes_disponiveis

    def imprimir_menu_acoes(self, acoes: list[Acao]) -> str:
        i = iter(acoes)
        texto = "Escolha uma ação das seguintes:"
        texto = "\n\t" + str(next(i))
        for distrito in i:
            texto += ", " + str(distrito)
        return texto
