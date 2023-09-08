from enum import Enum, auto


class TipoAcao(Enum):

    def _generate_next_value_(name: str, start: int, count: int, last_values: list[int]) -> int:
        return count

    # Final de turno
    PassarTurno = auto()

    # Ações básicas
    ColetarOuro = auto()
    ColetarCartas = auto()
    ConstruirDistrito = auto()

    # Ações de personagem
    # Rank 1
    HabilidadeAssassina = auto()
    # HabilidadeBruxa = auto()
    # HabilidadeMagistrado = auto()
    # Rank 2
    HabilidadeLadrao = auto()
    # HabilidadeEspiao = auto()
    # HabilidadeChantagista = auto()
    # Rank 3
    HabilidadeIlusionistaTrocar = auto()
    HabilidadeIlusionistaDescartar = auto()
    # HabilidadeMago = auto()
    # HabilidadeVidente = auto()
    # Rank 4
    HabilidadeRei = auto()
    # HabilidadeImperador = auto()
    # HabilidadePatricio = auto()
    # Rank 5
    HabilidadeBispo = auto()
    # HabilidadeAbade = auto()
    # HabilidadeCardeal = auto()
    # Rank 6
    HabilidadeComerciante = auto()
    # HabilidadeAlquimista = auto()
    # HabilidadeMercador = auto()
    # Rank 7
    # HabilidadeArquiteta = auto()
    # HabilidadeNavegadora = auto()
    # HabilidadeEstudiosa = auto()
    # Rank 8
    HabilidadeSenhorDaGuerraDestruir = auto()
    HabilidadeSenhorDaGuerraColetar = auto()
    # HabilidadeDiplomata = auto()
    # HabilidadeMarechal = auto()
    # Rank 9
    # HabilidadeRainha = auto()
    # HabilidadeArtista = auto()
    # HabilidadeColetorDeImpostos = auto()

    # Distritos Especiais
    Laboratorio = auto()
    # Arsenal = auto()
    Forja = auto()
    # Museu = auto()
