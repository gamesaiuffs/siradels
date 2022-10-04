# Importar classe do efeito_do_distrito
from TipoDistrito import TipoDistrito
from Efeito import Efeito


class CartaDistrito:
    def __init__(self, valor_do_distrito: int, tipo_de_distrito: TipoDistrito, nome_do_distrito: str, efeito_do_distrito: Efeito, quantidade: int):
        self.valor_do_distrito = valor_do_distrito
        self.tipo_de_distrito = tipo_de_distrito
        self.nome_do_distrito = nome_do_distrito
        self.efeito_do_distrito = efeito_do_distrito
        self.quantidade = quantidade

    def __str__(self):
        return f'valor_do_distrito: {self.valor_do_distrito} tipo_do_distrito: {self.tipo_de_distrito} nome_do_distrito: {self.nome_do_distrito} efeito_do_distrito: {self.efeito_do_distrito} quantidade {self.quantidade}'
