# Imports
from TipoDistrito import TipoDistrito
from Efeito import Efeito


class CartaDistrito:
    # Construtor
    def __init__(self, valor_do_distrito: int, tipo_de_distrito: TipoDistrito, nome_do_distrito: str, efeito_do_distrito: Efeito, quantidade: int):
        self.nome_do_distrito = nome_do_distrito
        self.valor_do_distrito = valor_do_distrito
        self.tipo_de_distrito = tipo_de_distrito
        self.efeito_do_distrito = efeito_do_distrito
        self.quantidade = quantidade

    # To String
    def __str__(self):
        return f'\nNome Do Distrito: {self.nome_do_distrito}' \
               f'\nTipo Do Distrito: {self.tipo_de_distrito}' \
               f'\nValor Do Distrito: {self.valor_do_distrito}' \
               f'\nEfeito Do Distrito: {self.efeito_do_distrito}' \
               f'\nQuantidade {self.quantidade}'
