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
    JaConstruidosEspecial = 9, 4
    # JaPersonagem = 10, 9
    JmConstruidos = 10, 8
    JmQtdCarta = 11, 6
    MediaOuroAdversarios = 12, 5
    Rank1Disponivel = 13, 2
    Rank2Disponivel = 14, 2
    Rank3Disponivel = 15, 2
    Rank4Disponivel = 16, 2
    Rank5Disponivel = 17, 2
    Rank6Disponivel = 18, 2
    Rank7Disponivel = 29, 2
    Rank8Disponivel = 20, 2
    MeuTurno = 21, 2
    # Dados implementados, mas retirados do método converter_estado
    # JaQtdPersonagem = 9, 6
    # JaPontuacao = 10, 7
    # JmQtdOuro = 12, 7
    # PersonagemDisponivel = 14, 256
    # PersonagemDescartado = 15, 9

    # Sugestões
    # MediaValorCartasAdversarios
    # Personagens que tem carta descartada para cima