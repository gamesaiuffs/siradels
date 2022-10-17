# Imports
from TipoDistrito import TipoDistrito


class CartaDistrito:
    # Construtor
    def __init__(self, valor_do_distrito: int, tipo_de_distrito: TipoDistrito, nome_do_distrito: str, quantidade: int):
        self.valor_do_distrito = valor_do_distrito
        self.tipo_de_distrito = tipo_de_distrito
        self.nome_do_distrito = nome_do_distrito
        self.quantidade = quantidade

    # To String
    def __str__(self) -> str:
        return f'{self.nome_do_distrito} ({self.tipo_de_distrito.name}, valor: {self.valor_do_distrito}, quantidade: {self.quantidade})'
