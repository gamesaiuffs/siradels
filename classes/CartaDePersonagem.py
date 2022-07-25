#Importar classe na tipagem habilidade e efeito
class CartaDePersonagem:
    def __init__(self, nome:str, efeito:str, rank:int, habilidade:str, morto:bool, roubado:bool):
        self.nome = nome 
        self.efeito = efeito 
        self.rank = rank
        self.habilidade = habilidade
        self.morto = morto
        self.roubado = roubado

    def __str__(self):
        return f'nome: {self.nome} efeito: {self.efeito} rank: {self.rank} skill: {self.habilidade} morto: {self.morto} roubado: {self.roubado}'
             
