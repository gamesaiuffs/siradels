from typing import Any, SupportsFloat

import gymnasium as gym
import numpy as np
from gymnasium import Space, spaces
from gymnasium.core import ObsType, ActType, RenderFrame

from classes.Simulacao import Simulacao
from classes.enum.TipoTabela import TipoTabela
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria


class Citadels(gym.Env):

    # Inicializa um novo ambiente de simulação
    def __init__(self):
        # Atributos específicos do jogo
        # Adversários
        self.estrategias = [EstrategiaTotalmenteAleatoria('Agente'), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
        # Cria simulação
        self.simulacao = Simulacao(self.estrategias, openaigym=True)
        # Marca pontuação, ouro e quantidade de cartas na mão atual do agente (usada para recompensa)
        self.pontuacao_atual = 0
        self.ouro_atual = 2
        self.qtd_cartas_atual = 4

        # Atributos da interface gym.Env
        # Mapeado apenas ação de escolha de personagem
        self.action_space: Space[ActType] = spaces.Discrete(self.simulacao.num_personagens)
        # Mapeado estado conforme implementado em método Estado.converter_estado() e TipoTabela
        self.estado_vetor: list[int] = []
        for tipo_tabela in TipoTabela:
            self.estado_vetor.append(tipo_tabela.tamanho)
        self.observation_space: Space[ObsType] = spaces.MultiDiscrete(self.estado_vetor)

    # Mapeia estado atual na estrutura do espaço observacional (observação do agente do ambiente do problema)
    def observation(self):
        return np.array(self.simulacao.estado.converter_estado(openaigym=True))

    # Método usado para iniciar uma nova simulação a partir de um estado inicial
    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[ObsType, dict[str, Any]]:
        super().reset(seed=seed)
        self.simulacao.criar_estado_inicial(self.simulacao.num_personagens, self.simulacao.automatico)
        # Marca pontuação, ouro e quantidade de cartas na mão atual do agente (usada para recompensa)
        self.pontuacao_atual = 0
        self.ouro_atual = 2
        self.qtd_cartas_atual = 4
        # O segundo argumento refere-se a alguma informação adicional repassada para o agente
        return self.observation(), dict()

    # Método usado para executar uma transição de estado a partir de uma ação do agente
    def step(self, action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        # Verifica se o personagem esoclhida está disponível e identifica o seu índice
        escolha_personagem = -1
        for idx, personagem in enumerate(self.simulacao.estado.tabuleiro.baralho_personagens):
            if action == personagem.rank - 1:
                escolha_personagem = idx
        # Caso não esteja, retorna estado atual com recompensa negativa
        if escolha_personagem == -1:
            return self.observation(), -10, self.simulacao.final_jogo, False, dict()

        # Simula a rodada inteira com a ação escolhida
        self.simulacao.executar_rodada(escolha_personagem)

        recompensa = 0
        # Recompensa no final do jogo
        if self.simulacao.final_jogo:
            # Rotina de final de jogo
            self.simulacao.computar_pontuacao_final()
            self.simulacao.estado.ordenar_jogadores_pontuacao()
            # Agente ganhou o jogo
            if self.simulacao.estado.jogadores[0].nome == 'Agente':
                recompensa = 100
            # Agente perdeu o jogo
            else:
                recompensa = -100
        # A diferença na pontuação atual, ouro e cartas atuais serão usadas na recompensa imediata
        else:
            for jogador in self.simulacao.estado.jogadores:
                if jogador.nome == 'Agente':
                    recompensa, self.pontuacao_atual = recompensa + jogador.pontuacao - self.pontuacao_atual, jogador.pontuacao
                    recompensa, self.ouro_atual = recompensa + (jogador.ouro - self.ouro_atual) * 0.5, jogador.ouro
                    recompensa, self.qtd_cartas_atual = recompensa + (len(jogador.cartas_distrito_mao) - self.qtd_cartas_atual) * 0.9, len(jogador.cartas_distrito_mao)
        # Retorna uma tupla contendo:
        # a observação do próximo estado, a recompensa imediata obtida, se o estado é final,
        # se a simulação deve ser encerrada (estado inválido, mas não final) e informações adicionais
        return self.observation(), recompensa, self.simulacao.final_jogo, False, dict()

    # Método (opcional) que implementa interface gráfica
    def render(self) -> RenderFrame | list[RenderFrame] | None:
        pass

    # Método (opcional) que encerra os recursos usados pelo ambiente ao finalizar uma simulação
    def close(self):
        pass
