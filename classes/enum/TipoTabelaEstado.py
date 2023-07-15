from enum import Enum


class TipoTabelaEstado(Enum):
    QtdOuro = 0
    QtdCarta = 1
    CartaCara = 2
    CartaBarata = 3
    Construidos = 4
    ConstruidosMilitar = 5
    ConstruidosReligioso = 6
    ConstruidosNobre = 7
    ConstruidosEspecial = 8
    PontuacaoParcial = 9
    QtdPersonagem = 10
    PersonagemDisponivel = 11
    PersonagemDescartado = 12
    Rotulo = 13
    #DistanciaDoRei = 13