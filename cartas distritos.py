
from random import shuffle 
class DistrictCard:
    def __init__(self, value, type, name, effect):
        self.value = value 
        self.type = type
        self.name = name 
        self.effect = effect 



def criar_baralho():
    mercado = DistrictCard(2, 'comercio', 'mercado', None)
    taverna = DistrictCard(1, 'comercio', 'taverna', None)
    torre_de_vigia = DistrictCard(1, 'militar', 'torre de vigia', None)
    palacio = DistrictCard(5, 'nobre', 'palacio', None)
    prisao = DistrictCard(2, 'militar', 'prisao',None)
    quartel = DistrictCard(3,'militar', 'barracos',None)
    fortaleza = DistrictCard(5,'militar','fortaleza',None)
    mansao = DistrictCard(3,'nobre','mansao',None)
    

    # Criar resto do deck
    deck = [mercado, taverna, torre_de_vigia, palacio,prisao,prisao,quartel,quartel,fortaleza,mansao,mansao]
    deck.append(deck)
    deck.append(deck)
    deck.append(deck)

    shuffle(deck)

    return deck
    
