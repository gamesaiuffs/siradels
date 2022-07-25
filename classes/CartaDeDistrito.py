#Importar classe do efeito_do_distrito
class CartaDeDistrito:
    def __init__(self, valor_do_distrito:int, tipo_de_distrito:str, nome_do_distrito:str, efeito_do_distrito:str):
        self.valor_do_distrito = valor_do_distrito 
        self.tipo_de_distrito = tipo_de_distrito
        self.nome_do_distrito = nome_do_distrito 
        self.efeito_do_distrito = efeito_do_distrito 

    def __str__(self):
        return f'valor_do_distrito: {self.valor_do_distrito} tipo_do_distrito: {self.tipo_de_distrito} nome_do_distrito: {self.nome_do_distrito} efeito_do_distrito: {self.efeito_do_distrito}'
