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
    # Ilusionista = auto()
    Mago = 3
    # Vidente = auto()
    # Rank 4
    Rei = 0
    # Imperador = auto()
    # Patricio = auto()
    # Rank 5
    # Bispo = auto()
    # Abade = auto()
    Cardeal = 5
    # Rank 6
    # Comerciante = auto()
    Alquimista = 6
    # Mercador = auto()
    # Rank 7
    # Arquiteta = auto()
    Navegadora = 7
    # Estudiosa = auto()
    # Rank 8
    SenhorDaGuerra = 8
    # Diplomata = auto()
    # Marechal = auto()
    # Rank 9
    # Rainha = auto()
    # Artista = auto()
    # ColetorDeImpostos = auto()
