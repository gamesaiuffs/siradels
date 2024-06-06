from enum import Enum


class TipoModeloAcao(Enum):
    # Sobrescreve método new padrão para adicionar atributos ao enum
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    # tamanho está relacionado à quantidade de valores distintos possíveis para o atributo
    def __init__(self, idx, tamanho):
        self.idx = idx
        self.tamanho = tamanho
    # EscolhaPersonagem + EscolherAcao(Ouro ou Carta) + ConstruirDistrito(5 Tipos, MaisCaro/MaisBarato)

    # Recompensa negativa ao escolher ação inválida = -12
    # Recompensa ao conseguir construir distrito = 6
    # Recompensa ao aumentar pontuação parcial = delta pontuacao parcial + ou -
    # Recompensa ao vencer jogo = 84
    # Recompensa em relação média pontuação adversários = variação entre sua pontuação e média

    # 17 ações
    # São 8 opções de personagens (ranks 1 a 8)
    EscolherPersonagem = 0, 8
    # São 15 ações distintas possíveis durante um turno (definidas no TipoAcao)
    EscolherAcao = 1, 15
    # São 31 cartas de distrito distintas
    ColetarCartas = 2, 31
    # São 31 cartas de distrito distintas + 1 opção de construção usando covil dos ladrões (combinação de custo será escolhida aleatoriamente)
    ConstruirDistrito = 3, 32
    # São 31 cartas de distrito distintas para pagar o custo da construção usando o covil dos ladrões
    ConstruirDistritoCovilDosLadroes = 4, 31
    # São 7 opções de personagens (ranks 2 a 8), mas por simplicidade manteremos as 8 posições
    HabilidadeAssassina = 5, 8
    # São 6 opções de personagens (ranks 3 a 8), mas por simplicidade manteremos as 8 posições
    HabilidadeLadrao = 6, 8
    # Abstraído em 2 opções (0 - escolher jogador com mais cartas, 1 - escolher jogador com mais pontos dentre os que tem cartas na mão)
    HabilidadeIlusionistaTrocar = 7, 2
    # Abstraído em até 4 cartas
    HabilidadeIlusionistaDescartarQtdCartas = 8, 4
    # São 31 cartas de distrito distintas
    HabilidadeIlusionistaDescartarCarta = 9, 31
    # São 31 cartas de distrito distintas para destruir (não trata repetições, escolhe aleatoriamente entre cartas de distrito iguais)
    HabilidadeSenhorDaGuerraDestruir = 10, 31
    # São 31 cartas de distrito distintas
    Laboratorio = 11, 31
