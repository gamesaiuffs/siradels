from enum import Enum


class TipoPersonagem(Enum):
    # Usado apenas para controle
    Nenhum = -1
    # Rank 1
    Assassina = 1
    # Bruxa = auto()
    # Magistrado = auto()
    # Rank 2
    Ladrao = 2
    # Espiao = auto()
    # Chantagista = auto()
    # Rank 3
    Ilusionista = 3
    # Mago = 3
    # Vidente = auto()
    # Rank 4
    Rei = 0
    # Imperador = auto()
    # Patricio = auto()
    # Rank 5
    Bispo = 4
    # Abade = auto()
    # Cardeal = 4
    # Rank 6
    Comerciante = 5
    # Alquimista = 5
    # Mercador = auto()
    # Rank 7
    Arquiteta = 6
    # Navegadora = 6
    # Estudiosa = auto()
    # Rank 8
    SenhorDaGuerra = 7
    # Diplomata = auto()
    # Marechal = auto()
    # Rank 9
    # Rainha = auto()
    # Artista = auto()
    # ColetorDeImpostos = auto()
