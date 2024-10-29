from typing import Any, SupportsFloat

import gymnasium as gym
import numpy as np
from gymnasium import Space, spaces
from gymnasium.core import ObsType, ActType, RenderFrame

from classes.Simulacao import Simulacao
from classes.enum.TipoTabela import TipoTabela
from classes.strategies.Estrategia import Estrategia
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria


class Citadels(gym.Env):

    # Inicializa um novo ambiente de simulação
    def __init__(self):
        # Atributos específicos do jogo
        # Agente + Adversários de Treino
        self.estrategias: list[Estrategia] = [EstrategiaTotalmenteAleatoria('Agente'), EstrategiaTotalmenteAleatoria('Bot 1'), EstrategiaTotalmenteAleatoria('Bot 2'), EstrategiaTotalmenteAleatoria('Bot 3'), EstrategiaTotalmenteAleatoria('Bot 4')]
        # Cria simulação
        self.simulacao: Simulacao = Simulacao(self.estrategias, treino_openaigym=True)
        # Marca pontuação atual do agente (usada para recompensa)
        self.pontuacao_atual: int = 0
        # Marca posição do agente na ordem de turno para escolha de personagem
        self.idx_jogador: int = -1
        
        # self.simulacao.final_jogo = False   # modificado 
        
        # Descobre index do Enumerador que marca a disponibilidade de cartas de personagem
        self.idx_enum_personagem_rank1: int | None = None
        for e in TipoTabela:
            if e == TipoTabela.Rank1Disponivel:
                self.idx_enum_personagem_rank1 = e.idx - len(TipoTabela)
                break

        # Marca se o agente venceu a partida
        self.sucesso: int = 0
        
        self.primeira_tentativa = True

        # Atributos da interface gym.Env
        # Mapeamento do espaço de ações
        # EscolhaPersonagem (0 a 7 - rank 1 a 8)
        self.action_space: Space[ActType] = spaces.Discrete(8)
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
        # print("Reset")
        # self.simulacao.iniciar_rodada()
        # self.idx_jogador = self.identificar_idx_jogador()
        # self.simulacao.executar_rodada(0, self.idx_jogador)
        # self.simulacao.nova_rodada = True
        # Marca pontuação atual do agente (usada para recompensa)
        self.simulacao: Simulacao = Simulacao(self.estrategias, treino_openaigym=True)
        self.pontuacao_atual = 0
        self.sucesso = 0
        
        self.primeira_tentativa = True 
        self.simulacao.final_jogo = False   # modificado 
        
        
        # O segundo argumento refere-se a alguma informação adicional repassada para o agente
        return self.observation(), dict()

    # Método usado para executar uma transição de estado a partir de uma ação do agente
    def step(self, action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        if self.simulacao.nova_rodada and self.primeira_tentativa:
            # print("="*20, " Nova rodada ", "="*20)
            self.simulacao.iniciar_rodada()
            
        # Jogo segue até chegar a escolha do Agente 
        if self.primeira_tentativa:    
            self.idx_jogador = self.identificar_idx_jogador()
            self.simulacao.executar_rodada(0, self.idx_jogador)
            # input("Teste nova rodada")
            # return self.observation(), 0, self.simulacao.final_jogo, False, dict()    # modificado
        
        recompensa = 0.0
        jogador_agente = None
        for jogador in self.simulacao.estado.jogadores:
            if jogador.nome == 'Agente':
                jogador_agente = jogador
        if jogador_agente is None:
            raise Exception("Agente não encontrado!")
        
        # Verifica e executa a ação no ambiente simulado
        if self.observation()[self.idx_enum_personagem_rank1 + action] == 1:
            # Identificar índice do personagem escolhido
            idx_escolha_personagem = -1
            for idx, personagem in enumerate(self.simulacao.estado.tabuleiro.baralho_personagens):
                if action == personagem.rank - 1:
                    idx_escolha_personagem = idx
            if idx_escolha_personagem == -1:
                raise Exception("Personagem não encontrado!")
            # Executa escolha de personagem
            
            self.primeira_tentativa = True 
            
            self.simulacao.executar_rodada(self.idx_jogador, self.simulacao.num_jogadores, idx_escolha_personagem)
        
        # Recompensa negativa ao escolher ação inválida
        else:
            #recompensa += -12.0
            recompensa += -100
            self.primeira_tentativa = False
            return self.observation(), recompensa, self.simulacao.final_jogo, False, dict()

        # Rotina executada se chegou no final do jogo após a ação
        if self.simulacao.final_jogo:
            self.simulacao.computar_pontuacao_final()
            self.simulacao.estado.ordenar_jogadores_pontuacao()
            
            self.primeira_tentativa = True 
            # print("fim de jogo +100")
            
            # Recompensa ao vencer jogo
            if self.simulacao.estado.jogadores[0].nome == 'Agente':
                recompensa += 100
                self.sucesso = 1
            
            # self.simulacao.final_jogo = False   # modificado
            # self.simulacao.nova_rodada = True           # modificado
            # self.reset()
            
            return self.observation(), recompensa, self.simulacao.final_jogo, False, {"is_success": self.sucesso}  # modificado
        
        else:
            for jogador in self.simulacao.estado.jogadores:
                if jogador == jogador_agente:
                    # Recompensa ao aumentar pontuação parcial = delta pontuacao parcial + ou -
                    recompensa = recompensa + (jogador.pontuacao - self.pontuacao_atual)*5
                    # print("Variacao: ", recompensa)
                    self.pontuacao_atual = jogador.pontuacao
                    
            # self.simulacao.nova_rodada = True           # modificado
            return self.observation(), recompensa, self.simulacao.final_jogo, False, {"is_success": self.sucesso}   # modificado

        # Retorna uma tupla contendo:
        # a observação do próximo estado, a recompensa imediata obtida, se o estado é final,
        # se a simulação deve ser encerrada (estado inválido, mas não final) e informações adicionais
        #return self.observation(), recompensa, self.simulacao.final_jogo, False, {"is_success": self.sucesso}

    # Método (opcional) que implementa interface gráfica
    def render(self) -> RenderFrame | list[RenderFrame] | None:
        pass

    # Método (opcional) que encerra os recursos usados pelo ambiente ao finalizar uma simulação
    def close(self):
        pass
