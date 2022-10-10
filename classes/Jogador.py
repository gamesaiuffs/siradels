class Jogador:
    def __init__(self, nome: str):
        self.pontuacao = 0 
        self.nome = nome 
        self.carta_personagem = []
        self.ouro = 2
        self.cartas_distrito_na_mao = []
        self.distritos_construidos = []
        self.eh_o_rei = False
        self.morto = False
        self.roubado = False

    def __str__(self):
        return f"Pontuação:  {self.pontuacao} Nome:  {self.nome} Carta de personagem: {self.carta_personagem} Ouro:  {self.ouro} Cartas de distrito na mão:  {self.cartas_distrito_na_mao} É o rei:  {self.eh_o_rei}"
