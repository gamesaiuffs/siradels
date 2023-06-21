import numpy as np
from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoTabelaPersonagem import TipoTabelaPersonagem
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random


class EstrategiaMCTS(Estrategia):
    def __init__(self, modelo: list[np.array], historico: list[np.array], modo: TipoTabelaPersonagem):
        super().__init__('MCTS')
        self.modelo = modelo
        self.historico = historico
        self.modo = modo

    # Estratégia usada na fase de escolha dos personagens
    def escolher_personagem(self, estado: Estado) -> int:
        # Tabela a ser treinada a partir do TipoTabelaPersonaem
        indice_linha_tabela = estado.converter_estado()[self.modo.value]
        linha_tabela = self.modelo[self.modo.value][indice_linha_tabela]
        # Deixar apenas colunas das ações disponíveis no estado atual
        personagens_disponiveis = []
        for personagem in estado.tabuleiro.baralho_personagens:
            personagens_disponiveis.append(linha_tabela[personagem.rank - 1])
        for personagem in estado.tabuleiro.baralho_personagens:
            personagens_disponiveis.append(linha_tabela[personagem.rank - 1 + 8])
        # Computar divisão proporcional
        divisao_proporcional = self.computar_divisao_proporcional(personagens_disponiveis)
        # Escolher opção seguindo distribuição da divisão
        escolha = random.choices(range(0, len(estado.tabuleiro.baralho_personagens)), divisao_proporcional)[0]
        # Salvar histórico das escolhas para acrescentar no modelo após resultado
        self.historico[self.modo.value][indice_linha_tabela][estado.tabuleiro.baralho_personagens[escolha].rank-1] = 1
        self.historico[self.modo.value][indice_linha_tabela][estado.tabuleiro.baralho_personagens[escolha].rank-1+8] = 1
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
                           distritos_para_construir_cardeal: list[(CartaDistrito, Jogador)],
                           distritos_para_construir_necropole: list[(CartaDistrito, CartaDistrito)],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)],
                           distritos_para_construir_estrutura: list[CartaDistrito]) -> int:
        tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_cardeal) + \
                         len(distritos_para_construir_necropole) + len(distritos_para_construir_covil_ladroes) + len(distritos_para_construir_estrutura)
        return random.randint(1, tamanho_maximo)

    # Estratégia usada na ação de construir distritos (efeito Cardeal)
    @staticmethod
    def construir_distrito_cardeal(estado: Estado, diferenca: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

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

    # Estratégia usada na habilidade do Mago (escolha do jogador alvo)
    @staticmethod
    def habilidade_mago_jogador(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        return random.randint(0, len(opcoes_jogadores) - 1)

    # Estratégia usada na habilidade do Mago (escolha da carta da mão)
    @staticmethod
    def habilidade_mago_carta(estado: Estado, opcoes_cartas: list[CartaDistrito]) -> int:
        return random.randint(0, len(opcoes_cartas) - 1)

    # Estratégia usada na habilidade da Navegadora
    @staticmethod
    def habilidade_navegadora(estado: Estado) -> int:
        return random.randint(0, 1)

    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    def habilidade_senhor_da_guerra(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador, int)]) -> int:
        return random.randint(0, len(distritos_para_destruir))

    # Estratégia usada na ação do Laboratório
    @staticmethod
    def laboratorio(estado: Estado) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na ação do Arsenal
    @staticmethod
    def arsenal(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        return random.randint(0, len(distritos_para_destruir))

    # Estratégia usada na ação do Museu
    @staticmethod
    def museu(estado: Estado) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Computa divisão proporcional entre vitórias (diretamente) e quantidade de simulações (inversamente)
    @staticmethod
    def computar_divisao_proporcional(linha_tabela: list[int], peso_explotacao: float = 1) -> list[float]:
        qtd_acoes = int(len(linha_tabela)/2)
        divisao = np.zeros(qtd_acoes)
        total = 0
        for i in range(qtd_acoes):
            divisao[i] = linha_tabela[i] ** peso_explotacao / linha_tabela[i+qtd_acoes]
            total += divisao[i]
        return divisao/total

