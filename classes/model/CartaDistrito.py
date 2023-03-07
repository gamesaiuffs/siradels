# Imports
from classes.enum.TipoDistrito import TipoDistrito


class CartaDistrito:
    # Construtor
    def __init__(self, valor_do_distrito: int, tipo_de_distrito: TipoDistrito, nome_do_distrito: str, quantidade: int, efeito: str = ""):
        self.valor_do_distrito = valor_do_distrito
        self.tipo_de_distrito = tipo_de_distrito
        self.nome_do_distrito = nome_do_distrito
        self.quantidade = quantidade
        self.efeito = efeito

    # To String
    def __str__(self) -> str:
        return f'{self.nome_do_distrito}'
    
    def imprimir_tudo(self) -> str:
        aux = f'{self.nome_do_distrito} ({self.valor_do_distrito} - {self.tipo_de_distrito.name})'
        if self.efeito:
            return aux
        return f'{aux} \n{self.efeito}'
        