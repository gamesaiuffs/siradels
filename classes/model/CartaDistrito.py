from classes.enum.TipoDistrito import TipoDistrito
from classes.model.IndexMCTS import IndexMCTS


class CartaDistrito(IndexMCTS):
    # Construtor
    def __init__(self, idx: int, valor_do_distrito: int, tipo_de_distrito: TipoDistrito, nome_do_distrito: str, quantidade: int, efeito: str = ''):
        super().__init__(idx)
        self.valor_do_distrito: int = valor_do_distrito
        self.tipo_de_distrito: TipoDistrito = tipo_de_distrito
        self.nome_do_distrito: str = nome_do_distrito
        self.quantidade: int = quantidade
        self.efeito: str = efeito

    # To String
    def __str__(self) -> str:
        return f'{self.nome_do_distrito}'
    
    def imprimir_tudo(self) -> str:
        aux = f'{self.nome_do_distrito} ({self.valor_do_distrito} - {self.tipo_de_distrito.name})'
        if self.efeito == '':
            return aux
        return f'{aux} \n\t{self.efeito}'
        
