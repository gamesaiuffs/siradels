import CartaDistrito
import CartaPersonagem


class Jogador:
    # variavel order removida 
    def __init__(self, pontuacao: int, nome: str, carta_personagem: CartaPersonagem, ouro: int, cartas_distritos_na_mao: list(CartaDistrito), distritos_construidos: list(CartaDistrito), eh_o_rei: bool, morto: bool, roubado: bool):
        self.pontuacao = pontuacao 
        self.nome = nome 
        self.carta_personagem = carta_personagem
        self.ouro = ouro
        self.cartas_distrito_na_mao = cartas_distritos_na_mao
        self.distritos_construidos = distritos_construidos
        self.eh_o_rei = eh_o_rei
        self.morto = morto
        self.roubado = roubado

    def __str__(self):
        return f"Pontuação:  {self.pontuacao} Nome:  {self.nome} Carta de personagem: {self.carta_personagem} Ouro:  {self.ouro} Cartas de distrito na mão:  {self.cartas_distrito_na_mao} É o rei:  {self.eh_o_rei}"
