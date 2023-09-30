import numpy as np
from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoTabela import TipoTabela
from classes.enum.TipoModeloAcao import TipoModeloAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random


class EstrategiaMCTS(Estrategia):
    def __init__(self, modelos_mcts: list[list[np.array]], modelos_historico: list[list[np.array]], modo: TipoTabela, treino: bool = True):
        super().__init__('MCTS')
        self.modelos_mcts = modelos_mcts
        self.modelos_historico = modelos_historico
        self.modo = modo
        self.treino = treino

    # Estratégia usada na fase de escolha dos personagens
    def escolher_personagem(self, estado: Estado) -> int:
        if self.treino:
            # Tabela a ser treinada a partir do TipoTabelaPersonaem
            indice_linha_tabela = estado.converter_estado()[self.modo.idx]
            linha_tabela = self.modelos_mcts[TipoModeloAcao.EscolherPersonagem.idx][self.modo.idx][indice_linha_tabela]
            # Deixar apenas colunas das ações disponíveis no estado atual
            personagens_disponiveis = []
            for personagem in estado.tabuleiro.baralho_personagens:
                personagens_disponiveis.append(linha_tabela[personagem.rank - 1])
            for personagem in estado.tabuleiro.baralho_personagens:
                personagens_disponiveis.append(linha_tabela[personagem.rank - 1 + 8])
            # Computar divisão proporcional
            divisao_proporcional = self.computar_divisao_proporcional(np.array(personagens_disponiveis))
            # Escolher opção seguindo distribuição da divisão
            escolha = random.choices(range(0, len(estado.tabuleiro.baralho_personagens)), divisao_proporcional)[0]
            # Salvar histórico das escolhas para acrescentar no modelo após resultado
            self.modelos_historico[TipoModeloAcao.EscolherPersonagem.idx][self.modo.idx][indice_linha_tabela][estado.tabuleiro.baralho_personagens[escolha].rank-1] = 1
            # Define se vamos contabilizar a quantidade de partida (= 1) ou se contaremos quantas vezes a ação foi escolhida na mesma partida (+= 1)
            self.modelos_historico[TipoModeloAcao.EscolherPersonagem.idx][self.modo.idx][indice_linha_tabela][estado.tabuleiro.baralho_personagens[escolha].rank-1+8] = 1
            return escolha
        else:
            # Converte estado e monta de consulta a partir de todas as tabelas individuais
            estado_vetor = estado.converter_estado()
            tabela_consulta = np.zeros((len(TipoTabela), 16))
            for i in range(len(TipoTabela)):
                tabela_consulta[i] = self.modelos_mcts[TipoModeloAcao.EscolherPersonagem.idx][i][estado_vetor[i]]
            # Deixar apenas colunas das ações disponíveis no estado atual
            personagens_disponiveis = []
            for personagem in estado.tabuleiro.baralho_personagens:
                personagens_disponiveis.append(tabela_consulta[:, personagem.rank - 1])
            personagens_disponiveis = np.stack(personagens_disponiveis, axis=1)
            soma_colunas = np.sum(personagens_disponiveis, axis=0)
            # Computar divisão proporcional com soma das colunas (considera apenas vitórias)
            divisao_proporcional = self.computar_divisao_proporcional(soma_colunas, 1, True)
            # Escolher opção seguindo distribuição da divisão
            escolha = random.choices(range(0, len(estado.tabuleiro.baralho_personagens)), divisao_proporcional)[0]
            return escolha

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        if len(acoes_disponiveis) > 1:
            return random.randint(1, len(acoes_disponiveis) - 1)
        return 0

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        return random.randint(0, qtd_cartas - 1)

    # Estratégia usada na ação de construir distritos
    @staticmethod
    def construir_distrito(estado: Estado,
                           distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)]) -> int:
        tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_covil_ladroes)
        return random.randint(1, tamanho_maximo)

    # Estratégia usada na ação de construir distritos (efeito Covil dos Ladrões)
    @staticmethod
    def construir_distrito_covil_dos_ladroes(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade da Assassina
    @staticmethod
    def habilidade_assassina(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade da Ilusionista (escolha do jogador alvo)
    @staticmethod
    def habilidade_ilusionista_trocar(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        return random.randint(0, len(opcoes_jogadores) - 1)

    # Estratégia usada na habilidade da Ilusionista (escolha de quantas cartas serão descartadas)
    @staticmethod
    def habilidade_ilusionista_descartar_qtd_cartas(estado: Estado, qtd_maxima: int) -> int:
        return random.randint(1, qtd_maxima)

    # Estratégia usada na habilidade da Ilusionista (escolha de qual carta descartar)
    @staticmethod
    def habilidade_ilusionista_descartar_carta(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    def habilidade_senhor_da_guerra_destruir(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        return random.randint(0, len(distritos_para_destruir))

    # Estratégia usada na ação do Laboratório
    @staticmethod
    def laboratorio(estado: Estado) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Computa divisão proporcional entre vitórias (diretamente) e quantidade de simulações (inversamente)
    @staticmethod
    def computar_divisao_proporcional(linha_tabela: np.ndarray, peso_explotacao: float = 1, apenas_vitorias: bool = False) -> list[float]:
        if apenas_vitorias:
            qtd_acoes = len(linha_tabela)
            divisao = np.zeros(qtd_acoes)
            total = 0
            for i in range(qtd_acoes):
                divisao[i] = linha_tabela[i] ** peso_explotacao
                total += divisao[i]
        else:
            qtd_acoes = int(len(linha_tabela)/2)
            divisao = np.zeros(qtd_acoes)
            total = 0
            for i in range(qtd_acoes):
                divisao[i] = linha_tabela[i] ** peso_explotacao / linha_tabela[i+qtd_acoes]
                total += divisao[i]
        return divisao/total

