# Imports
from enum import Enum


# Classe de enumeração
class TipoAcao(Enum):
    # Ações básicas
    ColetarOuro = 0
    ColetarCartas = 1
    ConstruirDistrito = 2

    # Ações de personagem
    # Rank 1
    HabilidadeAssassina = 3  # implementado
    HabilidadeBruxa = 4
    HabilidadeMagistrado = 5
    # Rank 2
    HabilidadeLadrao = 6  # implementado
    HabilidadeEspiao = 7
    HabilidadeChantagista = 8
    # Rank 3
    HabilidadeIlusionista = 9
    HabilidadeMago = 10  # implementado
    HabilidadeVidente = 11
    # Rank 4
    HabilidadeRei = 12  # implementado
    HabilidadeImperador = 13
    HabilidadePatricio = 14
    # Rank 5
    HabilidadeBispo = 15
    HabilidadeAbade = 16
    HabilidadeCardealAtivo = 17  # implementado
    HabilidadeCardealPassivo = 18  # implementado
    # Rank 6
    HabilidadeComerciante = 19
    HabilidadeAlquimista = 20  # implementado
    HabilidadeMercador = 21
    # Rank 7
    HabilidadeArquiteta = 22
    HabilidadeNavegadora = 23  # implementado
    HabilidadeEstudiosa = 24
    # Rank 8
    HabilidadeSenhordaGuerra = 25  # implementado
    HabilidadeDiplomata = 26
    HabilidadeMarechal = 27
    # Rank 9
    HabilidadeRainha = 28
    HabilidadeArtista = 29
    HabilidadeColetorDeImpostos = 30

    # Distritos Especiais
    # Ações Ativas
    CofreSecreto = 31
    Laboratorio = 32
    Necropole = 33
    Teatro = 34
    Estrutura = 35
    Estabulos = 36
    CovilDosLadroes = 37

    # Ações Passivas
    PortaoDoDragao = 38
    Muralha = 38
    MinaDeOuro = 38  # implementado
    TesouroImperial = 38
    AbrigoParaPobres = 38
    BairroAssombrado = 38
    EscolaDeMagia = 38

    Parque = 38
    Monumento = 38
    Estatua = 38
    Forja = 38
    PocoDosDesejos = 38
    Pedreira = 38
    TorreDeMenagem = 38
    Biblioteca = 38
    Fabrica = 38
    Arsenal = 38
    Basilica = 38
    Museu = 38
    Observatorio = 38
    Capitolio = 38
    TorreDeMarfim = 38
    SalaDeMapas = 38

    # Final de turno
    PassarTurno = 39

