
from random import shuffle 
class DistrictCard:
    def __init__(self, value, type, name, effect):
        self.value = value 
        self.type = type
        self.name = name 
        self.effect = effect 



def criar_baralho():
    mercado = DistrictCard(2, 'comercio', 'mercado', None)#3
    taverna = DistrictCard(1, 'comercio', 'taverna', None)#2
    torre_de_vigia = DistrictCard(1, 'militar', 'torre de vigia', None)#2
    palacio = DistrictCard(5, 'nobre', 'palacio', None)#1
    prisao = DistrictCard(2, 'militar', 'prisao',None)#4
    caserna = DistrictCard(3,'militar', 'barracos',None)#4
    fortaleza = DistrictCard(5,'militar','fortaleza',None)
    solar = DistrictCard(3,'nobre','solar',None)#4
    templo=DistrictCard(1,'religioso','templo',None)#1
    castelo=DistrictCard(4,'nobre','castelo',None)#2
    porto=DistrictCard(4,'comercio','porto',None)#2
    catedral=DistrictCard(5,'religioso','catedral',None)#2
    mosteiro=DistrictCard(3,'religioso','mosteiro',None)#3
    docas=DistrictCard(3,'comercio','docas',None)#2
    prefeitura=DistrictCard(5,'comercio','prefeitura',None)#1
    igreja=DistrictCard(2,'religioso','igreja',None)#2
    posto_de_comercio=DistrictCard(2,'comercio','posto de comercio',None)








    

    # Criar resto do deck
    deck = [mercado,mercado,mercado,mercado,mercado, taverna,taverna, torre_de_vigia,torre_de_vigia, palacio,prisao,prisao,prisao,caserna,caserna,caserna,caserna,fortaleza,solar,solar,solar,solar,templo,castelo,castelo,castelo,castelo,porto,porto,catedral,mosteiro
    ,mosteiro,mosteiro,docas,docas,prefeitura,igreja,igreja,posto_de_comercio,posto_de_comercio,prisao]
    deck.append(deck)
    deck.append(deck)
    deck.append(deck)

    shuffle(deck)

    return deck
    
