from enum import Enum, auto
from typing import Any


class TipoAcao(Enum):

    def _generate_next_value_(name: str, start: int, count: int, last_values: list[int]) -> int:
        return count

    # Final de turno
    PassarTurno = auto()

    # Ações básicas
    ColetarOuro = auto()  # implementado
    ColetarCartas = auto()  # implementado
    ConstruirDistrito = auto()  # implementado

    # Ações de personagem
    # Rank 1
    HabilidadeAssassina = auto()  # implementado
    HabilidadeBruxa = auto()
    HabilidadeMagistrado = auto()
    # Rank 2
    HabilidadeLadrao = auto()  # implementado
    HabilidadeEspiao = auto()
    HabilidadeChantagista = auto()
    # Rank 3
    HabilidadeIlusionista = auto()
    HabilidadeMago = auto()  # implementado
    HabilidadeVidente = auto()
    # Rank 4
    HabilidadeRei = auto()  # implementado
    HabilidadeImperador = auto()
    HabilidadePatricio = auto()
    # Rank 5
    HabilidadeBispo = auto()
    HabilidadeAbade = auto()
    HabilidadeCardealAtivo = auto()
    HabilidadeCardealPassivo = auto()
    # Rank 6
    HabilidadeComerciante = auto()
    HabilidadeAlquimista = auto()
    HabilidadeMercador = auto()
    # Rank 7
    HabilidadeArquiteta = auto()
    HabilidadeNavegadora = auto()
    HabilidadeEstudiosa = auto()
    # Rank 8
    HabilidadeSenhordaGuerra = auto()
    HabilidadeDiplomata = auto()
    HabilidadeMarechal = auto()
    # Rank 9
    HabilidadeRainha = auto()
    HabilidadeArtista = auto()
    HabilidadeColetorDeImpostos = auto()

    # Distritos Especiais
    # Ações Ativas
    Laboratorio = auto()
    Necropole = auto()
    Teatro = auto()
    Estrutura = auto()
    Estabulos = auto()
    CovilDosLadroes = auto()

    # Ações Passivas
    PortaoDoDragao = auto()
    Muralha = auto()
    MinaDeOuro = auto()  # implementado (parcial)
    TesouroImperial = auto()
    AbrigoParaPobres = auto()  # implementado
    CofreSecreto = auto()  # implementado (parcial)
    BairroAssombrado = auto()
    EscolaDeMagia = auto()  # implementado (parcial)

    Parque = auto()
    Monumento = auto()
    Estatua = auto()
    Forja = auto()
    PocoDosDesejos = auto()
    Pedreira = auto()
    TorreDeMenagem = auto()
    Biblioteca = auto()
    Fabrica = auto()
    Arsenal = auto()
    Basilica = auto()
    Museu = auto()
    Observatorio = auto()
    Capitolio = auto()
    TorreDeMarfim = auto()
    SalaDeMapas = auto()
