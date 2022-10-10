class Jogador:
    # Construtor
    def __init__(self, nome: str):
        self.pontuacao = 0 
        self.nome = nome 
        self.personagem = []
        self.ouro = 2
        self.cartas_distrito_mao = []
        self.distritos_construidos = []
        self.rei = False
        self.morto = False
        self.roubado = False

    # To String
    def __str__(self):
        return f"\nNome: {self.nome}" \
               f"\nPersonagem:{self.personagem}" \
               f"\nPontuação: {self.pontuacao}" \
               f"\nOuro: {self.ouro}" \
               f"\nCartas de distrito na mão: {self.cartas_distrito_mao}" \
               f"\nDistritos cronstruidos: {self.distritos_construidos}" \
               f"\nÉ o rei: {self.rei}" \
               f"\nEstá morto: {self.morto}" \
               f"\nFoi roubado: {self.roubado}"
