from CartaDeDistrito import CartaDeDistrito
from CartaDePersonagem import CartaDePersonagem


class Tabuleiro:
    def __init__(self, baralho_de_distritos:list(CartaDeDistrito), turno:int, fase:int, baralho_de_personagens:list(CartaDePersonagem)):  
        self.baralho_de_distritos = baralho_de_distritos 
        self.turno = turno 
        self.fase = fase 
        self.baralho_de_personagens = baralho_de_personagens

    def __str__(self):
        return f"deck: {self.baralho_de_distritos} turn: {self.turno} stage: {self.fase} characters:  {self.baralho_de_personagens}"
