from stable_baselines3 import DQN

from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoAcaoOpenAI import TipoAcaoOpenAI
from classes.enum.TipoDistrito import TipoDistrito
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random
import numpy as np


class Agente(Estrategia):
    def __init__(self, nome: str = 'Agente', imprimir: bool = False):
        super().__init__(nome, imprimir)
        self.model = DQN.load("citadels_agent")

    # Estratégia usada na fase de escolha dos personagens
    def escolher_personagem(self, estado: Estado) -> int:
        while True:
            action, _ = self.model.predict(np.array(estado.converter_estado(openaigym=True)), deterministic=False)
            # Verifica se o personagem escolhido está disponível e identifica o seu índice
            idx_escolha_personagem = -1
            for idx, personagem in enumerate(estado.tabuleiro.baralho_personagens):
                if action == personagem.rank - 1:
                    idx_escolha_personagem = idx
            # Caso não esteja, retorna estado atual
            if idx_escolha_personagem == -1:
                break
        return idx_escolha_personagem

    # Estratégia usada na fase de escolha das ações no turno
    def escolher_acao(self, estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        if len(acoes_disponiveis) > 1:
            # Verifica se ação de coletar recursos está disponível e armazena o seu índice
            idx_acao_coleta_ouro = -1
            idx_acao_coleta_carta = -1
            for idx, acao in enumerate(acoes_disponiveis):
                if acao == TipoAcao.ColetarOuro:
                    idx_acao_coleta_ouro = idx
                elif acao == TipoAcao.ColetarCartas:
                    idx_acao_coleta_carta = idx
            if idx_acao_coleta_ouro != idx_acao_coleta_carta:
                # Agente escolhe uma das ações
                while True:
                    action, _ = self.model.predict(np.array(estado.converter_estado(openaigym=True)), deterministic=False)
                    if action == TipoAcaoOpenAI.ColetarOuro.value:
                        return idx_acao_coleta_ouro
                    elif action == TipoAcaoOpenAI.ColetarCartas.value:
                        return idx_acao_coleta_carta
            # Caso contrário escolhe segue comportamente do totalmente aleatório
            else:
                # Deixa passar turno por último
                acao_escolhida = random.randint(0, len(acoes_disponiveis) - 1)
                while acoes_disponiveis[acao_escolhida] == TipoAcao.PassarTurno:
                    acao_escolhida = random.randint(0, len(acoes_disponiveis) - 1)
                return acao_escolhida
        return 0

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        return random.randint(0, qtd_cartas - 1)

    # Estratégia usada na ação de construir distritos
    def construir_distrito(self, estado: Estado, distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)]) -> int:
        tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_covil_ladroes)
        # Só usa habilidade do covil dos ladrões se não tiver outra opção
        if len(distritos_para_construir) == 0:
            return random.randint(0, tamanho_maximo - 1)
        while True:
            action, _ = self.model.predict(np.array(estado.converter_estado(openaigym=True)), deterministic=False)
            if 10 <= action:
                break
        # Seleciona distrito a ser construído segundo estratégia/ação selecionada
        distritos_selecionados = []
        # Verifica se é possível construir ao menos 1 distrito da mão para recompensar o agente
        if action < 15:
            # Verifica se possui tipo de distrito escolhido
            for idx, distrito in enumerate(distritos_para_construir):
                if distrito.tipo_de_distrito == TipoDistrito(action - 10):
                    distritos_selecionados.append(idx)
        elif action == TipoAcaoOpenAI.ConstruirDistritoMaisCaro.value:
            caro = distritos_para_construir[0]
            idx_caro = 0
            for idx, distrito in enumerate(distritos_para_construir):
                if caro.valor_do_distrito < distrito.valor_do_distrito:
                    caro = distrito
                    idx_caro = idx
            distritos_selecionados.append(idx_caro)
        elif action == TipoAcaoOpenAI.ConstruirDistritoMaisBarato.value:
            barato = distritos_para_construir[0]
            idx_barato = 0
            for idx, distrito in enumerate(distritos_para_construir):
                if barato.valor_do_distrito > distrito.valor_do_distrito:
                    barato = distrito
                    idx_barato = idx
            distritos_selecionados.append(idx_barato)
        if len(distritos_selecionados) > 0:
            return random.sample(distritos_selecionados, 1)[0]
        # Se tipo de distrito escolhido estiver indisponível, escolhe aleatoriamente
        return random.randint(0, tamanho_maximo - 1)

    # Estratégia usada na ação de construir distritos (efeito Covil dos Ladrões)
    @staticmethod
    def construir_distrito_covil_dos_ladroes(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade da Assassina
    @staticmethod
    def habilidade_assassina(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)
        # Retira opções de personagens descartados
        opcoes = []
        for personagem in opcoes_personagem:
            if personagem not in estado.tabuleiro.cartas_visiveis:
                opcoes.append(personagem)
        return random.randint(0, len(opcoes) - 1)

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)
        # Retira opções de personagens descartados
        opcoes = []
        for personagem in opcoes_personagem:
            if personagem not in estado.tabuleiro.cartas_visiveis:
                opcoes.append(personagem)
        return random.randint(0, len(opcoes) - 1)

    # Estratégia usada na habilidade da Ilusionista (escolha do jogador alvo)
    @staticmethod
    def habilidade_ilusionista_trocar(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        return random.randint(0, len(opcoes_jogadores) - 1)
        # Ilusionista sempre troca de mão com o adversário que possui mais cartas, o desempate é uma escolha aleatória entre empatados
        mais_cartas = 0
        for jogador in opcoes_jogadores:
            if len(jogador.cartas_distrito_mao) > mais_cartas:
                mais_cartas = len(jogador.cartas_distrito_mao)
        opcoes = []
        for idx, jogador in enumerate(opcoes_jogadores):
            if len(jogador.cartas_distrito_mao) == mais_cartas:
                opcoes.append(idx)
        return random.sample(opcoes, 1)[0]

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
        return random.randint(0, len(distritos_para_destruir) - 1)

    # Estratégia usada na ação do Laboratório
    @staticmethod
    def laboratorio(estado: Estado) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)
