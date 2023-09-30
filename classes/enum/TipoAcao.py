from enum import Enum


class TipoAcao(Enum):
    # Final de turno
    PassarTurno = 0

    # Ações básicas
    ColetarOuro = 1
    ColetarCartas = 2
    ConstruirDistrito = 3

    # Ações de personagem
    # Rank 1
    HabilidadeAssassina = 4
    # HabilidadeBruxa = auto()
    # HabilidadeMagistrado = auto()
    # Rank 2
    HabilidadeLadrao = 5
    # HabilidadeEspiao = auto()
    # HabilidadeChantagista = auto()
    # Rank 3
    HabilidadeIlusionistaTrocar = 6
    HabilidadeIlusionistaDescartar = 7
    # HabilidadeMago = auto()
    # HabilidadeVidente = auto()
    # Rank 4
    HabilidadeRei = 8
    # HabilidadeImperador = auto()
    # HabilidadePatricio = auto()
    # Rank 5
    HabilidadeBispo = 9
    # HabilidadeAbade = auto()
    # HabilidadeCardeal = auto()
    # Rank 6
    HabilidadeComerciante = 10
    # HabilidadeAlquimista = auto()
    # HabilidadeMercador = auto()
    # Rank 7
    # HabilidadeArquiteta = auto()
    # HabilidadeNavegadora = auto()
    # HabilidadeEstudiosa = auto()
    # Rank 8
    HabilidadeSenhorDaGuerraDestruir = 11
    HabilidadeSenhorDaGuerraColetar = 12
    # HabilidadeDiplomata = auto()
    # HabilidadeMarechal = auto()
    # Rank 9
    # HabilidadeRainha = auto()
    # HabilidadeArtista = auto()
    # HabilidadeColetorDeImpostos = auto()

    # Distritos Especiais
    Laboratorio = 13
    # Arsenal = auto()
    Forja = 14
    # Museu = auto()
