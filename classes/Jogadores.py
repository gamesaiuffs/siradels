from CartaDeDistrito import CartaDeDistrito
from CartaDePersonagem import CartaDePersonagem

#OBS: Variavel order removida 

class Jogadores:
    # variavel order removida 
    def __init__(self, pontuacao:int, nome:str, carta_personagem:CartaDePersonagem, ouro:int, cartas_distritos_na_mao:list(CartaDeDistrito), distritos_construidos:list(CartaDeDistrito), eh_o_rei:bool):
        self.pontuacao = pontuacao 
        self.nome = nome 
        self.carta_personagem = carta_personagem
        self.ouro = ouro
        self.cartas_distrito_na_mao = cartas_distritos_na_mao
        self.distritos_construidos = distritos_construidos
        self.eh_o_rei = eh_o_rei

    def __str__(self):
        return f"Pontuação:  {self.pontuacao} Nome:  {self.nome} Carta de personagem: {self.carta_personagem} Ouro:  {self.ouro} Cartas de distrito na mão:  {self.cartas_distrito_na_mao} É o rei:  {self.eh_o_rei}"
