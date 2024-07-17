from typing import Any, SupportsFloat

import gymnasium as gym
import numpy as np
import random
from gymnasium import Space, spaces
from gymnasium.core import ObsType, ActType, RenderFrame

from classes.Simulacao import Simulacao
from classes.enum.TipoAcaoOpenAI import TipoAcaoOpenAI
from classes.enum.TipoDistrito import TipoDistrito
from classes.enum.TipoTabela import TipoTabela
from classes.model.Acao import ConstruirDistrito
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria


class Citadels(gym.Env):
    passos = 0
    # Inicializa um novo ambiente de simulação
    def __init__(self):
        # Atributos específicos do jogo
        # Agente + Adversários de Treino
        self.estrategias = [EstrategiaTotalmenteAleatoria('Agente'), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
        # Cria simulação
        self.simulacao = Simulacao(self.estrategias, treino_openaigym=True)
        # Marca pontuação atual do agente (usada para recompensa)
        self.pontuacao_atual = 0
        # Marca posição do agente na ordem de turno para escolha de personagem
        self.idx_jogador = -1

        # Atributos da interface gym.Env
        # Mapeamento do espaço de ações
        # EscolhaPersonagem (8) + EscolherAcao(Ouro ou Carta) + ConstruirDistrito(5 Tipos, MaisCaro ou MaisBarato da mão)
        self.action_space: Space[ActType] = spaces.Discrete(17)
        # Mapeado estado conforme implementado em método Estado.converter_estado() e TipoTabela
        self.estado_vetor: list[int] = []
        for tipo_tabela in TipoTabela:
            self.estado_vetor.append(tipo_tabela.tamanho)
        self.observation_space: Space[ObsType] = spaces.MultiDiscrete(self.estado_vetor)

    # Mapeia estado atual na estrutura do espaço observacional (observação do agente do ambiente do problema)
    def observation(self) -> np.array:
        return np.array(self.simulacao.estado.converter_estado(openaigym=True))

    # Método que identificar e retorna o idx referente a vez do jogador na escolha de personagens
    def identificar_idx_jogador(self) -> int:
        for idx, jogador in enumerate(self.simulacao.estado.jogadores):
            if jogador.nome == 'Agente':
                return idx
        raise Exception("Agente não encontrado!")

    # Método usado para iniciar uma nova simulação a partir de um estado inicial até o turno do agente
    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[ObsType, dict[str, Any]]:
        super().reset(seed=seed)
        self.simulacao.criar_estado_inicial(self.simulacao.num_personagens)
        self.simulacao.iniciar_rodada()
        self.idx_jogador = self.identificar_idx_jogador()
        self.simulacao.executar_rodada(0, self.idx_jogador)
        # Marca pontuação atual do agente (usada para recompensa)
        self.pontuacao_atual = 0
        # O segundo argumento refere-se a alguma informação adicional repassada para o agente
        return self.observation(), dict()

    # Método usado para executar uma transição de estado a partir de uma ação do agente
    def step(self, action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        
        Citadels.passos += 1
        print("step: ", Citadels.passos, end="\r")
        
        if self.simulacao.nova_rodada:
            self.simulacao.iniciar_rodada()
            self.idx_jogador = self.identificar_idx_jogador()
        recompensa = 0.0
        jogador_agente = None
        for jogador in self.simulacao.estado.jogadores:
            if jogador.nome == 'Agente':
                jogador_agente = jogador
        if jogador_agente is None:
            raise Exception("Agente não encontrado!")
        # Verifica e executa a ação no ambiente simulado
        if 0 <= action < 8 and self.observation()[TipoTabela.EtapaPersonagem.idx] == 1 and self.observation()[-8 + action] == 1:
            # Identificar índice do personagem escolhido
            idx_escolha_personagem = -1
            for idx, personagem in enumerate(self.simulacao.estado.tabuleiro.baralho_personagens):
                if action == personagem.rank - 1:
                    idx_escolha_personagem = idx
            if idx_escolha_personagem == -1:
                raise Exception("Personagem não encontrado!")
            # Executa escolha de personagem
            self.simulacao.executar_rodada(self.idx_jogador, self.simulacao.num_jogadores, idx_escolha_personagem)
        elif 8 <= action < 10 and self.observation()[TipoTabela.EtapaOuroCarta.idx] == 1:
            # Executa coletar recursos
            self.simulacao.executar_coletar_recursos(TipoAcaoOpenAI(action), jogador_agente)
        elif 10 <= action and self.observation()[TipoTabela.EtapaConstrucao.idx] == 1:
            # Executa construção de distritos
            distritos_para_construir, distritos_para_construir_covil = ConstruirDistrito.distritos_possiveis_construir(jogador_agente)
            # Recompensa fixa por construir distritos
            if len(distritos_para_construir) + len(distritos_para_construir_covil) > 0:
                recompensa += 6
            # Usa escolha aleatória se consegue construir apenas com o efeito do covil dos ladrões
            if len(distritos_para_construir) == 0:
                self.simulacao.executar_construir_distrito(-1, jogador_agente)
            else:
                # Seleciona distrito a ser construído segundo estratégia/ação selecionada
                distritos_selecionados = []
                # Verifica se é possível construir ao menos 1 distrito da mão para recompensar o agente
                if len(distritos_para_construir) > 0:
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
                    idx_distrito_escolhido = random.sample(distritos_selecionados, 1)[0]
                    self.simulacao.executar_construir_distrito(idx_distrito_escolhido, jogador_agente)
                else:
                    self.simulacao.executar_construir_distrito(-1, jogador_agente)
        # Recompensa negativa ao escolher ação inválida
        else:
            #recompensa += -12.0
            recompensa += -120.0
            return self.observation(), recompensa, self.simulacao.final_jogo, False, dict()

        # Rotina executada se chegou no final do jogo após a ação
        if self.simulacao.final_jogo:
            self.simulacao.computar_pontuacao_final()
            self.simulacao.estado.ordenar_jogadores_pontuacao()
            # Recompensa ao vencer jogo
            if self.simulacao.estado.jogadores[0].nome == 'Agente':
                recompensa += 84.0
        else:
            media_adv = 0
            for jogador in self.simulacao.estado.jogadores:
                if jogador == jogador_agente:
                    # Recompensa ao aumentar pontuação parcial = delta pontuacao parcial + ou -
                    recompensa, self.pontuacao_atual = recompensa + jogador.pontuacao - self.pontuacao_atual, jogador.pontuacao
                else:
                    media_adv += jogador.pontuacao
            media_adv /= len(self.simulacao.estado.jogadores) - 1
            # Recompensa em relação média pontuação adversários = variação entre a sua pontuação e a média da pontuação dos adversários
            recompensa += self.pontuacao_atual - media_adv

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
