from enum import Enum


class TipoAcaoOpenAI(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    # tamanho está relacionado à quantidade de valores distintos possíveis para o atributo
    def __init__(self, idx):
        self.idx = idx

    # Ações básicas
    EscolherAssassina = 0
    EscolherLadrao = 1
    EscolherIlusionista = 2
    EscolherRei = 3
    EscolherBispo = 4
    EscolherComerciante = 5
    EscolherArquiteta = 6
    EscolherSenhorDaGuerra = 7
    ColetarOuro = 8
    ColetarCartas = 9
    ConstruirDistritoReligioso = 10
    ConstruirDistritoMilitar = 11
    ConstruirDistritoNobre = 12
    ConstruirDistritoComercial = 13
    ConstruirDistritoEspecial = 14
    ConstruirDistritoMaisCaro = 15
    ConstruirDistritoMaisBarato = 16
