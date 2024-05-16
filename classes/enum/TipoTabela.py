from enum import Enum


class TipoTabela(Enum):
    # Sobrescreve método new padrão para adicionar atributos ao enum
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    # tamanho está relacionado à quantidade de valores distintos possíveis para o atributo
    # Essas quantidades foram definidas/mapeadas no método Estado.converter_estado()
    def __init__(self, idx, tamanho):
        self.idx = idx
        self.tamanho = tamanho

    JaQtdOuro = 0, 7
    JaQtdCarta = 1, 6
    JaCartaCara = 2, 7
    JaCartaBarata = 3, 7
    JaConstruidos = 4, 8
    JaConstruidosMilitar = 5, 4
    JaConstruidosReligioso = 6, 4
    JaConstruidosNobre = 7, 4
    JaConstruidosComercial = 8, 4
    JaQtdPersonagem = 9, 5
    JaPontuacao = 10, 7
    JmConstruidos = 11, 8
    JmQtdOuro = 12, 7
    JmQtdCarta = 13, 6
    PersonagemDisponivel = 14, 252
    PersonagemDescartado = 15, 9
